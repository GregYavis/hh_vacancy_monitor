from django.db import models
from django.shortcuts import reverse


class Marker(models.Model):
    slug = models.SlugField()

    def __str__(self):
        return self.slug

    def get_marker_url(self):
        return reverse('monitor:vacancy-marker',
                       kwargs={'slug': self.slug})

    """def marker_objects_exists(self, marker):
        exists = Marker.objects.filter(slug=marker)
        print(exists)"""


# Create your models here.
class Vacancy(models.Model):
    vacancy_name = models.CharField(max_length=500)
    vacancy_link = models.CharField(max_length=500)
    marker = models.ForeignKey(Marker, on_delete=models.CASCADE)
    new_or_old = models.IntegerField(default=0)

    def __str__(self):
        return self.vacancy_link
