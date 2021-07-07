from flask import Flask, render_template, url_for, request, redirect
from manageDB import create_database, fetch_items_from_database, delete_item_from_database
from manageDB import format_date, fetch_one_item_from_database, edit_single_record, check_entry
import sqlite3 
import os 



# if the database doesn't exist, create it
db_is_new = not os.path.exists('journal.db')
if db_is_new:
    create_database()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ADD_KEY_HERE'
app.config['TESTING'] = True



"""
If accessed via GET request -> Display the home page with all the
already created posts (if they exist). It only shows the titles and
dates of the posts. If the user wants to view the post in more detail,
they have to click on the title.

If accessed via POST request -> When a user creates a new post from 
the new.html file, the start() route method will retrieve the data 
and use it to create a new record in the database.
"""
@app.route('/', methods=['GET', 'POST'])
def start():  
    if request.method == 'POST':
        
        try:
            X1 = request.form['title']
            X2 = request.form['date']
            X3 = request.form['timeSpent']
            X4 = request.form['whatILearned']
            X5 = request.form['ResourcesToRemember']
            X6 = format_date(X2)

            check_this_entry = {'title': X1, 'formattedDate': X6}
            already_exists = check_entry(check_this_entry)
            if not already_exists:
                conn = sqlite3.connect('journal.db')
                c = conn.cursor()
                c.execute("INSERT INTO entries (title,date,timespent,learned,resources,formattedDate) VALUES (?,?,?,?,?,?)", (X1,X2,X3,X4,X5,X6,) )
                conn.commit()
        except:
            conn.rollback() # roll back all changes if an exception occurs.
        finally:
            # re-fetch the rows so the new blog post shows up right away
            rows = fetch_items_from_database()
            return render_template("index.html", rows=rows)
            conn.close()

    # returns a Sqlite Row object containing all data from the journal db
    rows = fetch_items_from_database() 
    return render_template("index.html", rows=rows)



""" On the new.html page, the user will fill out the form to create
a new post (or record) in the journal.db file. The page will send the data and 
redirect the user, via the POST request, back to the home page. """
@app.route('/new')
def new_entry():
    return render_template('new.html')



"""After the user fills out the form on the edit.html page,
this routing method is what actually modifies the record in the 
database. It uses the data from the form and the id number of the
record to offically update the record. """
@app.route('/update_record<the_id>', methods=['GET', 'POST'])
def updateRecord(the_id):
    if request.method == 'POST':
        X1 = request.form['title']
        X2 = request.form['date']
        X3 = request.form['timeSpent']
        X4 = request.form['whatILearned']
        X5 = request.form['ResourcesToRemember']
        X6 = None 
        if (X2):
            X6 = format_date(X2)
        
        _dict = {'title': X1, 'date': X2, 'timespent': X3, 'learned': X4, 'resources': X5, 'formattedDate': X6}
        # Modified values and values the user left unmodified will appear.
        edit_single_record(_dict, the_id)
        return redirect(url_for('start'))
    return redirect(url_for('start'))



"""When the user clicks 'edit entry' on the detail.html page, the
user is redirected to the edit.html page, where there is a form. The
edit_post routing method accepts an id number as a
parameter in order to identify the correct record from the database. 
After the user fills out the form and clicks 'Publish Entry', it redirects
to the updateRecord routing method, sending the id number and data from the 
form to modify the record. """
@app.route('/edit<the_id>', methods=['GET', 'POST'])
def edit_post(the_id):
    return render_template('edit.html', the_id=the_id)


""" """
@app.route('/delete<the_id>', methods=['GET', 'POST'])
def delete_post(the_id):
    delete_item_from_database(the_id)
    return redirect(url_for('start'))



""" 
This allows the user to view each post in more detail.
If the user clicks on the title from one of the posts from the 
home page, the user gets redirected to the get_details() routing
method. It uses the id number from the parameter to correctly identify
the record. It displays the entire post. """
@app.route('/detail<the_id>', methods=['GET', 'POST'])
def get_details(the_id):
    # Note: fetch_one_item_from_database() returns a python dictionary, not Sqlite Row object.
    row = fetch_one_item_from_database(the_id)
    return render_template('detail.html', row=row)



""" This allows the user to view the entire database, both columns
and values. """
@app.route('/list')
def list():
    rows = fetch_items_from_database()
    return render_template("list.html", rows = rows)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)