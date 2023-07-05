from django.db import models


# Create your models here.
class ContactList(models.Model):
    firstname = models.CharField(max_length=10)
    lastname = models.CharField(max_length=15)
    street = models.CharField(max_length=30)
    zip = models.IntegerField()
    city = models.CharField(max_length=20)
    image = models.CharField(max_length=100)

    def __str__(self):
        return '-'.join([self.firstname, self.lastname])
