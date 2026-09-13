from __future__ import annotations
import argparse, json, platform, sys
from dataclasses import asdict
from ec import __version__
from ec.demos.manufacturing import build_demo

def main() -> None:
    p=argparse.ArgumentParser(prog="ec")
    sub=p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("doctor")
    sub.add_parser("demo-manufacturing")
    a=p.parse_args()
    if a.cmd=="doctor":
        result={"ecVersion":__version__,"python":sys.version.split()[0],"platform":platform.platform(),"status":"ok","productionPersistence":"not configured","note":"Reference runtime healthy. Configure production adapters separately."}
        print(json.dumps(result, indent=2))
    elif a.cmd=="demo-manufacturing":
        ctx,proposal=build_demo()
        print(json.dumps({"context":asdict(ctx),"experienceProposal":asdict(proposal)}, ensure_ascii=False, indent=2, default=str))

if __name__ == "__main__": main()
