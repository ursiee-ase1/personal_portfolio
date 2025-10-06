"""
Context processors for Portfolio
"""

from .models import SocialMediaLink, CompanyInfo

def social_media_links(request):
    """
    Add social media links to template context
    """
    return {
        'social_media_links': SocialMediaLink.objects.filter(is_active=True).order_by('display_order'),
    }

def company_info(request):
    """
    Add company information to template context
    """
    try:
        company_info = CompanyInfo.objects.first()
        if not company_info:
            # Create default company info if none exists
            company_info = CompanyInfo.objects.create()
    except CompanyInfo.DoesNotExist:
        company_info = CompanyInfo.objects.create()
    
    return {
        'company_info': company_info,
    }
