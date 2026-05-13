#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CLAIMS = ROOT / "public_claims.json"


def fail(message: str) -> None:
    print(f"publication validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def claims() -> dict:
    try:
        return json.loads(CLAIMS.read_text())
    except FileNotFoundError:
        fail("missing public_claims.json")
    except json.JSONDecodeError as exc:
        fail(f"public_claims.json is invalid JSON: {exc}")


def readme_image_refs() -> list[tuple[str, str]]:
    text = README.read_text()
    refs: list[tuple[str, str]] = []
    for match in re.finditer(r'<source[^>]+srcset="([^"]+)"', text):
        refs.append((match.group(1), ""))
    for match in re.finditer(r'<img[^>]+src="([^"]+)"[^>]+alt="([^"]+)"', text):
        refs.append((match.group(1), match.group(2)))
    return refs


def svg_aria_label(path: Path) -> str:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        fail(f"{path.name} is not valid SVG XML: {exc}")
    return root.attrib.get("aria-label", "").strip()


def validate_images() -> None:
    image_claims = claims().get("image_alt_text", {})
    refs = readme_image_refs()
    if not refs:
        fail("README.md does not reference any publication images")

    for ref, alt in refs:
        expected = image_claims.get(ref)
        if not expected:
            fail(f"public_claims.json is missing image_alt_text for {ref}")
        path = ROOT / ref
        if not path.exists():
            fail(f"README.md references missing image: {ref}")
        if path.suffix == ".svg":
            aria = svg_aria_label(path)
            if not aria:
                fail(f"{ref} is missing an aria-label")
            if aria != expected:
                fail(f"{ref} aria-label does not match public_claims.json")
            if alt and alt != expected:
                fail(f"README alt text for {ref} does not match public_claims.json")


def validate_links() -> None:
    text = README.read_text()
    links = re.findall(r'\]\((https?://[^)]+|mailto:[^)]+)\)', text)
    if not links:
        fail("README.md has no public links")
    required = set(claims().get("required_links", []))
    if not required:
        fail("public_claims.json must list required_links")
    missing = sorted(required - set(links))
    if missing:
        fail(f"README.md is missing required links: {', '.join(missing)}")


def main() -> None:
    validate_images()
    validate_links()
    print("publication validation passed")


if __name__ == "__main__":
    main()
