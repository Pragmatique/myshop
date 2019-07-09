
from datetime import datetime, timedelta, timezone
from django.conf import settings
from django.contrib import auth
from django.shortcuts import redirect
from authproj.models import User
import time
from tzlocal import get_localzone
from django.contrib.sessions.models import Session

from django.conf import settings

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


SESSION_TIMEOUT_KEY = "_session_init_timestamp_"

class AutoLogout(MiddlewareMixin):

    def process_request(self, request):
        if not hasattr(request, "session") or request.session.is_empty():
            return

        if request.user.is_authenticated:

            # print(request.user.id)
            init_time = User.objects.get(id=request.user.id).last_login
            # #init_time = request.session.setdefault('SESSION_TIMEOUT_KEY', time.time())
            # print(User.objects.get(id=request.user.id).last_login)
            # print(datetime.now(timezone.utc))
            # print((datetime.now(timezone.utc) - init_time).total_seconds())

            expire_seconds = getattr(
                settings, "SESSION_EXPIRE_SECONDS", settings.SESSION_COOKIE_AGE
            )

            session_is_expired = (datetime.now(timezone.utc) - init_time).total_seconds() > expire_seconds
            #session_is_expired = (datetime.now(timezone.utc) - init_time.replace(tzinfo=None)).total_seconds()  > expire_seconds

            if session_is_expired:
                request.session.flush()
                return redirect('authproj:signing_out')

            expire_since_last_activity = getattr(
                settings, "SESSION_EXPIRE_AFTER_LAST_ACTIVITY", True
            )
            grace_period = getattr(
                settings, "SESSION_EXPIRE_AFTER_LAST_ACTIVITY_GRACE_PERIOD", 1*60
            )



            if expire_since_last_activity and (datetime.now(timezone.utc) - init_time).total_seconds() > grace_period:
                request.session.flush()

            user=User.objects.get(id=request.user.id)
            user.last_login=datetime.now(timezone.utc)
            user.save()

        #request.session.set_expiry(1*60)
        #Session.objects.__setattr__('SESSION_TIMEOUT_KEY', time.time())


        #del request.session['SESSION_TIMEOUT_KEY']
        #session = request.session
        #self.add_to_session(request,'SESSION_TIMEOUT_KEY', time.time())
        #request.session.set('SESSION_TIMEOUT_KEY', time.time())
        #request.session.setdefault('SESSION_TIMEOUT_KEY', time.time())
        #request.session['SESSION_TIMEOUT_KEY'] = time.time()


    # def __init__(self, get_response):
    #     self.get_response = get_response
    #
    # # def __call__(self, request):
    # #     return self.get_response(request)
    #
    # def process_request(self, request):
    #
    #     try:
    #         print(request.session['last_touch'])
    #     except KeyError:
    #         print('No last touch jet')
    #
    #     if request.user.is_authenticated :
    #
    #         try:
    #             print(request.session['last_touch'])
    #             if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
    #                 pass
    #                 #auth.logout(request)
    #                 #del request.session['last_touch']
    #                 #return redirect('authproj:signing_out')
    #         except KeyError:
    #             pass
    #
    #     request.session['last_touch'] = datetime.now()
    #
    # def process_response(self, request, response):
    #     """Let's handle old-style response processing here, as usual."""
    #     # Do something with response, possibly using request.
    #     return response
    #
    # def __call__(self, request):
    #     """Handle new-style middleware here."""
    #     response = self.process_request(request)
    #     if response is None:
    #         # If process_request returned None, we must call the next middleware or
    #         # the view. Note that here, we are sure that self.get_response is not
    #         # None because this method is executed only in new-style middlewares.
    #         response = self.get_response(request)
    #
    #     response = self.process_response(request, response)
    #     return response
