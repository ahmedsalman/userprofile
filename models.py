from south.modelsinspector import add_ignored_fields
add_ignored_fields(["^felloz.taggit\.managers"])

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from taggit.managers import TaggableManager

from django_countries import CountryField
from djorm_pgarray.fields import ArrayField

class TimeStampAwareModel( models.Model ):
    """
    A model class that can be used as super class
    for any model that is considered timestamp aware 
    model.
    """
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_deleted = models.DateTimeField(blank=True, null=True)

    def is_deleted(self):
        if self.date_deleted:
            return True
        return False
    is_deleted.boolean = True
    
    class Meta:
        abstract = True


class UserProfileManager( models.Manager ):
    """
    User Profile manager
    """
    def create_user(self, user = None, username = None, email=None, password=None, **extra_fields):
        userprofile = self.model(user = user)
        userprofile.save()
        return {
            'user': user,
            'userprofile': userprofile,
            'backend': 'facebook',
            'is_new': True
            }


class UserProfile( TimeStampAwareModel ):
    """
    Profile model
    """
    user = models.ForeignKey(User)
    summary = models.TextField(_('summary'), null = True, blank = True)
    avatar = models.ImageField(_('profile pic'), upload_to = "images/", null = True, blank = True)
    languages = ArrayField(_('languages'), dbtype = "varchar(255)", null = True, blank = True)
    awards = ArrayField(_('awards'), dbtype = "varchar(255)", null = True, blank = True)
    interests = ArrayField(_('interests'), dbtype = "varchar(255)", null = True, blank = True)
    address = models.CharField(_('address'), max_length = 50, null = True, blank = True)
    country = CountryField(_('country'), null = True, blank = True)
    city = models.CharField(_('city'), max_length = 30, null = True, blank = True)
    phone = models.CharField(_('phone number'), max_length = 20, null = True, blank = True)
    mobile = models.CharField(_('mobile number'), max_length = 20, null = True, blank = True)
    date_of_birth = models.DateField(_('date of birth'), null = True, blank = True)
    website = models.URLField(_('website'), null = True, blank = True)
    score = models.PositiveIntegerField(_('user score'), default = 0)
    email = models.EmailField(_('e-mail address'), blank = True , null = True)
    
    objects = UserProfileManager()
    tags = TaggableManager()

    def __unicode__(self):
        return _("%s") % self.user.get_full_name()

    def is_authenticated(self):
        return self.user.is_authenticated()

    class Meta:
        app_label = "userprofile"
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"


class ProfessionalExperience( TimeStampAwareModel ):
    """
    Professional Experience model
    """
    user = models.ForeignKey(User)
    title = models.CharField(_('title'), max_length = 150)
    industry = ArrayField(_('industry'), dbtype = "varchar(255)", null = True, blank = True)
    description = models.TextField(_('description'), null = True, blank = True)
    date_from = models.DateField(_('starting date'))
    date_to = models.DateField(_('ending date'), null = True, blank = True)

    def __unicode__(self):
        return _("%s_%s") % (self.user.get_full_name(), self.title)

    def is_authenticated(self):
        return self.user.is_authenticated()

    class Meta:
        verbose_name = "professional experience"
        verbose_name_plural = "professional experience"

class FellozManager( models.Manager ):
    """
    Felloz Manager
    """
    def get_followers(self, user):
        felloz = self.get_query_set().all()
        return [fello.user for fello in felloz if fello.followings.filter(username = user.username)]
            

    def get_followings(self, user):
        try:
            followings = self.get_query_set().get(user = user).followings.all()
        except:
            followings = []
        return followings


class Felloz( TimeStampAwareModel ):
    """
    Felloz model
    """
    user = models.ForeignKey(User)

    followings = models.ManyToManyField(User, related_name="%(app_label)s_%(class)s_related")

    objects = FellozManager()

    def __unicode__(self):
        return _("%s") % (self.user.get_full_name())

    def is_authenticated(self):
        return self.user.is_authenticated()

    class Meta:
        verbose_name = "felloz"
        verbose_name_plural = "felloz"

