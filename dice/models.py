'''Dice app models'''

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
