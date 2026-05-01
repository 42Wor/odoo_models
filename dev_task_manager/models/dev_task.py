from odoo import models, fields, api

class DevTask(models.Model):
    _name = 'dev.task'
    _description = 'Developer Task'
    _order = 'priority desc, id desc' # Orders by High Priority first, then newest

    name = fields.Char(string='Task Title', required=True)
    description = fields.Text(string='Description')
    
    developer_id = fields.Many2one(
        'res.users', 
        string='Assigned Developer', 
        default=lambda self: self.env.user,
        required=True
    )
    
    priority = fields.Selection([
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High')
    ], string='Priority', default='normal', required=True)
    
    # THE FIX: group_expand=True forces the Kanban board to ALWAYS show 
    # all 3 columns, even if they are completely empty!
    state = fields.Selection([
        ('draft', 'New'),
        ('in_progress', 'In Progress'),
        ('done', 'Completed')
    ], string='Status', default='draft', group_expand=True)

    # --- Business Logic Methods ---

    def action_start_work(self):
        for record in self:
            record.state = 'in_progress'

    def action_mark_done(self):
        for record in self:
            record.state = 'done'

    def action_reset_draft(self):
        for record in self:
            record.write({
                'state': 'draft',
                'priority': 'normal'
            })

    def action_delete_task(self):
        self.unlink()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tasks',
            'res_model': 'dev.task',
            'view_mode': 'kanban,list,form',
            'target': 'current',
        }

