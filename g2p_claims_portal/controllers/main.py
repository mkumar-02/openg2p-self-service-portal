import logging

from werkzeug.exceptions import Forbidden, Unauthorized

from odoo import _, http
from odoo.http import request

from odoo.addons.g2p_self_service_portal.controllers.main import SelfServiceController

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

    @http.route(
        ["/claims/submitted/<int:_id>"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def claims_portal_post_submission(self, _id, **kwargs):
        self.check_roles("SERVICEPROVIDER")

        current_partner = request.env.user.partner_id

        # TODO: get only issued entitlements

        entitlement = request.env["g2p.entitlement"].sudo().browse(_id)
        if entitlement.vendor_id.id != current_partner.id:
            raise Forbidden()

        if request.httprequest.method == "POST":
            form_data = kwargs
            # check if already claimed
            if len(entitlement.claim_entitlement_ids) > 0:
                return request.redirect(f"/claims/submitted/{_id}")
            # TODO: allow resubmission

            # TODO: check active cycle in claims program
            # TODO: Check if beneficiary of claims program

            if not entitlement.code == form_data["Voucher Code"]:
                # TODO: raise error
                return

            claims_program = entitlement.program_id.claim_program_id
            claims_active_cycle = claims_program.default_active_cycle

            # TODO: remove billing statement hardcode
            document_form_key = "Billing Statement"
            supporting_document = form_data[document_form_key]
            supporting_document_file = SelfServiceController.add_file_to_store(
                supporting_document, claims_program.supporting_documents_store
            )
            if not supporting_document_file:
                _logger.warning(
                    "Empty/No File received for field %s", document_form_key
                )

            # TODO: remove following hardcodes
            claim = (
                request.env["g2p.entitlement"]
                .sudo()
                .create(
                    {
                        "cycle_id": claims_active_cycle.id,
                        "partner_id": current_partner.id,
                        "initial_amount": form_data["Actual Amount"],
                        "transfer_fee": 0.0,
                        "currency_id": claims_program.journal_id.currency_id.id,
                        "state": "draft",
                        "is_cash_entitlement": True,
                        "valid_from": claims_active_cycle.start_date,
                        "valid_until": claims_active_cycle.end_date,
                        "supporting_document": supporting_document_file.get(
                            "document_id", None
                        ),
                        "claim_original_entitlement_id": entitlement.id,
                    }
                )
            )
        else:
            # TODO: search and return currently active claim
            claim = request.env["g2p.entitlement"].search()

        return request.render(
            "g2p_claims_portal.claim_form_submitted",
            {
                "entitlement": entitlement.id,
                "submission_date": claim.create_date.strftime("%d-%b-%Y"),
                "application_id": claim.id,
                "user": current_partner.name.capitalize(),
            },
        )

    def check_roles(self, role_to_check):
        # And add further role checks and return types
        if role_to_check == "SERVICEPROVIDER":
            if not request.session or not request.env.user:
                raise Unauthorized(_("User is not logged in"))
            # change the following for vendor/service provider
            if not request.env.user.partner_id.supplier_rank > 0:
                raise Forbidden(_("User is not allowed to access the portal"))
