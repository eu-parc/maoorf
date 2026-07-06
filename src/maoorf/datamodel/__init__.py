"""Data model package for maoorf."""

from pathlib import Path
from .maoorf import *  # noqa: F403

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "maoorf.yaml"
