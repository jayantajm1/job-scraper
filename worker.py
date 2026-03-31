"""Celery worker placeholder for enterprise scaling.

This file provides a minimal Celery app definition so that
container orchestration can be prepared in advance.
"""

from __future__ import annotations

import os

try:
    from celery import Celery
except ImportError:  # pragma: no cover
    Celery = None  # type: ignore

BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")

if Celery is not None:
    celery_app = Celery("job_scraper", broker=BROKER_URL)
else:
    celery_app = None
