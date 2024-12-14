import django_filters
from job.models import Job

#filter for filte job by title end location
class JobFilter(django_filters.FilterSet):
    title=django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model=Job
        fields=['title','location']