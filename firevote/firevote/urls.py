"""firevote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from polls import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login/adminlog/candidates/', views.candidates),
    path('login/adminlog/candidates/validate/', views.validate),
    path('login/adminlog/candidates/cdelete/', views.cdelete),
    path('login/adminlog/positions/', views.positions),
    path('login/adminlog/positions/enter/', views.addpos),
    path('login/adminlog/positions/pdelete/', views.pdelete),
    path('login/adminlog/image/', views.image),
    path('login/adminlog/image/getimage/', views.getimage),
    path('login/', views.login_register),
    path('save/', views.save),
    path('login/otp/', views.otp),
    path('login/voterlog/', views.v_login),
    path('login/voterlog/profile/', views.profile),
    path('login/adminlog/', views.a_login),
    path('login/voterlog/logout/', views.v_logout),
    path('login/adminlog/logout/', views.a_logout),
    path('login/voterlog/current/', views.current),
    path('login/voterlog/current/show/', views.show),
    path('login/voterlog/current/vote/', views.vote),
]
