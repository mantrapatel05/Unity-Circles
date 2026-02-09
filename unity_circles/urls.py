from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Redirect /accounts/login/ to /login/ (Django's default auth redirect)
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=False)),

    # API endpoints
    path('api/auth/', include('accounts.urls')),
    path('api/onboarding/', include('onboarding.urls')),
    path('api/mentorship/', include('mentorship.urls')),

    # App URLs
    path('chat/', include('chat.urls')),
    path('mentors/', include('mentorship.urls')),
    
    # Core URLs (includes login, dashboard, etc.) - MUST BE LAST before static
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
