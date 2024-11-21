from odoo import api, fields, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class PosApiConfig(models.Model):
    _name = 'pos.api.config'

    name = fields.Char()
    payment_delay_validation = fields.Integer('Tiempo de validacion (seg)', default=0)
    min_amount = fields.Integer('Monto mínimo de pago')
    keep_alive = fields.Integer('Tiempo de vida de pago')

    @api.model
    def pre_validate_params(self, payment_id, amount):
        if not payment_id:
            return {'success': False, 'error': 'No se puede realizar la venta'}
        pos_api_config = self.env['pos.payment.method'].browse(payment_id).equipment_id.pos_api_config_id
        if  amount < pos_api_config.min_amount:
            return {'success': False, 'error': 'No se puede realizar una venta por menos de %s' % pos_api_config.min_amount}
        return {'success': True, 'keep_alive':pos_api_config.keep_alive}
