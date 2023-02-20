from datetime import date, datetime
import json
import random
from odoo import http
from odoo.http import request
from math import ceil

from odoo.addons.auth_oidc.controllers.main import OpenIDLogin


class SelfServiceContorller(http.Controller):
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

    @http.route(["/selfservice/home"], type="http", auth="user", website=True)
    def self_service_home(self, **kwargs):
        query = kwargs.get('q', '')
        domain = [('name', 'ilike', query)]
   
        programs = request.env["g2p.program"].sudo().search(
            domain).sorted("id")
        partner_id = request.env.user.partner_id
        states = {"draft": "Submitted", "enrolled": "Enrolled"}
        ammount_issued = 0
        amount_received = 0
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
            # date = datetime.strptime(membership['enrollment_date'], '%Y-%m-%d')
            # output_date = date.strftime('%d-%b-%Y')
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
            values.append(
                {
                    "id": program.id,
                    "name": program.name,
                    "has_applied": len(membership) > 0,
                    "status": states.get(membership.state, "Error"),
                    "issued": "{0: .2f}".format(amount_issued),
                    "paid": "{0: .2f}".format(amount_received),
                    "enrollment_date": membership.enrollment_date.strftime("%d-%b-%Y")
                    if membership.enrollment_date
                    else None,
                    "is_latest": (datetime.today() - program.create_date).days < 21,
                    "application_id": membership.application_id if membership.application_id
                    else None,
                }
            )

        entitlement = sum(
            ent.amount_issued
            for ent in request.env["g2p.payment"]
            .sudo()
            .search(
                [
                    ("partner_id", "=", partner_id.id)

                ]
            )
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
        return request.render(
            "g2p_self_service_portal.dashboard",
            {
                "programs": values,
                "received": str(received),
                "pending": str(pending)
            },
        )

    @http.route(["/selfservice/allprograms"], type="http", auth="user", website=True)
    def self_service_all_programs(self, page="1", limit="7", **kwargs):
        limit = int(limit)
        page = int(page)
        query = kwargs.get('q', '')
        domain = [('name', 'ilike', query)]

        if page < 1:
            page = 1
        if limit < 5:
            limit = 5
        programs = (
            request.env["g2p.program"]
            .sudo()
            .search(domain, limit=limit, offset=(page - 1) * limit, order="id")
        )

        total = ceil(request.env["g2p.program"].sudo().search_count([]) / limit)

        # page_info = pager('/selfservice/allprograms',total=total,page=page,step=5)

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
                    "is_latest": (datetime.today() - program.create_date).days < 21

                }
            )

        return request.render(
            "g2p_self_service_portal.allprograms",
            {
                "programs": values,
                "pager": {
                    "sel": page,
                    "total": total,
                },
            },
        )

    @http.route(["/selfservice/apply"], type="http", auth="user", website=True)
    def self_service_apply_programs(self, **kwargs):
        program = request.env['g2p.program'].sudo().search([("id", "=", kwargs['id'])])

        return request.render(
            "g2p_self_service_portal.self_service_default_form",
            {"program": program},
        )

    @http.route(["/selfservice/submitted"], type="http", auth="user", website=True)
    def self_service_form_details(self, **kwargs):

        form_data = {}
        current_user = request.env.user
        form_data['address'] = json.dumps(kwargs)
        form_data['additional_info'] = json.dumps(kwargs)

        request.env['res.partner'].sudo().search(
            [("name", "=", current_user.name)]).write(form_data)

        program_id = kwargs['id']

        today_date = datetime.date.today().strftime("%d-%b-%Y")

        d = datetime.date.today().strftime("%d")
        m = datetime.date.today().strftime("%m")
        y = datetime.date.today().strftime("%y")

        random_number = str(random.randint(1, 100000))

        def random_number_length(n):
            n = str(n)
            l = len(n)
            if (l < 5):
                while l > 5:
                    n = '0' + n
                    l = l + 1
                return '0' + n

            return n

        application_id = int(d + m + y + random_number_length(random_number))

        apply_to_program = {
            'partner_id': current_user.partner_id.id,
            'program_id': program_id,
            'application_id': application_id
        }

        request.env['g2p.program_membership'].sudo().create(apply_to_program)

        return request.render(
            "g2p_self_service_portal.self_service_form_submitted",
            {
                "submission_date": today_date,
                "application_id": application_id
            },
        )
