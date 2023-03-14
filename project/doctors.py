from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db, UPLOAD_FOLDER
from flask_login import login_required, current_user
from .models import Doctor, User, Department, Message
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import allowed_file
from werkzeug.utils import secure_filename
import os

doctors = Blueprint('doctors', __name__)

@doctors.route('/doctors/admin')
def admin_list_doctors():
    doctors = Doctor.query.all()

    result = []
    for doctor in doctors:
        user = User.query.get_or_404(doctor.user)
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profession": doctor.profession,
            "get_img": doctor.get_img,
            "is_top": doctor.is_top,
        }
        result.append(data)

    departments = Department.query.all()

    return render_template('admin/doctors.html', doctors=result, departments=departments)


@doctors.route('/doctors/admin', methods=['POST'])
def admin_create_doctors():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")

    print(first_name, last_name)
    email = request.form.get("email")
    password1 = request.form.get("password1")
    password2 = request.form.get("password1")


    # doctor fields
    department = request.form.get("department")
    profession = request.form.get("profession")
    bio = request.form.get("bio")
    is_top = request.form.get("is_top")



    if password1 != password2:
        flash('Email address already exists')
        return redirect(request.url)

    
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(request.url)


    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, is_doctor=True, password=generate_password_hash(password1, method='sha256'), first_name=first_name, last_name=last_name)

    print(new_user.first_name, new_user.last_name)
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

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

    # create patiient profilre here
    new_doctor = Doctor(user=new_user.id,profession=profession, bio=bio, department=department, img=filename, is_top=True if is_top == "on" else False)
    db.session.add(new_doctor)
    db.session.commit()

    print(new_doctor, "doctor added")
   
    return redirect(url_for('doctors.admin_list_doctors'))



# normal user 
@doctors.route('/doctors/list')
def list_doctors():
    doctors = Doctor.query.all()

    result = []
    for doctor in doctors:
        user = User.query.get_or_404(doctor.id)
        data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profession": doctor.profession,
            "get_img": doctor.get_img,
            "is_top": doctor.is_top,
        }
        result.append(data)

    departments = Department.query.all()

    return render_template('doctors/team.html', doctors=result, departments=departments)



@doctors.route('/doctors/messages')
@login_required
def doctors_messages():
    from_messages = list(Message.query.filter_by(from_user=current_user.id))
    to_messages = list(Message.query.filter_by(to_user=current_user.id))

    all_messages = from_messages + to_messages
    # get all user ids from all_messages
    user_ids = set()
    for message in all_messages:
        user_ids.add(message.from_user)
        user_ids.add(message.to_user)
    
    print(user_ids, "-----", current_user.id)
    user_ids.remove(current_user.id)
    
    users = []
    for user_id in user_ids:
        user = User.query.filter_by(id=user_id).first()
        users.append(user)


    return render_template('doctors/messages.html', users=users)


@doctors.route('/doctors/message/thread/<int:id>')
@login_required
def doctors_thread(id):
    user = User.query.filter_by(id=id).first()

    from_messages = list(Message.query.filter_by(from_user=current_user.id, to_user=id))
    to_messages = list(Message.query.filter_by(to_user=current_user.id, from_user=id))

    all_messages = from_messages + to_messages
    result = set(all_messages)

    message_ids = []
    for message in result:
        message_ids.append(message.id)

    message_ids.sort()

    # print(message_ids)
    final_result = []
    for message_id in message_ids:
        message = Message.query.filter_by(id=message_id).first()
        final_result.append(message)

    # print(final_result)

    return render_template('doctors/thread.html', messages=final_result, to_user_id=id, user=user)



@doctors.route('/doctors/message/thread/<int:id>', methods=["POST"])
@login_required
def create_message_post(id):
    text = request.form.get("text")
    user_sending = User.query.filter_by(id=current_user.id).first()
    message = Message(
        from_user=current_user.id,
        to_user= id,
        text=f"{user_sending.first_name} {user_sending.last_name}: {text}",
    )

    db.session.add(message)
    db.session.commit()

    return redirect(url_for('doctors.doctors_thread', id=id))