# -*- coding: utf-8 -*-
import uuid
import logging
from odoo import models, fields
import requests

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = 'pos.order'

    pushy_error = fields.Char(string='Pushy Error')

    def create_payment_from_kiosko(self):
        if self.config_id.self_ordering_mode == 'kiosk':
            payment_method = self.env['pos.payment.method'].search([('equipment_id', '!=', False)], limit=1)
            if payment_method.id:
                custom_uuid = uuid.uuid4().hex
                equipment = payment_method.get_equipment_info()
                if equipment.get('id', False):
                    url = "https://api.pushy.me/push?api_key=" + equipment.get('token', '')
                    data = {
                        "to": equipment.get('serial', False),
                        "data": {
                            "notiTitle": "Nuevo Pago",
                            "notiMessage": "Tienes un pago pendiente por $$ %s" % self.amount_total,
                            "command": "sale",
                            "paymentApp": equipment.get('model', False),
                            "data": {
                                "amount": self.amount_total,
                                "ticket": self.name,
                                "printVoucher": False,
                                'employeeId': self.employee_id.id,
                                'saleType': 0,
                                "uuid": custom_uuid
                            },
                        },
                        "notification": {
                            "title": "Pago pendiente",
                            "body": "Tienes un pago pendiente por $$ %s" % self.amount_total,
                            "message": "Tienes un pago por $$ %s" % self.amount_total,
                            "badge": 1,
                            "sound": "ping.aiff"
                        }
                    }
                    try:
                        response = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
                        if response.status_code != 200:
                            error_message = response.json().get("error", "Unknown error")
                            _logger.error(error_message)
                        response_data = response.json()
                        self.UUID = custom_uuid
                        if 'error' in response_data:
                            self.pushy_error = response_data['error']
                        else:
                            MAKE_PAY = self.env['pos.make.payment']
                            pos_pay = MAKE_PAY.with_context(active_id=self.id).create({
                                'config_id': self.config_id.id,
                                'payment_method_id': payment_method.id,
                            })
                            pos_pay.check()
                    except requests.exceptions.RequestException as error:
                        _logger.error(error)
