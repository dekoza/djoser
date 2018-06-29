from django.conf.urls import url, include

import djoser.urls

urlpatterns = (
    url(r'^auth/', include(djoser.urls)),
)
