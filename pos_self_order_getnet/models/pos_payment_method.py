# coding: utf-8
import logging
import uuid
import requests
import random
from datetime import datetime, timezone
from odoo import fields, models, api, _

_logger = logging.getLogger(__name__)


class PosPaymentMethod(models.Model):
    _inherit = 'pos.payment.method'

    def _get_payment_terminal_selection(self):
        return super()._get_payment_terminal_selection() + [('getnet', 'GetNet')]

    def _payment_request_from_kiosk(self, order):
        if self.use_payment_terminal != 'getnet':
            return super()._payment_request_from_kiosk(order)
        return self._create_request_get_net(order)

    def _create_request_get_net(self, order):
        custom_uuid = str(uuid.uuid4().hex) + 'SESSION' + str(order.session_id.id)
        equipment = self.get_equipment_info()
        url = "https://api.pushy.me/push?api_key=" + equipment.get('token', '')
        data = {
            "to": equipment.get('serial', False),
            "data": {
                "notiTitle": "Nuevo Pago",
                "notiMessage": "Tienes un pago pendiente por $$ %s" % order.amount_total,
                "command": "sale",
                "paymentApp": equipment.get('model', False),
                "data": {
                    "amount": order.amount_total,
                    "ticket": order.name,
                    "printVoucher": False,
                    'employeeId': order.employee_id.id,
                    'saleType': 0,
                    "uuid": custom_uuid
                },
            },
            "notification": {
                "title": "Pago pendiente",
                "body": "Tienes un pago pendiente por $$ %s" % order.amount_total,
                "message": "Tienes un pago por $$ %s" % order.amount_total,
                "badge": 1,
                "sound": "ping.aiff"
            }
        }
        order.custom_uuid = custom_uuid
        try:
            response = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
            response.raise_for_status()
            response_data = response.json()
            if 'error' in response_data:
                order.pushy_error = response_data['error']
                return {'error': response_data['error']}
            order.pushy_id_payment = response_data['id']
            response_data.update({'custom_uuid': custom_uuid, 'validation_delay': equipment.get('validation_delay', False)})
            return response_data
        except requests.exceptions.RequestException as error:
            _logger.error(error)
            order.pushy_error = 'Error al enviar el pago'
            return {'error': 'Error al enviar el pago'}
