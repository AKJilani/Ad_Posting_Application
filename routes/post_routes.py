from flask import Blueprint, render_template, request, redirect, session, flash
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
    print(ads)  # Debugging line to check the fetched ads
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
                Parking, Tenant_Type, Security, Water, Available_From_Date,
                Rent_Per_Month, Advance_Payment, Phone_Number, Address, Restrictions,
                Description, user_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['building_no'], data['Apartment_Type'], data['Apartment_Number'], data['Bedrooms'], data['Bathrooms'],
            data['Parking_Facility'], data['Tenant_Type'], data['Security'], data['Water'], data['Available_From_Date'],
            data['Rent_Per_Month'], data['Advance_Payment'], data['Phone_Number'], data['Address'], data['Restrictions'],
            data['Description'], session['user_id']
        ))

        conn.commit()
        conn.close()
        flash('Ad posted successfully!')
        return redirect('/dashboard')

    return render_template('post_ad.html')