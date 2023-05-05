import json
import logging
from datetime import datetime

from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import Forbidden, Unauthorized

from odoo import _, http
from odoo.http import request

from odoo.addons.auth_oidc.controllers.main import OpenIDLogin

_logger = logging.getLogger(__name__)


class SelfServiceController(http.Controller):
    @http.route(["/selfservice"], type="http", auth="public", website=True)
    def self_service_root(self, **kwargs):
        if request.session and request.session.uid:
            return request.redirect("/selfservice/home")
        else:
            return request.redirect("/selfservice/login")

    @http.route(["/selfservice/login"], type="http", auth="public", website=True)
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
        return request.render("g2p_self_service_portal.login_page", qcontext=context)

    @http.route(["/selfservice/logo"], type="http", auth="public", website=True)
    def self_service_logo(self, **kwargs):
        config = request.env["ir.config_parameter"].sudo()
        attachment_id = config.get_param(
            "g2p_self_service_portal.self_service_logo_attachment"
        )
        return request.redirect("/web/content/%s" % attachment_id)

    @http.route(["/selfservice/myprofile"], type="http", auth="public", website=True)
    def self_service_profile(self, **kwargs):
        if request.session and request.session.uid:
            return request.render("g2p_self_service_portal.profile_page")

    @http.route(["/selfservice/aboutus"], type="http", auth="public", website=True)
    def self_service_about_us(self, **kwargs):
        return request.render("g2p_self_service_portal.aboutus_page")

    @http.route(["/selfservice/contactus"], type="http", auth="public", website=True)
    def self_service_contact_us(self, **kwargs):
        return request.render("g2p_self_service_portal.contact_us")

    @http.route(["/selfservice/otherpage"], type="http", auth="public", website=True)
    def self_service_other_page(self, **kwargs):
        return request.render("g2p_self_service_portal.other_page")

    @http.route(["/selfservice/help"], type="http", auth="public", website=True)
    def self_service_help_page(self, **kwargs):
        return request.render("g2p_self_service_portal.help_page")

    @http.route(["/selfservice/home"], type="http", auth="user", website=True)
    def self_service_home(self, **kwargs):
        self.self_service_check_roles("REGISTRANT")
        query = request.params.get("query")
        domain = [("name", "ilike", query)]
        programs = request.env["g2p.program"].sudo().search(domain).sorted("id")
        partner_id = request.env.user.partner_id
        states = {"draft": "Submitted", "enrolled": "Enrolled"}
        amount_received = 0
        myprograms = []
        for program in programs:
            membership = (
                request.env["g2p.program_membership"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", partner_id.id),
                        ("program_id", "=", program.id),
                    ]
                )
            )
            amount_issued = sum(
                ent.amount_issued
                for ent in request.env["g2p.payment"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", partner_id.id),
                        ("program_id", "=", program.id),
                    ]
                )
            )
            amount_received = sum(
                ent.amount_paid
                for ent in request.env["g2p.payment"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", partner_id.id),
                        ("program_id", "=", program.id),
                    ]
                )
            )
            if len(membership) > 0:
                myprograms.append(
                    {
                        "id": program.id,
                        "name": program.name,
                        "has_applied": len(membership) > 0,
                        "status": states.get(membership.state, "Error"),
                        "issued": "{:,.2f}".format(amount_issued),
                        "paid": "{:,.2f}".format(amount_received),
                        "enrollment_date": membership.enrollment_date.strftime(
                            "%d-%b-%Y"
                        )
                        if membership.enrollment_date
                        else None,
                        "is_latest": (datetime.today() - program.create_date).days < 21,
                        "application_id": membership.application_id
                        if membership.application_id
                        else None,
                    }
                )

        entitlement = sum(
            ent.amount_issued
            for ent in request.env["g2p.payment"]
            .sudo()
            .search([("partner_id", "=", partner_id.id)])
        )
        received = sum(
            ent.amount_paid
            for ent in request.env["g2p.payment"]
            .sudo()
            .search(
                [
                    ("partner_id", "=", partner_id.id),
                ]
            )
        )
        pending = entitlement - received
        labels = ["Received", "Pending"]
        values = [received, pending]
        data = json.dumps({"labels": labels, "values": values})

        return request.render(
            "g2p_self_service_portal.dashboard",
            {"programs": myprograms, "data": data},
        )

    @http.route(["/selfservice/programs"], type="http", auth="user", website=True)
    def self_service_all_programs(self, **kwargs):
        self.self_service_check_roles("REGISTRANT")

        programs = request.env["g2p.program"].sudo().search([])

        partner_id = request.env.user.partner_id
        states = {"draft": "Submitted", "enrolled": "Enrolled"}

        values = []
        for program in programs:
            membership = (
                request.env["g2p.program_membership"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", partner_id.id),
                        ("program_id", "=", program.id),
                    ]
                )
            )
            values.append(
                {
                    "id": program.id,
                    "name": program.name,
                    "has_applied": len(membership) > 0,
                    "status": states.get(membership.state, "Error"),
                    "is_latest": (datetime.today() - program.create_date).days < 21,
                    "is_form_mapped": True
                    if program.self_service_portal_form
                    else False,
                    "is_multiple_form_submission": True
                    if program.multiple_form_submission
                    else False,
                }
            )

        return request.render(
            "g2p_self_service_portal.allprograms",
            {
                "programs": values,
                # "pager": {
                #     "sel": page,
                #     "total": total,
                # },
            },
        )

    @http.route(
        ["/selfservice/apply/<int:_id>"], type="http", auth="user", website=True
    )
    def self_service_apply_programs(self, _id):
        self.self_service_check_roles("REGISTRANT")

        program = request.env["g2p.program"].sudo().browse(_id)
        multiple_form_submission = program.multiple_form_submission
        current_partner = request.env.user.partner_id

        for mem in current_partner.program_membership_ids:
            if mem.program_id.id == _id and not multiple_form_submission:
                return request.redirect(f"/selfservice/submitted/{_id}")
            # elif mem.program_id.id == _id and mem.state == 'enrolled':
            #     return request.redirect(f"/selfservice/submitted/{_id}")

        view = program.self_service_portal_form.view_id

        return request.render(
            view.id,
            {
                "program": program.name,
                "program_id": program.id,
                "user": request.env.user.given_name,
            },
        )

    @http.route(
        ["/selfservice/submitted/<int:_id>"],
        type="http",
        auth="user",
        website=True,
        csrf=False,
    )
    def self_service_form_details(self, _id, **kwargs):
        self.self_service_check_roles("REGISTRANT")

        program = request.env["g2p.program"].sudo().browse(_id)
        current_partner = request.env.user.partner_id

        if request.httprequest.method == "POST":
            form_data = kwargs

            account_num = kwargs.get("Account Number", None)

            if account_num:
                if len(current_partner.bank_ids) > 0:
                    # TODO: Fixing value of first account number for now, if more than one exists
                    current_partner.bank_ids[0].acc_number = account_num
                else:
                    current_partner.bank_ids = [(0, 0, {"acc_number": account_num})]

            program_registrant_info_ids = (
                request.env["g2p.program.registrant_info"]
                .sudo()
                .search(
                    [
                        ("program_id", "=", program.id),
                        ("registrant_id", "=", current_partner.id),
                        ("status", "=", "active"),
                    ]
                )
            )
            program_registrant_info_ids.write({"status": "closed"})
            request.env["g2p.program.registrant_info"].sudo().create(
                {
                    "status": "active",
                    "program_registrant_info": self.jsonize_form_data(
                        form_data, program
                    ),
                    "program_id": program.id,
                    "registrant_id": current_partner.id,
                }
            )

            prog_membs = (
                request.env["g2p.program_membership"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", current_partner.id),
                        ("program_id", "=", program.id),
                    ]
                )
            )
            if len(prog_membs) == 0:
                apply_to_program = {
                    "partner_id": current_partner.id,
                    "program_id": program.id,
                }

                program_member = (
                    request.env["g2p.program_membership"]
                    .sudo()
                    .create(apply_to_program)
                )
            else:
                program_member = prog_membs[0]

        else:
            program_member = (
                request.env["g2p.program_membership"]
                .sudo()
                .search(
                    [
                        ("program_id", "=", program.id),
                        ("partner_id", "=", current_partner.id),
                    ],
                    limit=1,
                )
            )

            if len(program_member) < 1:
                return request.redirect(f"/selfservice/apply/{_id}")

        return request.render(
            "g2p_self_service_portal.self_service_form_submitted",
            {
                "program": program.name,
                "submission_date": program_member.enrollment_date.strftime("%d-%b-%Y"),
                "application_id": program_member.application_id,
                "user": current_partner.given_name.capitalize(),
            },
        )

    def self_service_check_roles(self, role_to_check):
        # And add further role checks and return types
        if role_to_check == "REGISTRANT":
            if not request.session or not request.env.user:
                raise Unauthorized(_("User is not logged in"))
            if not request.env.user.partner_id.is_registrant:
                raise Forbidden(_("User is not allowed to access the portal"))

    def jsonize_form_data(self, data, program):
        for key in data:
            value = data[key]
            if isinstance(value, FileStorage):
                if not program.supporting_documents_store:
                    _logger.error(
                        "Supporting Documents Store is not set in Program Configuration"
                    )
                    data[key] = None
                    continue

                data[key] = self.add_file_to_store(
                    value, program.supporting_documents_store
                )
                if not data.get(key, None):
                    _logger.warning("Empty/No File received for field %s", key)
                    continue

        return data

    @classmethod
    def add_file_to_store(cls, file: FileStorage, store):
        if store and file.filename:
            if len(file.filename.split(".")) > 1:
                supporting_document_ext = "." + file.filename.split(".")[-1]
            else:
                supporting_document_ext = None
            document_file = store.add_file(
                file.stream.read(),
                extension=supporting_document_ext,
            )
            document_uuid = document_file.name.split(".")[0]
            return {
                "document_id": document_file.id,
                "document_uuid": document_uuid,
                "document_name": document_file.name,
                "document_slug": document_file.slug,
                "document_url": document_file.url,
            }
        return None
