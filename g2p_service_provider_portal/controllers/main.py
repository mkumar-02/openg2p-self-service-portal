import logging
from argparse import _AppendAction

from werkzeug.exceptions import Forbidden, Unauthorized

from odoo import _, http
from odoo.http import request

from odoo.addons.g2p_self_service_portal.controllers.main import G2POpenIDLogin, SelfServiceController

_logger = logging.getLogger(__name__)


class ServiceProviderContorller(http.Controller):
    @http.route(["/serviceprovider"], type="http", auth="public", website=True)
    def portal_root(self, **kwargs):
        if request.session and request.session.uid:
            return request.redirect("/serviceprovider/home")
        else:
            return request.redirect("/serviceprovider/login")

    @http.route(["/serviceprovider/login"], type="http", auth="public", website=True)
    def service_provider_login(self, **kwargs):
        if request.session and request.session.uid:
            return request.redirect("/serviceprovider/home")
        request.params["redirect"] = "/"
        context = {}

        context.update(
            dict(
                providers=G2POpenIDLogin().list_providers(
                    domain=[("g2p_service_provider_allowed", "=", True)]
                )
            )
        )
        return request.render(
            "g2p_service_provider_portal.login_page", qcontext=context
        )

    @http.route(["/serviceprovider/home"], type="http", auth="user", website=True)
    def portal_home(self, **kwargs):
        self.check_roles("SERVICEPROVIDER")
        return request.redirect("/serviceprovider/voucher")

    @http.route(
        ["/serviceprovider/myprofile"], type="http", auth="public", website=True
    )
    def portal_profile(self, **kwargs):
        if request.session and request.session.uid:
            return request.render("g2p_service_provider_portal.profile_page")

    @http.route(["/serviceprovider/aboutus"], type="http", auth="public", website=True)
    def portal_about_us(self, **kwargs):
        return request.render("g2p_service_provider_portal.aboutus_page")

    @http.route(
        ["/serviceprovider/contactus"], type="http", auth="public", website=True
    )
    def portal_contact_us(self, **kwargs):
        return request.render("g2p_service_provider_portal.contact_us")

    @http.route(
        ["/serviceprovider/otherpage"], type="http", auth="public", website=True
    )
    def portal_other_page(self, **kwargs):
        return request.render("g2p_service_provider_portal.other_page")

    @http.route(["/serviceprovider/help"], type="http", auth="public", website=True)
    def portal_help_page(self, **kwargs):
        return request.render("g2p_service_provider_portal.help_page")

    @http.route(["/serviceprovider/voucher"], type="http", auth="user", website=True)
    def portal_new_entitlements(self, **kwargs):
        self.check_roles("SERVICEPROVIDER")
        partner_id = request.env.user.partner_id
        entitlements = (
            request.env["g2p.entitlement"]
            .sudo()
            .search(
                [
                    ("service_provider_id", "=", partner_id.id),
                    ("state", "=", "approved"),
                ]
            )
        )

        values = []
        for entitlement in entitlements:
            # to check no reimbursement claims are already made against this entitlement
            is_submitted = len(entitlement.reimbursement_entitlement_ids) > 0
            reimbursement_program = entitlement.program_id.reimbursement_program_id
            values.append(
                {
                    "entitlement_id": entitlement.id,
                    "program_name": entitlement.program_id.name,
                    "beneficiary_name": entitlement.partner_id.name,
                    "initial_amount": entitlement.initial_amount,
                    "is_submitted": is_submitted,
                    "status": "New"
                    if not is_submitted
                    else entitlement.reimbursement_entitlement_ids.state,
                    "is_form_mapped": True
                    if reimbursement_program
                    and reimbursement_program.self_service_portal_form
                    else False,
                }
            )

        return request.render(
            "g2p_service_provider_portal.reimbursements",
            {
                "entitlements": values,
            },
        )

    @http.route(
        ["/serviceprovider/voucher/<int:_id>"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_new_submission(self, _id, **kwargs):
        self.check_roles("SERVICEPROVIDER")

        current_partner = request.env.user.partner_id

        entitlement = request.env["g2p.entitlement"].sudo().browse(_id)
        if (
            entitlement.service_provider_id.id != current_partner.id
            or entitlement.state != "approved"
        ):
            raise Forbidden()

        # check if already claimed
        if len(entitlement.reimbursement_entitlement_ids) > 0:
            return request.redirect(f"/serviceprovider/claim/{_id}")

        return request.render(
            "g2p_service_provider_portal.reimbursement_submission_form",
            {
                "entitlement_id": _id,
                "current_user": current_partner,
                "first_name": current_partner.given_name,
                "last_name": current_partner.family_name,
                "email": current_partner.email,
                "mobile_number": current_partner.phone,
                "birthdate": current_partner.birthdate,
                "gender": current_partner.gender,
            },
        )

    @http.route(
        ["/serviceprovider/claim/<int:_id>"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def portal_post_submission(self, _id, **kwargs):
        self.check_roles("SERVICEPROVIDER")

        current_partner = request.env.user.partner_id

        # TODO: get only issued entitlements

        entitlement = request.env["g2p.entitlement"].sudo().browse(_id)
        if (
            entitlement.service_provider_id.id != current_partner.id
            or entitlement.state != "approved"
        ):
            raise Forbidden()

        if request.httprequest.method == "POST":
            form_data = kwargs
            # check if already claimed
            if len(entitlement.reimbursement_entitlement_ids) > 0:
                return request.redirect(f"/serviceprovider/claim/{_id}")

            # TODO: allow resubmission

            # TODO: Check if reimbursement program mapped to original program
            supporting_documents_store = (
                entitlement.program_id.reimbursement_program_id.supporting_documents_store
            )

            # TODO: remove all hardcoding in the next lines
            received_code = form_data.get("voucher_code", None)
            actual_amount = form_data.get("actual_amount", None)
            supporting_documents = request.httprequest.files.getlist(
                "statement_of_account"
            )
            supporting_document_file = SelfServiceController.add_file_to_store(
                supporting_documents, supporting_documents_store
            )

            if not supporting_document_file:
                _logger.warning(
                    "Empty/No File received for field %s", "Statement of Account"
                )
                supporting_document_file_id = None
            else:
                supporting_document_file_id = []

                # saving the multiple document id
                for document_id in supporting_document_file:
                    supporting_document_file_id.append(
                        document_id.get("document_id", None)
                    )

            reimbursement_claim = entitlement.submit_reimbursement_claim(
                current_partner,
                received_code,
                supporting_document_file_ids=supporting_document_file_id
                if supporting_document_file_id
                else None,
                amount=actual_amount,
            )

        else:
            # TODO: search and return currently active claim
            # TODO: Check whether entitlement.reimbursement_entitlement_ids[0].partner_id is same as current
            if len(entitlement.reimbursement_entitlement_ids) == 0:
                return request.redirect(f"/serviceprovider/entitlement/{_id}")
            else:
                reimbursement_claim = entitlement.reimbursement_entitlement_ids[0]

        return request.render(
            "g2p_service_provider_portal.reimbursement_form_submitted",
            {
                "entitlement": entitlement.id,
                "submission_date": reimbursement_claim.create_date.strftime("%d-%b-%Y"),
                "application_id": reimbursement_claim.id,
                "user": current_partner.given_name.capitalize(),
            },
        )

    def check_roles(self, role_to_check):
        if role_to_check == "SERVICEPROVIDER":
            if not request.session or not request.env.user:
                raise Unauthorized(_("User is not logged in"))
            if not request.env.user.partner_id.supplier_rank > 0:
                raise Forbidden(
                    _AppendAction("User is not allowed to access the portal")
                )
