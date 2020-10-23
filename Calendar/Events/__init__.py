#!/usr/bin/python3
import logging
from pathlib import Path

TOP_DIR = Path(__file__).resolve().parent.parent.parent
EVENT_DIR = TOP_DIR.joinpath('data')

LOGGER = logging.getLogger(__name__)


def clean_filename(filename: str) -> str:
    return filename.replace(':', '')
