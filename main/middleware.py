from django.shortcuts import redirect
from django.urls import reverse

class RestrictFrontendForAuthenticatedUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        
        if request.user.is_authenticated:
            
           
            public_urls = [
                reverse('home'),
            ]
            
            if request.path in public_urls:
                return redirect('login')  

        response = self.get_response(request)
        return response