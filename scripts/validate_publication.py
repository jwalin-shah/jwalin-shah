#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"


class ReadmeHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tags: list[tuple[str, dict[str, str]]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append((tag, {name: value or "" for name, value in attrs}))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def readme_tags() -> list[tuple[str, dict[str, str]]]:
    parser = ReadmeHTMLParser()
    parser.feed(README.read_text(encoding="utf-8"))
    return parser.tags


def local_refs_from_srcset(srcset: str) -> list[str]:
    refs: list[str] = []
    for part in srcset.split(","):
        ref = part.strip().split(" ", 1)[0]
        if ref:
            refs.append(ref)
    return refs


def is_remote_or_special(ref: str) -> bool:
    parsed = urlparse(ref)
    return parsed.scheme in {"http", "https", "mailto"} or ref.startswith("#")


def assert_local_file(errors: list[str], ref: str, owner: str) -> None:
    if is_remote_or_special(ref):
        return
    path = (ROOT / ref).resolve()
    if ROOT not in path.parents and path != ROOT:
        fail(errors, f"{owner}: local ref escapes repo: {ref}")
        return
    if not path.exists():
        fail(errors, f"{owner}: local ref is missing: {ref}")


def svg_accessibility(path: Path, errors: list[str]) -> str:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        fail(errors, f"{path.name}: invalid SVG XML: {exc}")
        return ""

    role = root.attrib.get("role")
    label = normalize(root.attrib.get("aria-label", ""))
    if role != "img":
        fail(errors, f"{path.name}: expected role=\"img\"")
    if not label:
        fail(errors, f"{path.name}: missing aria-label")
    return label


def readme_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)


def validate_links(errors: list[str], text: str, tags: list[tuple[str, dict[str, str]]]) -> None:
    for tag, attrs in tags:
        for attr in ("src", "href"):
            if attr in attrs:
                ref = attrs[attr]
                if tag == "a" and ref:
                    validate_url(errors, ref, f"<{tag} {attr}>")
                assert_local_file(errors, ref, f"<{tag} {attr}>")
        if "srcset" in attrs:
            for ref in local_refs_from_srcset(attrs["srcset"]):
                assert_local_file(errors, ref, f"<{tag} srcset>")

    for label, ref in readme_markdown_links(text):
        validate_url(errors, ref, f"markdown link {label!r}")
        assert_local_file(errors, ref, f"markdown link {label!r}")


def validate_url(errors: list[str], ref: str, owner: str) -> None:
    if ref.startswith("#"):
        return
    parsed = urlparse(ref)
    if parsed.scheme in {"http", "https"} and not parsed.netloc:
        fail(errors, f"{owner}: malformed URL: {ref}")
    elif parsed.scheme == "mailto" and "@" not in parsed.path:
        fail(errors, f"{owner}: malformed mailto: {ref}")
    elif parsed.scheme and parsed.scheme not in {"http", "https", "mailto"}:
        fail(errors, f"{owner}: unsupported URL scheme: {ref}")


def validate_picture_labels(tags: list[tuple[str, dict[str, str]]], errors: list[str]) -> None:
    pending_sources: list[str] = []
    for tag, attrs in tags:
        if tag == "source" and "srcset" in attrs:
            pending_sources.extend(local_refs_from_srcset(attrs["srcset"]))
        elif tag == "img":
            alt = normalize(attrs.get("alt", ""))
            src = attrs.get("src", "")
            if not alt:
                fail(errors, f"README image {src or '<missing src>'}: missing alt text")
            refs = pending_sources + ([src] if src else [])
            pending_sources = []
            for ref in refs:
                if ref.endswith(".svg") and (ROOT / ref).exists():
                    label = svg_accessibility(ROOT / ref, errors)
                    if label and label != alt:
                        fail(errors, f"{ref}: aria-label does not match README alt text")


def validate_claims(errors: list[str]) -> None:
    hero_label = svg_accessibility(ROOT / "hero-light.svg", errors)
    stats_label = svg_accessibility(ROOT / "stats-light.svg", errors)
    expected_hero_claims = ["3 scalars", "71M", "0.975 F1", "0.331", "transitive closure"]
    expected_stats_claims = ["19 public repos", "Python 80%", "TypeScript 9%", "JavaScript 3%", "Svelte 3%", "Shell 3%", "Other 2%", "26-week"]
    for claim in expected_hero_claims:
        if claim not in hero_label:
            fail(errors, f"hero-light.svg: missing headline claim in aria-label: {claim}")
    for claim in expected_stats_claims:
        if claim not in stats_label:
            fail(errors, f"stats-light.svg: missing stats claim in aria-label: {claim}")


def main() -> int:
    errors: list[str] = []
    if not README.exists():
        print("publication validation failed")
        print("- README.md is missing")
        return 1

    text = README.read_text(encoding="utf-8")
    tags = readme_tags()
    validate_links(errors, text, tags)
    validate_picture_labels(tags, errors)
    validate_claims(errors)

    if errors:
        print("publication validation failed")
        for error in errors:
            print(f"- {error}")
        return 1

    print("publication validation passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
