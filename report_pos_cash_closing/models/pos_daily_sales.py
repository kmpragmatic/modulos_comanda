# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class PosDailyReport(models.TransientModel):
    _inherit = 'pos.daily.sales.reports.wizard'

    @api.model
    def create_report_from_ui(self, pos_session_id):
        res = self.create({
            'pos_session_id': pos_session_id,
            'template_to_use': 'sec',
        })
        return res.generate_report()

    template_to_use = fields.Selection([
        ('original', 'Original'),
        ('sec', 'Personalizada'),
    ], string="Plantilla", default="sec")

    def generate_report(self):
        data = {
            'date_start': False,
            'date_stop': False,
            'config_ids': self.pos_session_id.config_id.ids,
            'session_ids': self.pos_session_id.ids,
            'template_to_use': self.template_to_use
        }
        report_id = self.env.ref('point_of_sale.sale_details_report')

        if self.template_to_use == "sec":
            paperformat_id = self.env.ref('report_pos_cash_closing.paperformat_cash_closing_custom').id
            report_id.paperformat_id = paperformat_id

        return report_id.report_action([], data=data)


class CustomReportSaleDetails(models.AbstractModel):
    _inherit = 'report.point_of_sale.report_saledetails'

    @api.model
    def get_sale_details(self, date_start=False, date_stop=False, config_ids=False, session_ids=False,
                         template_to_use=False):
        # Llamar al método original para obtener los datos por defecto
        sale_details = super(CustomReportSaleDetails, self).get_sale_details(
            date_start=date_start,
            date_stop=date_stop,
            config_ids=config_ids,
            session_ids=session_ids
        )

        # Asegurarnos de tener sesiones
        sessions = self.env['pos.session'].search([('id', 'in', session_ids)])
        if not sessions:
            return sale_details

        # Obtener el cajero
        cajero = sessions[0].user_id.name if len(sessions) == 1 else ''

        # Monto inicial del turno
        monto_inicial_turno = sessions[0].cash_register_balance_start if len(sessions) == 1 else 0

        # Monto total de ventas
        monto_total_ventas = sum(
            order.amount_total for order in self.env['pos.order'].search([('session_id', 'in', session_ids)]))

        # Monto total de ventas en efectivo
        payments = self.env["pos.payment"].search([('pos_order_id.session_id', 'in', session_ids)])
        monto_total_ventas_efectivo = sum(
            payment.amount for payment in payments if payment.payment_method_id.is_cash_count)

        # Total ingresos
        total_ingresos = sum(payment.amount for payment in
                             self.env['pos.payment'].search([('pos_order_id.session_id', 'in', session_ids)]))

        # Total retiros
        cash_moves = self.env['account.bank.statement.line'].search([('pos_session_id', 'in', session_ids)])
        total_retiros = sum(move.amount for move in cash_moves if move.amount < 0)

        # Total del turno
        total_turno = monto_inicial_turno + total_ingresos - total_retiros

        # Total del turno en efectivo
        total_turno_efectivo = monto_total_ventas_efectivo - total_retiros

        # Disponible cajero
        disponible_cajero = sessions[0].cash_register_balance_end_real if len(sessions) == 1 else 0

        # Total ventas por medio de pago
        total_ventas_medio_pago = []
        for payment in payments:
            payment_method = payment.payment_method_id.name
            existing_payment = next((item for item in total_ventas_medio_pago if item['method'] == payment_method),
                                    None)
            if existing_payment:
                existing_payment['total'] += payment.amount
            else:
                total_ventas_medio_pago.append({
                    'method': payment_method,
                    'total': payment.amount
                })

        sale_details.update({
            'cajero': cajero,
            'monto_inicial_turno': monto_inicial_turno,
            'monto_total_ventas': monto_total_ventas,
            'monto_total_ventas_efectivo': monto_total_ventas_efectivo,
            'total_ingresos': total_ingresos,
            'total_retiros': total_retiros,
            'total_turno': total_turno,
            'total_turno_efectivo': total_turno_efectivo,
            'disponible_cajero': disponible_cajero,
            'total_ventas_medio_pago': total_ventas_medio_pago,
            'total_ventas_tipo_documento': self.get_gruop_by_type_document_invoice_session(sessions[0]),
        })

        # Si se ha pasado un template específico para usar
        if template_to_use:
            sale_details['template_to_use'] = template_to_use

        return sale_details

    def get_gruop_by_type_document_invoice_session(self, session):
        gruop_invoice_by_type_document = {}
        for order in session.order_ids.filtered(lambda o: o.is_invoiced):
            document_type = order.account_move.l10n_latam_document_type_id
            if not document_type:
                document_type = '(Sin tipo)'
            else:
                document_type = document_type.name

            if gruop_invoice_by_type_document.get(document_type):
                gruop_invoice_by_type_document[document_type]['total'] += order.account_move.amount_total
            else:
                gruop_invoice_by_type_document[document_type] = {
                    'total': order.account_move.amount_total,
                    'name': document_type
                }

        return gruop_invoice_by_type_document
