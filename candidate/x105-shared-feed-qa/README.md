# QA only: signed legacy 1.0.3 and keyless 1.0.5 shared alpha index

NOT LIVE / NOT CONSUMER READY. This branch is a review snapshot of the two-version alpha feed; no user-installed update was performed. The public main signed 1.0.3 root must stay unchanged.

## Authentic packages

- Existing 1.0.3 signed envelope and original 1.0.3 Full NUPKG are unchanged, SHA-256 8F453FD64FD4B2364C961F33A45587FEDAF50A0D81A4A502856902346A5B1A03.
- 1.0.5 Full NUPKG SHA-256 6C2D0AEFDB937846E64B840E4496C14B3F697A8804EA103B0799AD344856B976, exact canonical source af521d8db69273624a4e7598285626ccf5932af8, Zülal Windows Quality Gate PASS.
- QA branch root alpha Setup is replaced with 1.0.5 Setup SHA-256 4CF0398846CC81680E448264DFCD283060F23CFE1E0C67F221E25AC9B50912DF.
- Root releases.alpha.json, RELEASES-alpha, assets.alpha.json now enumerate both 1.0.3 and 1.0.5 Full releases. 1x-feed-build.json remains consumerReleaseReady false, publication NOT_PERFORMED, auto-start Apply OFF.

## Evidence and limits

On the designated Zülal Windows PC, official public scripts/one_x_feed.py verified the exact two real package files plus indexes, legacy signed-envelope package reference, newest 1.0.5 source receipt and installer presence: mode legacy-signed+1x-keyless-staged PASS. The Python script does NOT cryptographically authenticate the legacy RSA signature; old installed client must still perform pinned signature verification. Earlier installed 1.0.4 single-release-only parser cannot be retroactively fixed; owner forbids 1.0.4 retests. The 1.0.5 shared-index parser was source-bound Windows-QA verified, but real installed upgrade, post-handoff partial-install rollback and operator acceptance remain NOT_RUN. X1-04 and PR #357 remain DRAFT / NOT_DONE. No native ONI Apply, game/save or user-installed app modifications were performed.

This candidate branch must never be merged to public main without separately authorized release promotion and required real installed rollback acceptance.