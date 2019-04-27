from django.conf.urls import url
from . import views

app_name = 'basic_app'

urlpatterns = [
    url('reviews/$',
         views.ReviewListView.as_view(),
         name='review_list'),

    url('reviews/(?P<pk>\d+)/$',
         views.ReviewDetailView.as_view(),
         name='review_detail'),
]
