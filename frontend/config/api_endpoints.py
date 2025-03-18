from django.conf import settings

API_BASE_URL = settings.API_BASE_URL


class APIEndpoints:
    URL_LOGIN = f"{API_BASE_URL}/api/auth/token/"
    URL_LOGOUT = f"{API_BASE_URL}/api/auth/logout/"
    URL_REFRESH = f"{API_BASE_URL}/api/auth/token/refresh/"

    URL_CONTACT_US_LIST = f"{API_BASE_URL}/api/contact-us/"

    @staticmethod
    def URL_CONTACT_US_DETAIL(uuid):
        """Returns the full URL for a specific ContactUs message by UUID."""
        return f"{API_BASE_URL}/api/contact-us/{uuid}/"

    @staticmethod
    def URL_CONTACT_US_UPDATE(uuid):
        """Returns the full URL for a specific ContactUs message by UUID."""
        return f"{API_BASE_URL}/api/contact-us/{uuid}/"
