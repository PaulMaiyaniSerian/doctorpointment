from flask import Blueprint, render_template, request, url_for, redirect
from . import db
from flask_login import login_required, current_user
from .models import Doctor, User, Service


main = Blueprint('main', __name__)

@main.route('/')
def index():
    doctors = Doctor.query.all()
    services = Service.query.all()

    result = []
    for doctor in doctors:
        user = User.query.get_or_404(doctor.user)
        print(user.first_name, "---doctor user--")

        doctor = {
            "id": doctor.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "profession": doctor.profession,
            "date_joined": doctor.date_created,
            "bio": doctor.bio,
            "get_img": doctor.get_img
        }
        result.append(doctor)

    top_2_services = Service.query.filter_by(is_top_2=True)
    bottom_2_services = Service.query.filter_by(is_bottom_2=True)
    top_services = Service.query.filter_by(is_top=True)


        
    return render_template(
        'index.html', 
        doctors=result,
        top_2_services=top_2_services,
        bottom_2_services=bottom_2_services,
        top_services=top_services,
        services=services,
    )

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/profile', methods=['POST'])
@login_required
def profile_post():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    bio = request.form.get('bio')
    current_user.email = email
    current_user.first_name = first_name
    current_user.last_name = last_name

    db.session.add(current_user)
    db.session.commit()

    doctor = Doctor.query.filter_by(user=current_user.id).first()

    if doctor:
        doctor.bio = bio
        db.session.add(current_user)
        db.session.commit()
    

    return redirect(url_for("main.profile"))