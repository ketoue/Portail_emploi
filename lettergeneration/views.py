from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .forms import ResumeForm
from .utils import extraire_donnees, generer_lettre_motivation
from job.models import Job 
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from django.http import FileResponse

#view for generate cover leter
def upload_resume(request, job_id):
    job = get_object_or_404(Job, pk=job_id)  
    if request.method == 'POST':
        form = ResumeForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save()
            contenu_cv = extraire_donnees(resume.file.path)
            job_info = (
                f"Exigences du poste : {job.requirements}\n"
                f"Description du poste : {job.ideal_candidate}"
            )
            donnees_combinees = f"{contenu_cv}\n\n{job_info}"
            lettre_motivation = generer_lettre_motivation(donnees_combinees)
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []
            title = Paragraph(f"<b>Lettre de Motivation pour le poste : {job.title}</b>", styles['Title'])
            elements.append(title)
            elements.append(Spacer(1, 20))
            sections = lettre_motivation.splitlines()
            for section in sections:
                paragraph = Paragraph(section, styles['BodyText'])
                elements.append(paragraph)
                elements.append(Spacer(1, 12)) 
            elements.append(PageBreak())
            doc.build(elements)
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename="lettre_motivation.pdf")

    else:
        form = ResumeForm()

    return render(request, 'letter/upload_resume.html', {'form': form, 'job': job})




