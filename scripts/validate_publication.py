#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ValidationError(Exception):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


def claims(root: Path) -> dict:
    claims_path = root / "public_claims.json"
    try:
        return json.loads(claims_path.read_text())
    except FileNotFoundError:
        fail("missing public_claims.json")
    except json.JSONDecodeError as exc:
        fail(f"public_claims.json is invalid JSON: {exc}")


def readme_image_refs(root: Path) -> list[tuple[str, str]]:
    text = (root / "README.md").read_text()
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


def validate_images(root: Path) -> None:
    image_claims = claims(root).get("image_alt_text", {})
    refs = readme_image_refs(root)
    if not refs:
        fail("README.md does not reference any publication images")

    for ref, alt in refs:
        expected = image_claims.get(ref)
        if not expected:
            fail(f"public_claims.json is missing image_alt_text for {ref}")
        path = root / ref
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


def validate_links(root: Path) -> None:
    text = (root / "README.md").read_text()
    links = re.findall(r'\]\((https?://[^)]+|mailto:[^)]+)\)', text)
    if not links:
        fail("README.md has no public links")
    required = set(claims(root).get("required_links", []))
    if not required:
        fail("public_claims.json must list required_links")
    missing = sorted(required - set(links))
    if missing:
        fail(f"README.md is missing required links: {', '.join(missing)}")


def validate_publication(root: Path) -> None:
    validate_images(root)
    validate_links(root)


def validate_failure_probe() -> None:
    """Prove the gate fails on stale SVG aria text."""
    expected = "Expected publication claim."
    with tempfile.TemporaryDirectory(prefix="publication-validator-") as tmp:
        root = Path(tmp)
        (root / "README.md").write_text(
            "\n".join(
                [
                    '<picture><img src="claim.svg" alt="Expected publication claim." /></picture>',
                    "[portfolio](https://example.com)",
                ]
            )
        )
        (root / "claim.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" role="img" '
            'aria-label="Stale publication claim."></svg>'
        )
        (root / "public_claims.json").write_text(
            json.dumps(
                {
                    "image_alt_text": {"claim.svg": expected},
                    "required_links": ["https://example.com"],
                }
            )
        )

        try:
            validate_publication(root)
        except ValidationError as exc:
            if "claim.svg aria-label does not match public_claims.json" in str(exc):
                return
            fail(f"failure probe raised the wrong validation error: {exc}")

    fail("failure probe did not reject stale SVG aria text")


def main() -> None:
    try:
        validate_publication(ROOT)
        validate_failure_probe()
    except ValidationError as exc:
        print(f"publication validation failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
    print("publication validation passed")


if __name__ == "__main__":
    main()
