def build_map_filter_from_request(params_request):
    """
    Build a dictionary of filters from the request parameters.

    :param params_request: Request parameters as key-value pairs.

    :return: A dictionary containing filters.
    """
    filters = {}
    for key, value in params_request:
        filters[key] = value
    return filters


def validate_data_type_param(filter_param, search_string):
    """
    Validate the data type of a filter parameter.

    :param filter_param: The filter parameter definition.
    :param search_string: The value to validate.

    :return: True if the data type is valid, otherwise False.
    """
    if search_string is not None:
        if filter_param.get('type', None) == 'number':
            return search_string.isdigit()
        return True
    return False


class PaginatedRequestDto:
    """
    Data Transfer Object (DTO) for paginated requests.
    """

    def __init__(self, request):
        """
        Initialize a PaginatedRequestDto object from a request.

        :param request: The HTTP request object.
        """
        self.page = int(request.args.get('pageNumber', 1))
        self.per_page = int(request.args.get('pageSize', 10))
        self.order_by = request.args.get('orderBy', None)
        self.order_type = request.args.get('orderType', 'desc')
        self.global_filter = request.args.get('globalFilter', None)
        self.filters = build_map_filter_from_request(request.args.items())

    def add_filter(self, key, value):
        """
        Add a filter to the PaginatedRequestDto object.

        :param key: The filter key.
        :param value: The filter value.
        """
        self.filters[key] = value

    def build_order_by(self, default, allowed_sorts):
        """
        Build the 'order_by' field from available sorting options.

        :param default: The default sorting field.
        :param allowed_sorts: List of allowed sorting fields.
        """
        if self.order_by not in allowed_sorts:
            self.order_by = default

    def build_filter_values(self, params_allowed):
        """
        Build filter values based on allowed parameters.

        :param params_allowed: List of allowed filter parameters.
        """
        allowed_filters = []

        for field, search_string in self.filters.items():
            filter_param = next((param for param in params_allowed if param['param'] == field), None)

            if filter_param and validate_data_type_param(filter_param, search_string):
                allowed_filters.append({
                    'value': search_string,
                    'operator': filter_param['operator'],
                    'entity': filter_param['entity'],
                    'field': filter_param['field']
                })

        self.filters = allowed_filters
