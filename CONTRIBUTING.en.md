# Maintaining the project

[Русский](CONTRIBUTING.md) | **English**

## One experiment — one clear result

Use the [template](experiments/TEMPLATE.en.md). Record the configuration actually booted, the change, expected sign, observation and conclusion.

- Built — the files have been created.
- Statically checked — the validator/dependency check passed.
- Boot tested — there is a result from a specific run on this laptop.
- Stable — confirmed through repeated runs and load, rather than one successful start.

Do not mark a checkbox complete simply because a file was created or a patch applied. If an experiment was not run, write “not run”.

## Working with Codex

Read the current status and local change log first. Do not roll back newer local results to match older documentation.

The agent prepares a separate build, pins dependencies and proposes one next test. The laptop owner performs the physical boot and observes it. The agent must not invent results.

After a confirmed result, update [status](docs/STATUS.en.md) and the [roadmap](ROADMAP.en.md); add a devlog entry for a substantial milestone.

## Documentation languages

Russian is the primary language: README.md and files without a language suffix are the source versions. English translations use .en.md. README.ru.md preserves the old link and points to the main Russian README.

Keep observations, status, checkboxes, versions, hashes and links consistent in both languages. When changing a document or adding a devlog entry, update its translation and both navigation pages in the same change. Clearly label a translation that has not yet been updated.

Keep Russian issue templates first and identify each language in the template picker. Translate prompts and privacy instructions; keep technical identifiers unchanged.

## Pre-publication checks

```sh
git diff --cached
python3 scripts/check_publication.py
python3 -m unittest discover -s tests -v
```

Enable the local check:

```sh
git config core.hooksPath .githooks
```

The GitHub web editor and API changes bypass the local hook. Review their contents separately. Do not attach original EFI folders/dumps to issues: use sanitized minimal excerpts.

For third-party patches, include the source, commit and license.
