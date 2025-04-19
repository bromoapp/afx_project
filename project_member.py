from trytond.model import ModelSQL, ModelView, fields

class ProjectMember(ModelSQL, ModelView):
    "Project Member"
    __name__ = "afx.project.member"

    # Hardcoded
    MAIN_COMPANY = 1

    project = fields.Many2One('afx.project', "Project", required=True)
    member = fields.Many2One('company.employee', "Member", required=False, domain=[
        ('company', '=', MAIN_COMPANY)
    ])
    role = fields.Char("Role", required=False)
    rate = fields.Integer("Charge-Out Rate")
    est_start_date = fields.Date("Start Date")
    est_end_date = fields.Date("End Date")
    est_duration = fields.Function(fields.Integer("Duration (Days)"), 'get_est_duration')

    def get_est_duration(self, name):
        """
        Compute the estimated duration in days based on est_start_date and est_end_date.
        """
        if self.est_start_date and self.est_end_date:
            # Calculate the difference in days
            delta = (self.est_end_date - self.est_start_date).days
            return max(delta, 0)  # Ensure non-negative duration
        return 0  # Return 0 if either date is missing

    @classmethod
    def validate(cls, records):
        """
        Validate that est_end_date is not earlier than est_start_date.
        """
        super(ProjectMember, cls).validate(records)
        for record in records:
            if record.est_start_date and record.est_end_date:
                if record.est_end_date < record.est_start_date:
                    raise ValueError("Estimated End Date cannot be earlier than Estimated Start Date.")
                
    def get_rec_name(self, name):
        if self.member:
            return self.member.party.name