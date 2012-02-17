from django.db import models

# Create your models here.

class Email(models.Model):

    email = models.EmailField()

    def __unicode__(self):
        return self.email


class Contact(models.Model):

    name = models.CharField(max_length=200)
    emails = models.ManyToManyField(Email)

    def __unicode__(self):
        return self.name


class Profile(models.Model):

    name = models.CharField(max_length=200)
    contacts = models.ManyToManyField(Contact)

    def __unicode__(self):
        return self.name
