from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from django.shortcuts import get_object_or_404
from .models import Job
from info.models import Info

#utils to calculate score 
def calculate_candidate_score(info, job):
    score = 0
    if info.skills and job.skills_required:
        candidate_skills = set(info.skills.lower().split(', '))
        job_skills = set(job.skills_required.lower().split(', '))
        matching_skills = candidate_skills.intersection(job_skills)
        score += len(matching_skills) * 10  
    if info.location and job.location and info.location.lower() == job.location.lower():
        score += 5

    return score


#utils for correspondence candidate to the job
def get_ranked_candidates(job_id):
    job = get_object_or_404(Job, pk=job_id)
    candidates = Info.objects.all()

    scored_candidates = []
    for candidate in candidates:
        score = calculate_candidate_score(candidate, job)
        scored_candidates.append({
            'candidate': candidate,
            'score': score
        })

    return sorted(scored_candidates, key=lambda x: x['score'], reverse=True)

