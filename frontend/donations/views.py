from django.shortcuts import render


def donation_list(request):
    return render(request, 'donations/list.html')


def donation_edit(request):
    return render(request, 'donations/create.html')
