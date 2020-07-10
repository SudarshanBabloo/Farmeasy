from django.urls import path,include,re_path
from . import views
#from django.contrib.auth import views as auth_views

app_name = "farmer"

urlpatterns = [
    path('',views.index,name='index'),
    path('profile/', views.edit,name='edit'),
    path('view_review/',views.viewreview,name='viewreview'),
    path('review/',views.reviewtext,name='review'),
    #path('logout/', views.logout ,name='logout'),
    #path('verify_email/', views.verify_email ,name='verify_email'),
    path('getrequests/',views.getrequests,name='requests'),
    path('inv/',views.invview,name='inv'),
    path('add/',views.add,name='add'),
    path('subtract/',views.subtract,name='subtract'),
    path('historydone/',views.history,name='historydone'),
    path('history/',views.currentview,name='history'),
    path('store/',views.store_home,name='store'),
    path('cat/<int:cid>/',views.cat_page,name='cat'),
    path('cat/<int:cid>/cost/',views.cat_page_by_price,name='cat_price'),
    path('cat/<int:cid>/rating/',views.cat_page_by_rating,name='cat_rating'),
    path('prod/<int:pid>/',views.prod_page,name='prod'),
    path('prod_review/<int:pid>/',views.prod_review,name='prod_review'),
    path('star/',views.star,name='star'),
]
