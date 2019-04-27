from django.conf.urls import url
from django.contrib.auth import views as auth_views
from basic_app import views
from django.urls import path

from basic_app.views import Graph
from django.views.generic import TemplateView



app_name = 'basic_app'
urlpatterns = [

    url(r'^register/$',views.register,name='register'),
    url(r"logout/$", auth_views.LogoutView.as_view(), name="logout"),
    url(r'^user_login/$',views.user_login,name='user_login'),
    url(r'^manage_review/$',views.manage_review,name='manage_review'),
    url(r'^delete_review/$',views.delete_review,name='delete_review'),
    url(r'^edit_review/$',views.edit_review,name='edit_review'),
    url(r'^add_review/$',views.add_review,name='add_review'),
    url(r'^review/$',views.review,name='review'),
    url(r'^search_company/$',views.search_company,name='search_company'),
    url(r'^search/$',views.search,name='search'),
    url(r'^add_helpful/$',views.add_helpful,name='add_helpful'),
    url(r'^software_engineer/$',views.software_engineer,name='software_engineer'),
    url(r'^intern/$',views.intern,name='intern'),
    url(r'^web/$',views.web,name='web'),
    url(r'^data/$',views.data,name='data'),
    url(r'^cloud/$',views.cloud,name='cloud'),
    url(r'^network/$',views.network,name='network'),
    url(r'^hardware/$',views.hardware,name='hardware'),
    url(r'^polls_list$',views.polls_list,name='polls_list'),
    path('details/<int:poll_id>/', views.poll_detail, name='poll_detail'),
    path('details/<int:poll_id>/vote/', views.poll_vote, name='poll_vote'),
    path('add/', views.add_poll, name='add_poll'),
    path('graph/', views.uProp,name='graph'),
    path('graphA/', Graph.as_view(), name='graphA'),









]
