
from .models import Favourite

def global_counts(request):
    favourite_count = 0
    if request.user.is_authenticated:
        favourite_count = Favourite.objects.filter(user=request.user).count()
    
  
    return {
        'favourite_count': favourite_count,
    }
