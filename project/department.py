from flask import Blueprint, redirect, render_template, request, url_for
from . import db
from flask_login import login_required, current_user
from .models import Department, User


department = Blueprint('department', __name__)



@department.route('/department/admin')
def admin_department():
    departments = Department.query.all()
    return render_template('admin/department.html', departments=departments)

@department.route('/department/admin', methods=['POST'])
def admin_department_post():
    name = request.form.get('name')

    department = Department(
        name=name
    )

    db.session.add(department)
    db.session.commit()

    print("department_name____", name)
    return redirect(url_for('department.admin_department'))


@department.route('/department/admin/delete/<int:id>', methods=['GET'])
def admin_department_delete(id):
    department = Department.query.get_or_404(id)

    db.session.delete(department)
    db.session.commit()

    print("department_delete____", department.name, "__id__:", department.id)
    return redirect(url_for('department.admin_department'))