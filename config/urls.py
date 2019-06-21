from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    # Site map
    url(r'^BingSiteAuth\.xml$', TemplateView.as_view(template_name='./BingSiteAuth.xml',  # File in template folder
                                                     content_type='text/xml; charset=utf-8')),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)