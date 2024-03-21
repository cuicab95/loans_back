from rest_framework import pagination


class DefaultPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"
    page_size = 10
    max_page_size = 3000
