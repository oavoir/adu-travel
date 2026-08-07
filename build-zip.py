#!/usr/bin/env python3
"""클로드 앱 업로드용 스킬 zip 생성.

앱은 스킬 폴더가 zip 최상위여야 하고, 한글 파일명 때문에 UTF-8 플래그가
반드시 설정돼야 한다. macOS 기본 `zip`은 이 플래그를 안 세워서 다른
환경에서 풀면 참고문서 파일명이 깨진다 — 그래서 파이썬으로 만든다.

    python3 build-zip.py
"""
import os
import zipfile

SRC = "skills/travel-planner"
OUT = "dist/travel-planner.zip"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
if os.path.exists(OUT):
    os.remove(OUT)

count = 0
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(SRC):
        dirs[:] = [d for d in dirs if d != "__MACOSX"]
        for name in sorted(files):
            if name == ".DS_Store":
                continue
            path = os.path.join(root, name)
            # zip 최상위가 travel-planner/ 가 되도록 skills/ 를 떼어낸다
            z.write(path, os.path.relpath(path, "skills"))
            count += 1

with zipfile.ZipFile(OUT) as z:
    bad = [
        i.filename
        for i in z.infolist()
        if any(ord(c) > 127 for c in i.filename) and not (i.flag_bits & 0x800)
    ]

print(f"{OUT} · 파일 {count}개 · {os.path.getsize(OUT) // 1024}KB")
print(f"UTF-8 플래그 누락: {len(bad)}건" + (f" — {bad}" if bad else " (정상)"))
