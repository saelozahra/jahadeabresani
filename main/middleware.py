from django.shortcuts import HttpResponseRedirect


# from django.urls import reverse
# from django.shortcuts import redirect

class AuthRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (not request.user.is_authenticated) and (not str(request.path).startswith("/modiriat")):
            print("MiddleWare Working")
            return HttpResponseRedirect('../../../../modiriat')
        response = self.get_response(request)
        return response
