import os
import datetime

from django.db import models
from django.utils.text import slugify

import tinymce


def now():
    now = int((datetime.datetime.utcnow() -
                datetime.datetime(2014, 1, 1)).total_seconds() * 10 ** 6)
    return unicode(now)

# issue_covers/issue.year/filename.jpg
def issue_upload_to(instance, filename):
    fname = ''.join([c for c in filename if c.isalnum() or c == '.'])
    return os.path.join('issue_covers', str(instance.year), now() + '_' + fname)


class Issue(models.Model):
    name = models.CharField(max_length=255, unique=True)
    theme = models.CharField(max_length=255, blank=True, null=True)
    cover_image = models.ImageField(upload_to=issue_upload_to, blank=True, null=True)
    
    ISSUE_CHOICES = (
        ('Fall', 'Fall'),
        ('Winter', 'Winter'),
        ('Spring', 'Spring'),
        ('Commencement', 'Commencement'),
    )
    issue = models.CharField(max_length=255, choices=ISSUE_CHOICES, default='Fall')
    year = models.IntegerField(blank=True, null=True)
    pub_date = models.DateField()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return '/issue/{0}-{1}/'.format(self.issue.lower(), self.year)

class Section(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __unicode__(self):
        return self.name


class Contributor(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)

    def __unicode__(self):
        return self.name


class Content(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    teaser = models.TextField()
    body = tinymce.models.HTMLField()

    # Legacy fields; we should probably get rid of this eventually
    medium = tinymce.models.HTMLField()
    size = tinymce.models.HTMLField()
    statement = tinymce.models.HTMLField()

    issue = models.ForeignKey('Issue')
    section = models.ForeignKey('Section')
    contributors = models.ManyToManyField(Contributor)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.title


class Article(Content):
    pass


def upload_image_to(instance, filename):
    fname = ''.join([c for c in filename if c.isalnum() or c == '.'])

    return os.path.join('images', slugify(instance.issue.name),
            now() + '_' + fname)


class Image(Content):
    photo = models.ImageField(upload_to=upload_image_to)

class ShopItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.CharField(max_length = 255)


class Donation(models.Model):

    amount = models.IntegerField()
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    streetAddress1 = models.CharField(max_length=255)
    streetAddress2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)    
    state = models.CharField(max_length=255)    
    country = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    customerID = models.CharField(max_length=255) 
    time = models.CharField(max_length=255)


class Subscriber(models.Model):

    SUBSCRIPTION_CHOICES = (
        ('Three year; US', 'Three year; US'),
        ('Two year; US', 'Two year; US'),
        ('One year; US', 'One year; US'),
        ('Three year; non-US', 'Three year; non-US'),
        ('Two year; non-US', 'Two year; non-US'),
        ('One year; non-US', 'One year; non-US')
    )

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    streetAddress1 = models.CharField(max_length=255)
    streetAddress2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)    
    state = models.CharField(max_length=255)    
    country = models.CharField(max_length=255)
    zipCode = models.CharField(max_length=255)
    customerID = models.CharField(max_length=255) 
    renew = models.BooleanField()
    subscriptionType = models.CharField(max_length=255, choices=SUBSCRIPTION_CHOICES)
    time = models.CharField(max_length=255)

