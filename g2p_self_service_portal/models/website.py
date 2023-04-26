# Part of OpenG2P. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class WebsitePage(models.Model):
    _inherit = "website.page"

    is_program_form_page = fields.Boolean("Program Form Page")
