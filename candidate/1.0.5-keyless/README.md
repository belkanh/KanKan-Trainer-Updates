# KanKan Trainer 1.0.5 — source-bound GitHub 1.x keyless update candidate (NOT LIVE)

Source: fbf4a6df4446252fe5d29ad365c68f2d8107be82
Private canonical source branch: candidate/x105-github-keyless-integration
This is the 1.0.5 baseline integrated with the 1.x official GitHub HTTPS/SHA-256 update-source implementation. No separate RSA update manifest public key is required by this version; manual Check/Download/Apply remains user-controlled. The source and package differ from the earlier private 1.0.5 QA draft.

The exact-source Windows Quality Gate and release builder passed. Isolated Velopack test-identity install, corrupt package preservation, valid update and uninstall smoke passed. No live installed/user rollback or real game/save acceptance was run. Artifacts are unsigned Authenticode=NotSigned, consumerReleaseReady=false, automaticStartupApply=OFF.

This directory is a candidate asset archive. Do not overwrite the live main-root 1.0.3 releases/legacy RSA envelope or imply that 1.0.3 has converted to keyless update. Existing users need a separately accepted manual migration path and real post-handoff last-good recovery evidence. This branch also contains the previously staged 1.0.4 candidates for historical comparison; neither was retested.
