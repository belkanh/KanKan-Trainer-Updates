# KanKan Trainer — Public Update Feed

This repository serves the public update metadata and package files required by KanKan Trainer's free 1.x HTTPS update channel.

- Feed format: Velopack `alpha` channel.
- Existing live 1.0.3 manifest: `kankan-update-manifest.json` (RSA-PSS/SHA-256, legacy signed clients). Future 1.x staging does not require a new RSA manifest.
- Release index: `releases.alpha.json`.
- Packages: exact full `.nupkg` files referenced by the index and signed manifest.

## 1.x update policy for the next 1.0.6 release (2026-10-20 owner clarification)

The owner reports manually installing the exact 1.0.5 QA Setup on the designated Zülal test PC. This is **USER-REPORTED / installed-update and recovery acceptance UNVERIFIED**, not approval to publish or overwrite the live feed.

- **New 1.x clients (starting with exact-source 1.0.5 `af521d8db69273624a4e7598285626ccf5932af8`) do not need RSA update-manifest signatures.** They consult only the official `https://raw.githubusercontent.com/belkanh/KanKan-Trainer-Updates/main/` feed, select the highest strictly valid 1.x Full release, and enforce package SHA-256 before safe user-initiated Apply. GitHub/TLS + SHA-256 are **not independent publisher signing**.
- The historical `kankan-update-manifest.json`, signed 1.0.3 package and associated root metadata are **legacy compatibility assets, not a dependency for 1.0.5→1.0.6**. Their mere presence does not make the new client use RSA. Do not bulk-delete or silently replace them while old installations may still rely on them (including the separately protected owner PC). Retire only after explicit compatibility/distribution decision and applicable checks.
- For **1.0.6**, first produce an exact-source Windows Quality Gate PASS and source/SHA-bound Full/Setup candidate; independently validate package bytes and complete `releases.alpha.json`, `RELEASES-alpha`, `assets.alpha.json` against the candidate. For a mixed live channel retain signed legacy identity plus the new Full entry. No fake version bump, reused old binary renamed 1.0.6, mismatched metadata or unsigned arbitrary-host feed.
- **LIVE publication is a separate gate.** The real installed 1.0.5→new-version Check/Download/Stop/Save/Apply/restart and controlled post-handoff last-good recovery, safe test identity, operator acceptance and canonical X1-04 decision remain outstanding. Until authorized and accepted, public `main` root stays at signed 1.0.3, and automatic startup Apply stays OFF. **No work on Belkan PC, no 1.0.4 retest.**

---

## Latest 1.0.5 candidate from corrected shared-index updater (2026-10-20)

**Stable public-main QA archive (NOT LIVE):** [`main/candidate/1.0.5-af521d8`](https://github.com/belkanh/KanKan-Trainer-Updates/tree/main/candidate/1.0.5-af521d8), binary-upload commit [`ca664017`](https://github.com/belkanh/KanKan-Trainer-Updates/commit/ca664017d753aa6f49e64ec944ef7d588570fae9) with independently verified GitHub tree blobs and byte sizes. The QA receipt JSON was corrected at [`e01cbe3d`](https://github.com/belkanh/KanKan-Trainer-Updates/commit/e01cbe3d6e3b4240b408dac6855403ca34a46edc), then parsed successfully from GitHub. This is a separate non-live candidate directory, not the root feed.

**Newest exact-source binary candidate (NOT LIVE):** [`candidate/x105-af521d8-20261020/candidate/1.0.5-keyless-af521d8`](https://github.com/belkanh/KanKan-Trainer-Updates/tree/candidate/x105-af521d8-20261020/candidate/1.0.5-keyless-af521d8), exact uploaded Git commit [`c29b25ecc85400d80498b3cb529adb3cccc7c2d6`](https://github.com/belkanh/KanKan-Trainer-Updates/commit/c29b25ecc85400d80498b3cb529adb3cccc7c2d6). These **newer** 1.0.5 files were compiled on the authorized Zülal Windows test machine from the private canonical source [`af521d8db69273624a4e7598285626ccf5932af8`](https://github.com/belkanh/KanKan-Trainer/commit/af521d8db69273624a4e7598285626ccf5932af8), which includes the bounded newest-Full shared-feed selector preserving the independently signed old 1.0.3 client.

- Full `KanKan.Trainer-1.0.5-alpha-full.nupkg`: **96,538,194 bytes**, SHA-256 `6C2D0AEFDB937846E64B840E4496C14B3F697A8804EA103B0799AD344856B976`; Git blob `b0f004c6d3e28ab086e5b45cd685d1923ecebce4`.
- Setup `KanKan.Trainer-alpha-Setup.exe`: **100,999,762 bytes**, SHA-256 `4CF0398846CC81680E448264DFCD283060F23CFE1E0C67F221E25AC9B50912DF`; Git blob `7be42b97b8b46a5b3d302f3b68e803ec780ed2cd`.
- Exact `af521d8` Windows Quality Gate and SHA-bound release builder **PASS**; isolated disposable Velopack install/valid update/corrupt-update preservation/uninstall smoke **PASS**. Local and GitHub binary blob IDs, byte counts, index SHA1/SHA256, and source-bound receipts **match**.
- **NotSigned; `consumerReleaseReady=false`; automatic startup Apply OFF.** No real installed-user 1.0.4→1.0.5 acceptance or real post-handoff partial-install last-good rollback was run. Owner prohibited further 1.0.4 retesting. No installed Trainer/game/save interaction or paid release infrastructure.

Both locations are **QA candidate archives only**, not live releases. Main root `releases.alpha.json` and its legacy signed `kankan-update-manifest.json` still serve **1.0.3** unchanged. The earlier `fbf4a6d` 1.0.5 package archived on `main/candidate/1.0.5-keyless` below is **superseded for new QA by this `af521d8` candidate**, but retained for independent historical provenance.

---

## Earlier: exact-source 1.0.5 keyless update candidate (2026-10-20)

**Real 1.0.5 Windows binaries and complete Velopack indexes are now retained in public [`main/candidate/1.0.5-keyless`](https://github.com/belkanh/KanKan-Trainer-Updates/tree/main/candidate/1.0.5-keyless)**, main commit [`07faa9ce9409bdc7131a6e10691e326d6f1c340c`](https://github.com/belkanh/KanKan-Trainer-Updates/commit/07faa9ce9409bdc7131a6e10691e326d6f1c340c). This is a **non-live, non-consumer-ready QA candidate folder**, not the signed root alpha feed. All eight files are identical Git blobs to the original [candidate branch commit `1f9edde`](https://github.com/belkanh/KanKan-Trainer-Updates/commit/1f9edde3a4053ba0be22b271459a328d2ad3bd27) and were copied server-side without rebuilding, retesting 1.0.4 or paying for a service. Source: private canonical [`fbf4a6df4446252fe5d29ad365c68f2d8107be82`](https://github.com/belkanh/KanKan-Trainer/commit/fbf4a6df4446252fe5d29ad365c68f2d8107be82), based on the already-tested 1.0.5 source and the active X1-04 official GitHub 1.x **no RSA manifest-key** implementation, with a hard-locked HTTPS feed and SHA-256 package checks.

- Full `.nupkg`: **96,541,440 bytes**, SHA-256 `AF804A6DF557C9D102BAB7E6E6419A57795FFFB6E9566F18AAD4B7CD827AF349`
- Setup: **101,003,008 bytes**, SHA-256 `67C37CD981AD69F7133CF603C775B73EB064D3DC4298D19FE9C894F2C031442A`
- Exact source Windows Quality Gate **PASS**; source-bound release builder **PASS**; isolated Velopack install, update, corrupt-package preservation and uninstall smoke **PASS**. GitHub byte sizes and Git blob IDs matched local staging, and metadata/receipt were re-read.
- `consumerReleaseReady=false`, `NotSigned`, automatic startup Apply OFF. **No actual installed-user 1.0.4 → 1.0.5 upgrade or genuine post-handoff partial-failure rollback was run**; owner requested no additional 1.0.4 tests.

**The live root on `main` still serves signed 1.0.3**, because installed 1.0.3 expects the old pinned RSA envelope. This candidate upload is **not live-feed promotion**, and publishing its unsigned 1.0.5 index alone would not provide a compatible legacy upgrade. Neither a paid GitHub service nor new GitHub Actions pipeline was needed to produce or upload these binaries; Git and the Windows toolchain sufficed.

---

## Official GitHub keyless 1.0.4 package staged (2026-10-20)

The **updated 1.0.4 build with an actual embedded official GitHub 1.x update source** is available in the [candidate/1.0.4-keyless directory](https://github.com/belkanh/KanKan-Trainer-Updates/tree/candidate/x104-manual-package-20261020/candidate/1.0.4-keyless) at public candidate commit [`fc37b75b26294c25478e8225d680f0a1d3a844e2`](https://github.com/belkanh/KanKan-Trainer-Updates/commit/fc37b75b26294c25478e8225d680f0a1d3a844e2). Exact **private canonical source** [`dd65cc054b25149c71e21259db8a159bab698f4d`](https://github.com/belkanh/KanKan-Trainer/commit/dd65cc054b25149c71e21259db8a159bab698f4d) integrates the 1.0.4 baseline with the X1-04 owner's no-RSA 1.x update-source changes and keeps an explicit manual Check/Download/Apply path. It embeds `https://raw.githubusercontent.com/belkanh/KanKan-Trainer-Updates/main` and **no 1.x RSA manifest key**. Windows source-bound Quality Gate **PASS**, release candidate builder **PASS**, isolated Velopack install/update/failure-preservation/uninstall smoke **PASS**. `Authenticode=NotSigned`; package's `consumerReleaseReady=false`.

- Full `.nupkg`: **96,541,265 bytes**, SHA-256 `AC679CB0A1B38EDC4527DC8D7A5A1AF723BCD6D0AD036743DF089B3BC4860872`
- Alpha Setup: **101,002,833 bytes**, SHA-256 `5F33692C62A486663D2D836304DF57DFFB1CCAEAD6207A8C8090D1795D86B438`

Local Git blobs and GitHub's public Git tree blob SHAs and byte counts match for both binaries. This is **a complete public Git QA staging upload**, not promotion of root live `alpha` index. Installed 1.0.3 still expects its pinned RSA manifest, so it cannot automatically transition to this newly built keyless client by rewriting an unsigned index. A separately accepted manual installer transition and real installed post-handoff failed-install recovery remain unverified. **Root live feed is still signed 1.0.3** and automatic startup Apply is OFF. The earlier `candidate/1.0.4` directory contains a different **feed-unconfigured** QA build retained for traceability; prefer the newer `candidate/1.0.4-keyless` only as an isolated release candidate.

---

## Newly uploaded 1.0.4 files — staged, not live alpha (2026-10-20)

The 1.0.4 Windows full package and Setup are **now present in this public repository on the isolated [candidate/x104-manual-package-20261020](https://github.com/belkanh/KanKan-Trainer-Updates/tree/candidate/x104-manual-package-20261020/candidate/1.0.4) branch**, commit [`33186107b74701d8f9cc5840e2095c8bd432b94d`](https://github.com/belkanh/KanKan-Trainer-Updates/commit/33186107b74701d8f9cc5840e2095c8bd432b94d). Source commit: `dcfc4a0dc179c6ca582fbf0cc37a5037e4eb71de`. The binary assets were rebuilt on an isolated Windows workspace, SHA-256-checked, pushed using ordinary free Git, and verified against GitHub's exact Git blob SHA/size. The candidate directory includes complete 1.0.4 Velopack metadata and a non-consumer-ready provenance receipt.

**Do not use these bytes as a live 1.0.3 → 1.0.4 automatic upgrade yet.** The rebuilt 1.0.4 app has no configured update feed, and the installed 1.0.3 client still requires its pinned RSA sidecar. The rebuilt binary's actual installed-runtime/partial-failure rollback acceptance is NOT_RUN. The root of `main` continues serving 1.0.3; no main feed metadata, legacy signature or live package was replaced. This is a completed **public binary staging upload**, not a completed automatic update release.

---

## Published alpha status (2026-10-20 snapshot)

- **Current authenticated public `alpha` feed: `1.0.3`.** The signed `kankan-update-manifest.json`, `releases.alpha.json`, `RELEASES-alpha` and `assets.alpha.json` refer to the existing `KanKan.Trainer-1.0.3-alpha-full.nupkg`. These files remain authoritative for the public feed until a separately authorized, verified promotion.
- **Newer `1.0.4` and `1.0.5` builds are not public feed releases.** A 1.0.4 candidate remains on its original staging branch; the 1.0.5 candidate binaries and source-bound checksums are now publicly archived under `main/candidate/1.0.5-keyless`. They are still controlled QA candidates from the canonical product repository. Source-bound Windows build and isolated Velopack package smoke results do not establish production update readiness.
- **Publication remains blocked:** The owner deferred the separate 1.x RSA manifest requirement to 2.0 and exact-source 1.0.5 builder/isolated smoke passed; however, the installed 1.0.3 client's RSA compatibility, real installed-user transition and genuine interrupted **post-handoff** last-good rollback acceptance remain incomplete. Automatic Apply stays disabled. Do not replace this feed with the private unsigned/unconfigured QA package, reuse an old signature or publish metadata pointing to missing binaries.
- **Scope:** This README status is documentation, not a new update offer, package approval, consumer rollout, or change to any `alpha` feed byte. The canonical source/acceptance records remain in the private Trainer project.


## Legacy 1.0.3 + newer 1.x shared-index validation (2026-10-20)

The `scripts/one_x_feed.py verify` command now checks a bounded shared `releases.alpha.json` containing **multiple** 1.x Full packages. It hashes **every** package, enforces exact `RELEASES-alpha` / `assets.alpha.json` membership, rejects duplicate/invalid versions, and requires the old signed-manifest payload to match **its own 1.0.3 entry** while a separate exact-source 1.x receipt describes the newest release. This structural check **does not authenticate the old RSA signature**; the installed old client continues doing that with its pinned key.

The eleven synthetic/negative regression cases and live 1.0.3 root-byte verification passed on [public Actions run 39433705778](https://github.com/belkanh/KanKan-Trainer-Updates/actions/runs/39433705778) / exact code SHA `469a0681e77f6bd53531f37a1bf7e570babb0f2f`. **No shared live-root index has been published yet.** Existing installed 1.0.4 single-release-only binaries are not retroactively fixed, and the current 1.0.5 candidate must be rebuilt from its newest source before consuming a mixed feed. Nothing here changes the old signed 1.0.3 root index or authorizes unattended Apply.

---

## 1.x feed development and verification

The repository now contains a real full-package integrity checker and a **staging-only** generator for numeric 1.x releases. They use Python 3.12 standard library only. The existing signed 1.0.3 feed stays unchanged while the new 1.x release path is developed.

```bash
# Verify live 1.0.3 feed metadata against actual package bytes:
python scripts/one_x_feed.py verify .

# Generate a future full 1.x candidate in a NEW EMPTY directory,
# using an exact-source release-built nupkg AND matching Setup:
python scripts/one_x_feed.py stage \
  --package /path/to/KanKan.Trainer-1.0.5-alpha-full.nupkg \
  --installer /path/to/KanKan.Trainer-alpha-Setup.exe \
  --source-commit FULL_40_HEX_SOURCE_COMMIT \
  --out /path/to/empty-staging-directory
python scripts/one_x_feed.py verify /path/to/empty-staging-directory
```

Staging writes `releases.alpha.json`, `RELEASES-alpha`, `assets.alpha.json`, copies exact binaries and records `1x-feed-build.json` with `publication=NOT_PERFORMED`. It neither rewrites live metadata nor publishes the staged files. The [Validate 1.x update feed](.github/workflows/validate-1x-feed.yml) GitHub Actions job runs six negative/positive regression checks and independently hashes the live package on every main push/PR.

**Before any 1.x promotion:** the candidate's application build must point to the intended feed, installed versions that require the legacy signed manifest need an explicit compatible transition, and separately authorized real install/failure recovery acceptance must complete. A repository metadata validation PASS is not a consumer release approval.

---
**This repository is intentionally public.** Published files can be downloaded and copied by anyone. The canonical application source repository is separate. No source tree, private signing key, credentials, or local test evidence belongs here.

**Current published 1.0.3:** existing signed-manifest clients use a pinned RSA key and exact package identity/hash. **Future 1.x development:** a GitHub HTTPS + SHA-256 source is under development; GitHub/TLS and a package hash are not independent publisher cryptographic signing. Do not treat a staged 1.x feed as an accepted or working installed update.

Only files generated by the source-bound, passing release pipeline may be added. Do not treat this repository as proof of live-update, rollback, or installed-user acceptance until those tests have independently passed. Automatic update/apply must remain disabled until release gates are satisfied.
