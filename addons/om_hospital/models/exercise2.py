from odoo import models,fields,api,_
from odoo.exceptions import ValidationError


class HospitalInventory(models.Model):
    _name = 'hospital.inventory'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Inventory Records'

    inventory_master = fields.Selection([('Technical parameter', 'Technical parameter'), ('Other parameter', 'Other parameter'), ('Requirement Area', 'Requirement Area')],
        string='Inventory Master Data Type', required=True)
    name_id = fields.Char(string='Name',required=True)

    @api.multi
    def write(self, vals):
        res2 = vals.get('inventory_master')
        if vals.get('inventory_master') == None:
            res2 = self.inventory_master
        res1 = vals.get('name_id')
        if vals.get('name_id') == None:
            res1 = self.name_id

        if self.env['hospital.inventory'].search(['&',('inventory_master', '=', res2),('name_id','=',res1)]):
            raise ValidationError("Duplicate Products are not allowed")
        res = super(HospitalInventory, self).write(vals)

        return res

    @api.model
    def create(self, vals):
        res2 = vals.get('inventory_master')
        res1 = vals.get('name_id')
        if self.env['hospital.inventory'].search(['&',('inventory_master', '=', res2), ('name_id', '=', res1)]):
            raise ValidationError("Duplicate Products are not allowed")
        res = super(HospitalInventory, self).create(vals)
        return res

