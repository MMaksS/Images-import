from odoo import models,api
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import base64
import requests

class Import(models.TransientModel):

    _inherit = 'base_import.import'
    
    @api.multi
    def _parse_import_data(self, data, import_fields, options):
        data = super(Import,self)._parse_import_data(data, import_fields, options)
        all_fields = self.env[self.res_model].fields_get()
        for name, field in all_fields.items():
            if field['type'] in ('binary') and name in import_fields:
                index = import_fields.index(name)
                for line in data:
                    if not line[index]:
                        continue
                    parsed_url = urlparse(line[index])
                    if parsed_url.scheme:
                        try:
                            content = base64.b64encode(requests.get(line[index]).content)
                        except Exception as e:
                            content = ''
                            pass
                        line[index] = content
                    
        return data

