from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool

class Project(ModelSQL, ModelView):
    "AFX Project"
    __name__ = 'afx.project'
    _rec_name = 'proj_name'

    no = fields.Char("No")
    customer = fields.Many2One('company.company', "Customer", 'name', required=True)
    end_user = fields.Many2One('company.employee', "End-User", 'name', required=False)
    so_no = fields.Char("S/O No")
    proj_no = fields.Char("Project No")
    proj_date = fields.Date("Project Date")
    proj_name = fields.Char("Project Name")
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    upd_date = fields.Date("Update Date")
    revenue = fields.Char("Revenue")
    closed = fields.Boolean("Closed")
    cancel = fields.Boolean("Cancel")
    user = fields.Many2One('company.employee', "User", 'name', required=False)
    members = fields.One2Many('afx.project.member', 'project', "Members", required=False)
    tasks = fields.One2Many('afx.project.task', 'project', "Tasks", required=False)

