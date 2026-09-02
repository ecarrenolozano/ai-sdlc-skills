#!/usr/bin/env python3
"""Validate the required Structurizr Local Docker Compose configuration."""
from __future__ import annotations
import argparse, json, shutil, subprocess, sys
from pathlib import Path

def validate(compose: Path,check_runtime: bool=False)->dict:
 text=compose.read_text(encoding='utf-8')
 checks={'image':'image: structurizr/structurizr' in text,'local_command':'command: ["local"]' in text or "command: ['local']" in text,'port':'8080:8080' in text,'volume':'./:/usr/local/structurizr' in text,'not_lite':'structurizr/lite' not in text}
 runtime=None
 if check_runtime:
  docker=shutil.which('docker')
  if not docker: runtime={"passed":False,"reason":"docker executable unavailable"}
  else:
   cp=subprocess.run([docker,'compose','-f',str(compose),'config'],text=True,capture_output=True)
   runtime={"passed":cp.returncode==0,"exit_code":cp.returncode,"stdout":cp.stdout.strip(),"stderr":cp.stderr.strip()}
 passed=all(checks.values()) and (runtime is None or runtime['passed'])
 return {"passed":passed,"checks":checks,"runtime":runtime}

def main()->int:
 p=argparse.ArgumentParser(); p.add_argument('compose',type=Path); p.add_argument('--check-runtime',action='store_true'); a=p.parse_args(); result=validate(a.compose,a.check_runtime); print(json.dumps(result,indent=2)); return 0 if result['passed'] else 1
if __name__=='__main__':
 try: raise SystemExit(main())
 except OSError as exc: print(json.dumps({"passed":False,"error":str(exc)},indent=2),file=sys.stderr); raise SystemExit(2)
