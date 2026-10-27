# maoorf development roadmap

This roadmap describes how the maoorf LinkML schema evolves from a faithful JSON representation of the OECD OORF (2023) Excel template into a formalised, FAIR schema.
It builds on the recommendations in `inputs/gemini_reports/` (not tracked in git) and on a review of the current schema.
Versioning, branching, documentation and team workflow are described in [DEVELOPMENT.md](DEVELOPMENT.md).

The ordering matters at two points:

- **Stage 2 before Stage 4**, so that SSSOM records stable identities before reporting elements are decomposed into atomic slots.
- **The Stage 1 version tag before Stage 3**, so that existing JSON instances can be migrated when the data shape changes.

## Background: attribute name collisions

Most reporting elements are class `attributes`. Because every attribute gets the URI `maoorf:<name>`, 132 attribute names are shared between classes, and 131 of them map to a different OORF element in each place they are used (e.g. `other` is used 23 times, `other_relevant_information` 14 times).

- **JSON/YAML is not affected.** A key is scoped by its parent object, so validation, the JSON Schema and the Python/Pydantic datamodels are correct.
- **Semantic artifacts are affected.** The SSSOM output claims that unrelated OORF elements are equivalent (`maoorf:other` has 23 `skos:exactMatch` rows). OWL collapses each name into one property with a generic definition and loses the mappings, and 30 properties are declared as both datatype and object property. JSON-LD/RDF use one predicate for distinct elements.

None of the planned fixes in Stage 2 change JSON keys, so Stage 1 instances stay valid.

## Stage 1 — Faithful JSON copy of the Excel template (current)

Goal: lossless, verbatim round-trip of any filled-in OORF 2023 workbook to JSON.

1. **Converter** (`scripts/convert_oorf_excel.py`)
   - Locate rows by element number or label instead of hard-coded row numbers, and fail loudly on mismatches (the example workbook and the 2023 template differ: `Required` vs `Recommended`, an extra EBP sheet).
   - Parse all DAPRM and DARM sheets (currently only RNA-Seq, DAM, MVA and BMD).
   - Support several runs per sheet (column D = run 1, E = run 2, …) as separate `daprm[]` / `darm[]` entries. EUT046 needs this for its two BMD analyses.
   - Take the output path as an argument and stop overwriting `tests/data/valid/OORF-EUT046.*`.
   - Skip instruction text that the template places in the input column of section header rows.
2. **Keep values verbatim**: sentinels (`NA`, `NOT IN VIVO STUDY`, `UNKNOWN`) and placeholders (`FOLLOW UP WITH …`) stay as strings, and all ranges stay `string`.
3. **Tests**
   - Validate examples against the JSON Schema in pytest.
   - Add negative examples to `tests/data/invalid/` and use them.
   - Add an Excel → JSON → compare round-trip test on the blank 2023 template and on EUT046.
4. **Schema hygiene**
   - Fix the description of the `type` discriminator (it is used by both DAPRM and DARM).
   - Mark the EBP module as not part of OORF 2023: it maps to `oecd_oorf_2023:8.x`, IDs that do not exist in the 2023 release.
   - Keep `recommended` as is for now.
   - Declare `openpyxl` as a direct dependency.
5. **Published artifacts**: publish JSON Schema, YAML and docs only. Hold back OWL, JSON-LD and SSSOM until Stage 2, or replace SSSOM with a path-based lookup table (e.g. `/darm[BMDDARM]/software_documentation/software ↔ 4.3.2.1`), which is unambiguous today.
6. **Versioning**: tag a schema version (e.g. `0.1.0`) and record it in each instance, so later data-shape changes can be migrated.

## Stage 2 — Clean up identities without changing the data format

Goal: one stable identifier per concept and per OORF element. Stage 1 JSON remains valid.

1. **Collapse shared concepts**
   - The 12 slots that are already shared (`software`, `operating_system`, `additional_libraries_used`, `software_availability`, `inputs`, `outputs`, `data_input`, `metadata_input`, `output_and_supporting_files`, `group_sizes`, `covariance`, `technical_replicates`) drop their per-module `exact_mappings`. Module-specific guidance stays in `slot_usage` (it still shows in JSON Schema, Pydantic, SHACL and the class docs pages).
   - Do the same for `software_documentation` and `assay_experimental_design`, whose ranges have a common parent.
   - Domain-expert review of the 30 names that differ only in their mappings (e.g. `sex`, `strain`, `test_item_name`, `temperature`, `humidity`, `ph`, MS/NMR workflow fields): decide which are the same concept and should be shared.
2. **Give the remaining attributes their own URIs**: `slot_uri: maoorf:<Class>.<attr>`, plus `use_native_uris: false` for the OWL generator in `config.yaml` (gen-owl ignores `slot_uri` otherwise).
3. **Fix OWL punning**
   - Remove or retype the string-ranged placeholder top-level slots in `core/base.yaml`. They currently also affect `linkml-convert`, so test this carefully.
   - Resolve the four names that are a string in one class and an object in another (`contrasts`, `overall_description_and_rationale`, `model_selection`, `commercial_source`). This needs a rename and is the only data-shape change here; consider doing it before the Stage 1 version tag.
4. **Keep element traceability for shared slots** with annotations (e.g. `annotations: {oorf_element: "4.3.2.1"}` on the `slot_usage`), rather than `exact_mappings`.
5. **Publish semantic artifacts**
   - Generate the baseline SSSOM mapping table.
   - Publish OWL and SHACL.
   - Decide on JSON-LD: the generated context is flat, so with per-attribute `slot_uri` it maps keys like `other` to a single IRI. Either drop it, or document `linkml-convert -t ttl` as the way to get RDF.

## Stage 3 — Structural formalisation (data shape changes; needs a v1 → v2 migration script)

1. **Missing values**: `any_of: [<semantic type>, MissingValueEnum]` (e.g. NCIT *Unknown*, *Not Applicable*). The converter maps sentinels to enum values, and placeholders become an explicit "pending" state.
2. **Conditional applicability**: add a `study_model_type` discriminator on TERM (in vivo, in vitro, …) and use LinkML `rules` to require the matching sections. At this point `recommended` can become `required` where the guidance mandates it. Note that template section 2.5.8 is wrongly flagged as in-vivo-only.
3. **Module identity**: give each DAPRM and DARM instance an `id`.
4. **File manifest as referential integrity**
   - Make `file_name` an identifier, and make `data_input`, `metadata_input` and `output_and_supporting_files` multivalued references to `FileManifestEntry`.
   - The converter flags free text it cannot resolve rather than guessing (EUT046 has 9 mismatches).
5. **SSRM**: keep section 1.1 (study identifiers). First add SSRM ↔ TERM consistency checks; later generate the SSRM summary from TERM, DAPRM and DARM instead of storing duplicated data.

## Stage 4 — Typed values and vocabularies

1. **Structured value objects**: `QuantityValue` / `DoseSeries` with units (UO/UCUM), `SoftwarePackage` (name, version, URL, RRID), `ChemicalIdentifier`. Decomposed fields get `broad_mappings` to the original OORF element, with the parsing rule recorded in the SSSOM.
2. **Ontology-backed enums**, starting with species (NCBITaxon), cell lines (Cellosaurus/CLO), tissues (UBERON) and route of administration (ExO); then OBI/EFO, EDAM/SWO, STATO and GO/Reactome/WikiPathways.
3. **Converter becomes an assisted parser**: it proposes typed values for human confirmation, because fully automatic parsing of free text is not reliable enough for regulatory data.

## Stage 5 — Ecosystem and extension

1. **Protocol/platform profiles** for outsourced assays (e.g. commercial TempO-Seq, LC-MS or NMR services), referenced by URI with study-specific overrides.
2. **Provenance export**: a PROV-O / RO-Crate lineage graph built from the file-manifest references.
3. **Guide for community modules** (proteomics, lipidomics, single-cell, …), using the `designates_type` plug-in mechanism on `DAPRM` / `DARM`.
4. **Non-OECD modules** (EBP and future extensions) maintained as clearly marked extensions under their own prefix.
