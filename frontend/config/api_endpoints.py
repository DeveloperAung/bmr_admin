from django.conf import settings

API_BASE_URL = settings.API_BASE_URL


class APIEndpoints:
    URL_LOGIN = f"{API_BASE_URL}/api/auth/token/"
    URL_LOGOUT = f"{API_BASE_URL}/api/auth/logout/"
    URL_REFRESH = f"{API_BASE_URL}/api/auth/token/refresh/"

    URL_CONTACT_US_LIST = f"{API_BASE_URL}/api/contact-us/"

    @staticmethod
    def URL_CONTACT_US_DETAIL(uuid):
        return f"{API_BASE_URL}/api/contact-us/{uuid}/"

    # @staticmethod
    # def URL_CONTACT_US_UPDATE(uuid):
    #     """Returns the full URL for a specific ContactUs message by UUID."""
    #     return f"{API_BASE_URL}/api/contact-us/{uuid}/"

    """ Event START """
    URL_EVENT_LIST = f"{API_BASE_URL}/api/e/event/"
    URL_EVENT_CATEGORY = f"{API_BASE_URL}/api/e/category/"
    URL_EVENT_SUB_CATEGORY = f"{API_BASE_URL}/api/e/sub-category/"

    @staticmethod
    def URL_EVENT_DETAILS(uuid):
        return f"{API_BASE_URL}/api/e/event/{uuid}/"

    @staticmethod
    def URL_EVENT_CATEGORY_DETAILS(uuid):
        return f"{API_BASE_URL}/api/e/category/{uuid}/"

    @staticmethod
    def URL_EVENT_SUB_CATEGORY_DETAILS(uuid):
        return f"{API_BASE_URL}/api/e/sub-category/{uuid}/"

    """ Event END """
