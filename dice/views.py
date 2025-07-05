'''Dice app views'''

from django.shortcuts import render, get_object_or_404

from .models import Dice

def all_dice(request):
    """View to return dice page"""

    dice = Dice.objects.all() # pylint: disable=E1101

    context = {
        'dice': dice,
    }

    return render(request, 'dice/dice.html', context)

def dice_detail(request, dice_id):
    '''Returns details for single dice'''

    dice = get_object_or_404(Dice, pk=dice_id)

    context = {
        'dice' : dice,
    }

    return render(request, 'dice/dice_detail.html', context)
