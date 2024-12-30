# -*- coding: utf-8 -*-
from odoo import models


class PosConfig(models.Model):
    _inherit = "pos.config"

    @property
    def _ALLOWED_PAYMENT_METHODS(self):
        original_methods = super(PosConfig, self)._ALLOWED_PAYMENT_METHODS
        return original_methods + ['getnet']
