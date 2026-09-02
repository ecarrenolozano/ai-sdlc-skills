#!/usr/bin/env python3
"""Check or create the minimum SDLC workspace without overwriting files."""
from __future__ import annotations
import argparse, json
from pathlib import Path

HEADER = "| Item | Type | Status | Current activity | Evidence | Missing or blocked | Next action |"
SEP = "|---|---|---|---|---|---|---|"
ROWS = [
("Project request","Foundation","Not Started","Request Clarification","None","Clarified request not approved","Continue with project request clarification"),
("Project context","Foundation","Not Started","Project Context Formation","None","Upstream project request incomplete","Continue after project request approval"),
("Initial requirements","Initial Release","Not Started","Product Requirements Management","None","Upstream project context incomplete","Continue after project context approval"),
("Architecture","Initial Release","Not Started","Product Architecture Design","None","Upstream requirements incomplete","Continue after requirements approval"),
("Repository preparation","Initial Release","Not Started","Repository Requirements Synchronization","None","Upstream architecture incomplete","Continue after architecture approval"),
("Technical foundation","Initial Release","Not Started","Technical Foundation Establishment","None","Repository preparation incomplete","Continue after repository preparation"),
("Implementation","Initial Release","Not Started","Repository Work Implementation","None","Technical foundation incomplete","Continue after technical foundation"),
("User story validation","Initial Release","Not Started","BDD User Story Completion Validation","None","Implementation incomplete","Continue after implementation"),
("Pull request","Initial Release","Not Started","Implementation Pull Request","None","User story validation incomplete","Continue after validation"),
("Release deployment","Initial Release","Not Started","Release and Deployment Preparation","None","Pull request incomplete","Continue after pull request"),
]

def expected(root: Path):
    return [root/'sdlc_docs', root/'sdlc_docs/00_inception', root/'sdlc_docs/00_inception/sources', root/'sdlc_docs/trace_workflow.md']

def trace_text():
    lines=["# SDLC Workflow Trace","",HEADER,SEP]
    lines += ["| " + " | ".join(r) + " |" for r in ROWS]
    return "\n".join(lines)+"\n"

def main():
    p=argparse.ArgumentParser(); g=p.add_mutually_exclusive_group(required=True); g.add_argument('--check',action='store_true'); g.add_argument('--apply',action='store_true'); p.add_argument('repository_root',type=Path); a=p.parse_args()
    root=a.repository_root.resolve(); trace=root/'sdlc_docs/trace_workflow.md'; missing=[str(x.relative_to(root)) for x in expected(root) if not x.exists()]
    result={'repository_root':str(root),'trace_exists':trace.is_file(),'missing':missing,'created':[],'errors':[]}
    if a.apply:
        if trace.exists(): result['errors'].append('trace already exists; refusing to overwrite')
        else:
            for d in [root/'sdlc_docs',root/'sdlc_docs/00_inception',root/'sdlc_docs/00_inception/sources']:
                if not d.exists(): d.mkdir(parents=True,exist_ok=True); result['created'].append(str(d.relative_to(root)))
            trace.write_text(trace_text(),encoding='utf-8'); result['created'].append(str(trace.relative_to(root))); result['trace_exists']=True; result['missing']=[]
    result['passed']=not result['errors'] and (result['trace_exists'] if a.apply else True)
    print(json.dumps(result,indent=2)); return 0 if result['passed'] else 1
if __name__=='__main__': raise SystemExit(main())
