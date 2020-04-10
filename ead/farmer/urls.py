from django.urls import path,include,re_path
from . import views
#from django.contrib.auth import views as auth_views

app_name = "farmer"

urlpatterns = [
    path('profile/', views.edit,name='edit'),
    #path('logout/', views.logout ,name='logout'),
    #path('verify_email/', views.verify_email ,name='verify_email'),
    path('',views.index,name='index'),
    path('add/',views.add,name='add'),
    path('view_review/',views.viewreview,name='viewreview'),
    path('getrequests/',views.getrequests,name='requests'),
    path('subtract/',views.subtract,name='subtract'),
    path('inv/',views.invview,name='inv'),
    path('review/',views.reviewtext,name='review'),
    path('history/',views.history,name='history'),
]
