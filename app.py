from flask import Flask, render_template, request, redirect, url_for, flash, session
import MySQLdb

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key in production


# MySQL Database Configuration
def connect_db():
    return MySQLdb.connect(host="localhost", user="root", passwd="password", db="user_db")


# Route for Root URL
@app.route('/')
def home():
    return redirect(url_for('register'))

#practice route
@app.route('/practice1')
def practice1():
    return render_template('practice1.html')


#string route
@app.route('/stringv')
def stringv():
    return render_template('stringv.html')

#practice route
@app.route('/practice2')
def practice2():
    return render_template('practice2.html')

# Route for Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            db.close()

            if user:
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('mainpage'))
            else:
                flash('Invalid username or password. Please try again.', 'danger')
        except MySQLdb.Error:
            flash('Database error occurred. Please try again later.', 'danger')

    return render_template('login.html')


# Route for Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm-password']

        # Server-side password validation
        error_message = []
        if len(password) < 8:
            error_message.append("Password must be at least 8 characters long.")
        if not any(char.isupper() for char in password):
            error_message.append("Password must include at least one uppercase letter.")
        if not any(char.isdigit() for char in password):
            error_message.append("Password must include at least one number.")
        if not any(char in "!@#$%^&*(),.?\":{}|<>" for char in password):
            error_message.append("Password must include at least one special character.")
        if password != confirm_password:
            error_message.append("Passwords do not match.")

        if error_message:
            flash("<br>".join(error_message), 'danger')
            return redirect(url_for('register'))

        # Insert into database if validation passes
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
            db.commit()
            db.close()

            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))

        except MySQLdb.Error as err:
            if err.args[0] == 1062:  # Duplicate entry
                flash('Username already exists. Please choose a different username.', 'danger')
            else:
                flash('Database error occurred. Please try again later.', 'danger')

    return render_template('register.html')

# Route for Page after successful login
@app.route('/mainpage')
def mainpage():
    if 'username' in session:
        return render_template('mainpage.html', username=session['username'])
    else:
        flash('You need to log in first!', 'warning')
        return redirect(url_for('login'))
    
#flashcards
@app.route('/flashcards')
def flashcards():
    return render_template('flashcards.html')

#practice route
@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

#ARV route
@app.route('/ARV')
def ARV():
    return render_template('arrayanm.html')

    # Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)