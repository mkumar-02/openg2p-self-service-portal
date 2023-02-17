import xml.etree.ElementTree as ET
from odoo import models, api, fields

class WebsitePage(models.Model):
    _inherit = "website.page"

    base_template = fields.Many2one("ir.ui.view", default=lambda self: self.env.ref("website.layout"))
   
    @api.onchange("base_template")
    def _onchage_base_template(self):
        
        tree = ET.fromstring(self.arch_db)
        base_template = tree[0][0]

        print(base_template.get('t-call'))
        
        base_template.set('t-call',self.base_template.xml_id)

        print(base_template.get('t-call'))



