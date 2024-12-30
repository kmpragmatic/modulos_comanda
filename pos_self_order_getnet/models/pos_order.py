# -*- coding: utf-8 -*-
import uuid
import logging
from odoo import models, fields
import requests

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = 'pos.order'

    custom_uuid = fields.Char(string='Custom UUID')
    pushy_error = fields.Char(string='Pushy Error')
    pushy_id_payment = fields.Char(string='Pushy ID Pago')
