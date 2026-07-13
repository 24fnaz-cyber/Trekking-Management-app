from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, User, Booking , Trekk_Staff

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template('index.html')

#Admin Functionalities

@login_required
@views.route('/admin', endpoint='admin')
def admin():
    if current_user.role  != 'admin':   #Backend validation
        return "unauthorized", 403
    
    search = request.args.get('search','')
    if search:
        term_search = "%{}%".format(search)
        trekks = Trekk_Staff.query.filter(Trekk_Staff.title.ilike(term_search)).all()
        staffs = User.query.filter(User.role == 'staff', User.username.ilike(term_search)).all()
        peoples = User.query.filter(User.role == 'people', User.username.ilike(term_search)).all()
    else:
        trekks = Trekk_Staff.query.all()
        staffs = User.query.filter_by(role = 'staff').all()
        peoples = User.query.filter_by(role = 'people').all()
    
    trekk_chart = Trekk_Staff.query.all()                 #chart data for the number of bookings per trek
    chart_label = [t.title for t in trekk_chart]
    chart_data = [len(t.bookings) for t in trekk_chart]
    
    return render_template('admin.html',trekks = trekks, staffs = staffs, peoples = peoples, search = search, chart_label = chart_label, chart_data = chart_data)

#create
@login_required
@views.route('/create_trekk',methods = ['POST'])
def create_trekk():
    if current_user.role  != 'admin':   #Backend validation
        return "unauthorized", 403
    
    title = request.form.get('title')
    location = request.form.get('location')
    slots = request.form.get('slots_available')
    existing = Trekk_Staff.query.filter_by(title=title,location=location).first()

    if existing:
        flash("This trek already exists.", "warning")
        return redirect(url_for('views.admin'))

    new_trekk = Trekk_Staff(title = title, location = location, slots_available = slots)
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
        flash(f'Staff {user.username} approved', 'success')
    elif action == 'blacklist':
        user.is_blacklisted = not user.is_blacklisted
        status = "blacklisted" if user.is_blacklisted else "restored"
        flash(f'User {user.username} {status}.', 'warning' )
    db.session.commit()
    return redirect(url_for('views.admin'))

#Staff routes
@login_required
@views.route('/staff_dash')
def staff_dash():
    if current_user.role  != 'staff':   #Backend validation
        return "unauthorized", 403
    
    assign_trekk = Trekk_Staff.query.filter_by(staff_id = current_user.id).all()
    return render_template('staff_dash.html', trekks = assign_trekk)

@login_required
@views.route('/update_status/<int:trek_id>', methods = ['POST'])
def update_status(trek_id):
    if current_user.role  != 'staff':   #Backend validation
        return "unauthorized", 403
    
    trekks = Trekk_Staff.query.get_or_404(trek_id)
    if trekks.staff_id == current_user.id:
        trekks.status = request.form.get('status')
        db.session.commit()
        flash('Status updated', 'success')
    return redirect(url_for('views.staff_dash'))

#Users route
@login_required
@views.route('/people')
def people():
    if current_user.role  != 'people':   #Backend validation
        return "unauthorized", 403  

    available_trekks = Trekk_Staff.query.filter_by(status = 'Open').all()
    register = Booking.query.filter_by(user_id = current_user.id).all()
    return render_template('people.html', trekks = available_trekks, bookings = register)

@login_required
@views.route('/book/<int:trek_id>', methods=['POST'])
def register_trekk(trek_id):
    if current_user.role != 'people':
        return "Unauthorized", 403

    trekk = Trekk_Staff.query.get_or_404(trek_id)

    # Check if the user has already booked this trek
    already = Booking.query.filter_by(user_id=current_user.id, trek_id=trekk.id).first()

    if already:
        flash("You have already booked this trek.", "warning")
        return redirect(url_for('views.people'))

    # Check if booking is allowed
    if trekk.slots_available > 0 and trekk.status == 'Open':
        booking = Booking(user_id=current_user.id, trek_id=trekk.id)
        trekk.slots_available -= 1
        db.session.add(booking)
        db.session.commit()
        flash('Trekking registered successfully!', 'success')
    else:
        flash('Registration is full or closed.', 'danger')

    return redirect(url_for('views.people'))
@login_required
@views.route('/cancel_booking/<int:booking_id>')
def cancel_booking(booking_id):
    if current_user.role != 'people':
        return "Unauthorized", 403

    booking = Booking.query.get_or_404(booking_id)

    # Ensure the booking belongs to the logged-in user
    if booking.user_id != current_user.id:
        return "Unauthorized", 403

    # Restore the available slot
    trekk = Trekk_Staff.query.get(booking.trek_id)
    if trekk:
        trekk.slots_available += 1

    # Delete the booking
    db.session.delete(booking)
    db.session.commit()

    flash("Booking cancelled successfully.", "success")
    return redirect(url_for('views.people'))

#API endpoints
@views.route('/api/trekks', methods = ['GET'])
def get_trekks():
    trekks = Trekk_Staff.query.all()
    trekks_data = []
    for trekk in trekks:
        trekk_info = {
            'id': trekk.id,
            'title': trekk.title,
            'slots_available': trekk.slots_available,
            'status': trekk.status,
            'staff_id': trekk.staff_id
        }
        trekks_data.append(trekk_info)
    return jsonify(trekks_data), 200

@views.route('/api/trekks', methods = ['POST'])
def create_api_trekk():
    data = request.get_json()

    if not data or not data.get('title') or not data.get('slots_available'):
        return jsonify({'error': 'Missing required data'}), 400
 
    trekk_new = Trekk_Staff(title=data['title'],slots_available=data['slots_available'],status=data.get('status', 'Open'))
    db.session.add(trekk_new)
    db.session.commit()
    return jsonify({'message': 'Trekking created successfully', 'trekk_id': trekk_new.id}), 201









    





