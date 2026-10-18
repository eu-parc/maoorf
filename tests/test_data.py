"""Data test."""

import os
import glob
import pytest
from pathlib import Path

import maoorf.datamodel.maoorf
from linkml_runtime.loaders import json_loader, yaml_loader

DATA_DIR_VALID = Path(__file__).parent / "data" / "valid"
DATA_DIR_INVALID = Path(__file__).parent / "data" / "invalid"

VALID_EXAMPLE_FILES = sorted(
    glob.glob(os.path.join(DATA_DIR_VALID, "*.yaml"))
    + glob.glob(os.path.join(DATA_DIR_VALID, "*.json"))
)
INVALID_EXAMPLE_FILES = glob.glob(os.path.join(DATA_DIR_INVALID, "*.yaml"))


@pytest.mark.parametrize("filepath", VALID_EXAMPLE_FILES)
def test_valid_data_files(filepath):
    """Test loading of all valid data files."""
    target_class_name = Path(filepath).stem.split("-")[0]
    tgt_class = getattr(
        maoorf.datamodel.maoorf,
        target_class_name,
    )
    loader = json_loader if str(filepath).endswith(".json") else yaml_loader
    obj = loader.load(filepath, target_class=tgt_class)
    assert obj
