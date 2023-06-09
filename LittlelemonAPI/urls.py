from django.urls import path
from . import views

#this is to automatically generate the users authentication token
from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    path('secret/',views.secret),
    #we can visit this endpoint in insomnia, we can only send post request
    #we can generate the authtoken using the username and password as a form url encoded post message
    path('api-token-auth/', obtain_auth_token),
    path('manager-view', views.manager_view),
    path('throttle-check',views.throttle_check),
    path('throttle-check-auth',views.throttle_check_auth)
]
