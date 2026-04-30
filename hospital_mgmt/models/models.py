from odoo import models, fields

class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'

    name = fields.Char(string="Department Name", required=True)
    description = fields.Text(string="Description")
    staff_ids = fields.One2many('hospital.staff', 'department_id', string="Staff Members")

class HospitalStaff(models.Model):
    _name = 'hospital.staff'
    _description = 'Hospital Staff'

    name = fields.Char(string="Name", required=True)
    role = fields.Selection([
        ('doctor', 'Doctor'),
        ('nurse', 'Nurse'),
        ('admin', 'Administrator')
    ], string="Role", required=True)
    department_id = fields.Many2one('hospital.department', string="Department")
    phone = fields.Char(string="Phone")

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient'

    name = fields.Char(string="Name", required=True)
    age = fields.Integer(string="Age")
    gender = fields.Selection([('m', 'Male'), ('f', 'Female')], string="Gender")
    blood_group = fields.Selection([
        ('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('b-', 'B-'), ('o+', 'O+'), ('o-', 'O-'), ('ab+', 'AB+'), ('ab-', 'AB-')
    ], string="Blood Group")
    
    # One2many relationship linking to appointments
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'

    name = fields.Char(string="Appointment ID", required=True, copy=False, readonly=True, default='New')
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('hospital.staff', string="Doctor", domain=[('role', '=', 'doctor')])
    date = fields.Datetime(string="Appointment Date", required=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')
    ], string="Status", default='draft')