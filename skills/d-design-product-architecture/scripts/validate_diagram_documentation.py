#!/usr/bin/env python3
"""Validate viewing instructions, Structurizr view references, and optional image links."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

def validate(root: Path)->dict:
 text=(root/'architecture.md').read_text(encoding='utf-8'); dsl=(root/'diagrams/workspace.dsl').read_text(encoding='utf-8'); errors=[]
 required=['## How to View This Architecture','sdlc_docs/02_architecture/diagrams/workspace.dsl','docker compose -f sdlc_docs/02_architecture/diagrams/docker-compose.yml up','docker compose -f sdlc_docs/02_architecture/diagrams/docker-compose.yml down','http://localhost:8080']
 for value in required:
  if value not in text: errors.append({"code":"missing_viewing_instruction","value":value})
 dsl_keys=set(re.findall(r'(?m)^\s*(?:systemContext|container|component|dynamic|deployment)\s+[^\n{]*?"([^"]+)"\s*\{',dsl))
 refs=re.findall(r'\*\*Structurizr view:\*\*\s*`([^`]+)`',text)
 for key in refs:
  if key not in dsl_keys: errors.append({"code":"unknown_view_key","key":key})
 images=re.findall(r'!\[[^\]]*\]\((diagrams/images/[^)]+)\)',text)
 for rel in images:
  path=root/rel
  if path.suffix.lower() not in {'.svg','.png'}: errors.append({"code":"unsupported_image_format","path":rel})
  elif not path.is_file(): errors.append({"code":"broken_image_link","path":rel})
 return {"passed":not errors,"view_references":refs,"image_references":images,"errors":errors}

def main()->int:
 p=argparse.ArgumentParser(); p.add_argument('architecture_dir',type=Path); a=p.parse_args(); result=validate(a.architecture_dir); print(json.dumps(result,indent=2)); return 0 if result['passed'] else 1
if __name__=='__main__':
 try: raise SystemExit(main())
 except OSError as exc: print(json.dumps({"passed":False,"error":str(exc)},indent=2),file=sys.stderr); raise SystemExit(2)
