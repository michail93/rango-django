from django.conf.urls import include, url, patterns
from django.contrib import admin

from rango import urls as rango_urls
from django.conf import settings

urlpatterns = [
    # Examples:
    # url(r'^$', 'tango_with_django_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r"^rango/", include(rango_urls), name="rango"),
]

if settings.DEBUG:
    urlpatterns+=patterns(
    "django.views.static",
    (r"^media/(?P<path>.*)",
    "serve",
    {"document_root":settings.MEDIA_ROOT}),
    )
