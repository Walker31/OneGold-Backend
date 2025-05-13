from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

def get_default_user():
    default_user, created = User.objects.get_or_create(username='default_user', defaults={'password': 'default_password'})
    return default_user

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        default=get_default_user
    )
    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_no = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    wishlist = ArrayField(models.IntegerField(), blank=True, default=list)

    def save(self, *args, **kwargs):
        if not self.name and self.user:
            self.name = self.user.username
        super(Customer, self).save(*args, **kwargs)

    def __str__(self):
        return self.name if self.name else self.user.username

    class Meta:
        db_table = 'customer'
        managed = False

class Address(models.Model):
    customer = models.ForeignKey(Customer, related_name='addresses', on_delete=models.CASCADE)
    pincode = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.location}, {self.city}"

    class Meta:
        db_table = 'address'
        managed = False


