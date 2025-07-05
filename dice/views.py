'''Dice app views'''

from django.shortcuts import render

from .models import Dice

def all_dice(request):
    """View to return dice page"""

    dice = Dice.objects.all() # pylint: disable=E1101

    context = {
        'dice': dice,
    }

    return render(request, 'dice/dice.html', context)
