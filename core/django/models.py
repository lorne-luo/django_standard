from django.db import models
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField


class ArchiveModelManager(models.Manager):
    def active(self):
        return super().all().filter(is_archived=False).order_by('-created_at')


class BaseModel(models.Model):
    # common fields
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True, editable=False)
    is_archived = models.BooleanField(blank=True, default=False)

    objects = ArchiveModelManager()

    class Meta:
        abstract = True


class NameSlugModel(models.Model):
    slug = AutoSlugField(populate_from='name', blank=True)

    class Meta:
        abstract = True

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = slugify(self.name)
        super(NameSlugModel, self).save(force_insert, force_update, using, update_fields)
