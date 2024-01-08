
from django.urls import path
from .views import RegisterView,UserLoginView,UserLogOutView,DepositView
urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',UserLoginView.as_view(),name='user_login'),
    path('logout/',UserLogOutView.as_view(),name='user_logout'),
    path('deposit/',DepositView.as_view(),name='deposit'),
]
