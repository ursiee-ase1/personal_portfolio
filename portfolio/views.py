from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Service, Project, Skill, Testimonial, Education, Certification
from .forms import ContactForm

def home(request):
    """Home page view"""
    profile = Profile.objects.first()
    services = Service.objects.all()[:3]
    featured_projects = Project.objects.filter(featured=True)[:3]
    testimonials = Testimonial.objects.all()[:3]
    
    context = {
        'profile': profile,
        'services': services,
        'featured_projects': featured_projects,
        'testimonials': testimonials,
    }
    return render(request, 'home.html', context)

def about(request):
    """About page view"""
    profile = Profile.objects.first()
    skills = Skill.objects.all()
    educations = Education.objects.all().order_by('-start_date')
    certifications = Certification.objects.all().order_by('-issue_date')
    projects = Project.objects.all()
    testimonials = Testimonial.objects.all()
    
    context = {
        'profile': profile,
        'skills': skills,
        'educations': educations,
        'certifications': certifications,
        'projects': projects,
        'testimonials': testimonials,
    }
    return render(request, 'about.html', context)

def services(request):
    """Services page view"""
    profile = Profile.objects.first()
    services = Service.objects.all()
    
    context = {
        'profile': profile,
        'services': services,
    }
    return render(request, 'services.html', context)

def projects(request):
    """Projects page view"""
    profile = Profile.objects.first()
    projects = Project.objects.all()
    
    context = {
        'profile': profile,
        'projects': projects,
    }
    return render(request, 'projects.html', context)

def contact(request):
    """Contact page view with form handling"""
    profile = Profile.objects.first()
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    context = {
        'profile': profile,
        'form': form,
    }
    return render(request, 'contact.html', context)