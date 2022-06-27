from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from datetime import datetime

class PurchaseJobOrder(models.Model):
    _inherit = 'purchase.order'

    name_seq = fields.Char(string='Job Order ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    flag_id = fields.Boolean(string="job order", default=False, store=True)
    partner_id1 = fields.Many2one('res.partner', string="Vendor")
    order_type = fields.Char(string="Order Type", readonly=True, default="Direct")
    date_order1 = fields.Datetime('Order Date', required=True, index=True, copy=False,
                                  default=fields.Datetime.now)
    currency_id1 = fields.Many2one('res.currency', 'Currency', required=True,
                                   default=lambda self: self.env.user.company_id.currency_id.id)
    company_id1 = fields.Many2one('res.company', 'Company', required=True, index=True,
                                  default=lambda self: self.env.user.company_id.id)
    partner_ref1 = fields.Char('Vendor Reference', copy=False, )
    process = fields.Selection([('Combo Box', 'Combo Box')], string='Processes', required=True)
    received_item = fields.Boolean(string="Same item to be Received")
    date_planned1 = fields.Datetime(string='Scheduled Date', required=True, index=True)
    incoterm_id1 = fields.Many2one('stock.incoterms', string='Incoterm')
    invoice_status1 = fields.Selection([
        ('no', 'Nothing to Bill'),
        ('to invoice', 'Waiting Bills'),
        ('invoiced', 'No Bill to Receive'),
    ], string='Billing Status', store=True, readonly=True, copy=False, default='no')
    payment_term_id1 = fields.Many2one('account.payment.term', 'Payment Terms')
    fiscal_position_id1 = fields.Many2one('account.fiscal.position', string='Fiscal Position',
                                          oldname='fiscal_position')
    date_approve1 = fields.Date('Approval Date', readonly=1, index=True, copy=False)
    order_line1=fields.One2many('purchase.order.line1','connecting',string='Product1')




    # @api.model
    # def create(self, vals):
    #     if 'flag_id' in vals and vals.get('flag_id'):
    #         if vals.get('name', _('New')) == _('New'):
    #             vals['name'] = self.env['ir.sequence'].next_by_code('job.order') or _('New')
    #         result = super(PurchaseJobOrder, self).create(vals)
    #         return result
    #
    #     else:
    #         if vals.get('name', _('New')) == _('New'):
    #             vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order') or _('New')
    #         result = super(PurchaseJobOrder, self).create(vals)
    #         return result

class PurchaseOrderLine1(models.Model):
    _name="purchase.order.line1"

    connecting=fields.Many2one('purchase.order',string="Product")
    name1=fields.Text(string="Description")
    product_id=fields.Many2one('product.product',string="Product")
    product_qty=fields.Float(string="Quantity",required=True)
    date_planned=fields.Datetime(string="Scheduled Date",required=True)
    received_qty=fields.Float(string='Received Qty.',required=True)
    billed_qty=fields.Float(string='Billed Qty.',required=True)
    price_unit=fields.Float(string='Unit Price')
    price_subtotal=fields.Float(string='Subtotal Price')



