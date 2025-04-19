from trytond.model import ModelSQL, ModelView, fields
from trytond.transaction import Transaction
from trytond.pool import Pool
import datetime as dt
import logging

logger = logging.getLogger(__name__)

# ---------------------------- PROJECT MODEL -----------------------------
class Project(ModelSQL, ModelView):
    "AFX Project"
    __name__ = 'afx.project'

    # Hardcoded
    MAIN_COMPANY = 1

    no = fields.Char("No")
    customer = fields.Many2One('company.company', "Customer", 'name', required=True, domain=[
        ('id', '!=', MAIN_COMPANY)
    ])
    end_user = fields.Many2One('company.company', "End User", 'name', required=True, domain=[
        ('id', '!=', MAIN_COMPANY)
    ])
    so_no = fields.Char("S/O Number", required=True)
    po_no = fields.Char("PO Number", required=True)
    proj_no = fields.Char("Project No", required=True)
    proj_name = fields.Char("Project Name", required=True)
    start_date = fields.Date("Start Date", required=True)
    end_date = fields.Date("End Date", required=False)
    upd_date = fields.Function(fields.Date("Update Date"), 'compute_upd_date')
    closed = fields.Boolean("Closed")
    cancel = fields.Boolean("Cancel")
    user = fields.Many2One('company.employee', "User", 'name', required=False, domain=[
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
        if user_id:
            # Add a condition to filter projects where the user is involved
            domain = [
                ('OR',
                    [('user', '=', user_id)],
                    [('members.member', '=', user_id)]
                ),
                *domain  # Preserve any existing domain conditions
            ]
        return super(Project, cls).search(domain, offset=offset, limit=limit, order=order, count=count, query=query)
    
    def get_rec_name(self, name):
        if self.proj_name:
            return self.proj_name