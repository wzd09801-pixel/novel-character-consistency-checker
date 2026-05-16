#!/usr/bin/env python3
"""
Validation script for novel-character-consistency-checker skill.
Checks frontmatter, structure, and file integrity.
"""

import os
import re
import json
from pathlib import Path


def validate_frontmatter(skill_md_path: str) -> tuple[bool, list[str]]:
    """Validate SKILL.md frontmatter format."""
    errors = []
    warnings = []

    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if file starts with frontmatter
    if not content.startswith('---'):
        errors.append("SKILL.md must start with YAML frontmatter (---)")
        return False, errors

    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        errors.append("Cannot parse YAML frontmatter")
        return False, errors

    frontmatter_text = frontmatter_match.group(1)

    # Check required fields
    required_fields = ['name', 'description']
    for field in required_fields:
        pattern = rf'^{field}:\s*.+$'
        if not re.search(pattern, frontmatter_text, re.MULTILINE):
            errors.append(f"Missing required frontmatter field: {field}")

    # Validate name format (hyphen-case)
    name_match = re.search(r'^name:\s*(.+)$', frontmatter_text, re.MULTILINE)
    if name_match:
        name_value = name_match.group(1).strip()
        if not re.match(r'^[a-z0-9-]+$', name_value):
            errors.append(f"name must be hyphen-case (lowercase with hyphens): '{name_value}'")
        if len(name_value) > 64:
            errors.append(f"name must be <= 64 characters")

    # Check no markdown title before frontmatter
    lines_before_frontmatter = content.split('---')[0]
    if lines_before_frontmatter.strip():
        errors.append("No content should appear before the frontmatter ---")

    return len(errors) == 0, errors


def validate_meta_json(meta_path: str) -> tuple[bool, list[str]]:
    """Validate _meta.json structure."""
    errors = []

    if not os.path.exists(meta_path):
        errors.append("_meta.json not found")
        return False, errors

    try:
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in _meta.json: {e}")
        return False, errors

    # Check required fields
    required_fields = ['id', 'version']
    for field in required_fields:
        if field not in meta:
            errors.append(f"Missing required field in _meta.json: {field}")

    # Validate version format (semantic versioning)
    if 'version' in meta:
        version = meta['version']
        if not re.match(r'^\d+\.\d+\.\d+$', version):
            errors.append(f"version must be semantic versioning (x.y.z): '{version}'")

    return len(errors) == 0, errors


def validate_structure(skill_dir: str) -> tuple[bool, list[str]]:
    """Validate skill directory structure."""
    errors = []

    required_files = ['SKILL.md', '_meta.json']
    for file in required_files:
        path = os.path.join(skill_dir, file)
        if not os.path.exists(path):
            errors.append(f"Missing required file: {file}")

    # Check optional directories
    optional_dirs = ['scripts', 'references', 'assets']
    for dir_name in optional_dirs:
        path = os.path.join(skill_dir, dir_name)
        if os.path.exists(path) and not os.path.isdir(path):
            errors.append(f"{dir_name} should be a directory")

    return len(errors) == 0, errors


def main():
    """Run all validations."""
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(skill_dir)  # Go up from scripts/

    print("=" * 60)
    print("Novel Character Consistency Checker - Skill Validation")
    print("=" * 60)

    all_passed = True

    # Validate structure
    print("\n[1] Checking directory structure...")
    passed, errors = validate_structure(skill_dir)
    if passed:
        print("    ✓ Directory structure valid")
    else:
        print("    ✗ Directory structure errors:")
        for e in errors:
            print(f"      - {e}")
        all_passed = False

    # Validate frontmatter
    print("\n[2] Checking SKILL.md frontmatter...")
    passed, errors = validate_frontmatter(os.path.join(skill_dir, 'SKILL.md'))
    if passed:
        print("    ✓ Frontmatter valid")
    else:
        print("    ✗ Frontmatter errors:")
        for e in errors:
            print(f"      - {e}")
        all_passed = False

    # Validate meta.json
    print("\n[3] Checking _meta.json...")
    passed, errors = validate_meta_json(os.path.join(skill_dir, '_meta.json'))
    if passed:
        print("    ✓ _meta.json valid")
    else:
        print("    ✗ _meta.json errors:")
        for e in errors:
            print(f"      - {e}")
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All validations passed!")
        return 0
    else:
        print("✗ Validation failed. Please fix the errors above.")
        return 1


if __name__ == '__main__':
    exit(main())
