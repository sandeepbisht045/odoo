from odoo import models, fields, api, _
class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    appointment_date = fields.Date(string="Appointment Date")

    def print_report(self):
        data = {
            'model': 'create.appointment',
            'form': self.read()[0]
        }
        # if data['form']['patient_id']:
        #     selected_patient = data['form']['patient_id'][0]
        #     appointments = self.env['hospital.appointment'].search([('patient_id', '=', selected_patient)])
        # else:
        #     appointments = self.env['hospital.appointment'].search([])
        # appointment_list = []
        # for app in appointments:
        #     vals = {
        #         'name': app.name,
        #         'notes': app.notes,
        #         'appointment_date': app.appointment_date
        #     }
        #     appointment_list.append(vals)
        # # print("appointments", appointments)
        # data['appointments'] = appointment_list
        # # print("Data", data)
        return self.env.ref('om_hospital.report_appointment').with_context(landscape=True).report_action(self,
                                                                                                         data=data)

    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date,
            'notes': 'Created From The Wizard/Code'
        }
        self.patient_id.message_post(body="Test string ", subject="Appointment Creation")
        # creating appointments from the code
        new_appointment = self.env['hospital.appointment'].create(vals)
        context = dict(self.env.context)
        import logging
        _logger = logging.getLogger(__name__)
        _logger.info("account.py cornerstone_account calling")
        context['form_view_initial_mode'] = 'edit'
        return {'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hospital.appointment',
                'res_id': new_appointment.id,
                'context': context
                }

    def delete_patient(self):
        for rec in self:
            rec.patient_id.unlink()

    def get_data(self):
        appointments = self.env['hospital.appointment'].search([])
        for rec in appointments:
            print("Appointment Name", rec.name)
        return {
            "type": "ir.actions.do_nothing"
        }
