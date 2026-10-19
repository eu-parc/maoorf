<!-- badges: start -->
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)
<a href="https://github.com/linkml/linkml-project-copier"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-inverted-border-teal.json" alt="Copier Badge" style="max-width:100%;"/></a>
<!-- badges: end -->

# maoorf

A machine actionable OORF schema using LinkML

> [!IMPORTANT]
> **Project Status & Disclaimer:**
> 1. **Community Initiative (not endorsed by the OECD):** This machine-actionable schema is **not endorsed by the OECD**. It is an effort initiated by the toxicology community within **[PARC (Partnership for the Assessment of Risks from Chemicals)](https://www.eu-parc.eu/)** to formalize and FAIRify the published OECD Omics Reporting Framework (OORF).
> 2. **Work in Progress:** This repository is actively under development. See [src/maoorf/schema/README.md](src/maoorf/schema/README.md) for details on the modular architecture and how to define custom reporting modules.

## Documentation Website

[https://eu-parc.github.io/maoorf](https://eu-parc.github.io/maoorf)

## Repository Structure

* [docs/](docs/) - mkdocs-managed documentation
  * [elements/](docs/elements/) - generated schema documentation
* [examples/](examples/) - Examples of using the schema
* [project/](project/) - project files (these files are auto-generated, do not edit)
* [src/](src/) - source files
  * [maoorf](src/maoorf)
    * [schema/](src/maoorf/schema) -- LinkML schema
      (**edit this**)
    * [datamodel/](src/maoorf/datamodel) -- generated
      Python datamodel
* [tests/](tests/) - Python tests
  * [data/](tests/data) - Example data

## Developer Tools

There are several pre-defined command-recipes available.
They are written for the command runner [just](https://github.com/casey/just/).
To list all pre-defined commands, run `just` or `just --list`.

## Upstream Specifications
This machine-actionable schema implements/derives:
> OECD (2023), OECD Omics Reporting Framework (OORF): Guidance on reporting elements for the regulatory use of omics data from laboratory-based toxicology studies, OECD Series on Testing and Assessment, No. 390, OECD Publishing, Paris, <https://doi.org/10.1787/6bb2e6ce-en>.

To download the reporting template and guidance pdf to the `inputs/` folder, run `just fetch-oorf-specs`.

## Credits

This project uses the template [linkml-project-copier](https://github.com/linkml/linkml-project-copier).
