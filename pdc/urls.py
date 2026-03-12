"""pdc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from haqqimizda import views as haqqimizda
from xidmetler import views as xidmetler
from portfolio import views as portfolio
from qalereya import views as qalereya
from yenilikler import views as yenilikler
from elaqe import views as elaqe
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('haqqimizda/', haqqimizda.haqqimizda, name='haqqimizda'),
    path('xidmetler/', xidmetler.xidmetler, name='xidmetler'),
    path('xidmetler/kateqoriya/<slug:slug>/', xidmetler.category_detail, name='category_detail'),
    path('korporativ-xidmetler/', xidmetler.kxidmetler, name='kxidmetler'),
    path('xidmetler/<int:id>', xidmetler.xidmetlerdetail, name='xidmetlerdetail'),
    path('xidmetler/sub/<int:id>', xidmetler.xidmetlerdetail, name='sub_category'),
    path('portfolio/', portfolio.portfolio, name='portfolio'),
    path('portfolio/<int:id>', portfolio.portfoliodetail, name='portfolio-detail'),
    path('qalereya/', qalereya.qalereya, name='qalereya'),
    path('yenilikler/', yenilikler.yenilikler, name='yenilikler'),
    path('yenilikler/<int:id>/', yenilikler.yeniliklerdetail, name='yeniliklerdetail'),
    path('elaqe/', elaqe.elaqe, name='elaqe'),
    path('elaqe/submit/', elaqe.contact_submit, name='contact_submit'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)