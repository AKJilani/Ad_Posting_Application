from flask import Flask, render_template, request, redirect, session, url_for
from conn import get_connection

app = Flask(__name__)
app.secret_key = 'aspdfkNM35cv@dfggh5s6fgsgt@s098765436e@4f6ggh@jBDSDASw@rekfpas@dkfpoa@sdok@f96a4d@s6@5sea5@df61as@d3f1Q@WDYF@HD@YG1K@UI@L13K@DF3D'

from routes import register_routes, login_routes, post_routes
app.register_blueprint(register_routes.bp)
app.register_blueprint(login_routes.bp)
app.register_blueprint(post_routes.bp)

@app.route('/')
def home():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT ads.*, users.username FROM ads JOIN users ON users.id = ads.user_id ORDER BY date_posted DESC")
    ads = cursor.fetchall()
    conn.close()
    return render_template('home.html', ads=ads)
