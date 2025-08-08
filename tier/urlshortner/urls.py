from django.urls import path
from urlshortner.views import *


urlpatterns = [
    path('visits/', VisitedURLCount.as_view(), name='url_count'),
    path('shorten-url/', ShortURL.as_view(), name='shorten_url'),
    path('articles/publish/', PublishArticleView.as_view(), name='publish_article'),
    path('<str:url>/', VisitURL.as_view(), name='visit_url'),

]
