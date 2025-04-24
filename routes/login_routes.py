from flask import Blueprint, render_template, request, redirect, session, flash
from conn import get_connection

bp = Blueprint('login_routes', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/dashboard')
        else:
            flash("Invalid username or password", "danger")

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash('🔒 You have been logged out successfully.', 'info')
    return redirect('/login')  # Redirect to login or homepage
