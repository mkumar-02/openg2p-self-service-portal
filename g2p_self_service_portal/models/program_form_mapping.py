from odoo import api, fields, models

class G2PProgram(models.Model):
    _inherit = "g2p.program"

    self_service_portal_form = fields.Many2one(
        "website.page", 
        string="Program Form", 
        domain=[('id', 'not in', [1, 2, 3, 4, 5, 6, 7, 8])]
    )
    
    @api.constrains('self_service_portal_form')
    def update_form_template(self):
        form_id = self.self_service_portal_form.id
        form_view_id = self.env["website.page"].sudo().search([("id", "=", form_id)]).view_id.id
        form_view_template = self.env["ir.ui.view"].sudo().search([("id", "=", form_view_id)]).arch_db

        index = form_view_template.find("</form>")
        csrf_generate_token_text = '<input type="hidden" name="csrf_token" t-att-value="request.csrf_token()"/>'

        if csrf_generate_token_text not in form_view_template:
            form_view_template = form_view_template[:index] + csrf_generate_token_text + form_view_template[index:]
        else:
            pass

        self.env["ir.ui.view"].sudo().search([("id", "=", form_view_id)]).write({'arch_db':form_view_template.replace("website.layout", "g2p_self_service_portal.self_service_form_template")})
    
class G2PCreateProgramWizard(models.TransientModel):
    _inherit = "g2p.program.create.wizard"

    self_service_portal_form = fields.Many2one("website.page", "Program Form", domain=[('id', 'not in', [1, 2, 3, 4, 5, 6, 7, 8])])

