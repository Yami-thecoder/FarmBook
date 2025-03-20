# routes.py (API Routes)
import os
import mimetypes
from flask import Blueprint, request, jsonify, send_from_directory, Response
from werkzeug.utils import secure_filename
from . import db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .models import User, FarmJournal, Post, Comment
from flask import send_file
from io import BytesIO
from fpdf import FPDF
from flask_cors import cross_origin

auth = Blueprint('auth', __name__)
journal = Blueprint('journal', __name__)
posts = Blueprint('posts', __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400

    if User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exists'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username=username, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token}), 200

@auth.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({'message': f'Welcome {user.username}!'}), 200

@journal.route('/journal', methods=['POST'])
@jwt_required()
def create_journal_entry():
    user_id = get_jwt_identity()
    data = request.get_json()
    # Convert empty or "None" values to proper None type for PostgreSQL
    harvest_date = data.get("harvest_date", None)
    if harvest_date in [None, "None", ""]:  # Ensure NULL is inserted correctly
        harvest_date = None
    entry = FarmJournal(
        user_id=user_id,
        crop_name=data["crop_name"],
        season=data.get("season"),
        farm_location=data.get("farm_location"),
        sowing_date=data["sowing_date"],
        harvest_date=harvest_date,
        yield_amount=data["yield_amount"],
        sold_amount=data.get("sold_amount", 0),  # Default to 0 if not provided
        unit_price=data["unit_price"],
        expenses=data["expenses"],
        notes=data.get("notes")
    )

    # Auto-calculate total revenue & profit
    entry.calculate_revenue_and_profit()

    db.session.add(entry)
    db.session.commit()
    
    return jsonify({"message": "Journal entry created successfully"}), 201


@journal.route('/journal', methods=['GET'])
@jwt_required()
def get_journal_entries():
    user_id = get_jwt_identity()
    entries = FarmJournal.query.filter_by(user_id=int(user_id)).order_by(FarmJournal.created_at.desc()).all()  # ✅ Sort by latest first
    
    return jsonify([{
        'id': entry.id,
        'crop_name': entry.crop_name,
        'season': entry.season,
        'farm_location': entry.farm_location,
        'sowing_date': str(entry.sowing_date),
        'harvest_date': str(entry.harvest_date),
        'yield_amount': entry.yield_amount,
        'sold_amount': entry.sold_amount,
        'unit_price': entry.unit_price,
        'total_revenue': entry.total_revenue,
        'expenses': entry.expenses,
        'profit': entry.profit,
        'notes': entry.notes
    } for entry in entries]), 200

@journal.route('/journal/<int:id>', methods=['PUT'])
@jwt_required()
def update_journal_entry(id):
    user_id = get_jwt_identity()
    entry = FarmJournal.query.filter_by(id=id, user_id=int(user_id)).first()

    if not entry:
        return jsonify({"error": "Entry not found"}), 404

    data = request.get_json()
    entry.crop_name = data["crop_name"]
    entry.season = data.get("season")
    entry.farm_location = data.get("farm_location")
    entry.sowing_date = data["sowing_date"]
    entry.harvest_date = data.get("harvest_date")
    entry.yield_amount = data["yield_amount"]
    entry.sold_amount = data.get("sold_amount", entry.sold_amount)
    entry.unit_price = data["unit_price"]
    entry.expenses = data["expenses"]
    entry.notes = data.get("notes")

    # Auto-calculate revenue & profit on update
    entry.calculate_revenue_and_profit()

    db.session.commit()
    
    return jsonify({"message": "Journal entry updated successfully"}), 200


@journal.route('/journal/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_journal_entry(id):
    user_id = get_jwt_identity()
    entry = FarmJournal.query.filter_by(id=id, user_id=int(user_id)).first()
    
    if not entry:
        return jsonify({'error': 'Entry not found'}), 404
    
    db.session.delete(entry)
    db.session.commit()
    return jsonify({'message': 'Journal entry deleted successfully'}), 200


@journal.route('/export/pdf', methods=['GET'])
@jwt_required()
def export_journal_to_pdf():
    user_id = get_jwt_identity()
    entries = FarmJournal.query.filter_by(user_id=int(user_id)).all()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Farm Journal Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    for entry in entries:
        pdf.cell(200, 10, f"Crop: {entry.crop_name} - {entry.season}", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 8, f"Location: {entry.farm_location}\nSowing Date: {entry.sowing_date}\nHarvest Date: {entry.harvest_date}\nYield: {entry.yield_amount} kg\nUnit Price: Rs.{entry.unit_price} per kg\nExpenses: Rs.{entry.expenses}\nProfit: Rs.{entry.profit}\nNotes: {entry.notes}\n", border=1)
        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)

    pdf_output = BytesIO()
    pdf_output.write(pdf.output(dest='S').encode('latin1'))
    pdf_output.seek(0)

    return send_file(pdf_output, mimetype='application/pdf', as_attachment=True, download_name="farm_journal.pdf")



@journal.route('/analytics/profit-trend', methods=['GET'])
@jwt_required()
def profit_trend():
    user_id = get_jwt_identity()
    entries = FarmJournal.query.filter_by(user_id=int(user_id)).order_by(FarmJournal.sowing_date).all()

    data = [{
        'sowing_date': entry.sowing_date.strftime('%Y-%m-%d'),
        'profit': entry.profit
    } for entry in entries]

    return jsonify(data), 200


@journal.route('/analytics/crop-comparison', methods=['GET'])
@jwt_required()
def crop_comparison():
    user_id = get_jwt_identity()
    entries = FarmJournal.query.filter_by(user_id=int(user_id)).all()
    
    crop_profits = {}
    for entry in entries:
        if entry.crop_name not in crop_profits:
            crop_profits[entry.crop_name] = 0
        crop_profits[entry.crop_name] += entry.profit
    
    data = [{'crop_name': crop, 'total_profit': profit} for crop, profit in crop_profits.items()]
    return jsonify(data), 200


@journal.route('/analytics/cost-breakdown', methods=['GET'])
@jwt_required()
def cost_breakdown():
    user_id = get_jwt_identity()
    entries = FarmJournal.query.filter_by(user_id=int(user_id)).all()
    
    crop_expenses = {}
    for entry in entries:
        if entry.crop_name not in crop_expenses:
            crop_expenses[entry.crop_name] = 0
        crop_expenses[entry.crop_name] += entry.expenses
    
    data = [{'crop_name': crop, 'total_expenses': expenses} for crop, expenses in crop_expenses.items()]
    return jsonify(data), 200



@posts.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()
    title = request.form.get('title', "").strip()
    description = request.form.get('description', "").strip()
    file = request.files.get('file')

    # ✅ Enforce validation rules
    if not title:
        return jsonify({'error': 'Post must have a title'}), 400
    if not description and not file:
        return jsonify({'error': 'Post must have either a description or a file'}), 400
    if description and len(description.split()) > 200:
        return jsonify({'error': 'Description cannot exceed 200 words'}), 400

    filename = None
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))

    new_post = Post(title=title, description=description, file_url=filename, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully', 'post_id': new_post.id}), 201


@posts.route('/posts', methods=['GET'])
@jwt_required()
def get_posts():
    posts = Post.query.order_by(Post.created_at.desc()).all()  # ✅ Sort posts latest first
    
    result = [
        {
            'id': post.id,
            'title': post.title,
            'description': post.description,
            'file_url': f"/uploads/{post.file_url}" if post.file_url else None,
            'username': post.author.username,
            'likes': post.likes or 0,
            'created_at': post.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            'comments': sorted(  # ✅ Sort comments latest first
                [
                    {'id': c.id, 'content': c.content, 'username': c.user.username, 'created_at': c.created_at.strftime("%Y-%m-%d %H:%M:%S")}
                    for c in post.comments
                ], 
                key=lambda x: x['created_at'], 
                reverse=True
            )
        }
        for post in posts
    ]
    
    return jsonify(result), 200

@posts.route('/posts/<int:post_id>/like', methods=['POST'])
@jwt_required()
def like_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    post.likes += 1
    db.session.commit()
    return jsonify({'message': 'Post liked', 'likes': post.likes}), 200

@posts.route('/posts/<int:post_id>/comment', methods=['POST'])
@jwt_required()
def add_comment(post_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'error': 'Missing comment content'}), 400

    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    new_comment = Comment(content=content, user_id=user_id, post_id=post_id)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({'message': 'Comment added'}), 201


@posts.route('/uploads/<path:filename>', methods=['GET'])
@cross_origin()
def serve_file(filename):
    """Serve uploaded files with correct MIME types to fix CORB issues."""
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    # Guess MIME type based on file extension
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = "application/octet-stream"  # Default MIME type

    # Read the file and serve with correct headers
    with open(file_path, "rb") as file:
        response = Response(file.read(), content_type=mime_type)
        response.headers["Access-Control-Allow-Origin"] = "*"  # ✅ Allow requests from anywhere
        response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        return response