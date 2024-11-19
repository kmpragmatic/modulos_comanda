from odoo import models, fields, api
import requests

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    billon_integration = fields.Boolean(string="Billon Integration", config_parameter='billon_integration')
    billon_username = fields.Char(string="Billon Username", config_parameter='billon_username')
    billon_password = fields.Char(string="Billon Password", config_parameter='billon_password')
    billon_service_url = fields.Char(string="Billon Service URL", config_parameter='billon_service_url')
    @api.model
    def get_service_token(self):
        # Obtener la URL del servicio desde los parámetros del sistema
        login_url = '/fapp/v1/auth/login'
        billon_service_url = self.env['ir.config_parameter'].sudo().get_param('billon_service_url')
        username = self.env['ir.config_parameter'].sudo().get_param('billon_username')
        password = self.env['ir.config_parameter'].sudo().get_param('billon_password')

        if not billon_service_url or not username or not password:
            return {'error': 'Parámetros del servicio no configurados'}

        # Construir el payload
        payload = {
            "username": username,
            "password": password
        }

        # Enviar el request
        response = requests.post(billon_service_url + login_url, json=payload)
        if response.status_code == 200:
            token = response.json().get('token')
            if token:
                # Guardar el token en otro parámetro del sistema
                self.env['ir.config_parameter'].sudo().set_param('billon_token', token)
                return {'success': 'Token guardado correctamente'}
            else:
                return {'error': 'Token no encontrado en la respuesta'}
        else:
            return {'error': f'Error en el request: {response.status_code}'}