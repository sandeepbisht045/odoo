from odoo import models,fields,api,_
from odoo.exceptions import  ValidationError

class SaleOrderInherit(models.Model):
    _inherit='sale.order'
    patient_name=fields.Char(string="Patient Name")
    # ----------------------------------------------
    tax_invisible = fields.Boolean(string="tax1")
    @api.onchange('partner_id')
    def tax_invisible_fun(self):
        self.tax_invisible = False
        if self.partner_id.vat:
            self.tax_invisible = True
            # -----------------------------


class ResPartners(models.Model):
    _inherit = 'res.partner'

    # How to OverRide Create Method Of a Model
    @api.model
    def create(self, vals_list):
        res = super(ResPartners, self).create(vals_list)
        print("yes working")
        # do the custom coding here
        return res



class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Patient Record'
    patient_name = fields.Char(string='Name',required=True,track_visibility="always")
    patient_age = fields.Integer('Age',track_visibility="always")
    patient_contact = fields.Integer('Contact')
    name = fields.Char(string='Test')
    name_seq = fields.Char(string='Patient ID', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    notes = fields.Text(string="Registration Note")
    appointment_count = fields.Integer(string='Appointment', compute='get_appointment_count')
    active=fields.Boolean("Active",default=True)
    patient_name_upper=fields.Char(compute='_compute_upper_name',inverse='_inverse_upper_name')

    @api.onchange('doctor_id')
    def set_doctor_gender(self):
        for rec in self:
            if rec.doctor_id:
                rec.doctor_gender = rec.doctor_id.gender

    @api.model
    def test_cron_job(self):
        print("abcd")

    @api.constrains("patient_age")
    def check_age(self):
        for rec in self:
            if rec.patient_age<=5:
                raise  ValidationError(_("The age must be greater than 5"))

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if rec.patient_age < 18:
                    rec.age_group = 'minor'
                else:
                    rec.age_group = 'major'

    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male', string="Gender")

    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor'),
    ], string="Age Group", compute='set_age_group', store=True)

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result

    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count

    @api.multi
    def open_patient_appointments(self):
        return {
            'name': _('Appointments'),
            'domain': [('patient_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    @api.multi
    def name_get(self):
        # name get function for the model executes automatically
        res = []
        for rec in self:
            res.append((rec.id, '%s - %s' % (rec.name_seq,rec.patient_name)))
        return res

    def action_send_card(self):
        # sending the patient report to patient via email
        template_id = self.env.ref('om_hospital.patient_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)

    @api.depends('patient_name')
    def _compute_upper_name(self):
        for rec in self:
            rec.patient_name_upper=rec.patient_name_upper() if rec.patient_name else False

    def _inverse_upper_name(self):
        for rec in self:
            rec.patient_name=rec.patient_name_upper().lower() if rec.patient_name_upper else False

