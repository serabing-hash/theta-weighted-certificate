#!/usr/bin/env python3
"""Extract the published reproduction ZIP into a new directory, fail closed."""
import argparse
import hashlib
from pathlib import Path, PurePosixPath
import stat
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive")
    parser.add_argument("destination")
    parser.add_argument("--sha256", required=True)
    parser.add_argument("--bytes", type=int, required=True)
    args = parser.parse_args()
    archive = Path(args.archive)
    if archive.is_symlink() or not archive.is_file() or archive.stat().st_size != args.bytes:
        raise RuntimeError("archive size/type mismatch")
    if hashlib.sha256(archive.read_bytes()).hexdigest() != args.sha256:
        raise RuntimeError("archive SHA256 mismatch")
    dest = Path(args.destination).absolute()
    if dest.exists() or dest.is_symlink() or dest.parent.resolve() != dest.parent:
        raise RuntimeError("destination must be new with a canonical parent")
    with zipfile.ZipFile(archive) as source:
        items = source.infolist()
        if len(items) > 200 or sum(x.file_size for x in items) > 20_000_000:
            raise RuntimeError("archive admission limit")
        seen = set()
        for item in items:
            p = PurePosixPath(item.filename)
            mode = item.external_attr >> 16
            if (item.filename in seen or "\\" in item.filename or p.is_absolute()
                or str(p) != item.filename or any(x in (".", "..") for x in p.parts)
                or item.is_dir() or (stat.S_IFMT(mode) not in (0, stat.S_IFREG))
                or item.flag_bits & 1):
                raise RuntimeError("unsafe ZIP member")
            seen.add(item.filename)
        dest.mkdir(mode=0o700)
        for item in items:
            target = dest.joinpath(*PurePosixPath(item.filename).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("xb") as output:
                output.write(source.read(item))
    print("EXTRACTED; run package byte verification before any replay")


if __name__ == "__main__":
    main()
