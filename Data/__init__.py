#!/usr/bin/python3
import logging
from pathlib import Path

TOP_DIR = Path(__file__).resolve().parent.parent
EVENT_DIR = TOP_DIR.joinpath('Events')

LOGGER = logging.getLogger(__name__)


def clean_filename(filename: str) -> str:
    return filename.replace(':', '')
