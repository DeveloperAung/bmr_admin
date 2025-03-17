from django.shortcuts import render


def event_category_list(request):
    return render(request, '')


def event_sub_category_list(request):
    return render(request, '')


def post_category(request):
    return render(request, '')


def dhamma_class_list(request):  # event
    return render(request, 'events/list.html')


def dhamma_class_create(request):   # event create
    return render(request, 'events/single_page_edit.html')
