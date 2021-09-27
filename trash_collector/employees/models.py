from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=5)
    phone_number = models.CharField(max_length=10)
    user = models.ForeignKey('accounts.User', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
# TODO: Create an Employee model with properties required by the user stories