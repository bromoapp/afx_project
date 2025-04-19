from trytond.model import ModelSQL, ModelView, fields
from trytond.transaction import Transaction
from trytond.pool import Pool
import datetime as dt
import logging
import hashlib
import os

logger = logging.getLogger(__name__)

# ---------------------------- PROJECT MODEL -----------------------------
class Project(ModelSQL, ModelView):
    "AFX Project"
    __name__ = 'afx.project'

    # Hardcoded
    MAIN_COMPANY = 1
    UUID_PREFIX = "prj_"

    unique_id = fields.Char("Uuid")
    proj_no = fields.Char("Project No", required=True)
    customer = fields.Many2One('company.company', "Customer", 'name', required=True, domain=[
        ('id', '!=', MAIN_COMPANY)
    ])
    end_user = fields.Many2One('company.company', "End User", 'name', required=True, domain=[
        ('id', '!=', MAIN_COMPANY)
    ])
    so_no = fields.Char("S/O Number", required=True)
    po_no = fields.Char("PO Number", required=True)
    proj_name = fields.Char("Project Name", required=True)
    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=False)
    upd_date = fields.Function(fields.Date("Update Date"), 'compute_upd_date')
    closed = fields.Boolean("Closed")
    cancel = fields.Boolean("Cancel")
    user = fields.Many2One('company.employee', "User", 'name', required=True, domain=[
        ('company', '=', MAIN_COMPANY)
    ])
    members = fields.One2Many('afx.project.member', 'project', "Members", required=False)
    tasks = fields.One2Many('afx.project.task', 'project', "Activities", required=False)    

    # ------- DEFAULT VALUES --------    
    @classmethod
    def default_user(cls):
        if (Transaction().user - 1) < 1:
            return None
        else:
            return Transaction().user

    @classmethod
    def default_closed(cls):
        return False
    
    @classmethod
    def default_cancel(cls):
        return False
    
    # -------- ON CHANGE ---------
    @fields.depends('start_date')
    def on_change_with_end_date(self):
        if self.start_date:
            return self.start_date + dt.timedelta(days=1)
            
    # -------- COMPUTE FIELDS ------
    def compute_upd_date(self, name):
        pool = Pool()
        Date = pool.get('ir.date')
        return Date.today()

    # -------- OVERRIDE METHOD --------
    @classmethod
    def search(cls, domain, offset=0, limit=None, order=None, count=False, query=False):
        """
        Override the search method to filter project records based on the logged-in user.
        So the logged-in user only sees project records related to him/her self
        """
        # Get the logged-in user's ID
        user_id = Transaction().user
        if user_id > 1:
            # Add a condition to filter projects where the user is involved
            domain = [
                ('OR',
                    [('user', '=', user_id)],
                    [('members.member', '=', user_id)]
                ),
                *domain  # Preserve any existing domain conditions
            ]
        return super(Project, cls).search(domain, offset=offset, limit=limit, order=order, count=count, query=query)
    
    @classmethod
    def create(cls, vlist):
        projects = super().create(vlist)
        for project in projects:
            if project.user:
                cls.create_project_member(project)
        return projects

    @classmethod
    def write(cls, *args):
        # Extract projects and values from args
        projects = args[0]
        values = args[-1]
        
        # Capture old users before the update
        old_users = {p.id: p.user for p in projects}
        
        # Perform the write operation
        result = super().write(*args)
        
        # Check if 'user' field was updated
        if 'user' in values:
            new_user = values['user']
            for project in projects:
                old_user = old_users.get(project.id)
                if old_user != new_user:
                    cls.update_project_member(project, old_user, new_user)
        return result

    @classmethod
    def create_project_member(cls, project):
        ProjectMember = Pool().get('afx.project.member')
        ProjectMember.create([{
            'project': project.id,
            'member': project.user.id,
            'role': 'Default Role',  # You can adjust this as needed
            'rate': 0,  # Default rate, adjust as needed
            'est_start_date': project.start_date,  # Use the date from the timesheet record
            'est_end_date': project.end_date,  # Use the same date for simplicity
        }])

    @classmethod
    def update_project_member(cls, project, old_user, new_user):
        ProjectMember = Pool().get('afx.project.member')
        # Find existing members with the old user
        members = ProjectMember.search([
            ('project', '=', project.id),
            ('member', '=', old_user.id),
        ])
        if members:
            # Update existing members to new user
            ProjectMember.write(members, {'member': new_user.id})
        else:
            # Create new member if none existed for old user
            cls.create_project_member(project)
            
    def get_rec_name(self, name):
        if self.proj_name:
            return self.proj_name
        