import json
import random
from datetime import datetime
import logging
from urllib.parse import urlencode

import werkzeug
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

    @http.route(["/selfservice/aboutus"], type="http", auth="public", website=True)
    def self_service_about_us(self, **kwargs):
        return request.render("g2p_self_service_portal.aboutus_page")

    @http.route(["/selfservice/contactus"], type="http", auth="public", website=True)
    def self_service_contact_us(self, **kwargs):
        return request.render("g2p_self_service_portal.contact_us")

    @http.route(["/selfservice/staticpage"], type="http", auth="public", website=True)
    def self_service_static_page(self, **kwargs):
        return request.render("g2p_self_service_portal.static_page")

    @http.route(["/selfservice/errorpage"], type="http", auth="public", website=True)
    def self_service_error_page(self, **kwargs):
        return request.render("g2p_self_service_portal.error_page")

    @http.route(["/selfservice/home"], type="http", auth="user", website=True)
    def self_service_home(self, **kwargs):
        query = request.params.get('query')
        domain = [('name', 'ilike', query)]

        programs = request.env["g2p.program"].sudo().search(
            domain).sorted("id")
        partner_id = request.env.user.partner_id
        states = {"draft": "Submitted", "enrolled": "Enrolled"}
        ammount_issued = 0
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
            myprograms.append(
                {
                    "id": program.id,
                    "name": program.name,
                    "has_applied": len(membership) > 0,
                    "status": states.get(membership.state, "Error"),
                    "issued": "{:,.2f}".format(amount_issued),
                    "paid": "{:,.2f}".format(amount_received),
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
        labels = ["Received","Pending"]
        values = [received,pending]
        data = json.dumps({"labels": labels,
                "values": values})

        return request.render(
            "g2p_self_service_portal.dashboard",
            {
                "programs": myprograms,
                "data":data

            },
        )

    @http.route(["/selfservice/programs"], type="http", auth="user", website=True)
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
        form_id = program["self_service_portal_form"].id

        if form_id == False:
            return "No form mapped with this program"
        
        form_url = request.env['website.page'].sudo().search([("id", "=", form_id)])['url']

        request.env['website.page'].sudo().search([("id", "=", form_id)]).write({'url': form_url.replace(form_url, '/selfservice/apply-' + str(form_id))})
        form_url = request.env['website.page'].sudo().search([("id", "=", form_id)])['url']

        current_user = request.env.user
        data = {
            'program': program['name'],
            'user': current_user.name.split(' ')[0].replace(',', '')
        }

        params = urlencode(data)
        redirect_url = form_url+ '?' + params

        return werkzeug.utils.redirect(redirect_url)
     
    
    @http.route(["/selfservice/submitted"], type="http", auth="user", website=True)
    def self_service_form_details(self, **kwargs):

        form_data = {}
        current_user = request.env.user
        form_data['additional_info'] = json.dumps(kwargs)

        request.env['res.partner'].sudo().search(
            [("name", "=", current_user.name)]).write(form_data)

        program = kwargs['program']
        program_id = request.env['g2p.program'].sudo().search([("name", "=", program)]).id
        
        today_date = datetime.today().strftime("%d-%b-%Y")

        d = datetime.today().strftime("%d")
        m = datetime.today().strftime("%m")
        y = datetime.today().strftime("%y")

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
                "program": kwargs['program'],
                "submission_date": today_date,
                "application_id": application_id,
                'user': current_user.name.split(' ')[0].replace(',', '')
            },
        )
