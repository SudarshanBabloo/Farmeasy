from django.urls import path,include,re_path
from . import views
#from django.contrib.auth import views as auth_views

app_name = "vendor"

urlpatterns = [
    #path('profile/', views.edit,name='edit'),
    #path('logout/', views.logout ,name='logout'),
    #path('verify_email/', views.verify_email ,name='verify_email'),
    path('',views.index,name='index'),
    path('add_new/',views.add_new,name='add_new'),
    path('add/<int:pid>',views.add,name='add'),
    #path('view_review/',views.viewreview,name='viewreview'),
    #path('getrequests/',views.getrequests,name='requests'),
    path('subtract/<int:pid>',views.subtract,name='subtract'),
    path('inv/',views.prod_profile,name='inv'),
    path('history/',views.history,name='history'),
]
