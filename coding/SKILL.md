# Coding

Rules for working on code projects.

## Principles

1. **Always branch first.** Create changes in a separate branch — never commit directly to `main`/`master`. Open a PR unless explicitly told otherwise.

2. **Big changes → Research, Plan, Implement loop.**
   - **Research:** Understand the codebase, read relevant files, check existing patterns.
   - **Plan:** Outline the approach, break it into steps, confirm with the user if needed.
   - **Implement:** Execute the plan incrementally, testing as you go.
   - Loop back if assumptions break.

3. **Use Claude Code** for running prompts, executing commands, and driving implementation. Prefer it over manual shell work when possible.

4. **Conventional Commits.** Always use the [Conventional Commits](https://www.conventionalcommits.org/) standard (`feat:`, `fix:`, `chore:`, `docs:`, etc.).

5. **Co-author commits.** Every commit should include:
   ```
   Co-authored-by: Claude Opus 4 <noreply@anthropic.com>
   ```

6. **Repos live in `~/Code`.** Always create and work on repositories in `/Users/junaidrahim/Code/`.

## Workflow

```
1. cd ~/Code/<project>
2. git checkout -b <descriptive-branch-name>
3. Make changes (research → plan → implement for big ones)
4. Commit with conventional commit messages + co-author trailer
5. Push and open a PR
6. Share the PR link
```

## Notes

- Keep PRs focused — one concern per PR when possible.
- Commit messages: `type(scope): description` — explain *why*, not just *what*.
- If unsure about scope or approach, ask before going deep.
