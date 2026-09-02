#!/usr/bin/env python3
"""Validate explicit provenance for crosscutting behavior and prevent silent proposals."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
ALLOWED={"Confirmed requirement","Confirmed architect decision","Internal architecture constraint","Open decision","Not applicable"}

def field(text: str,name: str)->str:
 m=re.search(rf'(?mi)^- \*\*{re.escape(name)}:\*\*\s*(.+?)\s*$',text); return m.group(1).strip() if m else ''
def section(text: str,heading: str)->str:
 m=re.search(rf'(?ms)^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|^#\s+Workflow Extensions\s*$|\Z)',text); return m.group(1).strip() if m else ''
def parse_table(body: str):
 lines=[l for l in body.splitlines() if l.strip().startswith('|')]
 if len(lines)<3:return [],[]
 headers=[c.strip() for c in lines[0].strip().strip('|').split('|')]; rows=[]
 for line in lines[2:]:
  cells=[c.strip() for c in line.strip().strip('|').split('|')]
  if len(cells)==len(headers): rows.append(dict(zip(headers,cells,strict=True)))
 return headers,rows

def validate(root: Path)->dict:
 doc=(root/'architecture.md').read_text(encoding='utf-8'); state=field(doc,'Architecture state'); errors=[]
 headers,rows=parse_table(section(doc,'8. Crosscutting Concepts')); required=['Concept','Classification','Evidence','Architecture approach']
 if headers!=required: errors.append({"code":"crosscutting_table_schema","expected":required,"found":headers})
 for idx,row in enumerate(rows,1):
  classification=row.get('Classification',''); evidence=row.get('Evidence',''); approach=row.get('Architecture approach','')
  if classification not in ALLOWED: errors.append({"code":"invalid_crosscutting_classification","row":idx,"value":classification})
  if not evidence: errors.append({"code":"crosscutting_evidence_missing","row":idx})
  if classification=='Confirmed requirement' and not re.search(r'\b(?:CAP-\d{3,}|US-\d{4,}|Project Context|Product Requirements)\b',evidence): errors.append({"code":"requirement_evidence_missing","row":idx,"evidence":evidence})
  if classification=='Confirmed architect decision' and not re.search(r'\bADR-\d{3,}\b',evidence): errors.append({"code":"architect_decision_without_adr","row":idx,"evidence":evidence})
  if classification=='Internal architecture constraint' and not re.search(r'\b(?:ADR-\d{3,}|Architecture rationale|AE-\d{3,})\b',evidence): errors.append({"code":"internal_constraint_without_architecture_evidence","row":idx,"evidence":evidence})
  if classification=='Not applicable' and len(approach.split())<4: errors.append({"code":"unexplained_not_applicable","row":idx})
  if state in {'Pending Approval','Complete'} and classification=='Open decision': errors.append({"code":"open_crosscutting_decision_in_reviewable_baseline","row":idx})
 all_md='\n'.join(p.read_text(encoding='utf-8') for p in root.rglob('*.md'))
 if state in {'Pending Approval','Complete'}:
  if re.search(r'(?mi)(?:^|\|)\s*Proposed\s*(?:\||$)',all_md): errors.append({"code":"proposed_content_in_reviewable_baseline"})
  if 'Approved decision' in all_md: errors.append({"code":"ambiguous_prebaseline_approval_term","use":"Confirmed architect decision"})
 unsupported=field(doc,'Unsupported product behavior introduced')
 if unsupported!='0': errors.append({"code":"unsupported_product_behavior_count","value":unsupported})
 return {"passed":not errors,"architecture_state":state,"crosscutting_rows":len(rows),"errors":errors}

def main()->int:
 p=argparse.ArgumentParser(); p.add_argument('architecture_dir',type=Path); a=p.parse_args(); result=validate(a.architecture_dir); print(json.dumps(result,indent=2)); return 0 if result['passed'] else 1
if __name__=='__main__':
 try: raise SystemExit(main())
 except OSError as exc: print(json.dumps({"passed":False,"error":str(exc)},indent=2),file=sys.stderr); raise SystemExit(2)
