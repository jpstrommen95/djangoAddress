from django.db import models


# 3 steps for making model changes

# Change your models (in models.py).
# Run python manage.py makemigrations to create migrations for those changes
# Run python manage.py migrate to apply those changes to the database.

# Create your models here.
class Contact(models.Model):
    # todo connect to a user
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email_address = models.CharField(max_length=200)
    street_address = models.CharField(max_length=200)

    @property
    def full_name(self):
        full_name = ""
        full_name += self.first_name
        full_name += " "
        full_name += self.last_name
        return full_name

    def __str__(self):
        ret_str = ""
        ret_str += self.full_name
        ret_str += " - "
        ret_str += self.email_address
        ret_str += " - "
        ret_str += self.street_address
        return ret_str


class PhoneNumber(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    phone_number = models.CharField('Un-formatted Phone Number', max_length=11)
    type = models.CharField(max_length=200)

    # a simple phone formatter
    @staticmethod
    def phone_format(n):
        return format(int(n[:-1]), ",").replace(",", "-") + n[-1]

    def __str__(self):
        ret_str = ""
        ret_str += self.type
        ret_str += ": "
        ret_str += self.phone_number  # fixme format this
        return ret_str
