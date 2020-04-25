from django.http import HttpResponse


def home_auth(request):
    return HttpResponse("Hello, world. You're at the authapp home_auth")
