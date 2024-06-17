from django.http import HttpResponse

def information_about_api(request):
    #todo: json
    return HttpResponse('version: 0.0.1')