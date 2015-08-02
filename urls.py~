from django.conf.urls.defaults import patterns, include, url

from userprofile.views import *

urlpatterns = patterns('',

    #Ajax user delete education
    url(r'^ajax/user/delete/user/education/$',
       delete_user_education,
       name = 'delete_user_education'
    ),

    #Ajax user delete education
    url(r'^ajax/user/user/notification/update/$',
       notification_ajax_update,
       name = 'notification_ajax_update'
    ),

    #Ajax user delete profession
    url(r'^ajax/user/delete/user/profession/$',
       delete_user_profession,
       name = 'delete_user_profession'
    ),

    #Ajax user profile tags
    url(r'^ajax/user/remove/profile/tag/$',
       remove_profile_tag,
       name = 'remove_profile_tag'
    ),

    #Ajax get academic backround
    url(r'^ajax/user/academic/background/get/$',
       academic_background_get,
       name = 'academic_background_get'
    ),

    #Ajax update academic backround
    url(r'^ajax/user/academic/background/update/$',
       academic_background_update,
       name = 'academic_background_update'
    ),

    #Ajax user full name
    url(r'^ajax/update/user/name/$',
       update_user_name,
       name = 'update_user_name'
    ),

    # Ajax user profile tags
    url(r'^ajax/user/profle/tags/$',
       user_profile_tags,
       name = 'user_profile_tags'
    ),

    # Ajax add update user summary
    url(r'^ajax/user/profession/edit/$',
       get_user_profession,
       name = 'get_user_profession'
    ),

    # Ajax add update user summary
    url(r'^ajax/user/language/edit/$',
       user_language_Interests_Awards_edit,
       name = 'user_language_edit'
    ),

    # Ajax get user contact
    url(r'^ajax/user/contact/edit/$',
       user_contact_edit,
       name = 'user_contact_edit'
    ),

    # Ajax add update user summary
    url(r'^ajax/user/summary/$',
       add_update_user_summary,
       name = 'add_update_user_summary'
    ),
    # update display picture
    url(r'^ajax/updatedp/$',
       dpupdate,
       name = 'update_dp'
    ),

    url(r'^follow/$',
       user_follow,
       name = 'user_follow'
    ),

    url(r'^scroller/$',
       newsfeed_scroller,
       name = 'newsfeed_scroller'
    ),

    # Ajax add user professional experience
    url(r'^add/experience/$',
       professional_experience,
       name = 'professional_experience'
    ),
    
    # Ajax update user professional experience
    url(r'^update/experience/$',
       update_professional_experience,
       name = 'update_professional_experience'
    ),


    # Ajax add user academic background 
    url(r'^add/academic-background/$',
       academic_background,
       name = 'academic_background'
    ),

    # Ajax add user language 
    url(r'^add/user/language/$',
       add_user_language,
       name = 'add_user_language'
    ),

    # Ajax add user interests 
    url(r'^add/user/interests/$',
       add_user_interests,
       name = 'add_user_interests'
    ),

    # Ajax add user awards 
    url(r'^add/user/awards/$',
       add_user_awards,
       name = 'add_user_awards'
    ),

    # Ajax add user awards 
    url(r'^user/personal/info/$',
       user_personal_info,
       name = 'user_personal_info'
    ),

    url(r'^(?P<username>[-\w\.]+)/$',
        user_profile,
        {'template_name': 'userprofile/user_profile.html'},
        name = 'user_profile'
    ),

    url(r'^(?P<username>[-\w\.]+)/followers/$',
       user_followers,
       {'template_name': 'userprofile/user_followers.html'},
       name = 'user_followers'
    ),

    url(r'^(?P<username>[-\w\.]+)/followings/$',
       user_followings,
       {'template_name': 'userprofile/user_followings.html'},
       name = 'user_followings'
    ),
    
    url(r'^(?P<username>[-\w\.]+)/recommendations/$',
       recommended_user,
       {'template_name': 'userprofile/user_recommendation.html'},
       name = 'recommended_user'
    ),
    
    url(r'^user/notification/redirect/after-mark-as-read/(?P<slug>\d+)/$',
       user_notification,
       name = 'user_notification'
    ),

)
