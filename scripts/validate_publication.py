#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ValidationError(Exception):
    pass


def fail(message: str) -> None:
    raise ValidationError(message)


@dataclass(frozen=True)
class ImageRef:
    path: str
    alt_text: str = ""


@dataclass(frozen=True)
class PublicClaims:
    image_alt_text: dict[str, str]
    required_links: set[str]

    @classmethod
    def load(cls, root: Path) -> "PublicClaims":
        claims_path = root / "public_claims.json"
        try:
            data = json.loads(claims_path.read_text())
        except FileNotFoundError:
            fail("missing public_claims.json")
        except json.JSONDecodeError as exc:
            fail(f"public_claims.json is invalid JSON: {exc}")

        return cls(
            image_alt_text=data.get("image_alt_text", {}),
            required_links=set(data.get("required_links", [])),
        )

    def expected_image_text(self, image_ref: ImageRef) -> str:
        expected = self.image_alt_text.get(image_ref.path)
        if not expected:
            fail(f"public_claims.json is missing image_alt_text for {image_ref.path}")
        return expected

    def require_links(self) -> set[str]:
        if not self.required_links:
            fail("public_claims.json must list required_links")
        return self.required_links


class PublicationValidator:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.readme_text = (root / "README.md").read_text()
        self.claims = PublicClaims.load(root)

    def validate(self) -> None:
        self._validate_images()
        self._validate_links()

    def _readme_image_refs(self) -> list[ImageRef]:
        refs: list[ImageRef] = []
        for match in re.finditer(r'<source[^>]+srcset="([^"]+)"', self.readme_text):
            refs.append(ImageRef(match.group(1)))
        for match in re.finditer(
            r'<img[^>]+src="([^"]+)"[^>]+alt="([^"]+)"', self.readme_text
        ):
            refs.append(ImageRef(match.group(1), match.group(2)))
        return refs

    def _readme_links(self) -> set[str]:
        return set(
            re.findall(r'\]\((https?://[^)]+|mailto:[^)]+)\)', self.readme_text)
        )

    def _validate_images(self) -> None:
        refs = self._readme_image_refs()
        if not refs:
            fail("README.md does not reference any publication images")

        for image_ref in refs:
            image_path = self.root / image_ref.path
            if not image_path.exists():
                fail(f"README.md references missing image: {image_ref.path}")
            self.claims.expected_image_text(image_ref)
            if image_ref.alt_text:
                self._validate_public_image_claim_text(
                    image_ref,
                    "README alt text",
                    image_ref.alt_text,
                )
            if image_path.suffix == ".svg":
                self._validate_svg_public_claim_text(image_ref, image_path)

    def _validate_svg_public_claim_text(
        self, image_ref: ImageRef, image_path: Path
    ) -> None:
        try:
            svg_root = ET.parse(image_path).getroot()
        except ET.ParseError as exc:
            fail(f"{image_path.name} is not valid SVG XML: {exc}")

        aria = svg_root.attrib.get("aria-label", "").strip()
        if not aria:
            fail(f"{image_ref.path} is missing an aria-label")
        self._validate_public_image_claim_text(image_ref, "aria-label", aria)

    def _validate_public_image_claim_text(
        self, image_ref: ImageRef, source: str, actual: str
    ) -> None:
        expected = self.claims.expected_image_text(image_ref)
        if actual != expected:
            fail(f"{source} for {image_ref.path} does not match public_claims.json")

    def _validate_links(self) -> None:
        links = self._readme_links()
        if not links:
            fail("README.md has no public links")
        missing = sorted(self.claims.require_links() - links)
        if missing:
            fail(f"README.md is missing required links: {', '.join(missing)}")


def validate_publication(root: Path) -> None:
    PublicationValidator(root).validate()


def write_publication_probe_fixture(
    root: Path,
    *,
    svg_aria: str,
    readme_alt: str,
    expected: str,
    extra_source: str | None = None,
    extra_source_claim: str | None = None,
) -> None:
    source_lines = []
    if extra_source:
        source_lines.append(f'  <source srcset="{extra_source}" />')
    (root / "README.md").write_text(
        "\n".join(
            [
                "<picture>",
                *source_lines,
                f'  <img src="claim.svg" alt="{readme_alt}" />',
                "</picture>",
                "[portfolio](https://example.com)",
            ]
        )
    )
    (root / "claim.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" role="img" '
        f'aria-label="{svg_aria}"></svg>'
    )
    if extra_source:
        (root / extra_source).write_bytes(b"publication probe image")
    image_alt_text = {"claim.svg": expected}
    if extra_source and extra_source_claim:
        image_alt_text[extra_source] = extra_source_claim
    (root / "public_claims.json").write_text(
        json.dumps(
            {
                "image_alt_text": image_alt_text,
                "required_links": ["https://example.com"],
            }
        )
    )


def assert_publication_probe_fails(
    *, svg_aria: str, readme_alt: str, expected: str, expected_error: str
) -> None:
    with tempfile.TemporaryDirectory(prefix="publication-validator-") as tmp:
        root = Path(tmp)
        write_publication_probe_fixture(
            root,
            svg_aria=svg_aria,
            readme_alt=readme_alt,
            expected=expected,
        )

        try:
            validate_publication(root)
        except ValidationError as exc:
            if expected_error in str(exc):
                return
            fail(f"failure probe raised the wrong validation error: {exc}")

    fail(f"failure probe did not reject {expected_error}")


def assert_non_svg_source_claim_is_required() -> None:
    with tempfile.TemporaryDirectory(prefix="publication-validator-") as tmp:
        root = Path(tmp)
        expected = "Expected publication claim."
        write_publication_probe_fixture(
            root,
            svg_aria=expected,
            readme_alt=expected,
            expected=expected,
            extra_source="claim.png",
        )

        try:
            validate_publication(root)
        except ValidationError as exc:
            expected_error = "public_claims.json is missing image_alt_text for claim.png"
            if expected_error in str(exc):
                return
            fail(f"non-SVG source probe raised the wrong validation error: {exc}")

    fail("non-SVG source probe did not require a public_claims.json entry")


def validate_failure_probe() -> None:
    """Prove both public image claim text call paths reject stale claims."""
    expected = "Expected publication claim."
    assert_publication_probe_fails(
        svg_aria="Stale publication claim.",
        readme_alt=expected,
        expected=expected,
        expected_error="aria-label for claim.svg does not match public_claims.json",
    )
    assert_publication_probe_fails(
        svg_aria=expected,
        readme_alt="Stale publication claim.",
        expected=expected,
        expected_error="README alt text for claim.svg does not match public_claims.json",
    )
    assert_non_svg_source_claim_is_required()


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
