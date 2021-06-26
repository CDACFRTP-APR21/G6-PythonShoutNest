from django.conf.urls import url
from django.urls import path
from . import views
from django.urls.resolvers import URLPattern
# from .views import LoginView,RegisterView
# from app.views import RegisterView
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt  
 
urlpatterns = [
    url(r'^login/$',views.LoginView.as_view(),name='login'),
    path('register/',views.RegisterView.as_view(),name='register'),
    url(r'^user/$', views.UserApi),
    url(r'^user/([0-9]+)$', views.UserApi),

    url(r'^SaveFile/$', views.SaveFile),

    url(r'^shouts/$', views.ShoutsApi),
    url(r'^shouts/([0-9]+)$', views.ShoutsApi),

    url(r'^friends/$', views.FriendsApi),
    url(r'^friends/([0-9]+)$', views.FriendsApi),
    
    url(r'^reports/$', views.ReportsApi),
    url(r'^reports/([0-9]+)$', views.ReportsApi),

    url(r'^friendshouts/([0-9]+)$',views.friendShoutsApi),
    
    url(r'^detailsoffriends/([0-9]+)$',views.DetailsOfFriendsApi),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
