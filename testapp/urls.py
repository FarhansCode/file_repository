from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^repository\/(?P<filedir>(?:[\w\.]*\/?)*)$', views.repository, name='repository'),
# repository(?P<filedir>(?:\w*\/)*)
]
