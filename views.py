import calendar
import datetime
import Image
import unicodedata

from djorm_pgarray.fields import ArrayField

from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt


from registration.views import register
from userprofile.forms import ProfessionalExperienceForm, UserProfileForm
from userprofile.models import Felloz, ProfessionalExperience, UserProfile
from taggit.models import *
from annoying.decorators import ajax_request

def homepage (request, template_name , page_template):
    """
    Homepage for logged in user and signin page for other
    """
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username = request.user.username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect(reverse('auth_logout'))
            
        try:
            user_profile = user.get_profile()
        except UserProfile.DoesNotExist:
            messages.error(request, "Profile does not exist.")
            return HttpResponseRedirect(reverse('auth_logout'))

        followers_widget = Felloz.objects.get_followers(user = user)
        followings_widget = Felloz.objects.get_followings(user = user)

        recommendations_widget = UserProfile.objects.filter( tags__in = user_profile.tags.all() ).distinct().exclude(user__in = followings_widget).exclude( user = user )
        if not recommendations_widget:
            recommendations_widget = UserProfile.objects.filter(~Q( user__in = followings_widget ) ).exclude( user = user ).order_by('?')

        tags = []
        tags_string = ''
        for x in Tag.objects.all():
            tag = unicodedata.normalize('NFKD', x.name).encode('ascii','ignore')
            tags.append( tag )

            tags_string = ','.join(tags)

        context = {
            'profile': user_profile,
            'followers_widget': followers_widget,
            'followings_widget': followings_widget,
            'recommendations_widget': recommendations_widget,
            'related_doc_widget': related_doc_widget,
            'page_template': page_template,
            'tags': tags_string,
            'site': Site.objects.get_current(),
            }

        if request.is_ajax():
            template_name = page_template
        return render_to_response(template_name, context, context_instance=RequestContext(request))
    else:
        form = AuthenticationForm(request)
        form_registration = register(request, settings.REGISTRATION_BACKENDS, homepage_referer = True)
        return render_to_response('registration/login_registration_forms.html', {'background': True, 'form': form, 'form_registration': form_registration},
                                  context_instance=RequestContext(request))


def user_profile (request, username, template_name):
    """
    Users profile
    """
    
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        messages.error(request, "Not a valid profile name.")
        return HttpResponseRedirect(reverse('auth_logout'))

    try:
        user_profile = user.get_profile()
    except UserProfile.DoesNotExist:
        messages.error(request, "Profile does not exist.")
        return HttpResponseRedirect(reverse('homepage'))

    pro_exp = ProfessionalExperience.objects.filter(user__username = username)

    followers_widget = Felloz.objects.get_followers(user = user_profile.user)
    followings_widget = Felloz.objects.get_followings(user = user_profile.user)
    tags = []
    tags_string = ''

    for x in Tag.objects.all():
        tag = unicodedata.normalize('NFKD', x.name).encode('ascii','ignore')
        tags.append( tag )

        tags_string = ','.join(tags)


    now = datetime.datetime.now()
    context = {
        'profile': user_profile,
        'experience': pro_exp,
        'related_doc_widget': related_doc_widget,
        'followers_widget': followers_widget,
        'followings_widget': followings_widget,
        'userprofileform' : UserProfileForm(),
        'tags': tags_string,
        'user':user,
        'current_date':now.strftime("%m/%d/%Y"),
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))                


def user_followers(request, username, template_name):
    """
    List of followers of a user
    """
    if request.user.is_authenticated():
    
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect(reverse('auth_logout'))

        try:
            user_profile = user.get_profile()
        except UserProfile.DoesNotExist:
            messages.error(request, "Profile does not exist.")
            return HttpResponseRedirect(reverse('homepage'))

        fello_followers = Felloz.objects.get_followers(user = user)
        user_followers = Felloz.objects.get_followers(user = request.user)

        followers = []
        for follower in fello_followers:
            if follower in user_followers:
                followers.append({'follower': follower, 'button': False})
            else:
                followers.append({'follower': follower, 'button': True})


        followers_widget = Felloz.objects.get_followers(user = user_profile.user)
        followings_widget = Felloz.objects.get_followings(user = user_profile.user)

        recommendations_widget = UserProfile.objects.filter( tags__in = user_profile.tags.all() ).distinct().exclude(user__in = followings_widget).exclude( user = user )
        if not recommendations_widget:
            recommendations_widget = UserProfile.objects.filter(~Q( user__in = followings_widget ) ).exclude( user = user ).order_by('?')

        context = {
            'followers': followers,
            'followers_widget': followers_widget,
            'followings_widget': followings_widget,
            'related_doc_widget': related_doc_widget,
            'user': user,
            'profile':user_profile,
            'recommendations_widget':recommendations_widget,
        }
        return render_to_response(template_name, context, context_instance=RequestContext(request))
    messages.error(request, "You are not a logged in user.")
    return HttpResponseRedirect(reverse('auth_login'))


def user_followings(request, username, template_name):
    """
    List of following users
    """
    
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect(reverse('auth_login'))
            
        try:
            user_profile = user.get_profile()
        except UserProfile.DoesNotExist:
            messages.error(request, "Profile does not exist.")
            return HttpResponseRedirect(reverse('homepage'))

        fello_followings = Felloz.objects.get_followings(user = user)
        user_followings = Felloz.objects.get_followings(user = request.user)

        followings = []
        for following in fello_followings:
            if following in user_followings:
                followings.append({'following': following, 'button': False})
            else:
                followings.append({'following': following, 'button': True})

        followers_widget = Felloz.objects.get_followers(user = request.user)
        followings_widget = Felloz.objects.get_followings(user = request.user)

        followers_widget = Felloz.objects.get_followers(user = user_profile.user)
        followings_widget = Felloz.objects.get_followings(user = user_profile.user)


        recommendations_widget = UserProfile.objects.filter( tags__in = user_profile.tags.all() ).distinct().exclude(user__in = followings_widget).exclude( user = user )
        if not recommendations_widget:
            recommendations_widget = UserProfile.objects.filter(~Q( user__in = followings_widget ) ).exclude( user = user ).order_by('?')

        context = {
            'followings': followings,
            'followers_widget': followers_widget,
            'followings_widget': followings_widget,
            'user': user,
            'profile':user_profile,
            'followers_widget': followers_widget,
            'followings_widget': followings_widget,
            'related_doc_widget': related_doc_widget,
            'recommendations_widget':recommendations_widget,
        }
        return render_to_response(template_name, context, context_instance=RequestContext(request))
    messages.error(request, "You are not a logged in user.")
    return HttpResponseRedirect(reverse('auth_login'))


def recommended_user(request, username, template_name):
    """
    List of recommended user
    """
        
    try:
        user = User.objects.get(username = username)
    except User.DoesNotExist:
        messages.error(request, "You are not a logged in user.")
        return HttpResponseRedirect(reverse('auth_logout'))

    try:
        user_profile = user.get_profile()
    except UserProfile.DoesNotExist:
        messages.error(request, "Profile does not exist.")
        return HttpResponseRedirect(reverse('homepage'))

    followers_widget = Felloz.objects.get_followers(user = user)
    followings_widget = Felloz.objects.get_followings(user = user)
#    recommendations = UserProfile.objects.filter(Q(~Q(user__in = followings_widget) or ~Q(user = user) ) ).order_by('?')
    
    recommendations = UserProfile.objects.filter( tags__in = user_profile.tags.all() ).distinct().exclude(user__in = followings_widget).exclude( user = user )
    if not recommendations:
        recommendations = UserProfile.objects.filter(~Q( user__in = followings_widget ) ).exclude( user = user ).order_by('?')

    context = {
        'user': user,
        'profile':user_profile,
        'followers_widget': followers_widget,
        'followings_widget': followings_widget,
        'related_doc_widget': related_doc_widget,
        'recommendations':recommendations,
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@ajax_request
@csrf_exempt
@login_required
def user_follow(request):
    """
    Follow a user
    """
    if request.is_ajax():
        if request.method == 'POST':
            try:
                user = User.objects.get(username = request.user.username)
            except User.DoesNotExist:
                messages.error(request, "You are not a logged in user.")
                return HttpResponseRedirect(reverse('auth_logout'))

            follow_id = request.POST.get('followId', '')
            try:
                follow = User.objects.get(id = follow_id)
            except User.DoesNotExist:
                return HttpResponse(simplejson.dumps('False'), mimetype = 'application/json' )

            felloz, flag = Felloz.objects.get_or_create(user = user)
            if flag:
                user_profile = user.get_profile()
                user_profile.score += 10
                user_profile.save()
                messages.success(request, "Congratulations you gained 10 points.")
            felloz.followings.add(follow)
            return HttpResponse(simplejson.dumps('True'), mimetype = 'application/json' )
            
    return HttpResponseRedirect(reverse('homepage'))



@ajax_request
@csrf_exempt
@login_required
def professional_experience(request, template_name):
    """
    Add professional experience 
    """
    date_from = False
    date_to = False
    
    if request.is_ajax():
        if request.method == 'POST':
        
            try:
                user = User.objects.get(username = request.user.username)
            except User.DoesNotExist:
                messages.error(request, "You are not a logged in user.")
                return HttpResponseRedirect(reverse('auth_logout'))

            try:
                user_profile = user.get_profile()
            except UserProfile.DoesNotExist:
                messages.error(request, "Profile does not exist.")
                return HttpResponseRedirect(reverse('homepage'))

            post = request.POST.copy()

            start_year = request.POST.get('start_year', '')
            start_month = request.POST.get('start_month', '')
            if start_year and start_month != 'Present':
                start_month = list(calendar.month_name).index(start_month)
                post['date_from'] = datetime.date(int(start_year), start_month, 1)
                date_from = post['date_from']

            end_year = request.POST.get('end_year', '')
            end_month = request.POST.get('end_month', '')
            if end_year and end_month != 'Present':
                end_month = list(calendar.month_name).index(end_month)
                post['date_to'] = datetime.date(int(end_year), end_month, 1)
                date_to = post['date_to']

            form = ProfessionalExperienceForm(post)

            if form.is_valid():
                form.user = request.user
                form.save()
                title = request.POST.get('title', '')
                industries = request.POST.get('industry', '')
                description = request.POST.get('description', '')
                pro_exp = ProfessionalExperience.objects.filter(user__username = request.user.username)
                context = {
                    'experience':pro_exp,
                    'profile':user_profile,
                }
                return render_to_response(template_name, context, context_instance=RequestContext(request))
            else:
                errors = form.errors
                return HttpResponse(simplejson.dumps(errors), mimetype = 'application/json' )

    return HttpResponse(simplejson.dumps('Invalid request type'), mimetype = 'application/json' )


@ajax_request
@csrf_exempt
def user_personal_info(request, valid_template_name, not_valid_template_name):
    """
    Add personal info 
    """
    if request.method == 'POST':
        try:
            user = User.objects.get(username = request.user.username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect( reverse('auth_logout') )

        try:
            user_profile = UserProfile.objects.get(user__username = request.user.username)
        except UserProfile.DoesNotExist:
            messages.error(request, "User Profile is not created yet.")
            return HttpResponseRedirect( reverse('auth_logout') )

        form = UserProfileForm(request.POST)

        if form.is_valid():
            user_profile.country = request.POST.get('country', '')
            user_profile.city = request.POST.get('city', '')
            user_profile.website = request.POST.get('website', '')
            user_profile.save()

            userprofileform = UserProfileForm()
            template_name = valid_template_name
            context = {
                'profile' : user_profile,
                'userprofileform' : UserProfileForm(),
            }
            return render_to_response(template_name, context, context_instance=RequestContext(request))

        template_name = not_valid_template_name
        context = {
            'profile': user_profile,
            'userprofileform': form,
        }
        return render_to_response(template_name, context, context_instance=RequestContext(request))



@csrf_exempt
@login_required
def dpupdate(request):
    """
    Update the profile picture of the user
    """
    if request.method == 'POST':
        try:
            user = User.objects.get(username = request.user.username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect( reverse('auth_logout') )
        
        try:
            user_profile = UserProfile.objects.get(user__username = request.user.username)
        except UserProfile.DoesNotExist:
            messages.error(request, "User Profile is not created yet.")
            return HttpResponseRedirect( reverse('auth_logout') )
        
        element = request.FILES['myfile']
        
        try:
            im=Image.open(element)
            user_profile.avatar =element
            user_profile.save()
        except:
            messages.error(request, "File you are trying to upload is not valid image please upload valid image.")
            return HttpResponseRedirect( request.META.get('HTTP_REFERER','/') )

    return HttpResponseRedirect( request.META.get('HTTP_REFERER','/') )


@ajax_request
@csrf_exempt
@login_required
def add_update_user_summary(request):
    """
    Update the profile picture of the user
    """
    if request.method == 'POST':
        try:
            user = User.objects.get(username = request.user.username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect( reverse('auth_logout') )
        
        try:
            user_profile = UserProfile.objects.get(user__username = request.user.username)
        except UserProfile.DoesNotExist:
            messages.error(request, "User Profile is not created yet.")
            return HttpResponseRedirect( reverse('auth_logout') )

        element = request.POST.get('summary', '')

        try:
            user_profile.summary =element
            user_profile.save()

            req = {}
            req['html'] = element
            response = simplejson.dumps(req)
            return HttpResponse(response ,mimetype = 'application/json')
        except:
            messages.error(request, "An error occur will saving user summary please try again.")
            return HttpResponseRedirect( request.META.get('HTTP_REFERER','/') )

    messages.error(request, "no ajax.")
    return HttpResponseRedirect( request.META.get('HTTP_REFERER','/') )
    
    
@csrf_exempt
@ajax_request
@login_required
def update_professional_experience(request, template_name):
#    """
#    get professional experience
#    """

    if request.method == 'POST':
        try:
            user = User.objects.get(username = request.user.username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect( reverse('auth_logout') )

        try:
            user_profile = UserProfile.objects.get(user__username = request.user.username)
        except UserProfile.DoesNotExist:
            messages.error(request, "User Profile is not created yet.")
            return HttpResponseRedirect( reverse('auth_logout') )

        post = request.POST.copy()

        start_year = request.POST.get('start_year', '')
        start_month = request.POST.get('start_month', '')
        if start_year and start_month != 'Present':
            start_month = list(calendar.month_name).index(start_month)
            post['date_from'] = datetime.date(int(start_year), start_month, 1)
            date_from = post['date_from']

        end_year = request.POST.get('end_year', '')
        end_month = request.POST.get('end_month', '')
        if end_year and end_month != 'Present':
            end_month = list(calendar.month_name).index(end_month)
            post['date_to'] = datetime.date(int(end_year), end_month, 1)
            date_to = post['date_to']

        job_id = request.POST.get('job_id', '')
        pe_obj = ProfessionalExperience.objects.get(id=job_id).delete()

        form = ProfessionalExperienceForm(post, instance=pe_obj)

        if form.is_valid():
            form.user = request.user
            form.save()

            pro_exp = ProfessionalExperience.objects.filter(user__username = request.user.username)
            context = {
                'experience':pro_exp,
                'profile':user_profile,
            }
            return render_to_response(template_name, context, context_instance=RequestContext(request))
        else:
            errors = form.errors
            return HttpResponse(simplejson.dumps(errors), mimetype = 'application/json' )


@ajax_request
@login_required
def add_user_language(request, template_name):
    """
    add user language
    """
    if request.method == 'POST':
        try:
            user = User.objects.get(username = request.user.username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect( reverse('auth_logout') )

        try:
            userprofile = UserProfile.objects.get(user__username = request.user.username)
        except UserProfile.DoesNotExist:
            messages.error(request, "You do not have a user profile.")
            return HttpResponseRedirect( reverse('auth_logout') )


        language = request.POST.get('language', '').split(',')
        try:
            userprofile.languages = language 
            userprofile.save()
        except TypeError:
            userprofile.languages =  language 
            userprofile.save()
        context = {
            'languages' : userprofile.languages,
        }
        return render_to_response(template_name, context, context_instance=RequestContext(request))

    messages.error(request, "no ajax.")
    return HttpResponseRedirect( request.META.get('HTTP_REFERER','/') )


@ajax_request
@login_required
def add_user_interests(request, template_name):
    """
    add user interests
    """
    if request.method == 'POST':
        try:
            user = User.objects.get(username = request.user.username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect( reverse('auth_logout') )

        try:
            userprofile = UserProfile.objects.get(user__username = request.user.username)
        except UserProfile.DoesNotExist:
            messages.error(request, "You do not have a user profile.")
            return HttpResponseRedirect( reverse('auth_logout') )


        user_interest = request.POST.get('user_interest', '').split(',')
        try:
            userprofile.interests = user_interest
            userprofile.save()
        except TypeError:
            userprofile.interests = user_interest
            userprofile.save()

        context = {
            'languages' : userprofile.interests,
        }
        return render_to_response(template_name, context, context_instance=RequestContext(request))

    messages.error(request, "no ajax.")
    return HttpResponseRedirect( request.META.get('HTTP_REFERER','/') )


@ajax_request
@login_required
def add_user_awards(request, template_name):
    """
    add user interests
    """
    if request.method == 'POST':
        try:
            user = User.objects.get(username = request.user.username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect( reverse('auth_logout') )

        try:
            userprofile = UserProfile.objects.get(user__username = request.user.username)
        except UserProfile.DoesNotExist:
            messages.error(request, "You do not have a user profile.")
            return HttpResponseRedirect( reverse('auth_logout') )


        user_interest = request.POST.get('user_awards', '').split(',')
        try:
            userprofile.awards = user_interest
            userprofile.save()
        except TypeError:
            userprofile.awards = user_interest
            userprofile.save()


        context = {
            'languages' : userprofile.awards,
        }
        return render_to_response(template_name, context, context_instance=RequestContext(request))

    messages.error(request, "no ajax.")
    return HttpResponseRedirect( request.META.get('HTTP_REFERER','/') )
    
    
@ajax_request
@csrf_exempt
@login_required
def user_language_Interests_Awards_edit(request):
    """
    return user language interests awards
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        messages.error(request, "You are not a logged in user.")
        return HttpResponseRedirect( reverse('auth_logout') )

    try:
        user_profile = UserProfile.objects.get(user__username = request.user.username)
    except UserProfile.DoesNotExist:
        messages.error(request, "User Profile is not created yet.")
        return HttpResponseRedirect( reverse('auth_logout') )

    try:
        req = {}
        req['language'] = user_profile.languages
        req['interests'] = user_profile.interests
        req['awards'] = user_profile.awards
        req['summary'] = user_profile.summary
        response = simplejson.dumps(req)
        return HttpResponse(response ,mimetype = 'application/json')
    except:
        messages.error(request, "An error occur")
        return HttpResponseRedirect( request.META.get('HTTP_REFERER','/') )




@ajax_request
@csrf_exempt
@login_required
def user_contact_edit(request, template_name):
    """
    return user language interests awards
    """
    try:
        user = User.objects.get(username = request.user.username)
    except User.DoesNotExist:
        messages.error(request, "You are not a logged in user.")
        return HttpResponseRedirect( reverse('auth_logout') )

    try:
        user_profile = UserProfile.objects.get(user__username = request.user.username)
    except UserProfile.DoesNotExist:
        messages.error(request, "User Profile is not created yet.")
        return HttpResponseRedirect( reverse('auth_logout') )

    userprofileform = UserProfileForm()
    userprofileform.fields["country"].initial = user_profile.country
    userprofileform.fields["city"].initial = user_profile.city
    userprofileform.fields["website"].initial = user_profile.website

    context = {
            'userprofileform' : userprofileform,
    }
    return render_to_response(template_name, context, context_instance=RequestContext(request))


@ajax_request
@csrf_exempt
@login_required
def get_user_profession(request):
    """
    return user profession
    """


    months = ['Present','January','February','March','April','May','June','July','August','September','October','November','  December']
    
    if request.user.is_authenticated():
        try:
            user = User.objects.get(username = request.user.username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect( reverse('auth_logout') )

        try:
            user_profile = UserProfile.objects.get(user__username = request.user.username)
        except UserProfile.DoesNotExist:
            messages.error(request, "User Profile is not created yet.")
            return HttpResponseRedirect( reverse('auth_logout') )

        try:
        
            pro_exp = ProfessionalExperience.objects.get(user__username = request.user.username, id=request.POST.get('id', '') )
            req = {}
            req['title'] = pro_exp.title
            req['industry'] = pro_exp.industry
            req['description'] = pro_exp.description

            start_month = pro_exp.date_from
            start_year = pro_exp.date_from
            end_month = pro_exp.date_to
            end_year = pro_exp.date_to

            req['start_month'] = months[ start_month.month ]
            req['start_year'] = start_year.year
            try:
                req['end_month'] = months[ end_month.month ]
                req['end_year'] = end_year.year
            except:
                req['end_month'] = "Present"
                req['end_year'] = "year"
        
            response = simplejson.dumps(req)
            return HttpResponse(response ,mimetype = 'application/json')
        except:
            messages.error(request, "An error occur")
            return HttpResponseRedirect( request.META.get('HTTP_REFERER','/') )

        messages.error(request, "You are not logged in")
        return HttpResponseRedirect( request.META.get('HTTP_REFERER','/') )

@ajax_request
@csrf_exempt
@login_required
def user_profile_tags(request):
    """
    user profile tags
    """
    if request.is_ajax():
        if request.method == 'POST':
            try:
                user = User.objects.get(username = request.user.username)
            except User.DoesNotExist:
                messages.error(request, "You are not a logged in user.")
                return HttpResponseRedirect( reverse('auth_logout') )

            try:
                user_profile = UserProfile.objects.get(user__username = request.user.username)
            except UserProfile.DoesNotExist:
                messages.error(request, "User Profile is not created yet.")
                return HttpResponseRedirect( reverse('auth_logout') )

            tags = request.POST.getlist('user_tags[]','')

            for tag in tags:
                user_profile.tags.add( tag.strip() )

            req = {}
            response = simplejson.dumps(req)
            return HttpResponse(response ,mimetype = 'application/json')

    messages.error(request, "Some thing went wrong please try again.")
    req = {}
    response = simplejson.dumps(req)
    return HttpResponse(response ,mimetype = 'application/json')


@ajax_request
@csrf_exempt
@login_required
def remove_profile_tag(request):
    """
    remove profile tag
    """
    if request.is_ajax():
        if request.method == 'POST':
            try:
                user = User.objects.get(username = request.user.username)
            except User.DoesNotExist:
                messages.error(request, "You are not a logged in user.")
                return HttpResponseRedirect( reverse('auth_logout') )

            try:
                user_profile = UserProfile.objects.get(user__username = request.user.username)
            except UserProfile.DoesNotExist:
                messages.error(request, "User Profile is not created yet.")
                return HttpResponseRedirect( reverse('auth_logout') )

            tag = request.POST.get('tag','')
            user_profile.tags.remove( tag )
            req = {}
            response = simplejson.dumps(req)
            return HttpResponse(response ,mimetype = 'application/json')
            
            
@ajax_request
@csrf_exempt
@login_required
def update_user_name(request):
    """
    update user full name
    """
    if request.is_ajax():

        try:
            user = User.objects.get(username = request.user.username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect( reverse('auth_logout') )

        try:
            user_profile = UserProfile.objects.get(user__username = request.user.username)
        except UserProfile.DoesNotExist:
            messages.error(request, "User Profile is not created yet.")
            return HttpResponseRedirect( reverse('auth_logout') )

        if request.method == 'POST':
            f_name = request.POST.get('first_name','')
            l_name = request.POST.get('last_name','')

            user.first_name = f_name
            user.last_name = l_name
            user.save()

            full_name = user.get_full_name()
            req = {}
            req['f_name'] = f_name
            req['l_name'] = l_name
            req['full_name'] = full_name

            response = simplejson.dumps(req)
            return HttpResponse(response ,mimetype = 'application/json')

@csrf_exempt
@ajax_request
@login_required
def delete_user_profession(request, template_name):
#    """
#    delete professional experience
#    """

    if request.method == 'POST':
        try:
            user = User.objects.get(username = request.user.username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect( reverse('auth_logout') )

        try:
            user_profile = UserProfile.objects.get(user__username = request.user.username)
        except UserProfile.DoesNotExist:
            messages.error(request, "User Profile is not created yet.")
            return HttpResponseRedirect( reverse('auth_logout') )

        job_id = request.POST.get('id', '')

        try:
            professional_experience = ProfessionalExperience.objects.get(id=job_id , user = user)
            professional_experience.delete()
        except ProfessionalExperience.DoesNotExist:
            messages.error(request, "You are not autherized.")
            return HttpResponseRedirect(reverse('homepage'))

        pro_exp = ProfessionalExperience.objects.filter(user__username = request.user.username)
        context = {
            'experience':pro_exp,
            'profile':user_profile,
        }
        return render_to_response(template_name, context, context_instance=RequestContext(request))
    else:
        errors = form.errors
        return HttpResponse(simplejson.dumps(errors), mimetype = 'application/json' )


@csrf_exempt
@ajax_request
@login_required
def delete_user_education(request, template_name):
#    """
#    delete professional experience
#    """

    if request.method == 'POST':
        try:
            user = User.objects.get(username = request.user.username)
        except User.DoesNotExist:
            messages.error(request, "You are not a logged in user.")
            return HttpResponseRedirect( reverse('auth_logout') )

        try:
            user_profile = UserProfile.objects.get(user__username = request.user.username)
        except UserProfile.DoesNotExist:
            messages.error(request, "User Profile is not created yet.")
            return HttpResponseRedirect( reverse('auth_logout') )

        job_id = request.POST.get('id', '')
        context = {
                'profile':user_profile,
        }
        return render_to_response(template_name, context, context_instance=RequestContext(request))

    return HttpResponse(simplejson.dumps('Invalid request type'), mimetype = 'application/json' )


def slug2id(slug):
    return long(slug) - 110909


def id2slug(id):
    return id + 110909
