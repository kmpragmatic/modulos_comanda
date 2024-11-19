from odoo import models, api
from odoo.http import request
import requests

from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def send_invoice_data(self):
        # Call the controller
        url = request.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/odoo_invoice'
        payload = {
            'account_move_id': self.id
        }
        headers = {
            'Content-Type': 'application/json',
        }
        cookies = request.httprequest.cookies
        response = requests.get(url, json=payload, headers=headers, cookies=cookies)
        response_data = response.json()

        # Handle the response
        if 'error' in response_data:
            raise UserError(response_data['error'])
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': 'Invoice data sent successfully',
                    'type': 'success',
                    'sticky': False,
                }
            }