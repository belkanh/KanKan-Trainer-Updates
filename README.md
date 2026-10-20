# KanKan Trainer — Clean Keyless 1.x Feed (Non-live candidate)

**Status: NON-LIVE TEST CANDIDATE, NOT CONSUMER RELEASE APPROVAL.**

This isolated branch is a cleanup/release-feed rehearsal for KanKan Trainer 1.x. It uses **no RSA manifest or legacy 1.0.2/1.0.3 packages**. Its live parent branch `main` is deliberately unchanged until release gates are met. The exact pre-cleanup tree is recoverable at [archive/legacy-signed-root-before-1x-cleanup-20261020](https://github.com/belkanh/KanKan-Trainer-Updates/tree/archive/legacy-signed-root-before-1x-cleanup-20261020).

## Exact clean 1.0.5 base

- Package: `KanKan.Trainer-1.0.5-alpha-full.nupkg`; **96,538,194 bytes**; SHA-256 `6C2D0AEFDB937846E64B840E4496C14B3F697A8804EA103B0799AD344856B976`.
- Installer: `KanKan.Trainer-alpha-Setup.exe`; **100,999,762 bytes**; SHA-256 `4CF0398846CC81680E448264DFCD283060F23CFE1E0C67F221E25AC9B50912DF`.
- Exact compiled source: private `belkanh/KanKan-Trainer@af521d8db69273624a4e7598285626ccf5932af8`; Windows Quality Gate, source-bound packaging, and disposable Velopack synthetic smoke **PASS**.
- Source-bound original `1x-feed-build.json` and `release-manifest.json` stay intact as historical QA receipts; fields describing publication/legacy preservation refer to the original QA build, not release acceptance of this branch.
- Required Velopack feed files at the root: `releases.alpha.json`, `RELEASES-alpha`, `assets.alpha.json`, plus exact Full and Setup package bytes. This root has **one** 1.x Full package and no independent RSA sidecar.
- Official production feed URL embedded in that 1.0.5 binary is **hard-coded to `https://raw.githubusercontent.com/belkanh/KanKan-Trainer-Updates/main/`**. This candidate branch cannot be selected as an override by the installed app and **does not itself deliver updates**.

## Owner's migration preference and future 1.0.6

On 2026-10-20 the owner reported **1.0.5 installed on both Belkan and Zülal PCs** and explicitly requested retirement of old RSA assets from the future feed. This is user-reported installation, **not a verified installed 1.0.5→1.0.6 update or post-handoff rollback**. No PC, game, save, or installed program was changed during this GitHub-only preparation.

For a later true 1.0.6 release: build a **real** exact-source 1.0.6 Setup and Full, verify bytes and SHA-256, prepare coherent Velopack metadata, run negative/fail-closed and user-operating tests, and meet the X1-04 real post-handoff recovery and operator-acceptance requirements. Only then approve a controlled root promotion on `main`. Never rename 1.0.5 as 1.0.6, turn on automatic startup Apply, or mark X1-04 DONE solely for this feed cleanup.

The new 1.x client verifies GitHub HTTPS origin plus SHA-256 before manual Apply. This **does not provide independent publisher cryptographic signing** and does not override native/game/save STOP rules. 2.0/Store/publisher-signing remains deferred.

## Integrity validation

Run `python -m unittest discover -s scripts -p 'test_*.py' -v` and `python scripts/one_x_feed.py verify .`. This branch also includes a scoped GitHub Actions feed validator. Full runtime upgrade and recovery acceptance are not performed by these tests.
