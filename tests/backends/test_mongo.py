def test_mongo_insert_get(context):
    # Add few objects to database.
    result = context.push([
        {
            'type': 'report',
            'status': '42',
        },
    ])

    result = {x.pop('type'): x for x in result}

    # mongo inserts ID at key `_id` and we also insert ID at key `id`, look up
    # code at: spinta/types/store.py::push
    assert result == {
        'report': {
            'id': result['report']['id'],
            'status': '42',
            'notes': [],
            'count': None,
            'report_type': None,
            'update_time': None,
            'valid_from_date': None,
        },
    }

    # Read those objects from database.
    get_data = context.getone('report', result['report']['id'])
    assert get_data == {
        'type': 'report',
        'revision': get_data['revision'],
        'id': result['report']['id'],
        'status': '42',
        'notes': [],
        'count': None,
        'report_type': None,
        'update_time': None,
        'valid_from_date': None,
    }


def test_mongo_update_get(context):
    # Add few objects to database.
    insert_result = context.push([
        {
            'type': 'report',
            'status': '42',
        },
    ])

    # change report status
    report_data = list(insert_result)[0]
    report_data['status'] = '13'

    # push updated report to database
    update_result = context.push([report_data])
    update_result = {x.pop('type'): x for x in update_result}

    # mongo inserts ID at key `_id` and we also insert ID at key `id`, look up
    # code at: spinta/types/store.py::push
    assert update_result == {
        'report': {
            'id': update_result['report']['id'],
            'status': '13',
            'notes': [],
            'count': None,
            'report_type': None,
            'update_time': None,
            'valid_from_date': None,
        },
    }

    # Read those objects from database.
    get_data = context.getone('report', update_result['report']['id'])
    assert get_data == {
        'type': 'report',
        'revision': get_data['revision'],
        'id': update_result['report']['id'],
        'status': '13',
        'notes': [],
        'count': None,
        'report_type': None,
        'update_time': None,
        'valid_from_date': None,
    }

    # Get all objects from database.
    result = context.getall('report')
    assert result == [
        {
            'type': 'report',
            'revision': result[0]['revision'],
            'id': update_result['report']['id'],
            'status': '13',
            'notes': [],
            'count': None,
            'report_type': None,
            'update_time': None,
            'valid_from_date': None,
        },
    ]
