# KanKan Trainer 1.0.5 — exact af521d8 QA candidate (NOT LIVE)

- Canonical private source: belkanh/KanKan-Trainer, branch candidate/x105-github-keyless-integration, exact SHA af521d8db69273624a4e7598285626ccf5932af8.
- This newly rebuilt version includes the mixed signed-legacy/keyless bounded multi-Full index selection fix; earlier candidate/1.0.5-keyless binaries came from fbf4a6df... and are NOT equivalent.
- Windows exact-source Quality Gate PASS on the designated Zülal device using .NET 10.0.402, PowerShell 7.6.7 and a protected running-application-safe isolated test path. 1,257 static checks; 40 architecture, 9 synthetic pack, 459 Core, 208 presentation, 153 smoke; controlled Windows and native ONI no-clobber fixtures PASS.
- Source-bound release builder BUILD PASS / CONSUMER RELEASE PENDING, including clean tracked-source shadow export, Win-x64 publish, and separate disposable-identity Velopack install, valid update, corrupt-update preservation, uninstall smoke PASS.
- Full: KanKan.Trainer-1.0.5-alpha-full.nupkg, 96,538,194 bytes, SHA-256 6C2D0AEFDB937846E64B840E4496C14B3F697A8804EA103B0799AD344856B976.
- Setup: KanKan.Trainer-alpha-Setup.exe, 100,999,762 bytes, SHA-256 4CF0398846CC81680E448264DFCD283060F23CFE1E0C67F221E25AC9B50912DF.
- Source-bound official feed URL embedded: https://raw.githubusercontent.com/belkanh/KanKan-Trainer-Updates/main ; update trust for 1.x = official GitHub HTTPS plus exact SHA-256, NOT independent publisher RSA authentication. Authenticode=NotSigned.
- This is a public QA candidate archive only. Public root releases.alpha.json and legacy RSA sidecar stay at signed 1.0.3; 1.0.5 is NOT promoted to the live channel. No automatic startup Apply.
- No installed user 1.0.4 -> 1.0.5 transition, real post-handoff partial-install last-good rollback, or real-game/save acceptance has occurred. Do not mark X1-04 DONE or consumerReleaseReady=true. No 1.0.4 retesting.
- Provenance files: release-manifest.json, 1x-feed-build.json, assets.alpha.json, releases.alpha.json, RELEASES-alpha. No secret-bearing source or test logs are included.