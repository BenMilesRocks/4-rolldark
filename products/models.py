'''Products app models'''

from django.db import models

class Category(models.Model):
    '''Top Level Category model'''

    class Meta:
        '''Fixes the pluralisation on the Admin page, shows Categories instead of Categorys'''
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return str(self.name)

    def get_friendly_name(self):
        '''return display name'''
        return str(self.friendly_name)

class Product(models.Model):
    '''Top level Product model'''
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    product_id = models.PositiveIntegerField(null=False, blank=False)
    name = models.CharField(max_length=254)
    description = models.TextField()
    delivery_charge = models.BooleanField(null=True, blank=True, default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.name)
