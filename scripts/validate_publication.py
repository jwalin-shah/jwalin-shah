#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUNTIME_DIR = ROOT / ".runtime" / "publication-validator"


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

        if not isinstance(data, dict):
            fail("public_claims.json must be a JSON object")

        image_alt_text = data.get("image_alt_text")
        if not isinstance(image_alt_text, dict) or not image_alt_text:
            fail("public_claims.json image_alt_text must be a non-empty object")
        for image_path, expected_text in image_alt_text.items():
            if not isinstance(image_path, str) or not image_path:
                fail("public_claims.json image_alt_text keys must be non-empty strings")
            if not isinstance(expected_text, str) or not expected_text.strip():
                fail("public_claims.json image_alt_text values must be non-empty strings")

        required_links = data.get("required_links")
        if not isinstance(required_links, list) or not required_links:
            fail("public_claims.json required_links must be a non-empty list")
        for link in required_links:
            if not isinstance(link, str) or not link:
                fail("public_claims.json required_links must contain only non-empty strings")

        return cls(
            image_alt_text=image_alt_text,
            required_links=set(required_links),
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
        try:
            self.readme_text = (root / "README.md").read_text()
        except FileNotFoundError:
            fail(f"missing README.md in {root}")
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


def write_valid_fixture(root: Path) -> None:
    expected = "Expected publication claim."
    write_publication_probe_fixture(
        root,
        svg_aria=expected,
        readme_alt=expected,
        expected=expected,
    )


def assert_publication_probe_fails(
    *,
    runtime_dir: Path,
    svg_aria: str,
    readme_alt: str,
    expected: str,
    expected_error: str,
) -> None:
    runtime_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="fixture-failure-", dir=runtime_dir
    ) as tmp:
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
    with tempfile.TemporaryDirectory(prefix="fixture-source-") as tmp:
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


def validate_failure_probe(runtime_dir: Path) -> None:
    """Prove both public image claim text call paths reject stale claims."""
    expected = "Expected publication claim."
    assert_publication_probe_fails(
        runtime_dir=runtime_dir,
        svg_aria="Stale publication claim.",
        readme_alt=expected,
        expected=expected,
        expected_error="aria-label for claim.svg does not match public_claims.json",
    )
    assert_publication_probe_fails(
        runtime_dir=runtime_dir,
        svg_aria=expected,
        readme_alt="Stale publication claim.",
        expected=expected,
        expected_error="README alt text for claim.svg does not match public_claims.json",
    )
    assert_non_svg_source_claim_is_required()


def validate_malformed_claims_probe(runtime_dir: Path) -> None:
    """Prove malformed public_claims.json fails before producing bad comparisons."""
    runtime_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix="fixture-malformed-claims-", dir=runtime_dir
    ) as tmp:
        root = Path(tmp)
        write_valid_fixture(root)
        (root / "public_claims.json").write_text(
            json.dumps(
                {
                    "image_alt_text": {"claim.svg": "Expected publication claim."},
                    "required_links": "https://example.com",
                }
            )
        )

        try:
            validate_publication(root)
        except ValidationError as exc:
            if "public_claims.json required_links must be a non-empty list" in str(exc):
                return
            fail(f"malformed claims probe raised the wrong validation error: {exc}")

    fail("malformed claims probe did not reject invalid required_links")


def validate_cli_smoke_contract(runtime_dir: Path) -> None:
    """Exercise imports, argument parsing, success, and bad-input reporting."""
    args = parse_args(["--root", ".", "--smoke"])
    if args.root != Path(".") or not args.smoke:
        fail("CLI smoke contract did not parse expected arguments")
    if args.runtime_dir != DEFAULT_RUNTIME_DIR:
        fail("CLI smoke contract defaulted runtime output outside the ignored path")

    runtime_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="fixture-smoke-", dir=runtime_dir) as tmp:
        root = Path(tmp)
        write_valid_fixture(root)
        if (
            run(
                Namespace(root=root, smoke=True, runtime_dir=runtime_dir),
                include_cli_smoke=False,
                emit=False,
            )
            != 0
        ):
            fail("CLI smoke contract rejected a valid fixture")

        missing_root = root / "missing"
        if (
            run(
                Namespace(root=missing_root, smoke=True, runtime_dir=runtime_dir),
                include_cli_smoke=False,
                emit=False,
            )
            == 0
        ):
            fail("CLI smoke contract accepted missing input")


def parse_args(argv: list[str] | None = None) -> Namespace:
    parser = ArgumentParser(
        description="Validate public profile publication claims and links."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=ROOT,
        help="repository root to validate; defaults to this script's parent repo",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="run only the no-secret CLI smoke contract",
    )
    parser.add_argument(
        "--runtime-dir",
        type=Path,
        default=DEFAULT_RUNTIME_DIR,
        help="local directory for generated self-test fixtures; defaults under .runtime/",
    )
    return parser.parse_args(argv)


def run(
    args: Namespace, *, include_cli_smoke: bool = True, emit: bool = True
) -> int:
    try:
        runtime_dir = args.runtime_dir
        if args.smoke:
            validate_publication(args.root)
        else:
            validate_publication(args.root)
            validate_failure_probe(runtime_dir)
            validate_malformed_claims_probe(runtime_dir)
            if include_cli_smoke:
                validate_cli_smoke_contract(runtime_dir)
    except ValidationError as exc:
        if emit:
            print(f"publication validation failed: {exc}", file=sys.stderr)
        return 1
    if emit:
        print("publication validation passed")
    return 0


def main(argv: list[str] | None = None) -> None:
    raise SystemExit(run(parse_args(argv)))


if __name__ == "__main__":
    main()
