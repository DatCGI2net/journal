from django.conf.urls import url
from app.views import APIUserView, APIAuthView, APIBalanceView
from app.views import APIEntryView, APIProfileView
from app.views import APIDashboarView


urlpatterns = [
	url(r'^user/profile/',APIProfileView.as_view()),
	url(r'^user/',APIAuthView.as_view()),
	#url(r'^user/logout$',APIAuthView.as_view()),
	url(r'^signup/',APIUserView.as_view()),
	#url(r'^signup/verify$',APIUserView.as_view()),
	
	
	url(r'^entry/',APIEntryView.as_view()),
	url('^dashboard/', APIDashboarView.as_view()),
	url(r'^balance/',APIBalanceView.as_view()),
]