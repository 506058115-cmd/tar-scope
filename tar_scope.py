#!/usr/bin/env python3
"""Inspect tar archive paths and entry types without extracting files."""

import argparse
import ntpath
from pathlib import Path, PurePosixPath
import sys
import tarfile


GIB = 1024 ** 3


def terminal_safe(value):
    return "".join(
        char if char.isprintable() else char.encode("unicode_escape").decode("ascii")
        for char in value
    )


def unsafe_path(name):
    normalized = name.replace("\\", "/")
    drive, _ = ntpath.splitdrive(normalized)
    parts = PurePosixPath(normalized).parts
    reasons = []
    if normalized.startswith("/") or drive:
        reasons.append("包含根路径或盘符")
    if ".." in parts:
        reasons.append("包含 .. 路径段")
    return reasons


def human_size(size):
    value = float(size)
    for unit in ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB"):
        if value < 1024 or unit == "EiB":
            return f"{int(value)} {unit}" if unit == "B" else f"{value:.1f} {unit}"
        value /= 1024


def inspect(path, show_entries):
    with tarfile.open(path, mode="r:*") as archive:
        # ponytail: tarfile keeps headers in memory; stream them only if million-entry archives matter.
        entries = archive.getmembers()

    files = [entry for entry in entries if entry.isfile()]
    expanded = sum(entry.size for entry in files)
    print(
        f"{len(entries)} 个条目 · {len(files)} 个文件 · "
        f"声明展开大小 {human_size(expanded)} · 压缩包 {human_size(path.stat().st_size)}"
    )
    if expanded >= GIB:
        print("提示：声明的展开体积达到或超过 1 GiB。")

    findings = 0
    seen = set()
    for entry in entries:
        reasons = unsafe_path(entry.name)
        if entry.name in seen:
            reasons.append("重复条目名")
        seen.add(entry.name)
        if entry.issym():
            reasons.append(f"符号链接目标 {ascii(entry.linkname)}")
        elif entry.islnk():
            reasons.append(f"硬链接目标 {ascii(entry.linkname)}")
        elif not entry.isfile() and not entry.isdir():
            reasons.append("特殊文件类型")
        if reasons:
            findings += 1
            print(f"需留意: {ascii(entry.name)} · {'、'.join(reasons)}")
    if not findings:
        print("未发现明显的路径越界条目或链接；这不能证明压缩包安全。")

    if show_entries:
        print("\n压缩包条目")
        for entry in entries:
            kind = "目录" if entry.isdir() else human_size(entry.size)
            print(f"  {kind:>10}  {ascii(entry.name)}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="检查 tar 文件名、条目类型与声明体积，不解压、不写入文件。"
    )
    parser.add_argument("archive", help="tar、tar.gz、tar.xz 等归档文件路径")
    parser.add_argument("--list", action="store_true", help="列出所有条目名称与声明大小")
    args = parser.parse_args(argv)

    try:
        inspect(Path(args.archive).expanduser(), args.list)
    except (OSError, UnicodeError, tarfile.TarError, EOFError) as error:
        print(
            f"tar-scope: 无法读取归档：{terminal_safe(str(error))}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
