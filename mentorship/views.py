from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MentorProfile

def mentors_view(request):
    mentors = MentorProfile.objects.select_related("user").all()
    return render(request, "mentors.html", {
        "mentors": mentors
    })

@login_required
def register_mentor(request):
    # Check if user already has a mentor profile
    if MentorProfile.objects.filter(user=request.user).exists():
        messages.info(request, 'You are already registered as a mentor.')
        return redirect('/mentors/')
    
    if request.method == 'POST':
        field = request.POST.get('field', '')
        expertise = request.POST.get('expertise', '')
        bio = request.POST.get('bio', '')
        
        if field and expertise:
            MentorProfile.objects.create(
                user=request.user,
                field=field,
                expertise=expertise,
                bio=bio
            )
            messages.success(request, 'You have successfully registered as a mentor!')
            return redirect('/mentors/')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'register_mentor.html')
