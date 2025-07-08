from django.shortcuts import render

from frontend.adminUsers.views import check_auth_request


def membership_list(request):
    try:
        page = request.GET.get("page", 1)
        search = request.GET.get("q", "")

        params = {"page": page}
        if search:
            params["search"] = search
        params["category_id"] = 5

        # response = check_auth_request("GET", APIEndpoints.URL_POST, request, params=params)
        #
        # if response.status_code == 401 or response.status_code == 400:
        #     messages.warning(request, "Your session has expired! Please login again.")
        #     return redirect("login")
        #
        # response_body = response.json()
        # context = {
        #     'messages': response_body["message"],
        #     'data_header': response_body["data"],
        #     'data_results': response_body["data"]["results"],
        #     "request": request,
        #     "query": search,
        # }
        return render(request, "memberships/list.html")
    except Exception as e:
        print('error', e)
        return render(request, "memberships/list.html", {"error": str(e)})
