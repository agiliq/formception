from django.db import models

# Create your models here.

# We have two models related by m2m: Email and Contact.
# We want users to be able to fill up multiple contacts
# and mutliple emails for each contact

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
