def get_filter_operators():
    """
    Get the available filter operators and their corresponding lambda functions.

    :return: A dictionary of filter operators and lambda functions.
    """
    return {
        'equals': lambda column, search_string: column == search_string,
        'contains': lambda column, search_string: column.ilike(f'%{search_string}%'),
    }


def filter_entities(filters, model_mapping):
    """
    Filter entities based on provided filter conditions.

    :param filters: A list of filter conditions.
    :param model_mapping: A mapping of entity names to models.

    :return: A list of filter conditions as lambda functions.
    """
    conditions = []
    for item in filters:
        condition = build_condition_filter(item, model_mapping)
        if condition is not None:
            conditions.append(condition)
    return conditions


def build_condition_filter(item, model_mapping):
    """
    Build a filter condition as a lambda function based on filter item.

    :param item: A filter condition item.
    :param model_mapping: A mapping of entity names to models.

    :return: A filter condition as a lambda function or None if the entity is not found.
    """
    entity_name = item['entity']
    entity = model_mapping.get(entity_name)
    if entity:
        column_name = item['field']
        operator = item['operator']
        search_string = item['value']
        column = entity.__dict__[column_name]
        return get_filter_operators()[operator](column, search_string)
    return None


def build_filter_values(filters, params_allowed):
    """
    Build filter conditions based on allowed parameters.

    :param filters: A dictionary of filters provided in the request.
    :param params_allowed: A list of allowed filter parameters and their details.

    :return: A list of filter conditions as dictionaries.
    """
    allowed_filters = []
    for field, search_string in filters.items():
        filter_param = next((param for param in params_allowed if param['param'] == field), None)
        if filter_param:
            allowed_filters.append({
                'value': search_string,
                'operator': filter_param['operator'],
                'entity': filter_param['entity'],
                'field': filter_param['field']
            })
    return allowed_filters
