# maoorf development workflow

This document describes how maoorf is versioned, branched, released and documented, and how teams can experiment with FAIRifying modules.
See [ROADMAP.md](ROADMAP.md) for the stages referred to below.

## Release lines

- **1.x — OORF 2023 as published.** Stage 1 (faithful JSON copy of the OECD OORF 2023 Excel template), plus the non-breaking parts of Stage 2. This is the stable basis for users who want compatibility with the published OORF.
- **2.x — formalised OORF.** Stage 3 onward, where the data format is allowed to change.

The compatible line is tied to the OORF edition (the `oecd_oorf_2023` prefix already encodes it). If the OECD publishes a revised OORF, the compatible line gets a new major version. Modules that are not part of the 2023 release (such as EBP) are not shipped unmarked in 1.x: before 1.0.0 they are moved out or clearly labelled as extensions.

## Version numbers

Versions follow semantic versioning, applied to the **JSON data**:

| Bump | When | Examples |
|---|---|---|
| **Major** | An existing valid JSON file stops validating, or a field changes meaning | Renaming keys, string → typed values, missing-value enums, file references |
| **Minor** | Additions only; old files stay valid | New optional fields, new modules, multiple runs per module, converter features |
| **Patch** | No effect on the data format | Fixes to descriptions, guidance text, mappings or template errata; converter bug fixes |

Most of Stage 2 (per-attribute `slot_uri`, collapsing shared slots such as `software`) does not change JSON keys, so it is released as 1.x minor versions.
The four renames needed to fix OWL punning (`contrasts`, `overall_description_and_rationale`, `model_selection`, `commercial_source`) are made **before 1.0.0**, so 1.x never needs a breaking change.

### Version sources

- **Package**: the version is derived from git tags (`uv-dynamic-versioning`). On the `1.x` branch it resolves from the `v1.*` tags.
- **Schema**: `maoorf.yaml` carries a `version:` field. CI fails if the release tag and the schema version differ (or CI sets the field from the tag at release time).
- **Instances**: each JSON instance records the schema version it follows in a `schema_version` slot on `OORF`. A slot is used rather than `$schema`, because the schema rejects unknown keys. The v1 → v2 migration script reads this field.

## Branches

```
main ──●──●──v1.0.0──●──●──v1.1.0──●──[Stage 3 starts]──●──v2.0.0a1──●──v2.0.0
                                    \
                              1.x    ●──v1.1.1──●──v1.2.0──●──v1.2.1
```

- Until the first breaking change, there is a single `main`. Releases `v1.0.0`, `v1.1.0`, … are tagged there.
- When the first Stage 3 change is about to merge, the `1.x` branch is created from the last 1.x tag. After that:
  - `main` holds 2.0 development, released as pre-releases (`v2.0.0a1`, …) until it settles.
  - `1.x` only takes fixes and additive changes. It is protected and requires pull requests.
- **Backports**: fixes land on `1.x` first and are then brought to `main`. Because `main` diverges structurally, cherry-picks often won't apply cleanly; expect to redo some fixes by hand. Pull requests that need a backport get the `backport-1.x` label.

### Support policy

1.x receives fixes until 12 months after the 2.0.0 release (adjust as agreed).
What qualifies for 1.x: template errata, guidance and mapping fixes, converter fixes, and additive fields. Data-format changes do not.

## URIs

- **Schema URIs are versioned.** Each release is published at `https://w3id.org/eu-parc/maoorf/<version>/` (schema YAML, JSON Schema, OWL, SSSOM). `https://w3id.org/eu-parc/maoorf/` points to the latest stable release, and `/1.x/` to the latest 1.x release. These are redirect rules in the w3id repository.
- **Term URIs are not versioned.** Terms such as `maoorf:software` or `maoorf:DAMStatisticalAnalysis.other` keep their meaning across major versions. When a term's meaning changes, a new term is minted and the old one is deprecated (`deprecated`, `deprecated_element_has_exact_replacement`); URIs are never reused for a different meaning.

## Documentation

Documentation is versioned with [mike](https://github.com/jimporter/mike) on the `gh-pages` branch.

| Docs version | Built from |
|---|---|
| `1.0`, `1.1`, … | each 1.x release tag (grouped per minor version; patch releases overwrite their minor) |
| `dev` | `main` |
| alias `stable` | latest final release; the site root redirects here |
| alias `oorf-2023` (optional) | latest 1.x release |

- `deploy-docs.yaml` runs on version tags (`v*`) and on pushes to `main` and `1.x`, and calls `mike deploy --push --update-aliases <version> <alias>`. `mike set-default stable` is run once.
- `mkdocs.yml` sets `extra.version.provider: mike`, so readers can switch versions.
- Generated schema docs (`docs/elements/`) and published artifacts (`docs/schema/`: YAML, JSON Schema, SSSOM) are built into each version's folder, and the w3id redirects for `/maoorf/<version>/` point to them.
- Each docs version states which OORF edition and which Excel template versions it supports, and, once 2.0 exists, how to migrate.

## Changelog and releases

- `CHANGELOG.md` has an entry for every release, with a **Data compatibility** note.
- The changelog entry is copied into the GitHub release notes, and the JSON Schema and SSSOM files are attached to each GitHub release.

### Release checklist

1. Tag `vX.Y.Z` on the right branch (`main` or `1.x`).
2. CI checks that:
   - the tag matches the schema `version`;
   - all files in `tests/data/valid` still validate. On `1.x`, this includes every example from earlier 1.x releases, which are kept as fixtures so that "additive" really means additive;
   - the converter round-trips the 2023 template.
3. Publish the package to PyPI, the artifacts to the GitHub release, and the docs via mike.
4. Update the w3id redirects for a new minor or major version.

## Experimenting with modules

Teams FAIRifying individual modules should not start long-lived branches that edit the existing module files before Stage 2 has landed. Stage 2 touches nearly every attribute in every module file, so such branches would conflict on almost every line.

### 1. Stage 2 lands first

1.0.0 is tagged and Stage 2 is merged before teams start editing module files.
Stage 2 is mostly mechanical; it only needs people for the domain review of the candidate shared slots and for the four renames (which belong before 1.0.0 anyway).
The Stage 2 transformation is committed as a script, so anyone who branched earlier can re-run it on their copy of the files instead of resolving conflicts line by line.

### 2. Work that can start now

Work that does not touch the existing module files does not conflict with Stage 2:

- vocabulary and enum definitions in new files (e.g. `core/vocab/species.yaml` with NCBITaxon-backed enums);
- value types such as `QuantityValue` or `SoftwarePackage`, in new files or agreed with the maintainers of `core/types.yaml`;
- example instances and design notes (e.g. "these RNA-Seq fields should become typed").

### 3. Experiments as overlay files

Experiments live in separate schema files rather than in the module files, for example `modules/daprm/experimental/rna_seq_fair.yaml`, which imports `rna_seq` and either subclasses it (`RNASeqDAPRMFair: is_a: RNASeqDAPRM`) or narrows fields with `slot_usage` (enums, typed ranges, `required`).
Because `DAPRM` and `DARM` use `designates_type`, an instance selects the experimental class through its `type` value.

- Experiments can be merged into `main` early, several teams can work side by side, and variants are easy to compare.
- Experimental classes have `status: testing` or live in an `experimental/` folder, and are not imported by `maoorf.yaml` (use a separate entry schema such as `maoorf_experimental.yaml`). They are therefore not part of release artifacts.
- When an experiment is accepted, it is folded into the real module as a separate change.
- Overlays can narrow fields but cannot restructure them (split one field into several, move sections). That work needs a branch that edits the module itself; it is Stage 3 work and starts after Stage 2.

### 4. Long-lived team branches

- Start from `main` after Stage 2.
- Merge `main` into the branch regularly (e.g. weekly) rather than rebasing at the end. Rebasing a shared branch rewrites history for everyone on it; merging keeps each conflict small and resolves it once. Anyone who prefers to rebase enables `git rerere`.
- Limit each branch to one module.
- Teams working from forks follow the same rules, with the upstream `main` as the base.

### 5. Shared parts

`CODEOWNERS` assigns each module file to its team and `core/` (including `base.yaml` and `entities.yaml`) to the core maintainers.
Changes to shared slots, such as turning the collapsed `software` slot into a typed `SoftwarePackage`, affect every DARM module at once and go through the core maintainers as a single change rather than through one team's branch.
