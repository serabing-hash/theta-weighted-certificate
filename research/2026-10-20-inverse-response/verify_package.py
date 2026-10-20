#!/usr/bin/env python3
"""Byte, dependency, and Python-syntax audit only. Never imports science code."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile
import urllib.request

INPUTS_SHA256 = "da4e4cc3cf8e1f49762e4e05aff73cef85fdceadd6d72d70b07c7be3b8e209b4"
CORE = {
    "INPUTS.json", "PROVENANCE.json", "README.md", "REPRODUCTION.md", "ASSUMPTIONS.md",
    "verify_package.py", "replay_once.py", "safe_extract.py",
    "code/public_worker.py", "code/shared_checker.py", "code/rank_one_checker.py",
    "results/shared_error.json", "results/rank_one.json",
}


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def read_json(path):
    def unique(items):
        result = {}
        for key, value in items:
            need(key not in result, "duplicate JSON key")
            result[key] = value
        return result
    return json.loads(path.read_bytes(), object_pairs_hook=unique)


def safe_path(root, value):
    need(isinstance(value, str) and "\\" not in value, "invalid relative path")
    rel = PurePosixPath(value)
    need(not rel.is_absolute() and rel.parts and
         all(p not in ("", ".", "..") for p in rel.parts), "unsafe relative path")
    need(str(rel) == value, "noncanonical relative path")
    result = root.joinpath(*rel.parts)
    cursor = root
    for part in rel.parts:
        cursor = cursor / part
        need(not cursor.is_symlink(), "symlink rejected")
    need(result.resolve().is_relative_to(root.resolve()), "path escapes package")
    return result


def validate_binding(row):
    need(type(row) is dict and {"path", "bytes", "sha256"} <= set(row), "binding schema")
    need(type(row["bytes"]) is int and 0 <= row["bytes"] <= 50_000_000,
         "invalid byte limit")
    need(type(row["sha256"]) is str and
         re.fullmatch(r"[0-9a-f]{64}", row["sha256"]) is not None, "invalid hash")


def check_bytes(path, row):
    validate_binding(row)
    need(path.is_file() and not path.is_symlink(), "missing/nonregular file: " + str(path))
    need(path.stat().st_size == row["bytes"], "byte count mismatch: " + str(path))
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    need(digest.hexdigest() == row["sha256"], "SHA256 mismatch: " + str(path))


def fetch_one(root, row):
    validate_binding(row)
    target = safe_path(root, row["path"])
    if target.exists():
        check_bytes(target, row)
        return
    url = row["url"]
    need(re.fullmatch(
        r"https://raw\.githubusercontent\.com/serabing-hash/theta-weighted-certificate/"
        r"[0-9a-f]{40}/research/2026-10-18-coefficient-obstruction/"
        r"(?:inputs/[A-Za-z0-9_]+\.json|results/coefficient_check\.json)", url
    ) is not None, "dependency URL is not pinned to the allowed public source")
    target.parent.mkdir(parents=True, exist_ok=True)
    safe_path(root, row["path"])
    fd, name = tempfile.mkstemp(prefix=".fetch-", dir=target.parent)
    temporary = Path(name)
    try:
        with os.fdopen(fd, "wb") as output, urllib.request.urlopen(url, timeout=45) as response:
            need(response.geturl() == url, "unexpected dependency redirect")
            left = row["bytes"] + 1
            while left:
                data = response.read(min(left, 1 << 20))
                if not data:
                    break
                output.write(data)
                left -= len(data)
            output.flush()
            os.fsync(output.fileno())
        check_bytes(temporary, row)
        os.link(temporary, target)  # Atomic no-overwrite publication.
    finally:
        temporary.unlink(missing_ok=True)


def verify(root, require_inputs=False, fetch=False):
    root = root.resolve(strict=True)
    manifest = read_json(root / "PACKAGE_MANIFEST.json")
    need(manifest["format"] == "INVERSE_RESPONSE_PUBLIC_PACKAGE_V1", "package format")
    need(type(manifest["files"]) is list, "manifest file list")
    seen = set()
    for row in manifest["files"]:
        validate_binding(row)
        path = safe_path(root, row["path"])
        need(row["path"] not in seen and row["path"] != "PACKAGE_MANIFEST.json",
             "duplicate or self-bound package path")
        seen.add(row["path"])
        check_bytes(path, row)
        if path.suffix == ".py":
            ast.parse(path.read_text(), filename=row["path"])
    need(CORE <= seen, "missing required core package bindings")
    need(hashlib.sha256((root / "INPUTS.json").read_bytes()).hexdigest() == INPUTS_SHA256,
         "frozen public input manifest mismatch")
    inputs = read_json(root / "INPUTS.json")
    need(inputs["format"] == "INVERSE_RESPONSE_PUBLIC_INPUTS_V1", "input format")
    dependencies = inputs["dependencies"]
    need(set(dependencies) == {
        "saved_A160", "saved_D160", "saved_K160", "saved_N160", "saved_F160",
        "saved_P_UP_EXACT", "witness_vector", "coefficient_report",
        "saved_SHIFT_SCALARS", "original_norm"
    }, "dependency role set")
    dep_paths = set()
    present = 0
    for role, row in dependencies.items():
        validate_binding(row)
        need(row["path"] == "dependencies/" + role + ".json", "restoration path")
        path = safe_path(root, row["path"])
        dep_paths.add(row["path"])
        if fetch:
            fetch_one(root, row)
        if path.exists():
            check_bytes(path, row)
            present += 1
        elif require_inputs or fetch:
            raise RuntimeError("missing dependency: " + role)
    allowed = seen | dep_paths | {"PACKAGE_MANIFEST.json"}
    for path in root.rglob("*"):
        need(not path.is_symlink(), "symlink anywhere in package")
        if path.is_file():
            need(path.relative_to(root).as_posix() in allowed,
                 "unmanifested package file: " + str(path))
    return {"status": "PACKAGE-BYTES-AND-SYNTAX-VERIFIED",
            "package_files": len(seen), "dependencies_present": present,
            "dependency_count": len(dependencies), "scientific_executions": 0,
            "physical_premises_recertified": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fetch-inputs", action="store_true")
    parser.add_argument("--require-inputs", action="store_true")
    args = parser.parse_args()
    try:
        print(json.dumps(verify(Path(__file__).parent, args.require_inputs, args.fetch_inputs),
                         sort_keys=True))
        return 0
    except Exception as error:
        print(json.dumps({"status": "HOLD", "reason": str(error),
                          "scientific_executions": 0, "automatic_retry": False}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
