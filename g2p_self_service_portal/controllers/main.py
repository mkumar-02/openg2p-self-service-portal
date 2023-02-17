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
        return request.render("g2p_self_service_portal.login_page", qcontext=context)

    @http.route(["/selfservice/logo"], type="http", auth="public")
    def self_service_logo(self, **kwargs):
        config = request.env["ir.config_parameter"].sudo()
        attachment_id = config.get_param(
            "g2p_self_service_portal.self_service_logo_attachment"
        )
        return request.redirect("/web/content/%s" % attachment_id)

    @http.route(["/selfservice/home"], type="http", auth="user")
    def self_service_home(self, **kwargs):
        programs = request.env["g2p.program"].sudo().search([]).sorted("id")
        partner_id = request.env.user.partner_id
        states = {"draft": "Submitted", "enrolled": "Enrolled"}
        ammount_issued = 0
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
            ammount_issued = sum(
                ent.amount_issued
                for ent in request.env["g2p.payment"]
                .sudo()
                .search(
                    [
                        ("partner_id", "=", request.session.uid),
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
                    "issued": ammount_issued,
                    "enrollment_date": membership.enrollment_date.strftime("%d-%b-%Y")
                    if membership.enrollment_date
                    else None,
                }
            )

        return request.render(
            "g2p_self_service_portal.dashboard",
            {
                "programs": values,
                "ammount_issued": ammount_issued,
            },
        )

    @http.route(["/selfservice/allprograms"], type="http", auth="user")
    def self_service_all_programs(self, page="1", limit="5", search="", **kwargs):
        limit = int(limit)
        page = int(page)
        if page < 1:
            page = 1
        if limit < 5:
            limit = 5
        programs = (
            request.env["g2p.program"]
            .sudo()
            .search([], limit=limit, offset=(page - 1) * limit, order="id")
        )

        total = request.env["g2p.program"].sudo().search_count([]) / limit
        total = total.__ceil__()
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

    @http.route(["/selfservice/apply"], type="http", auth="user")
    def self_service_apply_programs(self, **kwargs):
        # Implement applying for programs
        return request.redirect("/selfservice/home")
