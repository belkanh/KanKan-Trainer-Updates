#!/usr/bin/env python3
"""Regression tests for the public 1.x feed staging and full-byte validator."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from one_x_feed import FeedError, digests, stage, verify  # noqa: E402


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

    def prepare_legacy_signed_and_keyless(self):
        """Test metadata only, using tiny fake bytes; not an installed app test."""
        import base64
        self.prepare()
        legacy_path = self.out / "KanKan.Trainer-1.0.3-alpha-full.nupkg"
        legacy_path.write_bytes(b"fake historical legacy package" * 16)
        size, sha1, sha256 = digests(legacy_path)
        legacy = {"PackageId": "KanKan.Trainer", "Version": "1.0.3",
                  "Type": "Full", "FileName": legacy_path.name,
                  "SHA1": sha1, "SHA256": sha256, "Size": size}
        index_path = self.out / "releases.alpha.json"
        idx = json.loads(index_path.read_text())
        newer = idx["Assets"][0]
        idx["Assets"] = [legacy, newer]
        index_path.write_text(json.dumps(idx), encoding="utf-8")
        (self.out / "RELEASES-alpha").write_text(
            "\ufeff" + "\n".join(
                f"{entry['SHA1']} {entry['FileName']} {entry['Size']}"
                for entry in idx["Assets"]) + "\n", encoding="utf-8")
        asset_path = self.out / "assets.alpha.json"
        assets = json.loads(asset_path.read_text())
        assets.insert(1, {"RelativeFileName": legacy_path.name,
                          "Type": "Full"})
        asset_path.write_text(json.dumps(assets), encoding="utf-8")
        payload = {"packageId": "KanKan.Trainer", "channel": "alpha",
                   "version": "1.0.3", "packageFileName": legacy_path.name,
                   "packageSize": size, "packageSha256": sha256}
        envelope = {"payloadBase64": base64.b64encode(
            json.dumps(payload).encode()).decode(),
            "signatureBase64": base64.b64encode(bytes(384)).decode()}
        (self.out / "kankan-update-manifest.json").write_text(
            json.dumps(envelope), encoding="utf-8")
        return idx

    def test_shared_feed_keeps_old_signed_and_selects_latest(self):
        self.prepare_legacy_signed_and_keyless()
        result = verify(self.out)
        self.assertEqual("1.0.5", result["version"])
        self.assertEqual("legacy-signed+1x-keyless-staged", result["mode"])

    def test_shared_feed_rejects_tampered_old_package(self):
        self.prepare_legacy_signed_and_keyless()
        with (self.out / "KanKan.Trainer-1.0.3-alpha-full.nupkg").open("ab") as f:
            f.write(b"tamper")
        with self.assertRaisesRegex(FeedError, "package bytes"):
            verify(self.out)

    def test_shared_feed_rejects_duplicate_release(self):
        idx = self.prepare_legacy_signed_and_keyless()
        idx["Assets"].append(idx["Assets"][1])
        (self.out / "releases.alpha.json").write_text(json.dumps(idx))
        with self.assertRaisesRegex(FeedError, "Duplicate release version"):
            verify(self.out)

    def test_shared_feed_requires_newest_source_receipt(self):
        self.prepare_legacy_signed_and_keyless()
        (self.out / "1x-feed-build.json").unlink()
        with self.assertRaisesRegex(FeedError, "Cannot read valid JSON"):
            verify(self.out)

    def test_shared_feed_rejects_old_signed_manifest_mismatch(self):
        import base64
        self.prepare_legacy_signed_and_keyless()
        path = self.out / "kankan-update-manifest.json"
        env = json.loads(path.read_text())
        payload = json.loads(base64.b64decode(env["payloadBase64"]))
        payload["packageSha256"] = "0" * 64
        env["payloadBase64"] = base64.b64encode(json.dumps(payload).encode()).decode()
        path.write_text(json.dumps(env))
        with self.assertRaisesRegex(FeedError, "contradicts"):
            verify(self.out)

    def test_existing_folder_is_not_overwritten(self):
        self.prepare()
        with self.assertRaisesRegex(FeedError, "must be empty"):
            self.prepare()


if __name__ == "__main__":
    unittest.main()
