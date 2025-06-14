"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views.
For more information, see:
https://docs.djangoproject.com/en/5.2/topics/http/urls/

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
from django.urls import path, include

# Root URL configuration for the entire project
urlpatterns = [
    # Django admin interface
    path('admin/', admin.site.urls),

    # API route that includes all app-specific URLs
    path('api/', include([
        # Routes for user authentication and profile management
        path('', include('auth_app.api.urls')),

        # Routes for offer creation, listing and detail views
        path('', include('offers_app.api.urls')),

        # Routes for order handling and statistics
        path('', include('orders_app.api.urls')),

        # Routes for review system and public metrics
        path('', include('reviews_app.api.urls')),
    ])),
]
