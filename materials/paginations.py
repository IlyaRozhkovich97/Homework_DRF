from rest_framework.pagination import PageNumberPagination


class MaterialsPaginator(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page-size'
    max_page_size = 10
