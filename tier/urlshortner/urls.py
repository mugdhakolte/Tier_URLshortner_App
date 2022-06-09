from django.urls import path
from urlshortner.views import *


urlpatterns = [
    path('visits/', VisitedURLCount.as_view(), name='url_count'),
    path('shorten-url/', ShortURL.as_view(), name='shorten_url'),
    path('<str:url>/', VisitURL.as_view(), name='visit_url'),

]
