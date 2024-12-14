from django.shortcuts import render,redirect
from django.contrib import messages
from .form import  CreateJobForm,UpdateJobForm
from .models import Job,Apply
from info.models import Info
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from lettergeneration.utils import generer_lettre_motivation
from django.contrib import messages
from info.form import  InfoForm
from job.form import CoverLetterForm


#view to create a new job
def create_job(request):
    if request.user.is_recruiter and request.user.has_company:
        if request.method == 'POST':
            form = CreateJobForm(request.POST)
            if form.is_valid():
                var = form.save(commit=False)
                if hasattr(request.user, 'staf'):
                    var.user = request.user
                    var.staf = request.user.staf
                    var.save()
                    messages.info(request, 'New job has been created')
                    return redirect('dashboard')
                else:
                    messages.warning(request, 'No staf associated with the user.')
                    return render(request, 'job/create_job.html', {'form': form})
            else:
                print("Form errors:", form.errors) 
                messages.warning(request, 'Something went wrong')
                return render(request, 'job/create_job.html', {'form': form})
        else:
            form = CreateJobForm()
            return render(request, 'job/create_job.html', {'form': form})
    else:
        messages.warning(request, 'Permission denied')
        return redirect('dashboard')


# view to update an exist job 
def update_job(request, pk):
    job=Job.objects.get(pk=pk)
    if request.method == 'POST':
        form = UpdateJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your job has been updated')
            return redirect('dashboard')
        else:
            print(form.errors)  
            messages.warning(request, 'Something went wrong. Please correct the errors below.')
            context = {'form': form}
            return render(request, 'job/update_job.html', context)
    else:
        form = UpdateJobForm(instance=job)
        context = {'form': form}
        return render(request, 'job/update_job.html', context)


#view for all job crated
def manage_jobs(request):
    jobs=Job.objects.filter(user=request.user, staf=request.user.staf)
    context={'jobs':jobs}
    return render(request, 'job/manage_jobs.html', context)

    
#view for apply to job
def apply_job(request, pk):
    if request.user.is_authenticated and request.user.is_applicant:
        job = get_object_or_404(Job, pk=pk)
        if Apply.objects.filter(user=request.user, job=job).exists():
            messages.warning(request, 'You have already applied for this job.')
            return redirect('dashboard')
        info_form = InfoForm(instance=request.user.info)  
        cover_letter_form = CoverLetterForm()
        if request.method == "POST":
            info_form = InfoForm(request.POST, request.FILES, instance=request.user.info)
            cover_letter_form = CoverLetterForm(request.POST)
            if info_form.is_valid():  
                info_form.save() 
                if "confirm_application" in request.POST and cover_letter_form.is_valid():
                    cover_letter = None
                    if cover_letter_form.cleaned_data.get("add_cover_letter") == "yes":
                        cover_letter = cover_letter_form.cleaned_data.get("cover_letter")
                    Apply.objects.create(
                        job=job,
                        user=request.user,
                        status="Pending",
                        cover_letter=cover_letter,
                    )
                    messages.success(request, "You have successfully applied for this job.")
                    return redirect("dashboard")

                
                messages.success(request, "Your information has been updated. You can now apply for the job.")
                return redirect('apply-job', pk=job.pk)

        return render(
            request,
            "job/apply_job.html",
            {"job": job, "info_form": info_form, "cover_letter_form": cover_letter_form},
        )

    else:
        messages.warning(request, "Please log in to apply for jobs.")
        return redirect("login")


#view for all  details  job   applicant apply
def  applied_details(request):
    jobs = Apply.objects.filter(user=request.user)
    context={'jobs':jobs}
    return render(request,'job/applied_details.html',context)
    

#view for all applicant apply
def all_applicants(request, pk):
    job = get_object_or_404(Job, pk=pk)
    applicants = Apply.objects.filter(job=job)
    print(applicants)  
    context = {'job': job, 'applicants': applicants}
    return render(request, 'job/all_applicants.html', context)



#view for status (rejected, accepted,pending)
def update_application_status(request, application_id, status):
    if status not in ['Retained', 'Rejected']:
        messages.error(request, "Statut invalide.")
        return redirect('manage-jobs')
    application = get_object_or_404(Apply, pk=application_id)
    application.status = status
    application.save()
    messages.success(request, f"Le statut de la candidature de {application.user.username} a été mis à jour : {status}.")
    return redirect('manage-jobs')

#view for the correspondence cv to all applicant
def ranked_candidates_view(request, pk):
    job = Job.objects.get(pk=pk)
    applicants = Apply.objects.filter(job=job)  
    ranked_applicants = []
    for apply in applicants:
        candidate = apply.user  
        candidate_info = Info.objects.get(user=candidate) 
        candidate_skills = set(candidate_info.skills.lower().split(', ')) if candidate_info.skills else set()
        job_skills = set(job.skills_required.lower().split(', ')) if job.skills_required else set()
        score = len(candidate_skills.intersection(job_skills))

        ranked_applicants.append({
            'candidate': candidate_info,
            'score': score,
        })

    ranked_applicants = sorted(ranked_applicants, key=lambda x: x['score'], reverse=True)

    context = {
        'job': job,
        'ranked_applicants': ranked_applicants,
    }
    return render(request, 'job/ranked_candidates.html', context)
