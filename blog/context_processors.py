from users.models import Profile
import random


def suggested_profiles(request):
    # Check if the user is authenticated and not on login, register, or logout pages
    if request.user.id:
        all_profiles = Profile.objects.exclude(user=request.user)
        suggested_profiles = random.sample(list(all_profiles), min(len(all_profiles), 4))
    else:
        all_profiles = Profile.objects.all()
        suggested_profiles = random.sample(list(all_profiles), min(len(all_profiles), 4))

    return {'suggested_profiles': suggested_profiles}
