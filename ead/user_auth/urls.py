from django.urls import path,include,re_path
from . import views

app_name = "user_auth"

urlpatterns = [
    path('signup/', views.signup ,name='signup'),
    path('login/', views.login ,name='login'),
    path('loggedinhome/', views.loggedinhome ,name='loggedinhome'),
    path('logout/', views.logout ,name='logout'),
    path('verify_email/', views.verify_email ,name='verify_email'),
    #path('email_verified/<email>/<hash>/', views.email_verified ,name='email_verified'),
    path('reset-password/', views.resetpasswordview ,name='reset_password'),
    #path('display-reset-password/', views.display_reset_password ,name='display_reset_password'),
    path('save-password/', views.save_password ,name='save_password'),
    re_path(r'^display_reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',views.display_reset_password, name='display_reset_password'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
]
