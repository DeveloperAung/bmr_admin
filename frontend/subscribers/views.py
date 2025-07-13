from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

from api.subscribers.models import SubscriberUser
from frontend.adminUsers.views import check_auth_request
from frontend.config.api_endpoints import APIEndpoints
from django.conf import settings
import json


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

            if not email_list:
                return render(request, "subscribers/create.html", {
                    'warning_message': "Please enter at least one email address."
                })

            # Prepare data for API
            data = {
                'emails': email_list
            }
            
            # Call API to create subscribers
            response = check_auth_request("POST", f"{APIEndpoints.URL_SUBSCRIBERS}bulk-create/", request, data=data)
            
            if response.status_code == 401 or response.status_code == 400:
                return redirect("login")
            
            response_body = response.json()
            
            if response_body.get("success"):
                messages.success(request, response_body.get("message", "Subscribers created successfully."))
                return redirect('subscribers:list')
            else:
                # Handle errors
                error_message = response_body.get("message", "Failed to create subscribers")
                if response_body.get("errors"):
                    error_message += ": " + ", ".join(response_body.get("errors", {}).values())
                
                return render(request, "subscribers/create.html", {
                    'error_message': error_message,
                    'submitted_emails': email_list
                })
        else:
            context = {}
            return render(request, "subscribers/create.html", context)
    except Exception as e:
        print('error', e)
        return render(request, "subscribers/create.html", {"error_message": str(e)})


def subscriber_edit(request, uuid):    
    try:
        if request.method == "GET":
            print('subscriber_get', uuid)
            # Get subscriber details
            response = check_auth_request("GET", APIEndpoints.URL_SUBSCRIBERS_DETAILS(uuid), request)
            if response.status_code == 401 or response.status_code == 400:
                return redirect("login")
            print('response', response)
            response_body = response.json()
            print('response_body', response_body)
            if response_body.get("success"):
                print('response_body success', response_body)
                context = {
                    'subscriber_uuid': uuid,
                    'subscriber_data': response_body.get("data"),
                    'request': request,
                    'API_BASE_URL': settings.API_BASE_URL
                }

                try:
                    return render(request, "subscribers/edit.html", context)
                except Exception as e:
                    print('template error', e)
                    return render(request, "subscribers/edit.html", {"error": str(e)})
            else:
                print('error response_body', response_body)
                messages.error(request, "Failed to load subscriber data")
                return redirect('subscribers:list')
        
        elif request.method == "POST":
            print('subscriber_post', uuid)
            # Update subscriber
            subscrd_flag = request.POST.get('subscrd_flag')
            
            data = {
                'subscrd_flag': subscrd_flag
            }
            
            response = check_auth_request("PATCH", APIEndpoints.URL_SUBSCRIBERS_DETAILS(uuid), request, data=data)
            if response.status_code == 401 or response.status_code == 400:
                return redirect("login")
            
            response_body = response.json()
            if response_body.get("success"):
                return redirect('subscribers:list')
            else:
                context = {
                    'subscriber_uuid': uuid,
                    'subscriber_data': response_body.get("data", {}),
                    'errors': response_body.get("errors", {}),
                    'message': response_body.get("message", "Failed to update subscriber")
                }
                return render(request, "subscribers/edit.html", context)
        
        else:
            return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)
            
    except Exception as e:
        print('error what', e)
        messages.error(request, f"Error: {str(e)}")
        return redirect('subscribers:list')


def subscriber_soft_delete(request, uuid):
    if request.method == "DELETE":
        response = check_auth_request("DELETE", APIEndpoints.URL_SUBSCRIBERS_DETAILS(uuid), request)
        if response.status_code == 401 or response.status_code == 400:
            return redirect("login")

        if response.status_code == 200:
            return JsonResponse({"success": True, "message": "Subscriber deleted successfully."})
        else:
            return JsonResponse(
                {"success": False, "message": f"Failed to delete Subscriber {response.status_code}."}, status=400
            )
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=405)


