from django.shortcuts import render, get_object_or_404
from xidmetler.models import Xidmetler, KorporativXidmetler
from home.models import ServiceCategory
from haqqimizda.models import *


def xidmetler(request):
    categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('items')
    context = {
        "categories": categories,
    }
    return render(request, "new/services.html", context)


def kxidmetler(request):
    xidmetler_qs = Xidmetler.objects.all()
    kxidmetler_qs = KorporativXidmetler.objects.all()
    context = {
        "kxidmetler": kxidmetler_qs,
        "xidmetler": xidmetler_qs,
    }
    return render(request, "new/corservices.html", context)


def xidmetlerdetail(request, id):
    xidmet = Xidmetler.objects.get(pk=id)
    xidmetler_qs = Xidmetler.objects.all()
    kxidmetler_qs = KorporativXidmetler.objects.all()
    context = {
        "kxidmetler": kxidmetler_qs,
        "xidmetler": xidmetler_qs,
        "xidmet": xidmet,
    }
    return render(request, "new/service.html", context)


def category_detail(request, slug):
    category = get_object_or_404(ServiceCategory, slug=slug, is_active=True)
    all_categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('items')
    context = {
        "category": category,
        "all_categories": all_categories,
    }
    return render(request, "new/service_category.html", context)