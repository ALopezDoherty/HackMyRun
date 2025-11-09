from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    """Main index view - redirects to dashboard"""
    return render(request, 'dashboard.html')

@login_required
def dashboard(request):
    """Dashboard view"""
    return render(request, 'dashboard.html')