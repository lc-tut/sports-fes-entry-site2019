from django.conf import settings
from datetime import datetime
from django.http import HttpResponse


class ShortCircuitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        if (
            view_func.__name__ in ['token_signin_view', 'token_logout_view', 'is_registerable'] or
            '/admin/' in request.path or
            '/django-rq/' in request.path
        ):
            return view_func(request, *view_args, **view_kwargs)
    
        return None        

class EntryDateMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        
        now = datetime.now()

        if settings.ENTRY_START_DATE < now < settings.ENTRY_DEADLINE_DATE:
            return None

        elif now > settings.ENTRY_DEADLINE_DATE and request.method == 'GET':
            return None
        
        elif (
            view_func.__name__ in ['token_signin_view', 'token_logout_view', 'is_registerable'] or
            '/admin/' in request.path or
            '/django-rq/' in request.path
        ):
            return None
        else:
            response = HttpResponse("outside the specified period", status=400)
            return response