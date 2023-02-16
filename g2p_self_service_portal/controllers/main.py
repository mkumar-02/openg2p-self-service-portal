from odoo import http
from odoo.http import request

from odoo.addons.auth_oidc.controllers.main import OpenIDLogin


class SelfServiceContorller(http.Controller):
    @http.route(["/selfservice"], type="http", auth="public")
    def self_service_root(self, **kwargs):
        if request.session and request.session.uid:
            return request.redirect("/selfservice/home")
        else:
            return request.redirect("/selfservice/login")

    @http.route(["/selfservice/login"], type="http", auth="public")
    def self_service_login(self, **kwargs):
        if request.session and request.session.uid:
            return request.redirect("/selfservice/home")
        request.params["redirect"] = "/"
        context = {}

        context.update(
            dict(
                providers=[
                    p
                    for p in OpenIDLogin().list_providers()
                    if p.get("g2p_self_service_allowed", False)
                ]
            )
        )
        return request.render(
            "g2p_self_service_portal.g2p_self_service_login_page", qcontext=context
        )

    @http.route(["/selfservice/logo"], type="http", auth="public")
    def self_service_logo(self, **kwargs):
        config = request.env["ir.config_parameter"].sudo()
        attachment_id = config.get_param(
            "g2p_self_service_portal.self_service_logo_attachment"
        )
        return request.redirect("/web/content/%s" % attachment_id)

    @http.route(["/selfservice/home"], type="http", auth="user")
    def self_service_home(self, **kwargs):
        # Implement Home
        return request.redirect("/selfservice/home")

    @http.route(["/selfservice/allprograms"], type="http", auth="user")
    def self_service_all_programs(self, **kwargs):
        # Implement all programs
        return request.redirect("/selfservice/home")

    @http.route(["/selfservice/apply"], type="http", auth="user")
    def self_service_apply_programs(self, **kwargs):
        # Implement applying for programs
        return request.redirect("/selfservice/home")
