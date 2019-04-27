from django.conf import settings
from datetime import datetime
from django.http import HttpResponse

"""
def shortcircuitmiddleware(f):
    def _shortcircuitmiddleware(*args, **kwargs):
        return f(*args, **kwargs)

    return _shortcircuitmiddleware
"""

class ShortCircuitMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
        
    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.__name__ in ['token_signin_view', 'token_logout_view']:
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
        
        else:
            response = HttpResponse("outside the specified period", status=400)
            return response