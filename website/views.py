from django.shortcuts import render
from job.models import Job,Apply
from .filter import JobFilter

#home page with 3 job and if seaching you can see another job
def home(request):
    filter = JobFilter(request.GET, queryset=Job.objects.filter(is_available=True).order_by('-timestamp'))
    is_searching = any(param for param in request.GET.values())
    jobs = Job.objects.filter(is_available=True).order_by('-timestamp')[:3]
    context = {
        'filter': filter,
        'jobs': jobs,
        'is_searching': is_searching, 
    }
    return render(request, 'website/home.html', context)

#view for all job
def Job_list(request):
    jobs=Job.objects.filter(is_available=True).order_by('-timestamp')
    context={'jobs':jobs}
    return render(request,'website/job_list.html',context)

#view for all details to job
def job_details(request,pk):
    job= Job.objects.get(pk=pk)
    
    if request.user.is_authenticated:
        has_applied = Apply.objects.filter(user=request.user, job=job).exists()
    else:
        has_applied = False
  
    context={'job':job, 'has_applied':has_applied}
    return render(request,'website/job_details.html', context)