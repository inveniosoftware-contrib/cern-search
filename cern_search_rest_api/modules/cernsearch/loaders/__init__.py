#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This file is part of CERN Search.
# Copyright (C) 2018-2021 CERN.
#
# Citadel Search is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Record loading related code."""

from invenio_records_rest.loaders.marshmallow import marshmallow_loader

from cern_search_rest_api.modules.cernsearch.marshmallow import CSASRecordSchemaV1

csas_loader = marshmallow_loader(CSASRecordSchemaV1)

__all__ = ("csas_loader",)
