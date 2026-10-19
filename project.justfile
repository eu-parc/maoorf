## Add your own just recipes here. This is imported by the main justfile.

# Overriding recipes from the root justfile by adding a recipe with the same
# name in this file is not possible until a known issue in just is fixed,
# https://github.com/casey/just/issues/2540

# Download the the OORF template and guide to the `inputs` directory
[group('project management')]
fetch-oorf-specs:
    curl -O https://www.oecd.org/content/dam/oecd/en/publications/reports/2023/11/oecd-omics-reporting-framework-oorf-guidance-on-reporting-elements-for-the-regulatory-use-of-omics-data-from-laboratory-based-toxicology-studies_9f10a387/6bb2e6ce-en.pdf --output-dir inputs
    curl -LO https://www.oecd.org/chemicalsafety/testing/omics-reporting-framework-reporting-template-2023.xlsx --output-dir inputs

# Generate SSSOM mapping table
[group('model development')]
gen-sssom:
    mkdir -p project/sssom
    uv run gen-sssom {{source_schema_path}} -o project/sssom/{{schema_name}}.sssom.tsv

# Add SSSOM artifact to the distribution schema directory (docs/schema/)
_add-artifacts: gen-sssom
    -mkdir -p {{distrib_schema_path}}
    cp project/sssom/{{schema_name}}.sssom.tsv {{distrib_schema_path}}/
