   # DeepGuard Backend

   Backend orchestration platform for DeepGuard: API gateway, async job pipeline,
   ensemble engine and job management for multi-modal deepfake detection.

   ## Team workflow
   - `main` is protected. No direct pushes.
   - Branch names: `<type>/<task-id>-<short-name>` (feat, fix, docs, chore, test)
   - Commit messages: `<type>: <what changed>`
   - Every change goes through a Pull Request with 1 approval, merged with Squash.
   - Never commit secrets or `.env` files.