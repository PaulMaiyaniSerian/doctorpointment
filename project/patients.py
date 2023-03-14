from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db, UPLOAD_FOLDER
from flask_login import login_required, current_user
from .models import Doctor, User, Department, Message
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import allowed_file
from werkzeug.utils import secure_filename
import os


patients = Blueprint('patients', __name__)

@patients.route('/patients/messages')
@login_required
def patients_messages():
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


    return render_template('patients/messages.html', users=users)

@patients.route('/patients/message/thread/<int:id>')
@login_required
def patients_thread(id):
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

    return render_template('patients/thread.html', messages=final_result, to_user_id=id, user=user)


@patients.route('/patients/message/thread/<int:id>', methods=["POST"])
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

    return redirect(url_for('patients.patients_thread', id=id))