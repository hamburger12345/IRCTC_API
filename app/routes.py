from flask import request, jsonify
from app import app, db
from app.models import User, Train
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
import uuid

def admin_api_key_required(f): 
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('API-Key') != app.config['ADMIN_API_KEY']:
            return jsonify({'message': 'Unauthorized access'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'user') 

    if not username or not email or not password:
        return jsonify({'message': 'Username, email, and password are required'}), 400

    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'message': 'Username or email already exists'}), 400

    hashed_password = generate_password_hash(password)

    new_user = User(username=username, email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid username or password'}), 401

    access_token = create_access_token(identity=username)
    return jsonify({'access_token': access_token}), 200

@app.route('/admin/add_train', methods=['POST'])
@admin_api_key_required
def add_train():
    data = request.json
    source = data.get('source')
    destination = data.get('destination')
    total_seats = data.get('total_seats')

    if not source or not destination or not total_seats:
        return jsonify({'message': 'Source, destination, and total seats are required'}), 400

    if not isinstance(total_seats, int) or total_seats <= 0:
        return jsonify({'message': 'Total seats must be a positive integer'}), 400

    new_train = Train(source=source, destination=destination, total_seats=total_seats, available_seats=total_seats)
    db.session.add(new_train)
    db.session.commit()

    return jsonify({'message': 'Train added successfully'}), 201

@app.route('/trains/availability', methods=['GET'])
def get_seat_availability():
    source = request.args.get('source')
    destination = request.args.get('destination')

    if not source or not destination:
        return jsonify({'message': 'Source and destination are required'}), 400

    trains = Train.query.filter_by(source=source, destination=destination).all()

    if not trains:
        return jsonify({'message': 'No trains found for the given source and destination'}), 404

    response = []

    for train in trains:
        response.append({
            'train_id': train.id,
            'source': train.source,
            'destination': train.destination,
            'available_seats': train.available_seats
        })

    return jsonify({'trains': response}), 200

@app.route('/book_seat', methods=['POST'])
@jwt_required()
def book_seat():
    current_user = get_jwt_identity()

    data = request.json
    train_id = data.get('train_id')

    if not train_id:
        return jsonify({'message': 'Train ID is required'}), 400

    try:
        with db.session.begin_nested():
            train = Train.query.filter_by(id=train_id).with_for_update().first()  # Locking the row for update
            if not train:
                return jsonify({'message': 'Train not found'}), 404
            
            if train.available_seats < 1:
                return jsonify({'message': 'No seats available for booking'}), 400
            
            train.available_seats -= 1
            booking_id = str(uuid.uuid4())
            booking = Booking(id=booking_id, train_id=train.id, user_id=current_user, num_seats=1)
            db.session.add(booking)
            
            db.session.commit()
    except IntegrityError:
        # Rollbacking the transaction in case of database integrity errors
        db.session.rollback()
        return jsonify({'message': 'Database integrity error occurred. Please try again.'}), 500

    return jsonify({'message': 'Seat booked successfully'}), 200

@app.route('/booking_details/<booking_id>', methods=['GET'])
@jwt_required()
def get_booking_details(booking_id):
    booking = Booking.query.get(booking_id)

    if not booking:
        return jsonify({'message': 'Booking not found'}), 404

    current_user = get_jwt_identity()
    if booking.user_id != current_user:
        return jsonify({'message': 'Unauthorized'}), 403

    return jsonify({
        'booking_id': booking.id,
        'user_id': booking.user_id,
        'train_id': booking.train_id,
    }), 200
