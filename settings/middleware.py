from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils import timezone
from django.conf import settings as django_settings


class SessionIdleTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            timeout_seconds = getattr(django_settings, 'SESSION_IDLE_TIMEOUT', 900)  # default 15 mins

            if last_activity:
                elapsed = (timezone.now() - timezone.datetime.fromisoformat(last_activity)).total_seconds()
                if elapsed > timeout_seconds:
                    logout(request)
                    return redirect('login')

            # sura hahu husi tempu ikus interasaun
            request.session['last_activity'] = timezone.now().isoformat()

        return self.get_response(request)