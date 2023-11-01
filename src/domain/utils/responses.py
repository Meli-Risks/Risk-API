def response_paginated(total, page, per_page, pages, results):
    """
    Create a paginated response dictionary.

    :param total: Total number of records.
    :param page: Current page number.
    :param per_page: Number of records per page.
    :param pages: Total number of pages.
    :param results: List of results to be included in the response.

    :return: A dictionary containing paginated response information.
    """
    return {
        'totalRecords': total,
        'pageNumber': page,
        'pageSize': per_page,
        'totalPages': pages,
        'content': results
    }
