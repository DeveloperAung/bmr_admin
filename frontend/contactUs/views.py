from django.shortcuts import render


def contact_us_list(request):

    return render(request, 'contactUs/list.html')


def contact_us_edit(request):
    return render(request, 'contactUs/edit.html')
