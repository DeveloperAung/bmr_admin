from django.shortcuts import render



def single_page_list(request):
    return render(request, 'singlePages/pages/single_page_list.html')


def single_page_edit(request):
    return render(request, 'singlePages/pages/single_page_edit.html')
