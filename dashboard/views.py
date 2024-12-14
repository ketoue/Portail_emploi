from django.shortcuts import render, redirect
from info.models import Info
from job.models import Job
import openai



def dashboard(request):
    return render(request, 'dashboard/dashboard.html')


#The view for find applicant, who have skills for the job
def recruiter_cvs(request):
    if request.user.is_recruiter:
        cvs = Info.objects.exclude(upload_cv="") 
        search_query = request.GET.get('search', '')
        if search_query:
            cvs = cvs.filter(skills__icontains=search_query)
        ranked_cvs = sorted(cvs, key=lambda cv: cv.skills or "", reverse=True)

        return render(request, 'dashboard/recruiter_cvs.html', {'cvs': ranked_cvs})
    else:
        return redirect('login')


