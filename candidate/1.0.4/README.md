# KanKan Trainer 1.0.4 — isolated public staging (NOT live alpha)

This folder contains a newly rebuilt Windows x64 1.0.4 full package and Setup from the exact previously QA-tested source commit dcfc4a0dc179c6ca582fbf0cc37a5037e4eb71de. The rebuilt artifact bytes are new, so prior package hashes and runtime/rollback test PASS must not be recycled as acceptance for these exact bytes.

The 1.x metadata comes from Velopack 1.2.0 and the accompanying 1x-feed-build.json. This directory is a distribution *candidate*, not the live alpha feed or an authorized installed update. The app embedded in this old source was built with an UNCONFIGURED update feed and no RSA manifest key. It is NOT the newer 1.x keyless updater build; using it as an upgrade bridge would require additional acceptance.

Do not relabel this as consumerReady or update root releases.alpha.json / RELEASES-alpha / assets.alpha.json until the legacy 1.0.3 signed-manifest compatibility and genuine post-handoff installed rollback gates have been resolved.

No installed KanKan, game, save or owner workspace was modified by the staging operation.