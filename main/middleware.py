from django.shortcuts import HttpResponseRedirect
# from django.urls import reverse
# from django.shortcuts import redirect
# from django.contrib.auth.models import User, Group

class AuthRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (not request.user.is_authenticated) and (not str(request.path).startswith("/modiriat")):
            return HttpResponseRedirect('../../../../modiriat')
        response = self.get_response(request)
        return response

# class AuthRequiredMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         # One-time configuration and initialization.
#         print("init middle ware")
#
#     def __call__(self, *args, **kwargs):
#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#         print(User.is_authenticated.__str__())
#         print(User.is_authenticated)
#         print(User.is_authenticated.getter)
#         print(User.is_authenticated.fget)
#         if not User.is_authenticated:
#             return HttpResponseRedirect(reverse('admin'))
#         else:
#             print("login hast")
#
#         response = self.get_response(*args)
#
#         # Code to be executed for each request/response after
#         # the view is called.
#
#         return response

    # def process_request(self, request):
    #     print(request.user.is_authenticated)
    #     if not request.user.is_authenticated():
    #         return HttpResponseRedirect(reverse('admin'))
    #     return None
