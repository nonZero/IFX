import logging

import mwoauth
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import TemplateView
from mwoauth import initiate, complete, OAuthException, RequestToken

from ifx.base_views import IFXMixin

WIKIDATA_URL = "https://www.wikidata.org/w/index.php"

CONSUMER_TOKEN = mwoauth.ConsumerToken(settings.OAUTH_CONSUMER_KEY,
                                       settings.OAUTH_CONSUMER_SECRET)
REDIRECT_TO = "movies:home"

logger = logging.getLogger(__name__)


class MyProfileView(IFXMixin, TemplateView):
    template_name = "users/my_profile.html"
    title = _("My Profile")


class WikidataAuthView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        redirect_url, request_token = initiate(WIKIDATA_URL, CONSUMER_TOKEN)
        t = (request_token.key.decode(), request_token.secret.decode())
        request.session['oauth_request_token'] = t
        return redirect(redirect_url)


class WikidataAuthCallbackView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        if 'oauth_request_token' not in request.session:
            messages.warning(request,
                             _("Something went wrong. Please try again."))
            return redirect(REDIRECT_TO)
        d = request.GET
        t = request.session['oauth_request_token']
        request_token = RequestToken(t[0].encode(), t[1].encode())
        s = f"oauth_verifier={d.get('oauth_verifier', '')}&oauth_token={d.get('oauth_token', '')}"
        try:
            access_token = complete(WIKIDATA_URL, CONSUMER_TOKEN,
                                    request_token, s)
        except OAuthException as e:
            logger.exception("OAuth error")
            messages.error(request,
                           _("Something went wrong. Please try again."))
            return redirect(REDIRECT_TO)

        request.user.wikidata_access_token = {
            'key': access_token.key.decode(),
            'secret': access_token.secret.decode(),
        }
        request.user.wikidata_access_token_created_at = timezone.now()
        request.user.save()

        messages.success(request, _("Authenticated successfully."))

        return redirect(REDIRECT_TO)


class WikidataLogoutAuthView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        if request.user.wikidata_access_token:
            request.user.wikidata_access_token = None
            request.user.wikidata_access_token_created_at = None
            request.user.save()
        messages.success(request, _("Wikidata auth token deleted."))
        return redirect("movies:home")
