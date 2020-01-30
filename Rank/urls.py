from django.conf.urls import url
from rest_framework.authtoken import views as drf_views

from . import views
app_name = 'Rank'

urlpatterns = [
    #auth/
    url(r'^auth/$', drf_views.obtain_auth_token, name='auth'),

    #ranktank/signin
    url(r'^isloggedin/$',views.IsLoggedIn.as_view(), name = 'is-logged-in'),

    #ranktank/signup
    url(r'^signup/$',views.SignUp.as_view(), name = 'sign-up'),

    #ranktank/signin
    url(r'^signin/$',views.SignIn.as_view(), name = 'sign-in'),

    #ranktank/new_contest
    url(r'^new_contest/$',views.NewContest.as_view(), name = 'new_contest'),

    #ranktank/new_private_contest
    url(r'^new_private_contest/$',views.NewPrivateContest.as_view(), name = 'new_private_contest'),

    #ranktank/rank_vote
    url(r'^rank_vote/(?P<url>\w+)/$',views.RankVote.as_view(), name = 'rank_vote'),

    #ranktank/rank_vote
    url(r'^rank_result/(?P<url>\w+)/$',views.RankResult.as_view(), name = 'rank_result'),

    #ranktank/private_randk_vote
    url(r'^rank_private_vote/(?P<url>\w+)/$',views.RankPrivateVote.as_view(), name = 'rank_private_vote'),

    #ranktank/rank_vote
    url(r'^my_rtlist/$',views.MyRTList.as_view(), name = 'my-rtlist'),

    #ranktank/my_admin
    url(r'^my_admin/$',views.MyAdmin.as_view(), name = 'my-admin'),
    
    #iwansell/rank_title
    url(r'^rank_title/(?P<url>\w+)/$',views.RankTitle.as_view(), name = 'rank-title'),

    #iwansell/rank_tanker
    url(r'^rank_tanker/(?P<url>\w+)/$',views.RankTanker.as_view(), name = 'rank-tanker'),

    #iwansell/private_rank_title
    url(r'^private_rank_title/(?P<url>\w+)/$',views.PrivateRankTitle.as_view(), name = 'private-rank-title'),

    #iwansell/forgot_password
    url(r'^forgot_password/$',views.ResetPasswordEmail.as_view(), name = 'reset-password-email'),

]