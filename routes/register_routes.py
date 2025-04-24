from flask import Blueprint, render_template, request, redirect, flash
import sqlite3
from conn import get_connection

bp = Blueprint('register_routes', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        apartment_type = request.form['apartment_type']
        apartment_number = request.form['apartment_number']
        parking_number = request.form['parking_number']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('''
                INSERT INTO users 
                (Apartment_Type, Apartment_Number, Parking_Number, username, email, password)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (apartment_type, apartment_number, parking_number, username, email, password))
            conn.commit()
            flash('✅ Registered successfully!', 'success')
            return redirect('/login')
        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                flash('⚠️ Username or email already exists!', 'danger')
            else:
                flash('⚠️ Integrity error occurred!', 'danger')
            flash(f'⚠️ Error: {str(e)}', 'danger')
        finally:
            conn.close()

    return render_template('register.html')

