from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('home/', TemplateView.as_view(template_name='home.html'), name='home'),
    path('useradmin/', include('Useradmin.urls')),
    path('useradmin/', include('django.contrib.auth.urls')),
    path('plants/', include('Plants.urls')),
    path('customerservice/', include('Customerservice.urls')),
    path('shoppingcart/', include('Shoppingcart.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
