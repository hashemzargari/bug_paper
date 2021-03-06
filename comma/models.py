from django.db import models
from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager

from comma.helpers import generate_random_string
from django.utils.text import slugify
from django.utils import timezone

POST_STATUS = [('PU', 'publish'), ('DR', 'draft')]
ANONYMOUS_USER_ID = 1


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, unique=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self',
                               related_name='children',
                               on_delete=models.SET_DEFAULT,
                               default=None,
                               blank=True,
                               null=True)
    cat_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_parents(self):
        parent = self.parent
        if parent is None:
            return None
        return {
            self.title: {
                'url': f'url_for_{self.slug}',
                'parent': parent.get_parents()
            }
        }

    def get_all_children(self):
        children = self.children.all()
        if children is None:
            return None
        return {
            self.title: {
                'url': f'url_for_{self.slug}',
                'children': [ch.get_all_children() for ch in children]
            }
        }

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.cat_url:
            # self.cat_url =
            pass

        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_datetime = models.DateTimeField(blank=True)
    status = models.CharField(choices=POST_STATUS, max_length=2, default='PU')
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(get_user_model(),
                                   related_name='posts',
                                   on_delete=models.SET_DEFAULT,
                                   default=ANONYMOUS_USER_ID)
    image = models.ImageField(upload_to='posts/images',
                              blank=True,
                              null=True)

    category = models.ForeignKey(Category,
                                 on_delete=models.SET_DEFAULT,
                                 default=None,
                                 blank=True,
                                 null=True)
    # TODO: clickable and serializers(rest) for tags
    tags = TaggableManager(blank=True)

    # TODO: count of likes, reads, ...

    class Meta:
        ordering = ['-publish_datetime', '-updated_at']

    def __str__(self):
        return f'{self.id}: {self.title}'

    def save(self, *args, **kwargs):
        # check for slug
        if not self.slug:
            self.slug = slugify(self.title) + '-' + generate_random_string()

        # check for schedule
        if self.status == 'DR':
            if self.publish_datetime:
                if self.publish_datetime <= timezone.now():
                    raise ValueError('past date for publish-date is not ok!')
                # TODO: add Task
                # print(f'{self.title} = > in time : {self.publish_datetime}')
                pass
            else:
                self.publish_datetime = timezone.now()
        elif self.status == 'PU':
            if not self.publish_datetime:
                self.publish_datetime = timezone.now()

        # call default save method
        super().save(*args, **kwargs)
