# KanKan Trainer — official 1.x update feed (1.0.6 release candidate)

This tree is the proposed official GitHub HTTPS alpha channel, prepared
from the existing clean no-RSA 1.0.5 candidate. A Git branch alone does
not deliver updates: installed clients read only KanKan-Trainer-Updates/main.

## Source-bound 1.0.6 files

- Full: KanKan.Trainer-1.0.6-alpha-full.nupkg — 96,541,506 bytes
- Full SHA-256: 4B178495B2C9F08C409DFD622831DAEB6D9A5BC4C1CE72E497FA509702F6E941
- Installer: KanKan.Trainer-alpha-Setup.exe — 101,003,074 bytes
- Installer SHA-256: 037BF89F02749664858500DCFFB2EF69811D88760F245A379A2EC0414616D471
- Product source: belkanh/KanKan-Trainer@96d36ebc2793177410ca7459f11526a30e3b5de7
- Existing exact-source Windows Quality Gate / release builder: PASS
- Official feed files: releases.alpha.json, RELEASES-alpha, assets.alpha.json
- 1.x trust: official HTTPS GitHub origin and exact package SHA-256.
  An independent RSA signature is deferred to 2.0.

## Legacy and acceptance

The historical 1.0.3 signed channel is retained in branch
archive/legacy-signed-root-before-1x-cleanup-20261020. The previous
clean 1.0.5 candidate and its original source manifest remain in
candidate/clean-1x-keyless-feed-20261020 at commit
24269530d9ae73868029f8528e43b963abac490c.

Publication and installed acceptance are separate. This candidate has
not by itself proven a 1.0.5-to-1.0.6 in-app installed update, real
post-handoff automatic rollback, or owner acceptance. Automatic startup
Apply remains OFF. ONI KKA1 production Apply stays STOP/fail-closed.