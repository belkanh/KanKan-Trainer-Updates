# KanKan Trainer 1.0.4 — official GitHub keyless-update-capable *candidate*

Exact integrated source commit: dd65cc054b25149c71e21259db8a159bab698f4d
Private canonical source branch: candidate/x104-github-keyless-integration
This new build contains the explicit user-selected 1.x GitHub HTTPS updater and requires NO independent RSA manifest public key for this version. The feed is fixed to the official repository main URL. Automatic startup Apply remains disabled.

Exact SHA-bound Windows Quality Gate, release builder and isolated test-identity Velopack smoke all PASSED for this source. This is a distinct build from the older, feed-unconfigured candidate/1.0.4 directory and must never be silently interchanged with those binary hashes.

NOT a live alpha promotion or accepted installed-user update. The currently installed 1.0.3 client still requires its signed RSA manifest and cannot be converted retroactively by changing GitHub indexes. An owner-operated manual transition is required for the new 1.x update mode. Real installed failed post-handoff rollback remains NOT_RUN. Do not overwrite the existing live alpha root index, feed signature or packages.
