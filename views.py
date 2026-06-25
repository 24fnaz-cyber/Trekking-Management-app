from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, Booking , Trekk_Staff

views = Blueprint('views',__name__)

#Admin Functionalities

@login_required
@views.route('/admin', endpoint='admin')
def admin_dashboard():
    if current_user.role  != 'admin':   #Backend validation
        return "unauthorized", 403
    
    trekks = Trekk_Staff.query.all()
    staffs = User.query.filter_by(role = 'staff').all()
    peoples = User.query.filter_by(role = 'people').all()

    return render_template('admin.html',trekks = trekks, staffs = staffs, peoples = peoples)

#create
@login_required
@views.route('/create_trekk',methods = ['POST'])
def create_trekk():
    if current_user.role  != 'admin':   #Backend validation
        return "unauthorized", 403
    
    title = request.form.get('title')
    slots = request.form.get('slots_available')
    new_trekk = Trekk_Staff(title = title, slots_available = slots)
    db.session.add(new_trekk)
    db.session.commit()

    flash('Trekks created successfully', 'success')
    return redirect(url_for('views.admin'))

#delete
@login_required
@views.route('/delete_trekk/<int:id>')
def delete_trekk(id):
    if current_user.role != 'admin':
        return "Unauthorized", 403
    trekk = Trekk_Staff.query.get_or_404(id)
    db.session.delete(trekk)
    db.session.commit()
    flash("Trekk deleted successfully", 'info')
    return redirect(url_for('views.admin'))

@login_required
@views.route('/assign_staff/<int:trekk_id>', methods = ['POST'])
def assign_staff(trekk_id):
    if current_user.role  != 'admin':   #Backend validation
        return "unauthorized", 403
    
    trekk = Trekk_Staff.query.get_or_404(trekk_id)
    staff_id = request.form.get('staff_id')
    trekk.staff_id = staff_id
    db.session.commit()
    flash("Staff Assigned", 'success')
    return redirect(url_for('views.admin'))

@login_required
@views.route('/toggle_user_status/<int:user_id>/<action>')
def toggle_user_status(user_id, action):
    if current_user.role  != 'admin':   #Backend validation
        return "unauthorized", 403
    
    user = User.query.get_or_404(user_id)

    if action == 'approve':
        user.is_approved = True
        flash(f'Mentor {user.username} approved', 'success')
    elif action == 'blacklist':
        user.is_blacklisted = not user.is_blacklisted
        status = "blacklisted" if user.is_blacklisted else "restored"
        flash(f'User {user.username} {status}.', 'warning' )
    db.session.commit()
    return redirect(url_for('views.admin'))




    





