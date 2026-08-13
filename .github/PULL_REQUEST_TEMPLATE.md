## Summary

Briefly describe what this pull request changes and why.

## Related issue

Closes #

## Type of change

- [ ] New skill
- [ ] Change to an existing skill
- [ ] Fix
- [ ] Documentation / repository maintenance

## Trigger phrases

For a new or renamed skill, list the phrasings you expect to invoke it — the `description` has to
cover them or the skill never loads.

## How was this verified?

Which phrasings you actually tried, and the output of `python3 tools/validate_skill.py skills/<skill-name>`
plus any bundled validator you ran (e.g. `python3 scripts/validate_study_set.py study-set.csv`).

## Checklist

- [ ] One skill, or one focused change, per pull request.
- [ ] Frontmatter `name` exactly equals the folder name.
- [ ] Every `./`-relative link resolves and bundled files sit one level deep.
- [ ] `python3 tools/validate_skill.py skills/<skill-name>` passes, and so do the judgment checks in `CONTRIBUTING.md`.
