from flask import Flask,render_template,request,redirect,url_for,session, render_template_string
import mysql.connector
from db import db_config
import os
import joblib
app=Flask(__name__)
app.secret_key='your-secret-key'

model_filename='model.pickle'
model_path=os.path.abspath(model_filename)
with open(model_path,'rb') as pk1:
    model=joblib.load(pk1)

@app.route('/')

def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        session["username"]=username
        
        try:
            connection=mysql.connector.connect(**db_config)
            cur=connection.cursor()
            cur.execute("SELECT username, password FROM registration WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()
            connection.close()
            if username and pwd == user[1]: 
                return redirect(url_for('index'))
            else:
                return render_template('login.html', alert="Invalid username or password")
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template('login.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        name=request.form['name']   
        dob=request.form['dob']
        blood=request.form['blood']
        phone=request.form['phone']
        username=request.form['username']
        password=request.form['password'] 
        try:
            connection=mysql.connector.connect(**db_config)
            cur=connection.cursor()
            cur.execute("SELECT COUNT(*) FROM registration WHERE username = %s", (username,))
            result = cur.fetchone()
            
            if result[0] > 0:  
                cur.close()
                connection.close()
                return render_template('register.html', alert="Username Already Present")
            
            cur.execute(f"insert into registration(name,dob,blood_group,phone_no,username,password)values('{name}','{dob}','{blood}','{phone}','{username}','{password}')")
            connection.commit()
            cur.close()
            return render_template('login.html', alert="Registered Successfully")
            
            #return redirect(url_for('login'))
        except Exception as e:
            return f"An error occurred: {e}"
    return render_template('register.html')

@app.route('/index',methods=['GET','POST'])
def index():
    if "username" in session:
        return render_template('home.html')
    else:
      return render_template_string("""
    <script>
        alert('You need to log in to access this page!');
        window.location.href = "{{ url_for('login') }}";
    </script>
    """)

@app.route('/nav')
def about():
    return render_template('nav.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if "username" in session:
        username = session['username']

        if request.method == 'POST':
            try:
                connection = mysql.connector.connect(**db_config)
                cur = connection.cursor()
                cur.execute("SELECT name FROM registration WHERE username = %s", (username,))
                name_tuple = cur.fetchone()
                name = name_tuple[0]
                # Extracting form data
                gender = request.form['gender']
                smoking = request.form['smoking']
                heart_disease = request.form['heart_disease']
                hypertension = request.form['hypertension']
                age = float(request.form['age'])
                bmi = float(request.form['bmi'])
                haemoglobin = float(request.form['haemogloblin'])  # Fixed typo
                glucose = float(request.form['glucose'])

                # Converting form data to numerical values
                gender_value = 0 if gender == 'male' else 1
                smoke_value = (
                    0 if smoking == 'no info'
                    else 1 if smoking == 'never'
                    else 2 if smoking == 'former'
                    else 3 if smoking == 'current'
                    else 4 if smoking == 'not current'
                    else 5
                )
                heart_disease_value = 1 if heart_disease == 'yes' else 0
                hypertension_value = 1 if hypertension == 'yes' else 0

                # Making prediction using the model
                prediction = model.predict([[gender_value, age, hypertension_value, heart_disease_value, smoke_value, bmi, haemoglobin, glucose]])
                prediction = round(prediction[0])
                if prediction ==1:
                    prediction="Positive"
                else:
                    prediction="Negative"

                cur.execute("SELECT COUNT(*) FROM result WHERE name = %s", (name,))
                result_count = cur.fetchone()[0]
                if result_count > 0:
                    cur.execute("""
                    UPDATE result SET gender = %s, age = %s, hypertension = %s, heart_disease = %s,
                    smoking = %s, bmi = %s, haemoglobin = %s, glucose = %s, result = %s
                    WHERE name = %s
                    """, (gender, age, hypertension, heart_disease, smoking, bmi, haemoglobin, glucose, prediction, name))
                else:
                    cur.execute(
                        """
                        INSERT INTO result (name, gender, age, hypertension, heart_disease, smoking, bmi, haemoglobin, glucose, result)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (name, gender, age, hypertension, heart_disease, smoking, bmi, haemoglobin, glucose, prediction)
                )
                connection.commit()
                cur.close()
                connection.close()

                return redirect(url_for('result'))

            except Exception as e:
                return f"An error occurred: {e}"

        return render_template('prediction.html')

    else:
        return render_template_string("""
        <script>
            alert('You need to log in to access this page!');
            window.location.href = "{{ url_for('login') }}";
        </script>
        """)


@app.route('/result')
def result():
    if "username" in session:
        username = session['username']
        try:
            connection = mysql.connector.connect(**db_config)
            cur = connection.cursor()

            # Get the name from the registration table
            cur.execute("SELECT name FROM registration WHERE username = %s", (username,))
            name_tuple = cur.fetchone()
            
            if name_tuple:
                username = name_tuple[0]

                # Get the user's results from the result table
                cur.execute("SELECT name, gender, age, hypertension, heart_disease, smoking, bmi, haemoglobin, glucose, result FROM result WHERE name = %s", (username,))
                user = cur.fetchone()

                if user:
                    # If user data is found, pass it to the template
                    cur.close()
                    connection.close()
                    return render_template('result.html', user=user)
                else:
                    # No results found in the result table
                    cur.close()
                    connection.close()
                    return render_template_string("""
                    <script>
                    alert('No data found for this user');
                    window.location.href = "{{ url_for('index') }}";
                </script>
                """)
            else:
                # No user found in the registration table
                return "No data found for the username."
        
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        # User is not logged in
        return render_template_string("""
    <script>
        alert('You need to log in to access this page!');
        window.location.href = "{{ url_for('login') }}";
    </script>
    """)

@app.route('/profile')
def profile():
    if "username" in session:
        username=session['username']
        #return f"<h1>{username}</h1>"
        try:
            connection=mysql.connector.connect(**db_config)
            cur=connection.cursor()
            cur.execute("SELECT name,dob,blood_group,phone_no FROM registration WHERE username = %s", (username,))
            user = cur.fetchone()
            cur.close()
            connection.close()
            return render_template('profile.html',user=user)
        except Exception as e:
            return f"An error occurred: {e}"
    else:
        return render_template_string("""
    <script>
        alert('You need to log in to access this page!');
        window.location.href = "{{ url_for('login') }}";
    </script>
    """)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__=='__main__':
    app.run(debug=True)