from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


@login_required
def profile(request):
    return render(request, 'registration/profile.html')


def avatar(request):
    if request.FILES:
        pass
    return redirect('profile')
