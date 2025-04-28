from flask import Blueprint, render_template, request, redirect, session
from conn import get_connection

bp = Blueprint('post_routes', __name__)

@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ads WHERE user_id=? ORDER BY date_posted DESC", (session['user_id'],))
    ads = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', ads=ads)

@bp.route('/post-ad', methods=['GET', 'POST'])
def post_ad():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['description']
        price = request.form['price']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ads (title, description, price, user_id) VALUES (?, ?, ?, ?)",
                       (title, desc, price, session['user_id']))
        conn.commit()
        conn.close()
        return redirect('/dashboard')

    return render_template('post_ad.html')

@bp.route('/Check_route', methods=['GET', 'POST'])
def check_route():
    return render_template('ad_apartment.html')