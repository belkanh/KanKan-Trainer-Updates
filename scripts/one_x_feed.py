#!/usr/bin/env python3
"""Validate the live alpha feed, or prepare an isolated 1.x full-release feed.

No private keys and no implicit publication. The currently installed signed
client's manifest is preserved: staging never edits the public feed.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import shutil
from pathlib import Path

PACKAGE_ID = "KanKan.Trainer"
CHANNEL = "alpha"
VERSION_RE = re.compile(r"1\.\d+\.\d+\Z")
SHA1_RE = re.compile(r"[0-9a-fA-F]{40}\Z")
SHA256_RE = re.compile(r"[0-9a-fA-F]{64}\Z")
COMMIT_RE = re.compile(r"[0-9a-fA-F]{40}\Z")


class FeedError(ValueError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise FeedError(message)


def digests(path: Path) -> tuple[int, str, str]:
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    size = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            size += len(chunk)
            sha1.update(chunk)
            sha256.update(chunk)
    return size, sha1.hexdigest().upper(), sha256.hexdigest().upper()


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise FeedError(f"Cannot read valid JSON: {path.name}") from exc


def verify(root: Path) -> dict:
    """Hash every Full package and validate the legacy/new 1.x shared index.

    Signed 1.0.3 clients must keep a matching legacy-signed entry while new
    1.x clients can select the newest release. Signature authenticity is NOT
    verified here: the installed client's pinned RSA verifier still owns that.
    """
    root = root.resolve()
    index = read_json(root / "releases.alpha.json")
    require(isinstance(index, dict) and isinstance(index.get("Assets"), list)
            and 1 <= len(index["Assets"]) <= 32,
            "Feed must contain between 1 and 32 Full releases")
    releases = index["Assets"]
    versions: set[str] = set()
    checked: list[tuple[dict, str, str, int]] = []
    for asset in releases:
        require(isinstance(asset, dict), "Malformed release entry")
        version = asset.get("Version")
        require(isinstance(version, str) and VERSION_RE.fullmatch(version) is not None,
                "Only numeric 1.x versions are supported")
        require(version not in versions, "Duplicate release version is not allowed")
        versions.add(version)
        filename = f"{PACKAGE_ID}-{version}-{CHANNEL}-full.nupkg"
        require(asset.get("PackageId") == PACKAGE_ID
                and asset.get("Type") == "Full"
                and asset.get("FileName") == filename, "Wrong package ID/type/filename")
        require(type(asset.get("Size")) is int and asset["Size"] > 0,
                "Invalid package size")
        require(isinstance(asset.get("SHA1"), str)
                and SHA1_RE.fullmatch(asset["SHA1"]) is not None
                and isinstance(asset.get("SHA256"), str)
                and SHA256_RE.fullmatch(asset["SHA256"]) is not None,
                "Both package digests are required")
        package_path = root / filename
        require(package_path.is_file() and not package_path.is_symlink(),
                "Full package is absent or is a symlink")
        size, sha1, sha256 = digests(package_path)
        require(size == asset["Size"]
                and sha1 == asset["SHA1"].upper()
                and sha256 == asset["SHA256"].upper(),
                "Full package bytes do not match index size/SHA1/SHA256")
        checked.append((asset, sha1, sha256, size))

    try:
        release_text = (root / "RELEASES-alpha").read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        raise FeedError("Missing or unreadable RELEASES-alpha") from exc
    expected_lines = [f"{sha1} {asset['FileName']} {size}"
                      for asset, sha1, _, size in checked]
    require(release_text.strip() == "\n".join(expected_lines),
            "Velopack legacy RELEASES-alpha differs from the indexed packages")

    files = read_json(root / "assets.alpha.json")
    expected_files = [{"RelativeFileName": f"{PACKAGE_ID}-alpha-Setup.exe",
                       "Type": "Installer"}] + [
        {"RelativeFileName": asset["FileName"], "Type": "Full"}
        for asset, _, _, _ in checked
    ]
    require(files == expected_files,
            "assets.alpha.json must list installer and every exact Full package")
    installer = root / f"{PACKAGE_ID}-alpha-Setup.exe"
    require(installer.is_file() and not installer.is_symlink()
            and installer.stat().st_size > 0, "Matching installer is absent")
    installer_size, _, installer_sha256 = digests(installer)
    require(installer_size > 0, "Empty installer")

    newest = max(checked, key=lambda x: tuple(map(int, x[0]["Version"].split("."))))
    latest_asset, _, latest_sha256, latest_size = newest
    latest_version = latest_asset["Version"]
    signed = root / "kankan-update-manifest.json"
    mode = "legacy-signed" if signed.exists() else "1x-keyless-staged"
    signed_version = None
    if signed.exists():
        env = read_json(signed)
        require(isinstance(env, dict)
                and isinstance(env.get("payloadBase64"), str)
                and isinstance(env.get("signatureBase64"), str),
                "Malformed signed envelope")
        try:
            payload = json.loads(base64.b64decode(
                env["payloadBase64"], validate=True).decode("utf-8"))
            signature = base64.b64decode(env["signatureBase64"], validate=True)
        except (ValueError, UnicodeError, json.JSONDecodeError) as exc:
            raise FeedError("Malformed signed manifest encoding") from exc
        require(len(signature) >= 256 and isinstance(payload, dict),
                "Missing signed manifest signature or payload")
        legacy_entries = [row for row in checked
                          if row[0]["Version"] == payload.get("version")]
        require(len(legacy_entries) == 1,
                "Legacy signed manifest version is absent from the shared feed")
        legacy, _, legacy_sha256, legacy_size = legacy_entries[0]
        require(payload.get("packageId") == PACKAGE_ID
                and payload.get("channel") == CHANNEL
                and payload.get("packageFileName") == legacy["FileName"]
                and payload.get("packageSize") == legacy_size
                and str(payload.get("packageSha256", "")).upper() == legacy_sha256,
                "Legacy signed manifest contradicts active feed")
        signed_version = legacy["Version"]

    # A mixed shared feed needs BOTH the unmodified legacy signed entry and
    # a separately source-bound record for its newest no-RSA 1.x package.
    if not signed.exists() or latest_version != signed_version:
        receipt = read_json(root / "1x-feed-build.json")
        require(isinstance(receipt, dict)
                and receipt.get("version") == latest_version
                and receipt.get("channel") == CHANNEL
                and isinstance(receipt.get("packageSha256"), str)
                and receipt["packageSha256"].upper() == latest_sha256
                and isinstance(receipt.get("setupSha256"), str)
                and SHA256_RE.fullmatch(receipt["setupSha256"]) is not None
                and receipt["setupSha256"].upper() == installer_sha256
                and isinstance(receipt.get("sourceCommit"), str)
                and COMMIT_RE.fullmatch(receipt["sourceCommit"]) is not None
                and receipt.get("consumerReleaseReady") is not True,
                "Keyless staging receipt is absent, malformed or inconsistent")
        if signed.exists():
            mode = "legacy-signed+1x-keyless-staged"

    return {"version": latest_version, "mode": mode,
            "bytes": latest_size, "sha256": latest_sha256}



def stage(package: Path, installer: Path, source_commit: str, dest: Path) -> dict:
    """Generate an exact 1.x candidate in an EMPTY directory; never promote it."""
    require(COMMIT_RE.fullmatch(source_commit) is not None,
            "Exact 40-hex source commit required")
    match = re.fullmatch(
        r"KanKan\.Trainer-(1\.\d+\.\d+)-alpha-full\.nupkg", package.name)
    require(match is not None and VERSION_RE.fullmatch(match[1]) is not None,
            "Only 1.x alpha full packages may be staged")
    require(installer.name == f"{PACKAGE_ID}-alpha-Setup.exe",
            "Expected matching alpha Setup.exe name")
    require(package.is_file() and not package.is_symlink()
            and installer.is_file() and not installer.is_symlink(),
            "Input package and installer must both exist as ordinary files")
    require(not dest.exists() or (dest.is_dir() and not any(dest.iterdir())),
            "Destination must be empty; existing feeds cannot be overwritten")
    require(package.resolve().parent != dest.resolve()
            and installer.resolve().parent != dest.resolve(),
            "Use a separate staging directory")
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(package, dest / package.name)
    shutil.copyfile(installer, dest / installer.name)
    size, sha1, sha256 = digests(dest / package.name)
    require(size > 0, "Empty update package")
    _, _, setup_sha256 = digests(dest / installer.name)
    entry = {"PackageId": PACKAGE_ID, "Version": match[1], "Type": "Full",
             "FileName": package.name, "SHA1": sha1, "SHA256": sha256,
             "Size": size}
    (dest / "releases.alpha.json").write_text(
        json.dumps({"Assets": [entry]}, separators=(",", ":")),
        encoding="utf-8")
    (dest / "RELEASES-alpha").write_text(
        f"\ufeff{sha1} {package.name} {size}\n", encoding="utf-8")
    (dest / "assets.alpha.json").write_text(
        json.dumps([
            {"RelativeFileName": installer.name, "Type": "Installer"},
            {"RelativeFileName": package.name, "Type": "Full"},
        ], separators=(",", ":")), encoding="utf-8")
    (dest / "1x-feed-build.json").write_text(
        json.dumps({"schemaVersion": 1, "channel": CHANNEL,
                    "version": match[1], "sourceCommit": source_commit.lower(),
                    "packageSha256": sha256, "setupSha256": setup_sha256,
                    "publication": "NOT_PERFORMED"},
                   indent=2) + "\n", encoding="utf-8")
    return verify(dest)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    check = commands.add_parser("verify", help="Verify ALL active package bytes/metadata")
    check.add_argument("root", type=Path)
    prepare = commands.add_parser("stage", help="Prepare a 1.x feed without publishing")
    prepare.add_argument("--package", required=True, type=Path)
    prepare.add_argument("--installer", required=True, type=Path)
    prepare.add_argument("--source-commit", required=True)
    prepare.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    try:
        result = (verify(args.root) if args.command == "verify"
                  else stage(args.package, args.installer,
                             args.source_commit, args.out))
    except (FeedError, OSError) as exc:
        parser.exit(1, f"FAIL: {exc}\n")
    print("PASS: " + json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
