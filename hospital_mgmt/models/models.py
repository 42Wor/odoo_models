from odoo import models, fields

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient'

    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    gender = fields.Selection([('m', 'Male'), ('f', 'Female')], string="Gender")
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
  
class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'

    name = fields.Char(string="ID", required=True, default="New")
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    date = fields.Date(string="Date")