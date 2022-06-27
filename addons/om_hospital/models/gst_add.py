
from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
import re


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    tax_apply = fields.Boolean(string="Tax Apply")

    @api.onchange('partner_id')
    def tax_apply_fun(self):
        self.tax_apply = False
        if self.partner_id.vat:
            self.tax_apply = True


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'
    @api.model
    def create(self, vals):
        res = super(ResPartnerInherit, self).create(vals)

        return res

    @api.multi
    def write(self, vals):
        res = super(ResPartnerInherit, self).write(vals)
        if self.vat:
            self.vatValidation()
        return res


    def vatValidation(self):
        for rec in self:
            if rec.state_id.l10n_in_tin and self.vat and rec.country_id.name == "India":
                if self.state_id.l10n_in_tin != self.vat[:2]:
                    raise ValidationError(_("gst no not valid"))

    @api.onchange('vat')
    def do_stuff(self):
        try:
            # CHECK FORMAT AND SHOW WARNING
            if not ((self.vat)):
                return
            # record.vat = record.vat.upper()
            if (len(self.vat) != 15):
                return {
                    'warning': {'title': 'Warning',
                                'message': 'Invalid GSTIN. GSTIN number must be 15 digits. Please check.', },
                }
            # raise ValidationError("Invalid GSTIN. GSTIN number must be 15 digits. Please check.")
            if not (re.match("\d{2}[A-Z]{5}\d{4}[A-Z]{1}\d[Z]{1}[A-Z\d]{1}", self.vat.upper())):
                return {
                    'warning': {'title': 'Warning',
                                'message': 'Invalid GSTIN format.\r\n.GSTIN must be in the format nnAAAAAnnnnA_Z_ where n=number, A=alphabet, _=either.', },
                }
            # raise ValidationError("Invalid GSTIN.\r\n.GSTIN must be in the format nnAAAAAnnnnA_Z_ where n=number, A=alphabet, _=either.");
            if not (ResPartnerInherit.check_gstin_chksum(self.vat)):
                return {
                    'warning': {'title': 'Warning',
                                'message': 'Invalid GSTIN. Checksum validation failed. It means one or more characters are probably wrong.', },
                }
            # raise ValidationError("Invalid GSTIN. Checksum validation failed. It means one or more characters are probably wrong.")
            # CAPITALIZE GST NUMBER
            self.vat = self.vat.upper()
        except:
            pass


