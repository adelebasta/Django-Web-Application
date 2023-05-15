from datetime import date, datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from Shoppingcart.models import ShoppingCart


def get_date_20_years_ago():
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    return date(year - 20, month, day)

class MyUser(AbstractUser):
    USER_TYPES = [
        ('SU', 'superuser'),
        ('CS', 'customer support'),
        ('CU', 'customer'),
    ]

    date_of_birth = models.DateField(default=get_date_20_years_ago())  # Default is 20 years old
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    file = models.FileField(upload_to='uploaded_files/', blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    type = models.CharField(max_length=2,
                            choices=USER_TYPES,
							default='CU',
                            )

    def count_shopping_cart_items(self):
        count = 0
        if self.is_authenticated:
            shopping_carts = ShoppingCart.objects.filter(myuser=self)
            if shopping_carts:
                shopping_cart = shopping_carts.first()
                count = shopping_cart.get_number_of_items()

        return count

    def can_modify(self):
        is_allowed = False
        if self.type == 'SU' or self.type == 'CS':
            is_allowed = True
        return is_allowed

    def __str__(self):
        return self.first_name + ' ' + self.last_name + ' (' + str(self.date_of_birth) + ')'
