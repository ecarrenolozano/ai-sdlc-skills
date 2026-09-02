#!/usr/bin/env python3
"""Run deterministic regression tests for Product Architecture Design."""
from __future__ import annotations
import json, os, shutil, subprocess, sys, tempfile
from pathlib import Path

SKILL=Path(__file__).resolve().parents[1]
SCRIPTS=SKILL/'scripts'
GOLD=SKILL/'references/golden-example/browser-task-board'
CHILD_TIMEOUT_SECONDS=20
SELFTEST_TIMEOUT_SECONDS=180

def call(script,*args):
    command=[sys.executable,str(SCRIPTS/script),*(str(a) for a in args)]
    try:
        return subprocess.run(command,text=True,capture_output=True,timeout=CHILD_TIMEOUT_SECONDS)
    except subprocess.TimeoutExpired as exc:
        stdout=exc.stdout if isinstance(exc.stdout,str) else (exc.stdout or b'').decode(errors='replace')
        stderr=exc.stderr if isinstance(exc.stderr,str) else (exc.stderr or b'').decode(errors='replace')
        return subprocess.CompletedProcess(command,124,stdout,stderr+f"\nTimed out after {CHILD_TIMEOUT_SECONDS} seconds")

def copy_project(tmp: Path):
    (tmp/'sdlc_docs/00_inception').mkdir(parents=True)
    (tmp/'sdlc_docs/01_requirements').mkdir(parents=True)
    arch=tmp/'sdlc_docs/02_architecture'
    shutil.copytree(GOLD/'containers',arch/'containers')
    shutil.copytree(GOLD/'diagrams',arch/'diagrams')
    shutil.copytree(GOLD/'adr',arch/'adr')
    shutil.copy2(GOLD/'README.md',arch/'README.md')
    shutil.copy2(GOLD/'out-architecture.md',arch/'architecture.md')
    shutil.copy2(GOLD/'in-project-context.md',tmp/'sdlc_docs/00_inception/project_context.md')
    shutil.copy2(GOLD/'in-product-requirements.md',tmp/'sdlc_docs/01_requirements/product_requirements.md')
    shutil.copy2(GOLD/'out-trace-workflow.md',tmp/'sdlc_docs/trace_workflow.md')
    return arch

def expect(name,cp,success):
    ok=(cp.returncode==0)==success
    print(f"TEST {name}: {'PASS' if ok else 'FAIL'}", file=sys.stderr, flush=True)
    return {"name":name,"passed":ok,"expected":"accepted" if success else "correctly rejected","exit_code":cp.returncode,"stdout":cp.stdout[-1600:],"stderr":cp.stderr[-1600:]}

def direct_expect(name: str, passed: bool, details: str = ""):
    print(f"TEST {name}: {'PASS' if passed else 'FAIL'}", file=sys.stderr, flush=True)
    return {"name": name, "passed": passed, "expected": "accepted", "exit_code": 0 if passed else 1, "stdout": details, "stderr": ""}

def architecture_text(root: Path) -> str:
    parts = []
    for path in root.rglob('*'):
        if path.is_file() and path.suffix in {'.md', '.dsl'}:
            parts.append(path.read_text(encoding='utf-8').lower())
    return '\n'.join(parts)

def no_mixed_obsolete_and_server_architecture(root: Path) -> tuple[bool, str]:
    text = architecture_text(root)
    obsolete_claims = [
        'no backend is',
        'no backend,',
        'no backend.',
        'no backend;',
        'no http api',
        'server-managed persistence are excluded',
        'server-managed data model is included',
    ]
    server_architecture = ['flask', 'sqlite', 'http/json']
    found_obsolete = [claim for claim in obsolete_claims if claim in text]
    found_server = [claim for claim in server_architecture if claim in text]
    passed = not (found_obsolete and found_server)
    return passed, json.dumps({"obsolete_claims": found_obsolete, "server_architecture": found_server})

def temp_regression_dirs() -> set[Path]:
    tmp=Path(tempfile.gettempdir())
    return {path for path in tmp.glob('d-architecture-regression-*') if path.exists()}

def runner_selftest():
    before=temp_regression_dirs()
    env=os.environ.copy()
    env['D_ARCHITECTURE_RUNNER_SELFTEST']='1'
    try:
        cp=subprocess.run([sys.executable,str(Path(__file__).resolve())],text=True,capture_output=True,timeout=SELFTEST_TIMEOUT_SECONDS,env=env)
    except subprocess.TimeoutExpired as exc:
        stdout=exc.stdout if isinstance(exc.stdout,str) else (exc.stdout or b'').decode(errors='replace')
        stderr=exc.stderr if isinstance(exc.stderr,str) else (exc.stderr or b'').decode(errors='replace')
        return False, json.dumps({"exit_code":124,"stdout":stdout[-1600:],"stderr":stderr[-1600:],"timeout_seconds":SELFTEST_TIMEOUT_SECONDS})
    after=temp_regression_dirs()
    leftovers=sorted(str(path) for path in after-before if path.exists())
    return cp.returncode==0 and not leftovers, json.dumps({"exit_code":cp.returncode,"leftovers":leftovers,"stdout":cp.stdout[-1600:],"stderr":cp.stderr[-1600:]})

def clone(base: Path, name: str) -> Path:
    t=base/name
    shutil.copytree(base/'sdlc_docs',t/'sdlc_docs')
    return t

def mutate(base: Path, name: str, rel: str, fn) -> Path:
    t=clone(base,name)
    p=t/'sdlc_docs/02_architecture'/rel
    p.write_text(fn(p.read_text(encoding='utf-8')),encoding='utf-8')
    return t

def main():
    results=[]
    with tempfile.TemporaryDirectory(prefix='d-architecture-regression-') as td:
        base=Path(td)
        arch=copy_project(base)
        ctx=base/'sdlc_docs/00_inception/project_context.md'
        req=base/'sdlc_docs/01_requirements/product_requirements.md'
        # Positive baseline checks
        results.append(expect('golden Browser Task Board package',call('validate_architecture_package.py',ctx,req,arch,'--require-report-sync'),True))
        results.append(expect('official arc42 structure',call('validate_arc42_structure.py',arch/'architecture.md'),True))
        results.append(expect('container folder mapping',call('validate_container_structure.py',arch),True))
        results.append(expect('Structurizr structural model and concise text',call('validate_structurizr_model.py',arch/'diagrams/workspace.dsl'),True))
        results.append(expect('viewing instructions and view references',call('validate_diagram_documentation.py',arch),True))
        results.append(expect('Structurizr Docker Compose',call('validate_docker_compose.py',arch/'diagrams/docker-compose.yml'),True))
        results.append(expect('architecture repository hygiene',call('validate_architecture_hygiene.py',arch),True))
        results.append(expect('product behavior provenance discipline',call('validate_product_behavior_discipline.py',arch),True))
        results.append(expect('workflow and flowchart alignment',call('validate_workflow_alignment.py',SKILL/'SKILL.md',SKILL/'references/process-flowchart.md'),True))
        results.append(expect('full skill identifiers only',call('validate_skill_identifier_discipline.py',SKILL),True))
        ok, details = no_mixed_obsolete_and_server_architecture(arch)
        results.append(direct_expect('golden has no obsolete no-backend plus Flask/SQLite contradiction', ok, details))

        # Skill identifier discipline defects
        alias_skill=base/'alias-skill'
        shutil.copytree(SKILL,alias_skill)
        p=alias_skill/'SKILL.md'
        alias='Do not invoke '+chr(69)
        p.write_text(p.read_text().replace('Do not invoke `e-sync-repository-requirements`', alias, 1))
        results.append(expect('single-letter skill alias',call('validate_skill_identifier_discipline.py',alias_skill),False))

        # arc42 defects
        t=mutate(base,'missing-section','architecture.md',lambda s:s.replace('## 8. Crosscutting Concepts','## Crosscutting Concepts'))
        results.append(expect('missing arc42 section',call('validate_arc42_structure.py',t/'sdlc_docs/02_architecture/architecture.md'),False))
        t=mutate(base,'out-of-order','architecture.md',lambda s:s.replace('## 6. Runtime View','## 7. Deployment View TEMP').replace('## 7. Deployment View','## 6. Runtime View').replace('## 7. Deployment View TEMP','## 7. Deployment View'))
        results.append(expect('arc42 sections out of order',call('validate_arc42_structure.py',t/'sdlc_docs/02_architecture/architecture.md'),False))
        t=mutate(base,'placeholder','architecture.md',lambda s:s.replace('No additional level-3 decomposition is required. Exact files, classes, route names, schemas, and test helpers belong to technical foundation and implementation planning after architecture approval.','TBD'))
        results.append(expect('blocking placeholder',call('validate_arc42_structure.py',t/'sdlc_docs/02_architecture/architecture.md'),False))

        # Hygiene defects observed in the first functional run
        t=clone(base,'missing-readme'); (t/'sdlc_docs/02_architecture/README.md').unlink()
        results.append(expect('missing architecture README',call('validate_architecture_hygiene.py',t/'sdlc_docs/02_architecture'),False))
        t=mutate(base,'obsolete-skill','README.md',lambda s:s.replace('d-design-product-architecture','e-architecture-and-design'))
        results.append(expect('obsolete architecture skill identity',call('validate_architecture_hygiene.py',t/'sdlc_docs/02_architecture'),False))
        t=clone(base,'runtime-artifacts'); p=t/'sdlc_docs/02_architecture/diagrams/.structurizr/logs'; p.mkdir(parents=True); (p/'structurizr.log').write_text('runtime')
        results.append(expect('Structurizr runtime artifacts',call('validate_architecture_hygiene.py',t/'sdlc_docs/02_architecture'),False))
        t=clone(base,'missing-gitignore'); (t/'sdlc_docs/02_architecture/diagrams/.gitignore').unlink()
        results.append(expect('missing Structurizr gitignore',call('validate_architecture_hygiene.py',t/'sdlc_docs/02_architecture'),False))
        t=clone(base,'copied-template'); (t/'sdlc_docs/02_architecture/adr/ADR-000-template.md').write_text('# Blank template\n')
        results.append(expect('copied ADR template',call('validate_architecture_hygiene.py',t/'sdlc_docs/02_architecture'),False))

        # Container and model defects
        t=clone(base,'missing-folder'); shutil.rmtree(t/'sdlc_docs/02_architecture/containers/browser-frontend')
        results.append(expect('container without folder',call('validate_container_structure.py',t/'sdlc_docs/02_architecture'),False))
        t=clone(base,'orphan-folder'); p=t/'sdlc_docs/02_architecture/containers/backend-api'; p.mkdir(); (p/'architecture.md').write_text('# Backend\n')
        results.append(expect('folder without container',call('validate_container_structure.py',t/'sdlc_docs/02_architecture'),False))
        t=mutate(base,'missing-context-view','diagrams/workspace.dsl',lambda s:s.replace('systemContext taskBoard "SystemContext"','systemContext taskBoard "ContextRenamed"'))
        results.append(expect('missing SystemContext view',call('validate_structurizr_model.py',t/'sdlc_docs/02_architecture/diagrams/workspace.dsl'),False))
        t=mutate(base,'missing-container-view','diagrams/workspace.dsl',lambda s:s.replace('container taskBoard "Containers"','container taskBoard "ContainerRenamed"'))
        results.append(expect('missing Containers view',call('validate_structurizr_model.py',t/'sdlc_docs/02_architecture/diagrams/workspace.dsl'),False))
        t=mutate(base,'components-no-view','diagrams/workspace.dsl',lambda s:s.replace('        component flaskBackend "FlaskBackendComponents" {\n            include *\n            autolayout lr\n        }\n\n',''))
        results.append(expect('components without Component view',call('validate_structurizr_model.py',t/'sdlc_docs/02_architecture/diagrams/workspace.dsl'),False))
        t=clone(base,'boundary-no-components'); p=t/'sdlc_docs/02_architecture/diagrams/workspace.dsl'; s=p.read_text();
        # remove component definitions, their relations, and component view while leaving Boundary in architecture register
        s='\n'.join(line for line in s.splitlines() if not any(token in line for token in ['apiRoutes = component','taskApplicationService = component','boardRepositoryPort = component','persistenceAdapter = component','statusCounter = component','frontendApiClient -> apiRoutes','apiRoutes -> taskApplicationService','taskApplicationService -> boardRepositoryPort','persistenceAdapter -> boardRepositoryPort','persistenceAdapter -> persistenceMechanism','taskApplicationService -> statusCounter']))
        start=s.find('        component flaskBackend "FlaskBackendComponents" {')
        if start>=0:
            end=s.find('        }',start)+9
            s=s[:start]+s[end:]
        p.write_text(s)
        results.append(expect('material Boundary without Component view',call('validate_architecture_package.py',t/'sdlc_docs/00_inception/project_context.md',t/'sdlc_docs/01_requirements/product_requirements.md',t/'sdlc_docs/02_architecture'),False))
        t=mutate(base,'verbose-person-label','diagrams/workspace.dsl',lambda s:s.replace('user -> browserFrontend "Uses"','user -> browserFrontend "Creates, moves, edits, deletes, restores, and counts tasks"'))
        results.append(expect('verbose person relationship label',call('validate_structurizr_model.py',t/'sdlc_docs/02_architecture/diagrams/workspace.dsl'),False))
        t=mutate(base,'long-container-description','diagrams/workspace.dsl',lambda s:s.replace('Provides the HTML, CSS, and JavaScript task-board user interface.','Provides the complete task-board experience, renders every section, creates tasks, moves tasks, edits tasks, deletes tasks, restores state, calculates counts, validates data, handles errors, and persists everything through browser-local storage.'))
        results.append(expect('overlong container description',call('validate_structurizr_model.py',t/'sdlc_docs/02_architecture/diagrams/workspace.dsl'),False))
        t=mutate(base,'deployment-view-missing-environment','diagrams/workspace.dsl',lambda s:s.replace('deployment taskBoard "Local Personal Deployment" "Deployment"', 'deployment taskBoard "Deployment"'))
        results.append(expect('deployment view missing environment',call('validate_structurizr_model.py',t/'sdlc_docs/02_architecture/diagrams/workspace.dsl'),False))
        t=mutate(base,'deployment-view-unknown-environment','diagrams/workspace.dsl',lambda s:s.replace('deployment taskBoard "Local Personal Deployment" "Deployment"', 'deployment taskBoard "Server" "Deployment"'))
        results.append(expect('deployment view unknown environment',call('validate_structurizr_model.py',t/'sdlc_docs/02_architecture/diagrams/workspace.dsl'),False))
        t=mutate(base,'obsolete-no-backend-with-server-architecture','architecture.md',lambda s:s.replace('The architecture does not add authentication, collaboration, or cross-device synchronization to the first release.','The architecture does not add authentication, collaboration, or cross-device synchronization to the first release. No backend is part of the first release.'))
        ok, details = no_mixed_obsolete_and_server_architecture(t/'sdlc_docs/02_architecture')
        results.append(direct_expect('obsolete no-backend plus Flask/SQLite contradiction', not ok, details))

        # Diagram and compose defects
        t=mutate(base,'unknown-view','architecture.md',lambda s:s.replace('`SystemContext`','`MissingView`',1))
        results.append(expect('unknown documented view',call('validate_diagram_documentation.py',t/'sdlc_docs/02_architecture'),False))
        t=mutate(base,'broken-image','architecture.md',lambda s:s.replace('No exported image is currently included. The architect may export SVG or PNG files into `sdlc_docs/02_architecture/diagrams/images/` and add verified relative links to this document. `workspace.dsl` remains canonical.','![System Context](diagrams/images/missing.svg)',1))
        results.append(expect('broken exported image link',call('validate_diagram_documentation.py',t/'sdlc_docs/02_architecture'),False))
        t=mutate(base,'obsolete-lite','diagrams/docker-compose.yml',lambda s:s.replace('structurizr/structurizr','structurizr/lite'))
        results.append(expect('obsolete Structurizr Lite compose',call('validate_docker_compose.py',t/'sdlc_docs/02_architecture/diagrams/docker-compose.yml'),False))
        t=clone(base,'valid-image'); image=t/'sdlc_docs/02_architecture/diagrams/images/system-context.svg'; image.parent.mkdir(); image.write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>'); p=t/'sdlc_docs/02_architecture/architecture.md'; p.write_text(p.read_text().replace('No exported image is currently included. The architect may export SVG or PNG files into `sdlc_docs/02_architecture/diagrams/images/` and add verified relative links to this document. `workspace.dsl` remains canonical.','![System Context](diagrams/images/system-context.svg)',1))
        results.append(expect('valid optional exported image',call('validate_diagram_documentation.py',t/'sdlc_docs/02_architecture'),True))

        # Product behavior discipline defects
        t=mutate(base,'proposed-behavior','architecture.md',lambda s:s.replace('| Local server security model | Confirmed architect decision |','| Keyboard-only interaction | Proposed |'))
        results.append(expect('proposed product-facing behavior in review baseline',call('validate_product_behavior_discipline.py',t/'sdlc_docs/02_architecture'),False))
        t=mutate(base,'ambiguous-approved','architecture.md',lambda s:s.replace('Confirmed architect decision','Approved decision',1))
        results.append(expect('ambiguous Approved decision terminology',call('validate_product_behavior_discipline.py',t/'sdlc_docs/02_architecture'),False))
        t=mutate(base,'unsupported-count','architecture.md',lambda s:s.replace('**Unsupported product behavior introduced:** 0','**Unsupported product behavior introduced:** 1'))
        results.append(expect('unsupported product behavior count',call('validate_product_behavior_discipline.py',t/'sdlc_docs/02_architecture'),False))
        t=mutate(base,'missing-crosscut-evidence','architecture.md',lambda s:s.replace('| API boundary | Confirmed architect decision | ADR-002 |','| API boundary | Confirmed architect decision |  |'))
        results.append(expect('crosscutting concept without evidence',call('validate_product_behavior_discipline.py',t/'sdlc_docs/02_architecture'),False))

        # Coverage, approval, and report defects
        t=mutate(base,'omitted-cap','architecture.md',lambda s:'\n'.join(line for line in s.splitlines() if not line.startswith('| CAP-006 |'))+'\n')
        results.append(expect('omitted approved capability',call('validate_architecture_package.py',t/'sdlc_docs/00_inception/project_context.md',t/'sdlc_docs/01_requirements/product_requirements.md',t/'sdlc_docs/02_architecture'),False))
        t=mutate(base,'unknown-story','architecture.md',lambda s:s.replace('US-0006','US-9999',1))
        results.append(expect('unknown story reference',call('validate_architecture_package.py',t/'sdlc_docs/00_inception/project_context.md',t/'sdlc_docs/01_requirements/product_requirements.md',t/'sdlc_docs/02_architecture'),False))
        t=clone(base,'unapproved-req'); p=t/'sdlc_docs/01_requirements/product_requirements.md'; p.write_text(p.read_text().replace('**Active scope state:** Approved','**Active scope state:** Under Clarification'))
        results.append(expect('unapproved requirements gate',call('validate_architecture_package.py',t/'sdlc_docs/00_inception/project_context.md',p,t/'sdlc_docs/02_architecture'),False))
        t=mutate(base,'report-mismatch','architecture.md',lambda s:s.replace('**Architecture hygiene validator:** Passed','**Architecture hygiene validator:** Not run'))
        results.append(expect('unsynchronized validation report',call('validate_architecture_package.py',t/'sdlc_docs/00_inception/project_context.md',t/'sdlc_docs/01_requirements/product_requirements.md',t/'sdlc_docs/02_architecture','--require-report-sync'),False))
        t=mutate(base,'open-decision','architecture.md',lambda s:s.replace('**Unresolved material decisions:** 0','**Unresolved material decisions:** 1'))
        results.append(expect('Pending Approval with open decision',call('validate_architecture_package.py',t/'sdlc_docs/00_inception/project_context.md',t/'sdlc_docs/01_requirements/product_requirements.md',t/'sdlc_docs/02_architecture'),False))
        t=clone(base,'complete'); p=t/'sdlc_docs/02_architecture/architecture.md'; s=p.read_text().replace('**Architecture state:** Pending Approval','**Architecture state:** Complete').replace('| ARCH-0001 | Pending approval |  |  |  | Human architecture review required |','| ARCH-0001 | Approved | Edwin Carreno | SSC Developer | 2026-07-24 | None |'); p.write_text(s)
        results.append(expect('explicitly approved complete baseline',call('validate_architecture_package.py',t/'sdlc_docs/00_inception/project_context.md',t/'sdlc_docs/01_requirements/product_requirements.md',t/'sdlc_docs/02_architecture','--require-report-sync'),True))

        # Multi-container mapping
        t=clone(base,'multi-container'); p=t/'sdlc_docs/02_architecture/diagrams/workspace.dsl'; s=p.read_text().replace('            browserFrontend = container', '            backendApi = container "Backend API" "Provides server-managed task operations." "HTTP API"\n            browserFrontend = container'); p.write_text(s); c=t/'sdlc_docs/02_architecture/containers/backend-api'; c.mkdir(); (c/'architecture.md').write_text('# Backend API Architecture\n\n- **Structurizr container identifier:** backendApi\n- **Container folder:** backend-api\n')
        results.append(expect('valid multi-container folder mapping',call('validate_container_structure.py',t/'sdlc_docs/02_architecture'),True))

        # Trace guards and transaction safety
        before=base/'before.md'; after=base/'after.md'; before.write_text((GOLD/'out-trace-workflow.md').read_text()); after.write_text(before.read_text().replace('| Architecture | Initial Release | Pending Approval |','| Architecture | Initial Release | Complete |'))
        allow=['--allow-field','Architecture:Status']
        results.append(expect('authorized Architecture trace mutation',call('validate_trace_mutation.py',before,after,*allow),True))
        bad=base/'bad.md'; bad.write_text(after.read_text().replace('| Project context | Foundation | Complete |','| Project context | Foundation | Blocked |'))
        results.append(expect('unauthorized trace mutation',call('validate_trace_mutation.py',before,bad,*allow),False))
        trace=base/'trace.md'; trace.write_text(before.read_text()); init=call('trace_transaction.py','init',trace); data=json.loads(init.stdout); Path(data['before']).unlink(); cp=call('trace_transaction.py','commit',data['manifest'],'--validator',SCRIPTS/'validate_trace_mutation.py','--','--allow-field','Architecture:Status')
        results.append(expect('missing transaction snapshot',cp,False))
        trace2=base/'trace2.md'; trace2.write_text(before.read_text()); init=call('trace_transaction.py','init',trace2); data=json.loads(init.stdout); Path(data['proposed']).write_text(after.read_text()); trace2.write_text(trace2.read_text()+'\nconcurrent\n'); cp=call('trace_transaction.py','commit',data['manifest'],'--validator',SCRIPTS/'validate_trace_mutation.py','--','--allow-field','Architecture:Status')
        results.append(expect('concurrent trace modification',cp,False))

    if os.environ.get('D_ARCHITECTURE_RUNNER_SELFTEST') != '1':
        ok, details=runner_selftest()
        results.append(direct_expect('regression runner self-test timeout and cleanup',ok,details))

    passed=all(r['passed'] for r in results)
    print(json.dumps({"passed":passed,"tests":len(results),"results":results},indent=2))
    return 0 if passed else 1

if __name__=='__main__':
    raise SystemExit(main())
