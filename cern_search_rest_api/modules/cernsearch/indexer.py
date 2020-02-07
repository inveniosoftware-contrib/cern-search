#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of CERN Search.
# Copyright (C) 2018-2019 CERN.
#
# Citadel Search is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Indexer utilities."""

from cern_search_rest_api.modules.cernsearch.api import CernSearchRecord
from invenio_indexer.api import RecordIndexer


def index_file_content(record: CernSearchRecord, file_content: str, filename: str):
    """Index file content in search."""
    record['_data']['_attachment'] = dict(_content=file_content)
    record['_file'] = filename
    RecordIndexer().index(record)
