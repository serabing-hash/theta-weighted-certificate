"""400-digit directed LDL of the specified exact matrix minus its stated gap."""
import argparse
import interval_bounds
import verify_final_gate
interval_bounds.PRECISION=400
if __name__=='__main__':
    p=argparse.ArgumentParser()
    for name in ['candidate','T','G','K','gap','output']:p.add_argument('--'+name,required=True)
    verify_final_gate.main(p.parse_args())
