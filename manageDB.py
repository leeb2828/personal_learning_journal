import sqlite3 
import datetime


def check_entry(dict_item):
    conn = sqlite3.connect('journal.db')
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    c.execute("SELECT * FROM entries")
    rows = c.fetchall()

    already_exists = False
    for row in rows:
        val1 = row['title']
        val2 = dict_item['title']
        val3 = row['formattedDate']
        val4 = dict_item['formattedDate']
        if val1.upper() == val2.upper() and val3 == val4:
            already_exists = True
            conn.commit() 
            conn.close() 
            return already_exists
        
                 
    conn.commit() 
    conn.close() 

    return already_exists 


"""
Called from the start() and list() route methods in app.py.
Retrieves all the entries from the journal database.
@Returns: a Sqlite Row object containing all the keys and values
stored in the database.
"""
def fetch_items_from_database():
    conn = sqlite3.connect('journal.db')
    conn.row_factory = sqlite3.Row 
    c = conn.cursor()
    c.execute("SELECT * FROM entries")

    rows = c.fetchall()
    conn.commit() 
    conn.close() 
    return rows


"""
Called from the get_details() route method from app.py.
Using the id number from the parameter, it finds the correct
entry from the database. Using the record found in the database, 
creates a python dictionary storing the values.
@Returns: A python dictionary containing values from the record.
"""
def fetch_one_item_from_database(the_id):
    row_dict = {}

    # create connection
    conn = sqlite3.connect('journal.db')
    # create cursor object
    c = conn.cursor()
    # query the database using cursor object
    # https://techoverflow.net/2019/10/14/how-to-fix-sqlite3-python-incorrect-number-of-bindings-supplied-the-current-statement-uses-1-supplied/
    c.execute("SELECT * FROM entries WHERE id = (?)", [str(the_id)])
    # fetch items
    items = c.fetchone()

    row_dict['id'] = items[0]
    row_dict['title'] = items[1]
    row_dict['date'] = items[2]
    row_dict['timespent'] = items[3]
    row_dict['learned'] = items[4]
    row_dict['resources'] = items[5]
    row_dict['formattedDate'] = items[6]

    conn.commit() 
    conn.close() 

    return row_dict


""" Called from the delete_post routing method. """
def delete_item_from_database(the_id):
    # create connection
    conn = sqlite3.connect('journal.db')
    # create cursor object
    c = conn.cursor()
    # query the database using cursor object
    c.execute("DELETE FROM entries WHERE id = (?)", [str(the_id)])

    conn.commit()
    conn.close()


"""
Called from start() and update_record() route functions from app.py
@Parameter: A date from the HTML form.
This method will take a date for example, such as "2021-06-01", and 
return it in the string form as "June 01, 2021" that will be
displayed on the index.html page.
@Returns: 
"""
def format_date(param):
    the_date = param
    # convert string date to a datetime object
    my_date = datetime.datetime.strptime(the_date, "%Y-%m-%d")

    month = my_date.strftime("%B")
    day = my_date.strftime("%d")
    year = my_date.strftime("%Y")

    date_dict = {'month': month, 'day': day, 'year': year}
    
    month = date_dict['month']
    day = date_dict['day']
    year = date_dict['year']
    X6 = f"{month} {day}, {year}" 

    return X6 


"""
This function will only run once. Once journal.db is created,
it will not run again.
"""  
def create_database():
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()

    sql_query = """ CREATE TABLE entries (
        id integer PRIMARY KEY AUTOINCREMENT,
        title text NOT NULL,
        date integer NOT NULL,
        timespent text NOT NULL,
        learned text NOT NULL,
        resources text NOT NULL,
        formattedDate text NOT NULL
    )"""

    cursor.execute(sql_query)
    conn.commit()
    conn.close()

"""
Called from the updateRecord() route function from app.py
@parameter: python dictionary containing updated values for single record.
@parameter: number representing the id of the record to be updated.
"""
def edit_single_record(edited_dict, the_id):
    changed_items = {}
    
    for key, value in edited_dict.items():
        if value:
            changed_items[key] = value 

    print(changed_items)

    # create connection
    conn = sqlite3.connect('journal.db')
    # create cursor object
    c = conn.cursor()
    # query the database using cursor object
    
    for key, value in changed_items.items():
        val = str(value)
        recordID = str(the_id)
        c.execute("""UPDATE entries SET %s = ?
                WHERE id = ?
        """ %(key),(val, recordID,) )
        conn.commit()


    conn.close()

    
    