from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool

class ProjectTask(ModelSQL, ModelView):
    "AFX Project Task"
    __name__ = "afx.project.task"

    project = fields.Many2One('afx.project', "Project", "proj_name", required=True)
    task_name = fields.Char("Task Name")
    task_detail = fields.Char("Task Detail")
    pic = fields.Many2One('company.employee', "PIC", 'name', required=False)
    est_start_date = fields.Date("Est Start Date")
    est_end_date = fields.Date("Est End Date")
    est_days = fields.Char("Est Days", readonly=True)
    est_hours = fields.Float('Est Hours',
        digits=(16, 2))
    real_start_date = fields.Date("Real Start Date")
    real_end_date = fields.Date("Real End Date")
    real_days = fields.Char("Real Days")
    real_hours = fields.Float('Real Hours',
        digits=(16, 2))
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ], 'Priority', required=True)
    status = fields.Selection([
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('done', 'Done'),
        ('canceled', 'Canceled'),
        ], 'Status', required=True)
