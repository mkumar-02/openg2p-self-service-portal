import base64
import hashlib
import json
import logging
import secrets

import werkzeug.urls
from werkzeug.urls import url_decode, url_encode

from odoo.http import request

from odoo.addons.auth_oidc.controllers.main import OpenIDLogin

_logger = logging.getLogger(__name__)


# The following methods are taken from
# odoo/odoo/auth_oauth/controllers/main.py and
# OCA/server-auth/auth_oidc/controllers/main.py
# because of lack easier way to provide
# custom domain for list providers
# TODO : Find easier way to update controller
class G2POpenIDLogin(OpenIDLogin):
    def list_providers_oauth(self, domain=None):
        if not domain:
            domain = [("enabled", "=", True)]
        try:
            providers = request.env["auth.oauth.provider"].sudo().search_read(domain)
        except Exception:
            providers = []
        for provider in providers:
            return_url = request.httprequest.url_root + "auth_oauth/signin"
            state = self.get_state(provider)
            params = dict(
                response_type="token",
                client_id=provider["client_id"],
                redirect_uri=return_url,
                scope=provider["scope"],
                state=json.dumps(state),
                # nonce=base64.urlsafe_b64encode(os.urandom(16)),
            )
            provider["auth_link"] = "%s?%s" % (
                provider["auth_endpoint"],
                werkzeug.urls.url_encode(params),
            )
        return providers

    def list_providers(self, domain=None):
        providers = self.list_providers_oauth(domain)
        for provider in providers:
            flow = provider.get("flow")
            if flow in ("id_token", "id_token_code"):
                params = url_decode(provider["auth_link"].split("?")[-1])
                # nonce
                params["nonce"] = secrets.token_urlsafe()
                # response_type
                if flow == "id_token":
                    # https://openid.net/specs/openid-connect-core-1_0.html
                    # #ImplicitAuthRequest
                    params["response_type"] = "id_token token"
                elif flow == "id_token_code":
                    # https://openid.net/specs/openid-connect-core-1_0.html#AuthRequest
                    params["response_type"] = "code"
                # PKCE (https://tools.ietf.org/html/rfc7636)
                code_verifier = provider["code_verifier"]
                code_challenge = base64.urlsafe_b64encode(
                    hashlib.sha256(code_verifier.encode("ascii")).digest()
                ).rstrip(b"=")
                params["code_challenge"] = code_challenge
                params["code_challenge_method"] = "S256"
                # scope
                if provider.get("scope"):
                    if "openid" not in provider["scope"].split():
                        _logger.error("openid connect scope must contain 'openid'")
                    params["scope"] = provider["scope"]
                # auth link that the user will click
                provider["auth_link"] = "{}?{}".format(
                    provider["auth_endpoint"], url_encode(params)
                )
        return providers
