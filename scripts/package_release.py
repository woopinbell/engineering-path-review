#!/usr/bin/env python3
"""Create a deterministic, integrity-checked release ZIP."""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
REPO_NAME = "engineering-path-review"
DEFAULT_OUTPUT = ROOT / "dist" / f"{REPO_NAME}.zip"
MANIFEST = ROOT / "MANIFEST.sha256"
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def ignored(path: Path) -> bool:
    relative = path.relative_to(ROOT)
    return bool(relative.parts and relative.parts[0] == "dist")


def clean_local_caches() -> None:
    for directory in sorted(ROOT.rglob("__pycache__"), reverse=True):
        if directory.is_dir() and not directory.is_symlink():
            shutil.rmtree(directory)
    for path in ROOT.rglob("*.pyc"):
        if path.is_file() and not path.is_symlink():
            path.unlink()


def files_for_package() -> list[Path]:
    result: list[Path] = []
    for path in ROOT.rglob("*"):
        if ignored(path):
            continue
        if path.is_symlink():
            raise RuntimeError(f"symlink is not allowed: {path.relative_to(ROOT)}")
        if path.is_file():
            result.append(path)
    return sorted(result, key=lambda path: path.relative_to(ROOT).as_posix())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_check() -> None:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        ["make", "check"],
        cwd=ROOT,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "repository check failed")


def write_manifest() -> None:
    entries = []
    for path in files_for_package():
        relative = path.relative_to(ROOT).as_posix()
        if relative == "MANIFEST.sha256":
            continue
        entries.append(f"{sha256(path)}  {relative}")
    content = "\n".join(entries) + "\n"
    fd, name = tempfile.mkstemp(prefix=".MANIFEST.", dir=ROOT, text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, MANIFEST)
    except Exception:
        Path(name).unlink(missing_ok=True)
        raise


def mode_for(path: Path) -> int:
    relative = path.relative_to(ROOT).as_posix()
    if relative.startswith("scripts/") or "/scripts/" in relative or relative.endswith(".sh"):
        return 0o755
    return 0o644


def create_zip(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{output.name}.", dir=output.parent)
    os.close(fd)
    temp_path = Path(temp_name)
    try:
        with zipfile.ZipFile(temp_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in files_for_package():
                relative = path.relative_to(ROOT).as_posix()
                arcname = f"{REPO_NAME}/{relative}"
                info = zipfile.ZipInfo(arcname, date_time=FIXED_TIME)
                info.create_system = 3
                info.external_attr = (mode_for(path) & 0xFFFF) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        os.replace(temp_path, output)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise


def verify_zip(output: Path) -> None:
    expected = {f"{REPO_NAME}/{path.relative_to(ROOT).as_posix()}" for path in files_for_package()}
    with zipfile.ZipFile(output) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            raise RuntimeError("ZIP contains duplicate entries")
        for name in names:
            pure = PurePosixPath(name)
            if pure.is_absolute() or ".." in pure.parts or not name.startswith(f"{REPO_NAME}/"):
                raise RuntimeError(f"unsafe ZIP path: {name}")
            info = archive.getinfo(name)
            mode = (info.external_attr >> 16) & 0o170000
            if mode == 0o120000:
                raise RuntimeError(f"ZIP symlink entry: {name}")
        if set(names) != expected:
            missing = sorted(expected - set(names))
            extra = sorted(set(names) - expected)
            raise RuntimeError(f"ZIP file set mismatch; missing={missing[:5]} extra={extra[:5]}")
        with tempfile.TemporaryDirectory(prefix="engineering-path-review-verify-") as directory:
            archive.extractall(directory)
            extracted = Path(directory) / REPO_NAME
            environment = os.environ.copy()
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            result = subprocess.run(
                ["make", "check"],
                cwd=extracted,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            if result.returncode:
                raise RuntimeError(
                    "extracted package check failed: " + (result.stderr.strip() or result.stdout.strip())
                )


def write_external_hash(output: Path) -> Path:
    hash_path = output.with_name(output.name + ".sha256")
    content = f"{sha256(output)}  {output.name}\n"
    hash_path.write_text(content, encoding="utf-8", newline="\n")
    return hash_path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    try:
        clean_local_caches()
        MANIFEST.unlink(missing_ok=True)
        run_check()
        write_manifest()
        run_check()
        create_zip(output)
        verify_zip(output)
        hash_path = write_external_hash(output)
    except (OSError, RuntimeError, zipfile.BadZipFile) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {output}")
    print(f"wrote {hash_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
