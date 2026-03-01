from yenilikler.models import Yenilikler
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from portfolio.models import Category, Project
from haqqimizda.models import FAQ,Partnyorlar, Hashtag
from xidmetler.models import Xidmetler, KorporativXidmetler
from yenilikler.models import *
from .models import Subscriber

# Create your views here.

def home(request):

    project_categories = Category.objects.all()
    projects = Project.objects.all()[:5]
    faq = FAQ.objects.all()
    xidmetler = Xidmetler.objects.all()
    partnyorlar = Partnyorlar.objects.all()
    hashtaglar = Hashtag.objects.all()
    yenilikler = Yenilikler.objects.all()[:3]

    kxidmetler = KorporativXidmetler.objects.all()
    context = {
        "kxidmetler": kxidmetler,
        "project_categories": project_categories,
        "projects": projects,
        "faq": faq,
        "xidmetler": xidmetler,
        "partnyorlar": partnyorlar,
        "hashtaglar": hashtaglar,
        "yenilikler": yenilikler
    }
    return render(request, "new/index.html", context)


@require_POST
def subscribe(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Zəhmət olmasa email ünvanınızı daxil edin.'
            })
        
        # Check if email already exists
        if Subscriber.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'Bu email ünvanı artıq abunə olub.'
            })
        
        # Create new subscriber
        Subscriber.objects.create(email=email)
        
        return JsonResponse({
            'success': True,
            'message': 'Abunəliyiniz uğurla qeydə alındı!'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'Xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'Xəta baş verdi. Zəhmət olmasa yenidən cəhd edin.'
        })