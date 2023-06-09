#here we implement a class based throttle for our apps
from rest_framework.throttling import UserRateThrottle

class TenCallsPerMinute(UserRateThrottle):
  scope ='ten'