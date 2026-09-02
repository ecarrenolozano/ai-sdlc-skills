#!/usr/bin/env python3
"""Validate the official arc42 root section order and baseline content."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

EXPECTED=["Introduction and Goals","Constraints","Context and Scope","Solution Strategy","Building Block View","Runtime View","Deployment View","Crosscutting Concepts","Architectural Decisions","Quality Requirements","Risks and Technical Debt","Glossary"]
REQUIRED_SUBSECTIONS=["1.1 Requirements Overview","1.2 Quality Goals","1.3 Stakeholders","3.1 Business Context","5.1 Whitebox Overall System","10.1 Quality Requirements Overview","10.2 Quality Scenarios"]
PLACEHOLDER=re.compile(r"(?im)^\s*(?:TBD|TODO|N/?A|To be defined|<[^>]+>)\s*[.!]?$|\[TODO\]")

def section_body(text: str, heading: str) -> str:
 m=re.search(rf"(?ms)^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|^#\s+Workflow Extensions\s*$|\Z)",text)
 return m.group(1).strip() if m else ""

def validate(architecture: Path) -> dict:
 text=architecture.read_text(encoding='utf-8')
 found=[(int(n),title.strip()) for n,title in re.findall(r"(?m)^##\s+(\d+)\.\s+(.+?)\s*$",text)]
 errors=[]; expected_pairs=list(enumerate(EXPECTED,start=1))
 if found!=expected_pairs: errors.append({"code":"arc42_order","expected":expected_pairs,"found":found})
 if '## How to View This Architecture' not in text: errors.append({"code":"missing_viewing_instructions"})
 for n,title in expected_pairs:
  body=section_body(text,f'{n}. {title}')
  if not body: errors.append({"code":"empty_arc42_section","section":n})
  elif PLACEHOLDER.search(body): errors.append({"code":"blocking_placeholder","section":n})
  elif re.fullmatch(r"(?is)(?:not applicable|deferred)\.?",body.strip()): errors.append({"code":"unexplained_non_applicable","section":n})
 for subsection in REQUIRED_SUBSECTIONS:
  if not re.search(rf"(?m)^###\s+{re.escape(subsection)}\s*$",text): errors.append({"code":"missing_recommended_subsection","subsection":subsection})
 return {"passed":not errors,"sections":found,"errors":errors}

def main()->int:
 p=argparse.ArgumentParser(); p.add_argument('architecture',type=Path); a=p.parse_args(); result=validate(a.architecture); print(json.dumps(result,indent=2)); return 0 if result['passed'] else 1
if __name__=='__main__':
 try: raise SystemExit(main())
 except OSError as exc: print(json.dumps({"passed":False,"error":str(exc)},indent=2),file=sys.stderr); raise SystemExit(2)
