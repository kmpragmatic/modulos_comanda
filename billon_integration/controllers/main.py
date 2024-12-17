import json
import logging
import requests
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class BillonApi(http.Controller):

    @http.route(['/odoo_invoice'], type="json", auth="none", csrf=False,
                methods=['POST'])
    def send_invoice(self):
        # Obtener la factura

        boletas_url = '/fapp/sii/docs/v1/generarboleta'

        token = request.env['ir.config_parameter'].sudo().get_param('billon_token')
        headers = { 'Authorization': 'Bearer ' + token,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json' }

        if not token:
            return {'error': 'Token no encontrado'}
        account_move_id = json.loads(request.httprequest.data).get('account_move_id')
        if not account_move_id:
            return {'error': 'account_move_id no proporcionado'}
        account_move = request.env['account.move'].sudo().browse(account_move_id)


        # Obtener la URL del servicio desde los parámetros del sistema
        service_url = request.env['ir.config_parameter'].sudo().get_param('billon_service_url')
        if not service_url:
            return {'error': 'URL del servicio no configurada'}

        # Construir el payload
        payload = {
            "rutEmisor": account_move.company_id.vat if account_move.company_id.vat else "66666666-6",
            "rutFirmante": account_move.company_id.company_registry if account_move.company_id.company_registry else "66666666-6",
            "dtes": [
                {
                    "tipodocumento": "BOLETA_AFECTA",
                    "fechaemision": account_move.invoice_date.strftime('%Y-%m-%d') if account_move.invoice_date else "2024-01-01",
                    "receptor": {
                        "rut": account_move.partner_id.vat if account_move.partner_id.vat else "66666666-6",
                        "razonsocial": account_move.partner_id.name if account_move.partner_id else ""
                    },
                    "codigointerno": "RFG111",
                    "detalle": [
                        {
                            "nombreproducto": line.product_id.name,
                            "cantidadproducto": line.quantity,
                            "precioItem": line.price_unit,
                            "montoitem": line.price_subtotal
                        } for line in account_move.invoice_line_ids
                    ],
                    "referencias": [
                        {
                            "codref": "SET",
                            "razonref": "CASO-1",
                            "tpodocref": "39",
                            "folioref": "6"
                        }
                    ]
                }
            ]
        }

        _logger.info("payload")
        _logger.info(payload)

        # Enviar el request
        response = requests.post(service_url + boletas_url, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        return {'error': 'Error en la conexion con billonapp'}
