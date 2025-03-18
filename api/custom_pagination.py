from rest_framework.pagination import PageNumberPagination
from api.utlis import custom_api_response


class CustomPagination(PageNumberPagination):
    """Custom pagination class to include total pages and count."""
    page_size = 10  # Default page size
    page_size_query_param = "page_size"  # Users can change page size dynamically
    max_page_size = 100  # Prevent excessive page sizes

    def get_paginated_response(self, data):
        """Customize paginated response format."""
        return custom_api_response(
            success=True,
            message="Contact messages retrieved successfully.",
            data={
                "total_records": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "page_size": self.page.paginator.per_page,  # Include current page size
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data
            }
        )
