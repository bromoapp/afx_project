# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from . import project
from . import project_task
from . import project_member

def register():
    Pool.register(
        project.Project,
        project_task.ProjectTask,
        project_member.ProjectMember,
        module='afx_project', type_='model')
    # Pool.register(
    #     module='afx_project', type_='wizard')
    # Pool.register(
    #     module='afx_project', type_='report')
