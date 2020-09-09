from django.db import models
from django.contrib.auth import get_user_model

from comma.helpers import generate_random_string
from django.utils.text import slugify

POST_STATUS = [('PU', 'publish'), ('DR', 'draft')]
ANONYMOUS_USER_ID = 1


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_datetime = models.DateTimeField()
    status = models.CharField(choices=POST_STATUS, max_length=2)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='posts',
                                   on_delete=models.SET_DEFAULT,
                                   default=ANONYMOUS_USER_ID)
    image = models.ImageField(upload_to='posts/images',
                              blank=True,
                              null=True)

    def __str__(self):
        return f'{self.id}: {self.title}'

    def save(self, *args, **kwargs):

        # check for slug
        if not self.slug:
            self.slug = slugify(self.title) + '_' + generate_random_string()
        else:
            self.slug = slugify(self.slug) + '_' + generate_random_string()

        # call default save method
        super().save(*args, **kwargs)
