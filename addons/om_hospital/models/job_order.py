from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from  datetime import  datetime
class ResPartner1(models.Model):
    _inherit = 'res.partner'


class PurchaseJobOrder(models.Model):
    _inherit = 'purchase.order'

    name_seq = fields.Char(string='Job Order ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    flag_id = fields.Boolean(string="job order", default=False, store=True)
    partner_id1 = fields.Many2one('res.partner', string='Vendor', required=True, track_visibility='always')
    order_type = fields.Char(string="Order Type", readonly=True, default="Direct")
    date_order1 = fields.Datetime('Order Date', required=True, index=True, copy=False,
                                  default=fields.Datetime.now)
    currency_id1 = fields.Many2one('res.currency', 'Currency', required=True,
                                   default=lambda self: self.env.user.company_id.currency_id.id)
    company_id1 = fields.Many2one('res.company', 'Company', required=True, index=True,
                                  default=lambda self: self.env.user.company_id.id)
    partner_ref1 = fields.Char('Vendor Reference')
    process = fields.Selection([('Combo Box', 'Combo Box')], string='Processes', required=True)
    received_item = fields.Boolean(string="Same item to be Received")
    incoterm_id1 = fields.Many2one('stock.incoterms', string='Incoterm')
    invoice_status1 = fields.Selection([
        ('no', 'Nothing to Bill'),
        ('to invoice', 'Waiting Bills'),
        ('invoiced', 'No Bill to Receive'),
    ], string='Billing Status', store=True, readonly=True, copy=False, default='no')
    payment_term_id1 = fields.Many2one('account.payment.term', 'Payment Terms')
    date_planned1 = fields.Datetime(string='Scheduled Date')
    fiscal_position_id1 = fields.Many2one('account.fiscal.position', string='Fiscal Position',
                                          oldname='fiscal_position')
    date_approve1 = fields.Date('Approval Date', readonly=1, index=True, copy=False)
    order_line1 = fields.One2many('purchase.order.line1', 'connect', string='Order Lines')
    order_line2 = fields.One2many('purchase.order.line1', 'connect1', string='Order Lines')

    @api.model
    def create(self, vals):
        if 'flag_id' in vals and vals.get('flag_id'):
            if vals.get('name_seq', _('New')) == _('New'):
                vals['name_seq'] = self.env['ir.sequence'].next_by_code('job.order') or _('New')
            result = super(PurchaseJobOrder, self).create(vals)
            return result

        else:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('purchase.order') or _('New')
            result = super(PurchaseJobOrder, self).create(vals)
            return result

class PurchaseOrderLine1(models.Model):
    _name = 'purchase.order.line1'


    date_planned = fields.Datetime(string='Scheduled Date')
    connect = fields.Many2one('purchase.order', string="Product")
    connect1 = fields.Many2one('purchase.order', string="Product")
    product_id = fields.Many2one('product.product',  string='Product')
    name = fields.Text(string='Description')
    product_qty = fields.Float(string='Quantity')
    price_unit = fields.Float(string='Unit Price')
    qty_invoiced = fields.Float(string="Billed Qty", store=True)
    qty_received = fields.Float(string="Received Qty", store=True)
    price_subtotal = fields.Float(string='Subtotal', store=True, compute='_compute_amount')
    currency_id = fields.Many2one('res.currency', 'Currency',
                                   default=lambda self: self.env.user.company_id.currency_id.id)
    notes = fields.Text('Terms and Conditions')
    amount_untaxed = fields.Float(string='Untaxed Amount', store=True, readonly=True)
    amount_tax = fields.Float(string='Taxes', store=True, readonly=True)
    amount_total = fields.Float(string='Total', store=True)
    taxes_id = fields.Float(string='Taxes', store= True)

    price_total = fields.Float(string='Total', store=True)
    price_tax = fields.Float(string='Tax', store=True)


    @api.depends('product_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            amount = 1
            amount = line.product_qty * line.price_unit
            line.update({
                'price_subtotal': amount,
            })






