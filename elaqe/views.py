from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.cache import cache
import json
import re

from haqqimizda.models import Partnyorlar, Hashtag
from xidmetler.models import Xidmetler, KorporativXidmetler
from .forms import ContactForm
from .models import Contact

def elaqe(request):
    xidmetler = Xidmetler.objects.all()
    partnyorlar = Partnyorlar.objects.all()
    hashtaglar = Hashtag.objects.all()
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mesajınız uğurla göndərildi!")
            return redirect('elaqe')  # Redirect to clear form fields and avoid resubmission issues

    kxidmetler = KorporativXidmetler.objects.all()
    context = {
        "kxidmetler": kxidmetler,
        "xidmetler": xidmetler,
        "hashtaglar": hashtaglar,
        "partnyorlar": partnyorlar,
        "form": form
    }
    return render(request, "new/contact.html", context)


@require_POST
def contact_submit(request):
    try:
        data = json.loads(request.body)
        
        # Get form data
        full_name = data.get('full_name', '').strip()
        email = data.get('email', '').strip().lower()
        phone = data.get('phone', '').strip()
        message = data.get('message', '').strip()
        honeypot = data.get('website', '')  # Honeypot field - should be empty
        
        # Spam protection: Check honeypot field (bots fill this)
        if honeypot:
            return JsonResponse({
                'success': False,
                'message': 'Spam aşkarlandı.'
            })
        
        # Rate limiting: Check if same IP submitted recently (within 60 seconds)
        client_ip = get_client_ip(request)
        cache_key = f'contact_form_{client_ip}'
        if cache.get(cache_key):
            return JsonResponse({
                'success': False,
                'message': 'Zəhmət olmasa bir az gözləyin və yenidən cəhd edin.'
            })
        
        # Validation
        if not full_name or len(full_name) < 2:
            return JsonResponse({
                'success': False,
                'message': 'Zəhmət olmasa adınızı düzgün daxil edin.'
            })
        
        if not email or not is_valid_email(email):
            return JsonResponse({
                'success': False,
                'message': 'Zəhmət olmasa düzgün email ünvanı daxil edin.'
            })
        
        if not message or len(message) < 10:
            return JsonResponse({
                'success': False,
                'message': 'Zəhmət olmasa mesajınızı daxil edin (minimum 10 simvol).'
            })
        
        # Spam protection: Check for suspicious content
        if contains_spam(full_name) or contains_spam(message):
            return JsonResponse({
                'success': False,
                'message': 'Mesajınız spam kimi qiymətləndirildi.'
            })
        
        # Check for too many links in message (spam indicator)
        link_count = len(re.findall(r'https?://', message))
        if link_count > 2:
            return JsonResponse({
                'success': False,
                'message': 'Mesajda çox sayda link var. Zəhmət olmasa linkləri azaldın.'
            })
        
        # Save the contact message
        Contact.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            message=message
        )
        
        # Set rate limit cache (60 seconds)
        cache.set(cache_key, True, 60)
        
        return JsonResponse({
            'success': True,
            'message': 'Mesajınız uğurla göndərildi! Tezliklə sizinlə əlaqə saxlayacağıq.'
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


def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def contains_spam(text):
    """Check if text contains common spam patterns"""
    spam_patterns = [
        r'viagra', r'cialis', r'casino', r'lottery', r'winner',
        r'click here', r'buy now', r'free money', r'make money fast',
        r'bitcoin', r'crypto', r'investment opportunity',
        r'\$\d+', r'SEO', r'backlink'
    ]
    text_lower = text.lower()
    for pattern in spam_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True
    return False
