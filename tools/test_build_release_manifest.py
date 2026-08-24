#!/usr/bin/env python3

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("build_release_manifest.py")
SPEC = importlib.util.spec_from_file_location("build_release_manifest", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class ReleaseManifestTest(unittest.TestCase):
    def test_manifest_is_sorted_and_excludes_its_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "b.txt").write_text("bb")
            (root / "a.txt").write_text("a")
            output = root / "MANIFEST.json"
            output.write_text("old manifest")

            manifest = MODULE.build_manifest(root, output)

            self.assertEqual(manifest["file_count"], 2)
            self.assertEqual(manifest["total_bytes"], 3)
            self.assertEqual([item["path"] for item in manifest["files"]], ["a.txt", "b.txt"])

    def test_verify_manifest_detects_changed_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            data = root / "data.bin"
            output = root / "MANIFEST.json"
            data.write_bytes(b"original")
            manifest = MODULE.build_manifest(root, output)
            output.write_text(json.dumps(manifest))

            self.assertEqual(MODULE.verify_manifest(root, output), [])

            data.write_bytes(b"changed")
            errors = MODULE.verify_manifest(root, output)
            self.assertTrue(any("data.bin bytes" in error for error in errors))
            self.assertTrue(any("data.bin sha256" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
