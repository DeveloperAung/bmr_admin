from django.conf import settings

API_BASE_URL = settings.API_BASE_URL


class APIEndpoints:
    URL_LOGIN = f"{API_BASE_URL}/api/auth/token/"
    URL_LOGOUT = f"{API_BASE_URL}/api/auth/logout/"
    URL_REFRESH = f"{API_BASE_URL}/api/auth/token/refresh/"

    """ Admin Users START """
    URL_ADMIN_USERS = f"{API_BASE_URL}/api/auth/admin-user/"
    URL_ADMIN_USER_ROLES = f"{API_BASE_URL}/api/auth/admin-user-role/"

    @staticmethod
    def URL_ADMIN_USER_DETAILS(uuid):
        return f"{API_BASE_URL}/api/auth/admin-user/{uuid}/"
    """ Admin Users END """

    """ Subscribers START """
    URL_SUBSCRIBERS = f"{API_BASE_URL}/api/sub/subscribers/"

    @staticmethod
    def URL_SUBSCRIBERS_DETAILS(uuid):
        return f"{API_BASE_URL}/api/sub/subscribers/{uuid}/"


    """ Subscribers END """

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
    URL_EVENTS = f"{API_BASE_URL}/api/e/event/"
    URL_EVENT_CATEGORY = f"{API_BASE_URL}/api/e/category/"
    URL_EVENT_SUB_CATEGORY = f"{API_BASE_URL}/api/e/sub-category/"

    @staticmethod
    def URL_EVENT_DETAILS(uuid):
        return f"{API_BASE_URL}/api/e/event/{uuid}/"

    @staticmethod
    def URL_EVENT_PUBLISH_TOGGLE(uuid):
        return f"{API_BASE_URL}/api/e/event/{uuid}/publish-toggle/"

    @staticmethod
    def URL_EVENT_CATEGORY_DETAILS(uuid):
        return f"{API_BASE_URL}/api/e/category/{uuid}/"

    @staticmethod
    def URL_EVENT_SUB_CATEGORY_DETAILS(uuid):
        return f"{API_BASE_URL}/api/e/sub-category/{uuid}/"

    """ Event END """

    """ Donation START """
    URL_DONATIONS = f"{API_BASE_URL}/api/d/donation/"
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
    URL_POST = f"{API_BASE_URL}/api/p/post/"
    URL_POST_CATEGORY = f"{API_BASE_URL}/api/p/category/"

    @staticmethod
    def URL_POST_DETAILS(uuid):
        return f"{API_BASE_URL}/api/p/post/{uuid}/"

    @staticmethod
    def URL_POST_CATEGORY_DETAILS(uuid):
        return f"{API_BASE_URL}/api/p/category/{uuid}/"

    @staticmethod
    def URL_POST_PUBLISH_TOGGLE(uuid):
        return f"{API_BASE_URL}/api/p/post/{uuid}/publish-toggle/"

    # @staticmethod
    # def URL_POST():
    #     return f"{API_BASE_URL}/api/p/post/"

    """ Post END """

    """ Home Page START """
    URL_HOME_BANNERS = f"{API_BASE_URL}/api/h/home-banner/"
    URL_HOME_BANNER_REORDER = f"{API_BASE_URL}/api/h/home-banner/update-order/"

    """ Home Page END """

    """ Notice START """
    URL_NOTICES = f"{API_BASE_URL}/api/n/notice/"

    @staticmethod
    def URL_NOICE_DETAILS(uuid):
        return f"{API_BASE_URL}/api/n/notice/{uuid}/"

    @staticmethod
    def URL_NOICE_PUBLISH_TOGGLE(uuid):
        return f"{API_BASE_URL}/api/n/notice/{uuid}/publish-toggle/"

    """ Notice END """

    """ Single Page Start """
    URL_SINGLE_PAGES = f"{API_BASE_URL}/api/s/single-page/"

    @staticmethod
    def URL_SINGLE_PAGE_DETAILS(uuid):
        return f"{API_BASE_URL}/api/s/single-page/{uuid}/"

    """ Single Page END """
