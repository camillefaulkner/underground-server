"""underground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from undergroundapi.views import register_user, login_user, EventView, CategoryView, ArtistView, SelectionView, UserView, EvtArtistView, VenueView
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'events', EventView, 'event')
router.register(r'categories', CategoryView, 'category')
router.register(r'artists', ArtistView, 'artist')
router.register(r'venues', VenueView, 'venue')
router.register(r'users', UserView, 'user')
router.register(r'chosenshows', SelectionView, 'chosenshow')
router.register(r'evtartist', EvtArtistView, 'evtartist')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
