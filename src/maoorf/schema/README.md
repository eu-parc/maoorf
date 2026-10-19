# OECD Omics Reporting Framework (OORF) LinkML Schema

This directory contains the modular LinkML schema formalization of the OECD Omics Reporting Framework (OORF 2023, OECD Series on Testing and Assessment No. 381 / Series on Adverse Outcome Pathways No. 20).

The schema is organized modularly to enable domain-specific extensibility: external communities can define custom Data Acquisition and Processing Reporting Modules (DAPRMs) or Data Analysis Reporting Modules (DARMs) without modifying the core study summary or toxicology modules.

---

## Directory Structure

```
src/maoorf/schema/
├── maoorf.yaml                 # Root orchestrator combining imports and tree_root (OORF)
├── core/
│   ├── types.yaml              # CURIE patterns, custom types, and unit primitives
│   ├── base.yaml               # Abstract DAPRM and DARM base classes and shared slots
│   └── entities.yaml           # Reusable entities (FileManifestEntry, SoftwareDocumentation, etc.)
└── modules/
    ├── ssrm.yaml               # 1. Study Summary Reporting Module (SSRM)
    ├── term.yaml               # 2. Toxicology Experiment Reporting Module (TERM)
    ├── daprm/                  # 3. Data Acquisition and Processing Reporting Modules
    │   ├── base_daprm.yaml     # Base DAPRM module definitions
    │   ├── microarray.yaml     # 3.1 Microarray DAPRM
    │   ├── rna_seq.yaml        # 3.2 RNA-Seq and Targeted RNA-Seq DAPRM
    │   ├── qrt_pcr.yaml        # 3.3 qRT-PCR Array DAPRM
    │   ├── ms.yaml             # 3.4 Mass Spectrometry (Metabolomics) DAPRM
    │   └── nmr.yaml            # 3.5 Nuclear Magnetic Resonance (NMR Metabolomics) DAPRM
    └── darm/                   # 4. Data Analysis Reporting Modules
        ├── base_darm.yaml      # Base DARM module definitions
        ├── dam.yaml            # 4.1 Differentially Abundant Molecules (DAM) Univariate DARM
        ├── mva.yaml            # 4.2 Multivariate Statistical Analysis (MVA) DARM
        ├── bmd.yaml            # 4.3 Benchmark Dose (BMD) Analysis DARM
        └── ebp.yaml            # 8. Enriched Biological Pathways (EBP) DARM (Draft)
```

---

## Module Purposes & Roles

### 1. Root Orchestrator: `maoorf.yaml`
- Defines the `tree_root: true` root class `OORF`.
- Assembles all submodules and shared dependencies via LinkML `imports:`.
- Represents the top-level submission object containing:
  - `ssrm`: exactly one [`SSRM`](modules/ssrm.yaml) instance.
  - `term`: exactly one [`TERM`](modules/term.yaml) instance.
  - `daprm`: list of polymorphic [`DAPRM`](core/base.yaml) modules (`MicroarrayDAPRM`, `RNASeqDAPRM`, etc.).
  - `darm`: list of polymorphic [`DARM`](core/base.yaml) modules (`DAMDARM`, `MVADARM`, `BMDDARM`, `EBPDARM`, etc.).
  - `file_manifest`: list of [`FileManifestEntry`](core/entities.yaml) records listing all data objects, scripts, and checksums.

### 2. Core Definitions: `core/`
- **`types.yaml`**: Defines LinkML custom scalar types, URI prefixes, and placeholder CURIE formats.
- **`base.yaml`**:
  - Abstract base class [`DAPRM`](core/base.yaml) with `type` designating polymorphic specialization.
  - Abstract base class [`DARM`](core/base.yaml) with polymorphic `type`, plus common analysis slots `inputs` (range: `DARMInputs`) and `outputs` (range: `DARMOutputs`).
  - Common slot definitions shared across multiple modules (preventing ambiguous attribute collisions during generator execution).
- **`entities.yaml`**:
  - [`FileManifestEntry`](core/entities.yaml): Tabular and file manifest tracking metadata (`file_name`, `file_description`, `md5_checksum`).
  - [`SoftwareDocumentation`](core/entities.yaml): Common software specifications (`software`, `operating_system`, `additional_libraries_used`, `software_availability`).
  - [`AssayExperimentalDesign`](core/entities.yaml): Experimental groupings, covariance notes, and replicate structure across assays.

### 3. Study & Experiment Modules: `modules/`
- **`ssrm.yaml` (Module 1 - Study Summary Reporting Module)**:
  - Captures high-level study identity, executive abstract, regulatory test guidelines, and summary representations of the experimental rationale, DAPRM technologies, and DARM analyses.
- **`term.yaml` (Module 2 - Toxicology Experiment Reporting Module)**:
  - Exhaustive descriptions of in vivo and in vitro test systems, chemical test and control items, physicochemical parameters, stability, exposure conditions, dosing schedules, husbandry/cell culture, sample harvest, and sample identifiers.

### 4. Data Acquisition and Processing Modules: `modules/daprm/`
Specialized classes inheriting from abstract `DAPRM` (`is_a: DAPRM`):
- **`base_daprm.yaml`**: Anchor and import hub for acquisition modules.
- **`microarray.yaml` (`MicroarrayDAPRM`)**: 1-channel / 2-channel microarray hybridizations, scanner protocols, background subtraction, and post-normalization filters.
- **`rna_seq.yaml` (`RNASeqDAPRM`)**: Short-read sequencing and targeted RNA-seq (e.g. TempO-Seq), wet-lab QC, sequencing standards, trimming, pseudo-alignment/mapping, and count normalization.
- **`qrt_pcr.yaml` (`QRTPCRDAPRM`)**: Quantitative reverse-transcription PCR array protocols, primer designs, efficiency checks, reference gene selections, and $\Delta\Delta C_q$ calculations.
- **`ms.yaml` (`MassSpectrometryDAPRM`)**: LC-MS and GC-MS metabolomics assays, extraction solvents, instrument configurations, batch acquisition order, peak picking/alignment, and metabolite identification levels.
- **`nmr.yaml` (`NMRDAPRM`)**: 1D and 2D NMR metabolomics, pulse sequences, solvent suppression, phasing, baseline corrections, and spectral binning/bucketing.

### 5. Data Analysis Reporting Modules: `modules/darm/`
Specialized classes inheriting from abstract `DARM` (`is_a: DARM`):
- **`base_darm.yaml`**: Anchor and import hub for analysis modules.
- **`dam.yaml` (`DAMDARM`)**: Univariate differential analysis (e.g. DESeq2, limma), linear models, p-value thresholds, and log2 fold-change outputs.
- **`mva.yaml` (`MVADARM`)**: Multivariate unsupervised (PCA, WGCNA) and supervised (PLS-DA, OPLS-DA) analyses, cross-validation, and feature importance.
- **`bmd.yaml` (`BMDDARM`)**: Benchmark dose (BMD) and point of departure (PoD) modeling (e.g. BMDExpress, EPA BMDS), model averaging, BMR factor configurations, and pathway/gene-set level BMD derivations.
- **`ebp.yaml` (`EBPDARM`)**: Enriched biological pathways and functional gene set overrepresentation analyses (e.g. ORA, GSEA).

---

## Design Principles

1. **Strict OECD Element Alignment**:
   - Every class and slot is tagged with `exact_mappings:` referencing `oecd_oorf_2023:<element_id>` (e.g., `oecd_oorf_2023:2.1.5.a`). This supports direct generation of SSSOM mapping tables.
2. **Safe Documentation Generation**:
   - The first line of every `description:` matches the OECD Reporting Element title with abbreviations stripped of dots (`eg`, `ie`, `aka`, `txt`) to prevent truncation in `gen-doc`.
   - The remaining lines of the description preserve the exact official OECD Guidance PDF text.
3. **Comment Preservation**:
   - Instructions from the `NOTES AND INSTRUCTIONS FOR DATA PROVIDERS` spreadsheet columns are preserved as LinkML `comments:`.
4. **Permissive Ingestion**:
   - Required and Recommended OECD elements are specified as `recommended: true` rather than strict schema-level `required: true`, allowing real-world workbooks and historical submissions with partial entries to validate while signaling missing recommendations.
5. **Polymorphic Modules**:
   - Subclasses of `DAPRM` and `DARM` declare their concrete type with `type: <ClassName>`, allowing automated deserialization into the appropriate typed classes.

---

## How to Create Your Own DAPRM or DARM

The modular architecture allows external groups to create custom reporting modules (e.g., Proteomics LC-MS/MS, Spatial Transcriptomics, Single-Cell RNA-seq, Epigenomics/ChIP-seq, Machine Learning/Deep Learning QSAR).

### Important Note on Relative Imports
LinkML's `SchemaLoader` automatically resolves relative imports in subdirectories **only if the import path starts with `.`** (e.g., `./base_daprm` or `../../core/base`). Always start relative file paths with `./` or `../`.

---

### Example: Creating a Custom DARM

1. **Location**: Place your new module YAML under `src/maoorf/schema/modules/darm/` (e.g., `spatial_clustering.yaml`).
2. **Imports**: Import `linkml:types` and `./base_darm` (which provides `DARM`, `DARMInputs`, `DARMOutputs`, `SoftwareDocumentation`, and `AssayExperimentalDesign`).
3. **Inheritance**: Subclass `DARM` (`is_a: DARM`).
4. **Inherited Slots**:
   - `DARM` already inherits standard `inputs` and `outputs` slots. You can refine them using `slot_usage:` (e.g., specifying custom input/output classes derived from `DARMInputs` and `DARMOutputs`), or keep the base ones.
   - For software documentation, you can reuse `SoftwareDocumentation` directly or subclass it.

#### Example DARM Template (`modules/darm/spatial_clustering.yaml`):

```yaml
id: https://w3id.org/eu-parc/maoorf/modules/darm/spatial_clustering
name: maoorf_spatial_clustering
title: Spatial Clustering and Neighborhood Analysis DARM
description: >-
  Data Analysis Reporting Module (DARM) for Spatial Transcriptomics Neighborhood and Clustering Analysis
license: MIT

prefixes:
  maoorf: https://w3id.org/eu-parc/maoorf/
  linkml: https://w3id.org/linkml/

default_prefix: maoorf
default_range: string

imports:
  - linkml:types
  - ./base_darm

classes:
  SpatialClusteringDARM:
    is_a: DARM
    description: |-
      Data Analysis Reporting Module for Spatial Clustering and Cell-Cell Interaction Analysis
    slot_usage:
      inputs:
        range: SpatialClusteringInputs
      outputs:
        range: SpatialClusteringOutputs
    attributes:
      software_documentation:
        description: Software package and libraries used for spatial analysis
        range: SoftwareDocumentation
        recommended: true
      clustering_method:
        description: Spatial clustering algorithm, spatial graph construction, and hyper-parameters
        range: SpatialClusteringMethodDetails
        recommended: true

  SpatialClusteringInputs:
    is_a: DARMInputs
    description: Input spatial matrix and coordinate registration data objects.

  SpatialClusteringOutputs:
    is_a: DARMOutputs
    description: Spatial cluster maps, neighbor interaction matrices, and marker tables.

  SpatialClusteringMethodDetails:
    description: Details of the spatial neighborhood graph and clustering algorithm.
    attributes:
      spatial_graph_method:
        description: Graph construction method (e.g., k-nearest neighbors, Delaunay triangulation)
        recommended: true
      clustering_algorithm:
        description: Graph clustering algorithm (e.g., Leiden, Louvain, BayesSpace)
        recommended: true
      resolution_parameter:
        description: Resolution parameter or target cluster count k
        recommended: true
```

---

### Registering Your New Module in the Root Schema

Once your DAPRM or DARM module file is created:
1. Open [`maoorf.yaml`](maoorf.yaml).
2. Add your module path to the `imports:` list:
   ```yaml
   imports:
     ...
     - modules/darm/spatial_clustering
   ```
3. Run linting and test suite:
   ```bash
   just lint
   just test
   ```
4. Any valid OORF instance can now include your new module in its `daprm` or `darm` lists using the module class name as the discriminator:
   ```yaml
   darm:
     - type: SpatialClusteringDARM
       clustering_method:
         clustering_algorithm: Leiden
   ```

