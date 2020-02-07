# -*- coding: utf-8 -*-
#
# This file is part of CERN Search.
# Copyright (C) 2019 CERN.
#
# Citadel Search is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
"""Tests for receivers."""

from unittest.mock import patch

from cern_search_rest_api.modules.cernsearch.api import CernSearchRecord
from cern_search_rest_api.modules.cernsearch.receivers import file_processed_listener, file_uploaded_listener


@patch('cern_search_rest_api.modules.cernsearch.receivers.delete_previous_record_file_if_exists')
@patch('cern_search_rest_api.modules.cernsearch.receivers.process_file_async.delay')
def test_file_uploaded_listener(
        process_file_async_mock,
        delete_previous_record_file_if_exists_mock,
        base_app,
        record_with_file
):
    """Test process file calls."""
    obj = record_with_file.files['hello.txt']
    file_uploaded_listener(obj)

    process_file_async_mock.assert_called_once_with(str(obj.bucket_id), obj.key)
    delete_previous_record_file_if_exists_mock.assert_called_once_with(obj)


@patch('cern_search_rest_api.modules.cernsearch.receivers.delete_file')
@patch('cern_search_rest_api.modules.cernsearch.receivers.index_file_content')
@patch('cern_search_rest_api.modules.cernsearch.receivers.persist_file_content')
@patch('cern_search_rest_api.modules.cernsearch.receivers.record_from_object_version')
def test_file_processed_listener(
        record_from_object_version_mock,
        persist_file_content_mock,
        index_file_content_mock,
        delete_file_mock,
        base_app,
        record_with_file
):
    """Test process file calls."""
    record = CernSearchRecord.get_record(record_with_file.id)
    record_from_object_version_mock.return_value = record

    file = record_with_file.files['hello.txt']
    file_processed_listener(
        app=base_app,
        processor_id='some-processor',
        file=file.obj,
        data=dict(content='    A simple frase.     With some empty space.   ')
    )

    record_from_object_version_mock.assert_called_once_with(file.obj)
    persist_file_content_mock.assert_called_once_with(
        record,
        'A simple frase. With some empty space.',
        file.obj.basename
    )
    index_file_content_mock.assert_called_once_with(
        record,
        'A simple frase. With some empty space.',
        file.obj.basename
    )
    delete_file_mock.assert_called_once_with(file.obj)
