#!/usr/bin/env python3
"""Validate architecture repository hygiene and current workflow identity."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
OBSOLETE=("e-architecture-and-design","d-user-story-product-readiness","f-user-story-technical-readiness"); TEMPLATES={"ADR-000-template.md","TEMPLATE.md","ADR-TEMPLATE.md"}

def validate(root: Path)->dict:
 errors=[]; readme=root/'README.md'
 if not readme.is_file(): errors.append({"code":"architecture_readme_missing"}); text=''
 else:
  text=readme.read_text(encoding='utf-8')
  if '`d-design-product-architecture`' not in text: errors.append({"code":"current_skill_not_identified"})
  for value in OBSOLETE:
   if value in text: errors.append({"code":"obsolete_workflow_identifier","value":value})
 gitignore=root/'diagrams/.gitignore'
 if not gitignore.is_file(): errors.append({"code":"diagram_gitignore_missing"})
 elif '.structurizr/' not in gitignore.read_text(encoding='utf-8'): errors.append({"code":"structurizr_runtime_not_ignored"})
 runtime=[str(p.relative_to(root)) for p in root.rglob('*') if '.structurizr' in p.parts]
 if runtime: errors.append({"code":"structurizr_runtime_artifacts_present","paths":runtime[:30]})
 adr=root/'adr'; copied=sorted(p.name for p in adr.iterdir() if p.is_file() and p.name in TEMPLATES) if adr.is_dir() else []
 if copied: errors.append({"code":"copied_adr_template","files":copied})
 return {"passed":not errors,"readme":str(readme),"diagram_gitignore":str(gitignore),"workspace_json_present":(root/'diagrams/workspace.json').is_file(),"errors":errors}

def main()->int:
 p=argparse.ArgumentParser(); p.add_argument('architecture_dir',type=Path); a=p.parse_args(); result=validate(a.architecture_dir); print(json.dumps(result,indent=2)); return 0 if result['passed'] else 1
if __name__=='__main__':
 try: raise SystemExit(main())
 except OSError as exc: print(json.dumps({"passed":False,"error":str(exc)},indent=2),file=sys.stderr); raise SystemExit(2)
