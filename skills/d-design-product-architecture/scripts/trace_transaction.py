#!/usr/bin/env python3
"""Create and commit guarded trace_workflow.md mutations atomically."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def emit(payload: dict, *, stream=sys.stdout) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False), file=stream)


def init_transaction(source: Path) -> int:
    source = source.resolve()
    if not source.is_file():
        emit({"passed": False, "error": f"Traceability source does not exist: {source}"}, stream=sys.stderr)
        return 2

    txn_dir = Path(tempfile.mkdtemp(prefix="d-architecture-trace-"))
    before = txn_dir / "before.md"
    proposed = txn_dir / "proposed.md"
    manifest = txn_dir / "manifest.json"

    try:
        shutil.copy2(source, before)
        shutil.copy2(source, proposed)
        if not before.is_file() or not proposed.is_file():
            raise OSError("Transaction snapshot files were not created")
        source_hash = sha256(source)
        if sha256(before) != source_hash or sha256(proposed) != source_hash:
            raise OSError("Transaction snapshot hash mismatch")
        data = {
            "version": 1,
            "source": str(source),
            "before": str(before),
            "proposed": str(proposed),
            "source_sha256": source_hash,
        }
        manifest.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    except Exception as exc:
        shutil.rmtree(txn_dir, ignore_errors=True)
        emit({"passed": False, "error": str(exc)}, stream=sys.stderr)
        return 2

    emit({
        "passed": True,
        "manifest": str(manifest),
        "before": str(before),
        "proposed": str(proposed),
        "source": str(source),
        "source_sha256": source_hash,
    })
    return 0


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = {"version", "source", "before", "proposed", "source_sha256"}
    missing = sorted(required - data.keys())
    if missing:
        raise ValueError(f"Manifest missing fields: {', '.join(missing)}")
    if data["version"] != 1:
        raise ValueError(f"Unsupported manifest version: {data['version']}")
    return data


def commit_transaction(manifest_path: Path, validator: Path, validator_args: list[str], cleanup: bool) -> int:
    manifest_path = manifest_path.resolve()
    validator = validator.resolve()
    try:
        data = load_manifest(manifest_path)
        source = Path(data["source"])
        before = Path(data["before"])
        proposed = Path(data["proposed"])
        for label, path in (("source", source), ("before", before), ("proposed", proposed), ("validator", validator)):
            if not path.is_file():
                raise OSError(f"Required {label} file does not exist: {path}")
        current_hash = sha256(source)
        if current_hash != data["source_sha256"]:
            raise RuntimeError("Canonical traceability file changed after transaction initialization")
        if sha256(before) != data["source_sha256"]:
            raise RuntimeError("Before snapshot no longer matches the initialized canonical file")

        command = [sys.executable, str(validator), str(before), str(proposed), *validator_args]
        completed = subprocess.run(command, text=True, capture_output=True, check=False)
        validator_stdout = completed.stdout.strip()
        validator_stderr = completed.stderr.strip()
        if completed.returncode != 0:
            emit({
                "passed": False,
                "committed": False,
                "validator_exit_code": completed.returncode,
                "validator_stdout": validator_stdout,
                "validator_stderr": validator_stderr,
                "source_unchanged": sha256(source) == data["source_sha256"],
            }, stream=sys.stderr if completed.returncode == 2 else sys.stdout)
            return 1 if completed.returncode == 1 else 2

        temp_target = source.with_name(f".{source.name}.d-architecture-{os.getpid()}.tmp")
        shutil.copy2(proposed, temp_target)
        os.replace(temp_target, source)
        emit({
            "passed": True,
            "committed": True,
            "source": str(source),
            "before_sha256": data["source_sha256"],
            "after_sha256": sha256(source),
            "validator_exit_code": 0,
            "validator_stdout": validator_stdout,
        })
        if cleanup:
            shutil.rmtree(manifest_path.parent, ignore_errors=True)
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        emit({"passed": False, "committed": False, "error": str(exc)}, stream=sys.stderr)
        return 2


def abort_transaction(manifest_path: Path) -> int:
    try:
        data = load_manifest(manifest_path.resolve())
        source = Path(data["source"])
        unchanged = source.is_file() and sha256(source) == data["source_sha256"]
        shutil.rmtree(manifest_path.resolve().parent, ignore_errors=True)
        emit({"passed": True, "aborted": True, "source_unchanged": unchanged})
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        emit({"passed": False, "error": str(exc)}, stream=sys.stderr)
        return 2


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init")
    init_parser.add_argument("source", type=Path)

    commit_parser = sub.add_parser("commit")
    commit_parser.add_argument("manifest", type=Path)
    commit_parser.add_argument("--validator", required=True, type=Path)
    commit_parser.add_argument("--cleanup", action="store_true")

    abort_parser = sub.add_parser("abort")
    abort_parser.add_argument("manifest", type=Path)

    args, extra = parser.parse_known_args()
    if args.command == "init":
        if extra:
            parser.error(f"unexpected arguments: {' '.join(extra)}")
        return init_transaction(args.source)
    if args.command == "commit":
        if extra and extra[0] == "--":
            extra = extra[1:]
        return commit_transaction(args.manifest, args.validator, extra, args.cleanup)
    if extra:
        parser.error(f"unexpected arguments: {' '.join(extra)}")
    return abort_transaction(args.manifest)


if __name__ == "__main__":
    raise SystemExit(main())
