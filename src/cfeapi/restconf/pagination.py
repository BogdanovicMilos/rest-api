from rest_framework import pagination


class CFEAPIPagination(pagination.LimitOffsetPagination):  # PageNumberPagination
    # page_size = 5
    default_limit = 10
    max_limit = 10

    # limit_query_param = 'lim'
