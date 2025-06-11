from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from api.subscribers.models import SubscriberUser
from frontend.adminUsers.views import check_auth_request
from frontend.config.api_endpoints import APIEndpoints


def subscriber_list(request):
    try:
        page = request.GET.get("page", 1)
        search = request.GET.get("q", "")

        params = {"page": page}
        if search:
            params["search"] = search

        response = check_auth_request("GET", APIEndpoints.URL_SUBSCRIBERS, request, params=params)
        if response.status_code == 401 or response.status_code == 400:  # Unauthorized
            return redirect("login")
        response_body = response.json()
        context = {
            'messages': response_body["message"],
            'data_header': response_body["data"],
            'data_results': response_body["data"]["results"],
            "request": request,
            "query": search,
        }
        return render(request, "subscribers/list.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "subscribers/list.html", {"error": str(e), "request": request, })


def subscribers_bulk_create(request):
    try:
        if request.method == "POST":
            email_list = request.POST.getlist('subscriber_email[]')
            email_list = [email.strip() for email in email_list if email.strip()]  # clean whitespace, remove empty

            # Get already existing emails
            existing_emails = set(
                SubscriberUser.objects.filter(email__in=email_list).values_list('email', flat=True)
            )

            # Filter out emails that already exist
            new_emails = [email for email in email_list if email not in existing_emails]

            if not new_emails:
                messages.warning(request, "All entered emails already exist.")
                return redirect('subscriber_create')

            # Prepare Subscriber instances
            new_subscribers = [SubscriberUser(email=email) for email in new_emails]

            # Bulk create
            SubscriberUser.objects.bulk_create(new_subscribers)

            messages.success(request, f"{len(new_subscribers)} new subscriber(s) added.")
            return redirect('subscriber_list')
        else:
            context = {

            }
        return render(request, "subscribers/create.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "subscribers/create.html", {"error": str(e)})


def single_page_soft_delete(request, uuid):
    if request.method == "DELETE":
        response = check_auth_request("DELETE", APIEndpoints.URL_SINGLE_PAGE_DETAILS(uuid), request)
        if response.status_code == 401 or response.status_code == 400:
            return redirect("login")

        if response.status_code == 200:
            return JsonResponse({"success": True, "message": "Subscriber deleted successfully."})
        else:
            return JsonResponse(
                {"success": False, "message": f"Failed to delete Subscriber {response.status_code}."}, status=400
            )
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


