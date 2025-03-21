from django.conf import settings

API_BASE_URL = settings.API_BASE_URL


class APIEndpoints:
    URL_LOGIN = f"{API_BASE_URL}/api/auth/token/"
    URL_LOGOUT = f"{API_BASE_URL}/api/auth/logout/"
    URL_REFRESH = f"{API_BASE_URL}/api/auth/token/refresh/"

    """ Contact START """
    URL_CONTACT_US_LIST = f"{API_BASE_URL}/api/contact-us/"

    @staticmethod
    def URL_CONTACT_US_DETAIL(uuid):
        return f"{API_BASE_URL}/api/contact-us/{uuid}/"

    # @staticmethod
    # def URL_CONTACT_US_UPDATE(uuid):
    #     """Returns the full URL for a specific ContactUs message by UUID."""
    #     return f"{API_BASE_URL}/api/contact-us/{uuid}/"
    """ Contact START """

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

    """ Donation START """
    URL_DONATION_LIST = f"{API_BASE_URL}/api/d/donation/"
    URL_DONATION_CATEGORY = f"{API_BASE_URL}/api/d/category/"
    URL_DONATION_SUB_CATEGORY = f"{API_BASE_URL}/api/d/sub-category/"

    @staticmethod
    def URL_DONATION_DETAILS(uuid):
        return f"{API_BASE_URL}/api/d/donation/{uuid}/"

    @staticmethod
    def URL_DONATION_CATEGORY_DETAILS(uuid):
        return f"{API_BASE_URL}/api/d/category/{uuid}/"

    @staticmethod
    def URL_DONATION_SUB_CATEGORY_DETAILS(uuid):
        return f"{API_BASE_URL}/api/d/sub-category/{uuid}/"

    """ Donation END """

    """ Post START """
    URL_POST_LIST = f"{API_BASE_URL}/api/p/donation/"
    URL_POST_CATEGORY = f"{API_BASE_URL}/api/p/category/"

    # @staticmethod
    # def URL_DONATION_DETAILS(uuid):
    #     return f"{API_BASE_URL}/api/d/donation/{uuid}/"

    @staticmethod
    def URL_POST_CATEGORY_DETAILS(uuid):
        return f"{API_BASE_URL}/api/p/category/{uuid}/"
    """ Post END """

    """ Home Page START """
    URL_HOME_BANNER_LIST = f"{API_BASE_URL}/api/h/home-banner/"
    URL_HOME_BANNER_REORDER = f"{API_BASE_URL}/api/h/home-banner/update-order/"

    """ Post END """
