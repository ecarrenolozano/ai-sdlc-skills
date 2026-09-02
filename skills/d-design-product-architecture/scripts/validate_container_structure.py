#!/usr/bin/env python3
"""Validate one documentation folder per internal Structurizr container."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

def slug(name: str)->str: return re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')

def validate(root: Path)->dict:
 text=(root/'diagrams/workspace.dsl').read_text(encoding='utf-8')
 containers=re.findall(r'(?m)^\s*([A-Za-z_]\w*)\s*=\s*container\s+"([^"]+)"',text)
 expected={slug(name):(identifier,name) for identifier,name in containers}
 croot=root/'containers'; actual={p.name:p for p in croot.iterdir() if p.is_dir()} if croot.is_dir() else {}
 errors=[]
 for folder,(identifier,name) in expected.items():
  if folder not in actual: errors.append({"code":"container_folder_missing","container":name,"expected":folder}); continue
  doc=actual[folder]/'architecture.md'
  if not doc.is_file(): errors.append({"code":"container_document_missing","folder":folder}); continue
  content=doc.read_text(encoding='utf-8')
  if f'**Structurizr container identifier:** {identifier}' not in content: errors.append({"code":"container_identifier_mismatch","folder":folder,"identifier":identifier})
  if f'**Container folder:** {folder}' not in content: errors.append({"code":"container_folder_metadata_mismatch","folder":folder})
 for folder in sorted(set(actual)-set(expected)): errors.append({"code":"orphan_container_folder","folder":folder})
 return {"passed":not errors,"expected_folders":sorted(expected),"actual_folders":sorted(actual),"errors":errors}

def main()->int:
 p=argparse.ArgumentParser(); p.add_argument('architecture_dir',type=Path); a=p.parse_args(); result=validate(a.architecture_dir); print(json.dumps(result,indent=2)); return 0 if result['passed'] else 1
if __name__=='__main__':
 try: raise SystemExit(main())
 except OSError as exc: print(json.dumps({"passed":False,"error":str(exc)},indent=2),file=sys.stderr); raise SystemExit(2)
