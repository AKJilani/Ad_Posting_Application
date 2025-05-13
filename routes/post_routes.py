from flask import Blueprint, render_template, request, redirect, session, flash, jsonify
from conn import get_connection

bp = Blueprint('post_routes', __name__)

@bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ad_apartment WHERE user_id=? ORDER BY Post_Date DESC", (session['user_id'],))
    ads = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', ads=ads)

# --- POST and DISPLAY Ad Form ---
@bp.route('/post_ad', methods=['GET', 'POST'])
def post_ad():
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        data = request.form
        conn = get_connection()
        cursor = conn.cursor()

        # INSERT with exactly 17 values for 17 fields (excluding Post_Date and Ad_Active_Status)
        cursor.execute("""
            INSERT INTO ad_apartment (
                Building_Number, Apartment_Type, Apartment_Number, Bedrooms, Bathrooms,
                Parking, Tenant_Type, Available_From_Date,
                Rent_Per_Month, Advance_Payment, Phone_Number, Address, Restrictions,
                Description, user_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['building_no'], data['Apartment_Type'], data['Apartment_Number'], data['Bedrooms'], data['Bathrooms'],
            data['Parking_Facility'], data['Tenant_Type'], data['Available_From_Date'],
            data['Rent_Per_Month'], data['Advance_Payment'], data['Phone_Number'], data['Address'], data['Restrictions'],
            data['Description'], session['user_id']
        ))

        conn.commit()
        conn.close()
        flash('Ad posted successfully!')
        return redirect('/dashboard')

    return render_template('post_ad.html', ad=None)

@bp.route('/edit_ad_flat/<int:id>', methods=['GET'])
def edit_ad_flat(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ad_apartment WHERE Id = ?", (id,))
    ad_data = cursor.fetchone()
    conn.close()

    if ad_data:
        # Convert to dictionary if you're using tuple fetch
        keys = [description[0] for description in cursor.description]
        ad_dict = dict(zip(keys, ad_data))

        return render_template('update_ad.html', ad=ad_dict, is_edit=True)
    else:
        flash("Ad not found", "danger")
        return redirect('/dashboard')


@bp.route('/update_ad_flat/<int:id>', methods=['POST'])
def update_ad_flat(id):
    if 'user_id' not in session:
        return redirect('/login')

    if request.method == 'POST':
        data = request.form
        conn = get_connection()
        cursor = conn.cursor()

        # UPDATE with all necessary fields
        cursor.execute("""
            UPDATE ad_apartment SET
                Building_Number = ?, 
                Apartment_Type = ?, 
                Apartment_Number = ?, 
                Bedrooms = ?, 
                Bathrooms = ?,
                Parking = ?, 
                Tenant_Type = ?, 
                Available_From_Date = ?,
                Rent_Per_Month = ?, 
                Advance_Payment = ?, 
                Phone_Number = ?, 
                Address = ?, 
                Restrictions = ?,
                Description = ?
            WHERE Id = ? AND user_id = ?
        """, (
            data['building_no'], data['Apartment_Type'], data['Apartment_Number'], 
            data['Bedrooms'], data['Bathrooms'], data['Parking_Facility'], 
            data['Tenant_Type'], data['Available_From_Date'],
            data['Rent_Per_Month'], data['Advance_Payment'], data['Phone_Number'], 
            data['Address'], data['Restrictions'], data['Description'], 
            id, session['user_id']
        ))

        conn.commit()
        conn.close()
        flash('Ad updated successfully!')
        return redirect('/dashboard')

    return redirect('/dashboard')


@bp.route('/delete_ad_flat/<int:ad_id>', methods=['DELETE'])
def delete_ad_flat(ad_id):
    if 'user_id' not in session:
        return jsonify(success=False), 403

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ad_apartment WHERE Id=? AND user_id=?", (ad_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify(success=True)

@bp.route('/mark_available_flat/<int:ad_id>', methods=['POST'])
def mark_available_flat(ad_id):
    if 'user_id' not in session:
        return jsonify(success=False), 403

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ad_apartment SET Ad_Active_Status=0 WHERE Id=? AND user_id=?", (ad_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify(success=True)

@bp.route('/mark_not_available_flat/<int:ad_id>', methods=['POST'])
def mark_not_available_flat(ad_id):
    if 'user_id' not in session:
        return jsonify(success=False), 403

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ad_apartment SET Ad_Active_Status=1 WHERE Id=? AND user_id=?", (ad_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify(success=True)
