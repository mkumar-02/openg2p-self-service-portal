import logging

from werkzeug.exceptions import Forbidden, Unauthorized

from odoo import _, http
from odoo.http import request

_logger = logging.getLogger(__name__)


class ServiceProviderContorller(http.Controller):
    @http.route(["/claims"], type="http", auth="public", website=True)
    def claims_portal_root(self, **kwargs):
        if request.session and request.session.uid:
            return request.redirect("/claims/home")
        else:
            return request.redirect("/selfservice/login")

    @http.route(["/claims/home"], type="http", auth="user", website=True)
    def claims_portal_home(self, **kwargs):
        self.check_roles("SERVICEPROVIDER")
        return request.render("g2p_claims_portal.dashboard")

    @http.route(["/claims/entitlements"], type="http", auth="user", website=True)
    def claims_portal_new_claims(self, **kwargs):
        self.check_roles("SERVICEPROVIDER")
        partner_id = request.env.user.partner_id
        entitlements = (
            request.env["g2p.entitlement"]
            .sudo()
            .search(
                [
                    ("vendor_id", "=", partner_id.id),
                    # TODO: get only issued entitlements
                    # to check no claims are already made against this entitlement
                    # ("claim_entitlement_ids", "=", []),
                ]
            )
        )

        values = []
        for entitlement in entitlements:
            # to check no claims are already made against this entitlement
            is_submitted = len(entitlement.claim_entitlement_ids) > 0
            claims_program = entitlement.program_id.claim_program_id
            values.append(
                {
                    "entitlement_id": entitlement.id,
                    "program_name": entitlement.program_id.name,
                    "beneficiary_name": entitlement.partner_id.name,
                    "initial_amount": entitlement.initial_amount,
                    "is_submitted": is_submitted,
                    "is_form_mapped": True
                    if claims_program and claims_program.self_service_portal_form
                    else False,
                }
            )

        return request.render(
            "g2p_claims_portal.claims",
            {
                "entitlements": values,
            },
        )

    @http.route(
        ["/claims/entitlement/<int:_id>"], type="http", auth="user", website=True
    )
    def claims_portal_new_submission(self, _id, **kwargs):
        self.check_roles("SERVICEPROVIDER")

        current_partner = request.env.user.partner_id

        # TODO: get only issued entitlements

        entitlement = request.env["g2p.entitlement"].sudo().browse(_id)
        if entitlement.vendor_id.id != current_partner.id:
            raise Forbidden()

        # check if already claimed
        if len(entitlement.claim_entitlement_ids) > 0:
            return request.redirect(f"/claims/submitted/{_id}")

        claims_program = entitlement.program_id.claim_program_id
        view = claims_program.self_service_portal_form.view_id

        return request.render(
            view.id,
            {
                "entitlement_id": _id,
            },
        )

    def check_roles(self, role_to_check):
        # And add further role checks and return types
        if role_to_check == "SERVICEPROVIDER":
            if not request.session or not request.env.user:
                raise Unauthorized(_("User is not logged in"))
            # change the following for vendor/service provider
            if not request.env.user.partner_id.is_registrant:
                raise Forbidden(_("User is not allowed to access the portal"))
