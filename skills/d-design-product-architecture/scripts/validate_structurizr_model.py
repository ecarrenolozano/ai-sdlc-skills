#!/usr/bin/env python3
"""Perform deterministic structural and diagram-text checks on Structurizr DSL."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path

def validate(workspace: Path)->dict:
 text=workspace.read_text(encoding='utf-8'); errors=[]
 persons=re.findall(r'(?m)^\s*([A-Za-z_]\w*)\s*=\s*person\s+"([^"]+)"',text)
 systems=re.findall(r'(?m)^\s*([A-Za-z_]\w*)\s*=\s*softwareSystem\s+"([^"]+)"',text)
 containers=re.findall(r'(?m)^\s*([A-Za-z_]\w*)\s*=\s*container\s+"([^"]+)"\s+"([^"]*)"',text)
 components=re.findall(r'(?m)^\s*([A-Za-z_]\w*)\s*=\s*component\s+"([^"]+)"',text)
 deployment_environments=set(re.findall(r'(?m)^\s*deploymentEnvironment\s+"([^"]+)"\s*\{',text))
 view_pairs=re.findall(r'(?m)^\s*(systemContext|container|component|dynamic|deployment)\s+[^\n{]*?"([^"]+)"\s*\{',text); keys=[k for _,k in view_pairs]
 if not re.search(r'(?m)^\s*workspace\s+"',text): errors.append({"code":"missing_workspace"})
 if not systems: errors.append({"code":"missing_software_system"})
 if not containers: errors.append({"code":"missing_container"})
 if 'SystemContext' not in keys: errors.append({"code":"missing_system_context_view"})
 if 'Containers' not in keys: errors.append({"code":"missing_container_view"})
 if components and not any(t=='component' for t,_ in view_pairs): errors.append({"code":"components_without_component_view"})
 duplicates=sorted({k for k in keys if keys.count(k)>1})
 if duplicates: errors.append({"code":"duplicate_view_keys","keys":duplicates})
 defined={i for i,_ in persons+systems+components}|{i for i,_,_ in containers}; person_ids={i for i,_ in persons}
 for left,right,label in re.findall(r'(?m)^\s*([A-Za-z_]\w*)\s*->\s*([A-Za-z_]\w*)\s+"([^"]*)"',text):
  for identifier in (left,right):
   if identifier not in defined: errors.append({"code":"undefined_relationship_element","identifier":identifier})
  if left in person_ids and (label.count(',')>1 or len(label.split())>10): errors.append({"code":"verbose_person_relationship","relationship":f'{left}->{right}',"label":label})
 for identifier,name,description in containers:
  if len(description)>160: errors.append({"code":"container_description_too_long","container":name,"length":len(description)})
 for line_no,line in enumerate(text.splitlines(),start=1):
  m=re.match(r'^\s*deployment\s+([A-Za-z_]\w*)\s+(.+?)\s*\{\s*$',line)
  if not m: continue
  quoted=re.findall(r'"([^"]+)"',m.group(2))
  if len(quoted)<2:
   errors.append({"code":"deployment_view_missing_environment","line":line_no,"view":quoted[0] if quoted else ""})
   continue
  if quoted[0] not in deployment_environments:
   errors.append({"code":"deployment_view_unknown_environment","line":line_no,"environment":quoted[0]})
 return {"passed":not errors,"software_systems":[{"identifier":i,"name":n} for i,n in systems],"containers":[{"identifier":i,"name":n,"description_length":len(d)} for i,n,d in containers],"components":[{"identifier":i,"name":n} for i,n in components],"views":[{"type":t,"key":k} for t,k in view_pairs],"errors":errors}

def main()->int:
 p=argparse.ArgumentParser(); p.add_argument('workspace',type=Path); a=p.parse_args(); result=validate(a.workspace); print(json.dumps(result,indent=2)); return 0 if result['passed'] else 1
if __name__=='__main__':
 try: raise SystemExit(main())
 except OSError as exc: print(json.dumps({"passed":False,"error":str(exc)},indent=2),file=sys.stderr); raise SystemExit(2)
