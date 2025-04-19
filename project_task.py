from trytond.model import ModelSQL, ModelView, fields
from trytond.pyson import Bool, Eval
from trytond.pool import Pool
import logging

logger = logging.getLogger(__name__)

class ProjectTask(ModelSQL, ModelView):
    "Activity"
    __name__ = "afx.project.task"
    _rec_name = 'activity'

    # Hardcoded
    MAIN_COMPANY = 1

    unique_id = fields.Char("Uuid")
    project = fields.Many2One('afx.project', "Project")
    activity = fields.Text("Activity")
    pic = fields.Many2One('afx.project.member', "User", required=False, domain=[
        ('project', '=', Eval('project'))
    ])
    start_time = fields.Time("Start Time")
    end_time = fields.Time("End Time")
    total_hours = fields.Float('Total Hours',digits=(16, 2))
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ], 'Priority')
    status = fields.Selection([
        ('to_do', 'To Do'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('done', 'Done'),
        ('canceled', 'Canceled'),
        ], 'Status')

    # ------- DEFAULT VALUES --------    
    @classmethod
    def default_priority(cls):
        return 'medium'
    
    @classmethod
    def default_status(cls):
        return 'to_do'
