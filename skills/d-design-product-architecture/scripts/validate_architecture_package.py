#!/usr/bin/env python3
"""Validate an architecture package against approved Product Requirements."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

SCRIPT_DIR=Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0,str(SCRIPT_DIR))

from validate_arc42_structure import validate as validate_arc42
from validate_container_structure import validate as validate_containers
from validate_structurizr_model import validate as validate_structurizr
from validate_diagram_documentation import validate as validate_diagrams
from validate_docker_compose import validate as validate_compose
from validate_architecture_hygiene import validate as validate_hygiene
from validate_product_behavior_discipline import validate as validate_behavior

def ids(pattern: str,text: str)->set[str]: return set(re.findall(pattern,text))

def field(text: str,name: str)->str:
    m=re.search(rf'(?mi)^- \*\*{re.escape(name)}:\*\*\s*(.+?)\s*$',text)
    return m.group(1).strip() if m else ''

def element_rows(text: str):
    m=re.search(r'(?ms)^## Architecture Element Register\s*$\n(.*?)(?=^##\s+|\Z)',text)
    if not m:return []
    lines=[l for l in m.group(1).splitlines() if l.strip().startswith('|')]
    if len(lines)<3:return []
    headers=[c.strip() for c in lines[0].strip().strip('|').split('|')]; rows=[]
    for line in lines[2:]:
        cells=[c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells)==len(headers): rows.append(dict(zip(headers,cells,strict=True)))
    return rows

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument('project_context',type=Path)
    p.add_argument('product_requirements',type=Path)
    p.add_argument('architecture_dir',type=Path)
    p.add_argument('--require-report-sync',action='store_true')
    a=p.parse_args(); root=a.architecture_dir
    arch=(root/'architecture.md').read_text(encoding='utf-8')
    req=a.product_requirements.read_text(encoding='utf-8')
    context=a.project_context.read_text(encoding='utf-8')
    errors=[]
    if '**Document state:** Closed' not in context and '**Document state:** Approved' not in context: errors.append({"code":"project_context_not_approved"})
    if '**Active scope state:** Approved' not in req: errors.append({"code":"requirements_not_approved"})
    req_open=field(req,'Unresolved blocking questions')
    if req_open and req_open!='0': errors.append({"code":"requirements_questions_open","value":req_open})
    caps=ids(r'\bCAP-\d{3,}\b',req); stories=ids(r'\bUS-\d{4,}\b',req)
    arch_caps=ids(r'\bCAP-\d{3,}\b',arch); arch_stories=ids(r'\bUS-\d{4,}\b',arch)
    if caps-arch_caps: errors.append({"code":"capabilities_omitted","ids":sorted(caps-arch_caps)})
    if arch_caps-caps: errors.append({"code":"unknown_capabilities","ids":sorted(arch_caps-caps)})
    if arch_stories-stories: errors.append({"code":"unknown_stories","ids":sorted(arch_stories-stories)})
    for cap in caps:
        if not re.search(rf'(?m)^\|\s*{re.escape(cap)}\s*\|.*\|\s*(Covered|Blocked|Not architecturally relevant)\s*\|',arch):
            errors.append({"code":"capability_without_coverage_disposition","id":cap})
    state=field(arch,'Architecture state')
    if state not in {'In Progress','Under Clarification','Pending Approval','Complete','Blocked'}: errors.append({"code":"invalid_architecture_state","state":state})
    unresolved=field(arch,'Unresolved material decisions')
    validation_result=field(arch,'Validation result')
    report_sync=field(arch,'Validation report synchronized')
    command=field(arch,'Architecture package validator command')
    unsupported=field(arch,'Unsupported product behavior introduced')
    if state in {'Pending Approval','Complete'} and unresolved!='0': errors.append({"code":"material_decisions_open","value":unresolved})
    if unsupported!='0': errors.append({"code":"unsupported_product_behavior","value":unsupported})
    if state in {'Pending Approval','Complete'}:
        proposed=[]
        for adr in (root/'adr').glob('ADR-*.md'):
            if re.search(r'(?mi)^- \*\*Status:\*\*\s*Proposed\s*$',adr.read_text(encoding='utf-8')): proposed.append(adr.name)
        if proposed: errors.append({"code":"essential_adr_not_accepted","files":proposed})
    if state=='Complete' and not re.search(r'(?m)^\|\s*ARCH-\d+\s*\|\s*Approved\s*\|\s*[^|]+\|\s*[^|]+\|\s*\d{4}-\d{2}-\d{2}\s*\|\s*None\s*\|',arch):
        errors.append({"code":"missing_valid_approval_record"})

    checks={
        'arc42':validate_arc42(root/'architecture.md'),
        'containers':validate_containers(root),
        'structurizr':validate_structurizr(root/'diagrams/workspace.dsl'),
        'diagrams':validate_diagrams(root),
        'compose':validate_compose(root/'diagrams/docker-compose.yml'),
        'hygiene':validate_hygiene(root),
        'behavior':validate_behavior(root),
    }
    for name,payload in checks.items():
        if not payload.get('passed'): errors.append({"code":f'{name}_validation_failed',"details":payload})
    boundaries=[r for r in element_rows(arch) if r.get('Type')=='Boundary']
    component_views=[v for v in checks['structurizr'].get('views',[]) if v.get('type')=='component']
    if boundaries and not component_views:
        errors.append({"code":"material_boundary_without_component_view","boundaries":[r.get('Name') for r in boundaries]})

    expected_command='python3 .agents/skills/d-design-product-architecture/scripts/validate_architecture_package.py sdlc_docs/00_inception/project_context.md sdlc_docs/01_requirements/product_requirements.md sdlc_docs/02_architecture --require-report-sync'
    calculated='Passed' if not errors else 'Failed'
    if a.require_report_sync:
        expected_fields={
            'arc42 structure validator':'Passed',
            'Container structure validator':'Passed',
            'Structurizr model validator':'Passed',
            'Diagram documentation validator':'Passed',
            'Docker Compose validator':'Passed',
            'Architecture hygiene validator':'Passed',
            'Product behavior discipline validator':'Passed',
        }
        for name,value in expected_fields.items():
            found=field(arch,name)
            if found!=value: errors.append({"code":"subvalidator_report_not_synchronized","field":name,"expected":value,"found":found})
        if command!=f'`{expected_command}`': errors.append({"code":"validation_command_not_synchronized","expected":expected_command,"found":command})
        if report_sync!='Yes': errors.append({"code":"validation_report_not_synchronized","found":report_sync})
        if validation_result!=calculated: errors.append({"code":"validation_result_not_synchronized","expected":calculated,"found":validation_result})
    result={
        'passed':not errors,
        'architecture_state':state,
        'capabilities':len(caps),
        'stories':len(stories),
        'containers':len(checks['containers'].get('expected_folders',[])),
        'material_boundaries':len(boundaries),
        'component_views':len(component_views),
        'checks':checks,
        'errors':errors,
        'calculated_validation_result':calculated,
        'expected_sync_command':expected_command,
    }
    print(json.dumps(result,indent=2))
    return 0 if not errors else 1

if __name__=='__main__':
    try: raise SystemExit(main())
    except OSError as exc: print(json.dumps({"passed":False,"error":str(exc)},indent=2),file=sys.stderr); raise SystemExit(2)
