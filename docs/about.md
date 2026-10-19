# About maoorf

`maoorf` is a machine-actionable formalization of the **OECD Omics Reporting Framework (OORF)** built with [LinkML (Linked Data Modeling Language)](https://linkml.io/).

!!! warning "Disclaimer & Project Status"
    1. **Not Yet Endorsed by the OECD:** This schema is an independent community effort started by the toxicology community in **[PARC (Partnership for the Assessment of Risks from Chemicals)](https://www.eu-parc.eu/)**. It has not yet been formally reviewed or endorsed by the OECD.
    2. **Work in Progress:** The model is under active development. In its current stage, it closely mirrors the structure of the 2023 OECD OORF Excel reporting templates so that existing filled-in templates can be validated and converted into JSON/YAML while preserving exact 1:1 mappings (`oecd_oorf_2023`) for [SSSOM](https://mapping-commons.github.io/sssom/) generation. Subsequent iterations will link slots to domain ontologies and controlled vocabularies to further FAIRify regulatory omics reporting.

## Upstream OECD Specification

This schema derives from the published OECD guidance document and reporting templates:

> OECD (2023), *OECD Omics Reporting Framework (OORF): Guidance on reporting elements for the regulatory use of omics data from laboratory-based toxicology studies*, OECD Series on Testing and Assessment, No. 390, OECD Publishing, Paris, <https://doi.org/10.1787/6bb2e6ce-en>.

## Extensible Modular Design

Because omics technologies and data analysis methods continuously evolve, the OORF is designed as a modular framework. `maoorf` reflects this modularity in LinkML:

- **[`OORF`](elements/classes/OORF.md)**: The root container representing a complete study report.
- **[`SSRM`](elements/classes/SSRM.md)** & **[`TERM`](elements/classes/TERM.md)**: Study summary and toxicology experiment modules.
- **[`DAPRM`](elements/classes/DAPRM.md)**: Abstract base class for platform-specific Data Acquisition and Processing Reporting Modules (`MicroarrayDAPRM`, `RNASeqDAPRM`, `QRTPCRDAPRM`, `MassSpectrometryDAPRM`, `NMRDAPRM`).
- **[`DARM`](elements/classes/DARM.md)**: Abstract base class for Data Analysis Reporting Modules (`DAMDARM`, `MVADARM`, `BMDDARM`, `EBPDARM`).

External researchers and tool developers can define their own custom `DAPRM` or `DARM` modules by subclassing `DAPRM` or `DARM` in a standalone YAML file. See the [schema directory README](https://github.com/eu-parc/maoorf/blob/main/src/maoorf/schema/README.md) for a step-by-step guide.
