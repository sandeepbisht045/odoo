# -*- coding: utf-8 -*-

from odoo import models, fields




class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherits = {'hospital.patient': 'related_patient_id'}
    _description = 'Doctor Record'

    name = fields.Char(string="Name", required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('fe_male', 'Female'),
    ], default='male', string="Gender")
    user_id = fields.Many2one('res.users', string='Related User')
    patient_id = fields.Many2one('hospital.patient', string='Related Patient')
    related_patient_id = fields.Many2one('hospital.patient', string='Related Patient ID')