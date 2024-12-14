from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Info
from users.models import User
from .form import UpdateInfoForm,InfoForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404




#view to update info(resume)
def update_info(request):
    if request.user.is_applicant:
        info = Info.objects.get(user=request.user)
        if request.method == 'POST':
            form = UpdateInfoForm(request.POST, request.FILES, instance=info)
            if form.is_valid():
                var = form.save(commit=False)
                user = User.objects.get(pk=request.user.id)
                user.has_resume = True
                user.save()
                var.save()
                messages.info(request, 'Your info has been updated')
                return redirect('dashboard')
            else:
                messages.warning(request, 'Something went wrong')
        else:
            form = UpdateInfoForm(instance=info)
        
        context = {'form': form}
        return render(request, 'info/update_info.html', context)
    else:
        messages.warning(request, 'Permission denied')
        return redirect('dashboard')

        

#view to detaifs of the applicant(info in his resume)
def info_details(request, pk):
    info = get_object_or_404(Info, pk=pk)
    context = {'info': info}
    return render(request, 'info/info_details.html', context)



#the view for update info(resume) before apply
@login_required
def edit_info(request, job_pk):  
    info, created = Info.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = InfoForm(request.POST, request.FILES, instance=info)
        if form.is_valid():
            form.save()
            messages.success(request, "Vos informations ont été mises à jour avec succès.")
            return redirect('apply-job', pk=job_pk)  
    else:
        form = InfoForm(instance=info)

    return render(request, 'info/edit_info.html', {'form': form})

