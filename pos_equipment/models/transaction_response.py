from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime
import uuid
import logging
import json

_logger = logging.getLogger(__name__)

from odoo.api import depends
from odoo.exceptions import UserError


class TransactionResponse(models.Model):
    _name = 'transaction.response'

    def unlink(self):
        if self.code == '0':
            raise UserError('No puede eliminar un pago validado.')
        return super(TransactionResponse, self).unlink()

    name = fields.Char(readonly=True, compute='_compute_name')

    code = fields.Char()
    message = fields.Char()
    provider = fields.Char()
    data = fields.Json()
    sale_id = fields.Many2one(
        string='Venta vinculada',
        comodel_name='sale.order'
    )

    response_uuid = fields.Char(string="UUID", copy=False, default=None, required=True)
    json_txt = fields.Text(string="JSON Text", readonly=True, compute='_compute_json_txt')

    def _compute_json_txt(self):
        for record in self:
            if record.data:
                try:
                    record.json_txt = json.dumps(record.data, indent=4, sort_keys=True)
                except (TypeError, ValueError) as e:
                    record.json_txt = f"Error al convertir a JSON: {e}"
            else:
                record.json_txt = "{}"

    def _compute_name(self):
        for record in self:
            if isinstance(record.data, str):
                try:
                    data = json.loads(record.data)  # Convertir JSON de texto a diccionario
                except json.JSONDecodeError:
                    data = {}  # Si falla la carga, usar un diccionario vacío
            else:
                data = record.data or {}

            # Buscar el POS Order por el custom_order_uuid
            sale_id = self.env['pos.order'].search([('custom_order_uuid', '=', record.response_uuid)], limit=1)

            # Asignar el pos_reference si se encontró el sale_id
            if sale_id:
                record.name = sale_id.pos_reference

            # Obtener TerminalId y Ticket del JSON
            terminal_id = data.get('TerminalId', '')
            commerce_code = data.get('CommerceCode', '')

            # Concatenar TerminalId y Ticket al nombre
            record.name = f"{record.name or ''} - Terminal: {terminal_id}, Comercio: {commerce_code}"

    @api.model
    def get_payment_uuid_info(self, uuid):
        payment_uuid = self.search([('response_uuid', '=', uuid)], limit=1)
        return {
            'code': payment_uuid.code,
            'uuid': payment_uuid.response_uuid,
            'response': payment_uuid.message
        }

    def _action_send_transaction_notification(self):
        session_str = self.response_uuid or ''
        session_id = session_str.split('SESSION')[1]
        pos_session_sudo = self.env['pos.session'].sudo().browse(int(session_id))
        self.env['bus.bus']._sendone(pos_session_sudo._get_bus_channel_name(), 'PUSHY_NOTIFICATION_PAYMENT', {
            'code': self.code,
            'uuid': session_str.split('SESSION')[0],
            'response': self.message
        })

    def create(self, vals):
        if self.env['transaction.response'].search(
                [('response_uuid', '=', vals.get('response_uuid')), ('code', '=', '0')]):
            raise UserError('El valor UUID ya existe o no puede ser vacio')
        res = super(TransactionResponse, self).create(vals)
        json_getnet = json.loads(res.json_txt)
        res.name = res.response_uuid
        res.code = json_getnet.get('ResponseCode', '103')
        res.message = json_getnet.get('ResponseMessage', '')
        res._action_send_transaction_notification()
        return res
