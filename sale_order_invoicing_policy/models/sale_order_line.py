# -*- coding: utf-8 -*-
# Copyright 2019 Quartile Limited
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Overwriting original _get_to_invoice_qty method
    # Ref: https://github.com/odoo/odoo/blob/43bf9ff29d1897405a575fa8643b7f80b5112c24/addons/sale/models/sale.py#L746-L759
    # Changes: Making the compute method depends on
    #          order_id.sale_invoice_policy
    #          
    @api.depends('qty_invoiced', 'qty_delivered', 'product_uom_qty',
                 'order_id.state', 'order_id.sale_invoice_policy')
    def _get_to_invoice_qty(self):
        for line in self:
            if line.order_id.state in ['sale', 'done']:
                if line.product_id.type == 'service':
                    invoice_policy = line.product_id.invoice_policy
                else:
                    invoice_policy = line.order_id.sale_invoice_policy or \
                                     line.product_id.invoice_policy
                if invoice_policy == 'order':
                    line.qty_to_invoice = line.product_uom_qty - \
                                          line.qty_invoiced
                else:
                    line.qty_to_invoice = line.qty_delivered - \
                                          line.qty_invoiced
            else:
                line.qty_to_invoice = 0