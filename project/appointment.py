from flask import Blueprint,flash, render_template, redirect, url_for, request
from . import db

from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Patient, Doctor, Service, Appointment
from flask_login import login_user, login_required, logout_user, current_user

appointment = Blueprint('appointment', __name__)


@appointment.route('/appointment/create')
@login_required
def create():
    doctors = Doctor.query.all()

    services = Service.query.all()


    patient = Patient.query.filter_by(user=current_user.id).first()
    appointments = Appointment.query.filter_by(patient=patient.id)
    # appointments = Appointment.query.all()

    appointment_result = []
    for appointment in appointments:
        patient = Patient.query.filter_by(id=appointment.patient).first()
        patient_user = None
        if patient:
            patient_user = User.query.filter_by(id=patient.user).first()

        doctor = Doctor.query.filter_by(id=appointment.doctor).first()
        doctor_user = None
        if doctor:
            doctor_user = User.query.filter_by(id=doctor.user).first()
            print("doctor user", doctor_user)

        service = Service.query.filter_by(id=appointment.service).first()


        appointment = {
            "id": appointment.id,
            "patient": patient_user.first_name + " " + patient_user.last_name if patient_user else None,
            "patient_user_id": patient_user.id if patient_user else None,
            "doctor": doctor_user.first_name + " " + doctor_user.last_name if doctor_user else None,
            "service": service.name,
            "status": appointment.status,
            "appointment_date": appointment.appointment_date,
            "appointment_time": appointment.appointment_time,
        }
        appointment_result.append(appointment)

    result = []
    for doctor in doctors:
        user = User.query.get_or_404(doctor.user)
        data = {
            "id": doctor.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profession": doctor.profession,
            "get_img": doctor.get_img,
            "is_top": doctor.is_top,
        }
        result.append(data)

    return render_template('appointment.html', doctors=result, services=services, appointments=appointment_result)



@appointment.route('/appointment/create', methods=["POST"])
@login_required
def create_post():
    service = request.form.get('service')
    doctor = request.form.get('doctor')
    appointment_date = request.form.get('appointment_date')
    appointment_time = request.form.get('appointment_time')

    print(request.form.keys())

    # get patient
    patient = Patient.query.filter_by(user=current_user.id).first()
    if patient:
        # create Appointment
        appointment = Appointment(
            patient=patient.id,
            service = service,
            doctor = doctor,
            appointment_date = appointment_date,
            appointment_time = appointment_time
        )
        db.session.add(appointment)
        db.session.commit()
    
    return redirect(url_for("appointment.create"))

@appointment.route('/appointment/admin/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    appointment = Appointment.query.get_or_404(id)

    db.session.delete(appointment)
    db.session.commit()

    # print("department_delete____", service.name, "__id__:", service.id)
    return redirect(url_for('appointment.create'))


@appointment.route('/appointment/doctor')
@login_required
def doctor_list():
    doctors = Doctor.query.all()

    services = Service.query.all()


    doctor = Doctor.query.filter_by(user=current_user.id).first()
    appointments = Appointment.query.filter_by(doctor=doctor.id)
    # appointments = Appointment.query.all()

    appointment_result = []
    for appointment in appointments:
        patient = Patient.query.filter_by(id=appointment.patient).first()
        patient_user = None
        if patient:
            patient_user = User.query.filter_by(id=patient.user).first()

        doctor = Doctor.query.filter_by(id=appointment.doctor).first()
        doctor_user = None
        if doctor:
            doctor_user = User.query.filter_by(id=doctor.user).first()
            print("doctor user", doctor_user)

        service = Service.query.filter_by(id=appointment.service).first()


        appointment = {
            "id": appointment.id,
            "patient": patient_user.first_name + " " + patient_user.last_name if patient_user else None,
            "patient_user": patient_user.id,
            "patient_user_id": patient_user.id if patient_user else None,
            "doctor_user": doctor_user.id,
            "doctor": doctor_user.first_name + " " + doctor_user.last_name if doctor_user else None,
            "service": service.name,
            "status": appointment.status,
            "appointment_date": appointment.appointment_date,
            "appointment_time": appointment.appointment_time,
        }
        appointment_result.append(appointment)

    result = []
    for doctor in doctors:
        user = User.query.get_or_404(doctor.user)
        data = {
            "id": doctor.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profession": doctor.profession,
            "get_img": doctor.get_img,
            "is_top": doctor.is_top,
        }
        result.append(data)

    return render_template('doctors/appointment.html', doctors=result, services=services, appointments=appointment_result)


@appointment.route('/appointment/doctor/delete/<int:id>', methods=['GET'])
@login_required
def doctor_delete(id):
    appointment = Appointment.query.get_or_404(id)

    db.session.delete(appointment)
    db.session.commit()

    # print("department_delete____", service.name, "__id__:", service.id)
    return redirect(url_for('appointment.doctor_list'))

@appointment.route('/appointment/doctor/accept/<int:id>', methods=['GET'])
@login_required
def doctor_accept(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = "accepted"

    db.session.add(appointment)
    db.session.commit()

    # print("department_delete____", service.name, "__id__:", service.id)
    return redirect(url_for('appointment.doctor_list'))

@appointment.route('/appointment/doctor/reject/<int:id>', methods=['GET'])
@login_required
def doctor_reject(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = "rejected"

    db.session.add(appointment)
    db.session.commit()

    # print("department_delete____", service.name, "__id__:", service.id)
    return redirect(url_for('appointment.doctor_list'))

@appointment.route('/appointment/doctor/pend/<int:id>', methods=['GET'])
@login_required
def doctor_pend(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.status = "pending"

    db.session.add(appointment)
    db.session.commit()

    # print("department_delete____", service.name, "__id__:", service.id)
    return redirect(url_for('appointment.doctor_list'))