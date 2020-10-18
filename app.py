from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL



app = Flask(__name__)
app.secret_key = 'cookie dough'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'traxex23999'
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)



@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM students")
    data = cur.fetchall()
    cur.close()




    return render_template('index.html', students=data )



@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == "POST":
        flash("Data Saved Successfully")
        id_number = request.form['id_number']
        name = request.form['name']
        department = request.form['department']
        course = request.form['course']
        year = request.form['year']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (id_number, name, department, course, year) VALUES (%s,%s, %s, %s, %s)", (id_number, name, department, course, year))
        mysql.connection.commit()
        return redirect(url_for('home'))




@app.route('/delete/<string:id_number>', methods = ['GET'])
def delete(id_number):
    flash("Student Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id_number=%s", (id_number,))
    mysql.connection.commit()
    return redirect(url_for('home'))





@app.route('/update',methods=['POST','GET'])
def update():

    if request.method == 'POST':
        id_number = request.form['id_number']
        name = request.form['name']
        department = request.form['department']
        course = request.form['course']
        year = request.form['year']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE students
               SET name=%s, department=%s, course=%s, year=%s
               WHERE id_number=%s
            """, (name, department, course, year, id_number))
        flash("Data Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)
