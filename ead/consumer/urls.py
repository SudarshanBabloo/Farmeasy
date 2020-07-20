from django.urls import path,include,re_path
from . import views
#from django.contrib.auth import views as auth_views

app_name = "consumer"

urlpatterns = [
       path('review/',views.reviewtext,name='review'),
       path('search/', views.search, name="search"),
       path('farmer_page/<str:enc>/', views.farmer_page, name="farmer_page"),
]