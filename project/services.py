from flask import Blueprint, flash, redirect, render_template, request, url_for
from . import db, UPLOAD_FOLDER
from flask_login import login_required, current_user
from .models import   Service, Department
from .utils import allowed_file
from werkzeug.utils import secure_filename
import os

services = Blueprint('services', __name__)


@services.route('/services/admin/list/<int:id>')
def admin_list_services(id):
    services = Service.query.filter_by(department=id)
    department = Department.query.get_or_404(id)

    return render_template('admin/services.html', services=services, department=department)


@services.route('/services/admin/list/<int:id>', methods=['POST'])
def admin_service_post(id):
    name = request.form.get('name')
    is_top_2 = request.form.get('is_top_2')
    is_bottom_2 = request.form.get('is_bottom_2')
    is_top = request.form.get('is_top')

    department = Department.query.get_or_404(id)

    # print(request.files.keys())

    # check if the post request has the file part
    if 'img' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['img']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)

        file.save(os.path.join(UPLOAD_FOLDER, filename))

    service = Service(
        name=name,
        department=department.id,
        img=filename,
        is_top_2=True if is_top_2 == "on" else False ,
        is_bottom_2=True if is_bottom_2 == "on" else False,
        is_top=True if is_top == "on" else False
    )

    db.session.add(service)
    db.session.commit()


    print("service_name____", name, department.id)
    return redirect(url_for('services.admin_list_services', id=id))


@services.route('/services/admin/delete/<int:id>', methods=['GET'])
def admin_service_delete(id):
    service = Service.query.get_or_404(id)

    db.session.delete(service)
    db.session.commit()

    print("department_delete____", service.name, "__id__:", service.id)
    return redirect(url_for('services.admin_list_services', id=service.department))



@services.route('/services/patient/search', methods=['POST'])
def search():
    # if request.method == "GET":
    service_name = request.form.get("service_name")

    services = Service.query.filter_by(name=service_name)
    print(request.form)

    # print("department_delete____", service.name, "__id__:", service.id)
    return render_template('patients/services.html', services=services)
 