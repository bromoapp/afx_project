from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import Pool

class ProjectMember(ModelSQL, ModelView):
    "AFX Project Member"
    __name__ = "afx.project.member"
    _rec_name = 'proj_name'

    project = fields.Many2One('afx.project', "Project", "proj_name", required=True)
    member = fields.Many2One('company.employee', "Member", 'name', required=False)
    role = fields.Char("Role")
