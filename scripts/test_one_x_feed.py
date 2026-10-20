#!/usr/bin/env python3
"""Regression tests for the public 1.x feed staging and full-byte validator."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from one_x_feed import FeedError, stage, verify  # noqa: E402


class OneXFeedTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="kkt-update-feed-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pkg = self.root / "KanKan.Trainer-1.0.5-alpha-full.nupkg"
        self.setup = self.root / "KanKan.Trainer-alpha-Setup.exe"
        self.out = self.root / "staged"
        self.pkg.write_bytes(b"fake test package, not an installable executable" * 32)
        self.setup.write_bytes(b"fake test installer" * 4)

    def prepare(self):
        return stage(self.pkg, self.setup, "a" * 40, self.out)

    def test_exact_staging_generates_all_three_indexes(self):
        result = self.prepare()
        self.assertEqual("1.0.5", result["version"])
        self.assertEqual("1x-keyless-staged", result["mode"])
        self.assertEqual(result, verify(self.out))
        self.assertTrue((self.out / "releases.alpha.json").is_file())
        self.assertTrue((self.out / "assets.alpha.json").is_file())
        self.assertTrue((self.out / "RELEASES-alpha").is_file())
        self.assertEqual("NOT_PERFORMED",
                         json.loads((self.out / "1x-feed-build.json").read_text())
                         ["publication"])

    def test_tampered_download_is_rejected(self):
        self.prepare()
        with (self.out / self.pkg.name).open("ab") as f:
            f.write(b"tamper")
        with self.assertRaisesRegex(FeedError, "package bytes"):
            verify(self.out)

    def test_wrong_package_version_is_rejected(self):
        self.pkg.rename(self.root / "KanKan.Trainer-2.0.0-alpha-full.nupkg")
        with self.assertRaisesRegex(FeedError, "Only 1.x"):
            stage(self.root / "KanKan.Trainer-2.0.0-alpha-full.nupkg",
                  self.setup, "a" * 40, self.out)

    def test_wrong_index_digest_is_rejected(self):
        self.prepare()
        index_path = self.out / "releases.alpha.json"
        index = json.loads(index_path.read_text())
        index["Assets"][0]["SHA256"] = "0" * 64
        index_path.write_text(json.dumps(index), encoding="utf-8")
        with self.assertRaisesRegex(FeedError, "package bytes"):
            verify(self.out)

    def test_mismatched_legacy_sidecar_rejected(self):
        import base64
        self.prepare()
        receipt = self.out / "1x-feed-build.json"
        receipt.unlink()
        payload = {"packageId": "KanKan.Trainer", "channel": "alpha",
                   "version": "1.0.3", "packageFileName": self.pkg.name,
                   "packageSize": self.pkg.stat().st_size,
                   "packageSha256": "F" * 64}
        sidecar = {"payloadBase64": base64.b64encode(
            json.dumps(payload).encode()).decode(),
                   "signatureBase64": base64.b64encode(bytes(384)).decode()}
        (self.out / "kankan-update-manifest.json").write_text(
            json.dumps(sidecar), encoding="utf-8")
        with self.assertRaisesRegex(FeedError, "contradicts"):
            verify(self.out)

    def test_existing_folder_is_not_overwritten(self):
        self.prepare()
        with self.assertRaisesRegex(FeedError, "must be empty"):
            self.prepare()


if __name__ == "__main__":
    unittest.main()
