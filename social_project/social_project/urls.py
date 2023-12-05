
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/',include('social_app.urls_1')), # class based
    #path('',include('social_app.urls')), # function based
]
