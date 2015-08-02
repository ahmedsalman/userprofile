from felloz.userprofile.models import UserProfile

from social_auth.backends.pipeline.user import create_user
from social_auth.models import UserSocialAuth


def create_user(backend, details, response, uid, username, user=None, *args, **kwargs):
    """
    Create user and user profile.
    """
    if user:
        return {'user': user}
    if not username:
        return None

    request = kwargs['request']
    user = UserSocialAuth.create_user(username = username)
#    profile = UserProfile.objects.create_user(user = user)

    return {
        'user': user,
        'is_new': True
    }

