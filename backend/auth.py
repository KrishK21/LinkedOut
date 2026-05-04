from flask import Flask, render_template, jsonify
import os

from werkzeug.utils import secure_filename
from db import get_db, close_db, init_db
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__, 
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "instance"), exist_ok=True)

# Close DB after each request
app.teardown_appcontext(close_db)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/home")        
def homepage(): 
    return render_template("Homepage.html")

@app.route("/health")
def health():
    return jsonify(status="ok") # Makes sure flask is running


@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    if not username or not password:
        return jsonify({"error": "Please enter username, password. Positions can not be empty"}), 400
    try:
        db = get_db()
        # This creates a users table if it doesn't exist already.
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)

        # This checks if the chosen username already exists.
        existing = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if existing:
            return jsonify({"error": "Username already exists"}), 400

        # This handles the hashing of our users passwords so that their passwords are protected.
        hashed_password = generate_password_hash(password) 
        db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, hashed_password))
        db.commit()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        return jsonify({"message": "Account created successfully!", "user_id": user["id"]}), 201
    except Exception as e:
        return jsonify({"error": f"Error occurred while in signup route: {str(e)}"}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    if not username or not password:
        return jsonify({"error": "Please enter password and username."}), 400
    try:
        db = get_db()
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)
        user = db.execute(
            "SELECT * FROM users WHERE username = ?", (username,)
        ).fetchone()
        if user is None:
            return jsonify({"error": "Invalid credentials"}), 401
        if not check_password_hash(user["password_hash"], password):
            return jsonify({"error": "Invalid credentials"}), 401
        return jsonify({
            "message": "Login was successful",
            "user_id": user["id"],
            "username": user["username"]
        }), 200
    except Exception as e:
        return jsonify({"error": f"Error while in login route: {str(e)}"}), 400
    
@app.route("/profile", methods=['GET', 'POST'])
def profile():
    if request.content_type and 'application/json' in request.content_type:
        data = request.get_json() or {}
    else:
        data = {}
    user_id = request.form.get('user_id') or request.args.get('user_id') or data.get('user_id')
    name = request.form.get('name') or data.get('name', '').strip()
    bio = request.form.get('bio') or data.get('bio', '').strip()
    try:
        db = get_db()
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        if request.method == 'POST':

            # This handles and allows the user to upload their resume to their profile. 
            resume_file = request.files.get('resume')
            resume_path = None
            if resume_file and allowed_file(resume_file.filename):
                resume_filename = f"user_{user_id}_resume_{secure_filename(resume_file.filename)}"
                resume_file.save(os.path.join(UPLOAD_FOLDER, resume_filename))
                resume_path = resume_filename

            # This handles and lets the user input their information into their profile. 
            db.execute("""
                CREATE TABLE IF NOT EXISTS profiles (
                    user_id INTEGER PRIMARY KEY,
                    name TEXT,
                    bio TEXT,
                    resume TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)
            db.commit()
            existing = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
            if existing:
                db.execute("""
                    UPDATE profiles
                    SET name = ?, bio = ?, resume = COALESCE(?, resume)
                    WHERE user_id = ?
                """, (name, bio, resume_path, user_id))
            else:
                db.execute("""
                    INSERT INTO profiles (user_id, name, bio, resume)
                    VALUES (?, ?, ?, ?)
                """, (user_id, name, bio, resume_path))
            db.commit()
            return jsonify({'message': 'Profile updated successfully!'}), 200
        else:
            # This handles the user getting to their profile.
            profile = db.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,)).fetchone()
            if not profile:
                return jsonify({'error': 'Profile not found'}), 404
            return jsonify({
                'user_id': profile['user_id'],
                'name': profile['name'],
                'bio': profile['bio'],
                'resume': profile['resume']
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/db-test")
def db_test():
    db = get_db()
    db.execute("SELECT 1;")
    db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jobs';")
    return jsonify(db="connected", jobs_table="exists")

@app.route("/profile-page")
def profilePage():
    return render_template("Profilepage.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
