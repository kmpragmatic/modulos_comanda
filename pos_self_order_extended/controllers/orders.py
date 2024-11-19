# -*- coding: utf-8 -*-
from odoo import http, fields
from odoo.http import request
from odoo.tools import float_is_zero
from odoo.addons.pos_self_order.controllers.orders import PosSelfOrderController
import logging

_logger = logging.getLogger(__name__)


class PosSelfOrderControllerExtended(PosSelfOrderController):
    @http.route("/pos-self-order/process-new-order/<device_type>/", auth="public", type="json", website=True)
    def process_new_order(self, order, access_token, table_identifier, device_type):
        export_for_self_order = super(PosSelfOrderControllerExtended, self).process_new_order(order, access_token,
                                                                                              table_identifier,
                                                                                              device_type)
        order_id = export_for_self_order.get('id', False)
        if device_type == 'kiosk' and order_id:
            new_order = request.env["pos.order"].browse(order_id)
            new_order.create_payment_from_kiosko()
        return export_for_self_order
