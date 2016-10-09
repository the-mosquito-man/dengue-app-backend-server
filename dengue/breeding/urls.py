from django.conf.urls import url
from breeding import views

urlpatterns = [
    url(r'^$', views.SourceCollection.as_view()),
]
