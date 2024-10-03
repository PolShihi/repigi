import zoneinfo
from django.http import HttpRequest
from django.utils import timezone
from pharmacy_app.models import Client, Employee
from pharmacy_app.usefuls import is_in_groups
import logging

logger = logging.getLogger(__name__)

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.user.is_authenticated:
            tzname = request.session.get("django_timezone")
            if is_in_groups('Client')(request.user):
                tzname = Client.objects.get(user_id=request.user.id).timezone_info
                
            if is_in_groups('Employee')(request.user):
                tzname = Employee.objects.get(user_id=request.user.id).timezone_info
            
            request.session["django_timezone"] = tzname
                
        tzname = request.session.get("django_timezone")
        
        if tzname:
            logger.warning(f'{tzname} time zone is activated')
            timezone.activate(zoneinfo.ZoneInfo(tzname))
        else:
            logger.warning('Time zone set to default')
            timezone.deactivate()
            
        return self.get_response(request)