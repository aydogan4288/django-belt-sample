from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^dash$', views.dash),
	url(r'^logout$', views.logout),
	url(r'^show/(?P<tripid>\d+)$', views.show),
	url(r'^create$', views.create),
	url(r'^new$', views.new),
	url(r'^join/(?P<tripid>\d+)$', views.join),
	url(r'^cancel/(?P<tripid>\d+)$', views.cancel),
	url(r'^delete/(?P<tripid>\d+)$', views.delete),



	# url(r'^new$', views.new),
	# url(r'^create$', views.create),
	# url(r'^clear$', views.clear),
	# url(r'^favorite/(?P<movieid>\d+)$', views.favorite),
	# url(r'^delete/(?P<movieid>\d+)$', views.delete),
	# url(r'^unfavorite/(?P<movieid>\d+)$', views.unfavorite),
	# url(r'^show/(?P<movieid>\d+)$', views.show),
]
