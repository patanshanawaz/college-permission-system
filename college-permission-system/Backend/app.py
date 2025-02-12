from flask import Flask, render_template, request, redirect, url_for, flash
from models import init_db, db, PermissionRequest

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/student', methods=['GET', 'POST'])
def student_dashboard():
    if request.method == 'POST':
        student_name = request.form['name']
        reason = request.form['reason']
        details = request.form['details']
        new_request = PermissionRequest(
            student_name=student_name, reason=reason, details=details, status="Pending"
        )
        db.session.add(new_request)
        db.session.commit()
        flash("Permission request submitted successfully!")
        return redirect(url_for('student_dashboard'))
    return render_template('student_dashboard.html')

@app.route('/dean', methods=['GET', 'POST'])
def dean_dashboard():
    requests = PermissionRequest.query.all()
    if request.method == 'POST':
        request_id = request.form['request_id']
        action = request.form['action']
        letter_content = request.form.get('letter_content', '')
        permission_request = PermissionRequest.query.get(request_id)
        permission_request.status = "Approved" if action == "approve" else "Rejected"
        permission_request.letter = letter_content
        db.session.commit()
        flash("Request processed successfully!")
        return redirect(url_for('dean_dashboard'))
    return render_template('dean_dashboard.html', requests=requests)

@app.route('/letter/<int:request_id>')
def generate_letter(request_id):
    permission_request = PermissionRequest.query.get(request_id)
    return render_template('letter.html', request=permission_request)

if __name__ == "__main__":
    app.run(debug=True)
