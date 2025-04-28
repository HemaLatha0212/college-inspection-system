from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3
import os

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'inspection.db')
app.config['SECRET_KEY'] = 'change_this_to_a_secure_random_key'

# Database helpers
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# CLI command to initialize the database
def init_db():
    db = get_db()
    with app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    print('Initialized the database.')

import click
@app.cli.command('init-db')
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()

# Routes
@app.route('/')
def index():
    db = get_db()
    colleges = db.execute('SELECT * FROM Colleges').fetchall()
    return render_template('index.html', colleges=colleges)

@app.route('/add_college', methods=['GET', 'POST'])
def add_college():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        if not name or not location:
            flash('Name and location are required.')
        else:
            db = get_db()
            db.execute('INSERT INTO Colleges (name, location) VALUES (?, ?)', (name, location))
            db.commit()
            return redirect(url_for('index'))
    return render_template('add_college.html')

@app.route('/departments/<int:college_id>', methods=['GET', 'POST'])
def departments(college_id):
    db = get_db()
    college = db.execute('SELECT * FROM Colleges WHERE id = ?', (college_id,)).fetchone()
    if not college:
        flash('College not found.')
        return redirect(url_for('index'))
    if request.method == 'POST':
        dept = request.form['department_name']
        head = request.form['head']
        desc = request.form['description']
        if not dept:
            flash('Department name is required.')
        else:
            db.execute('INSERT INTO Departments (college_id, department_name, head, description) VALUES (?, ?, ?, ?)',
                       (college_id, dept, head, desc))
            db.commit()
            return redirect(url_for('departments', college_id=college_id))
    depts = db.execute('SELECT * FROM Departments WHERE college_id = ?', (college_id,)).fetchall()
    return render_template('departments.html', college=college, depts=depts)

@app.route('/inspections', methods=['GET'])
def inspections():
    db = get_db()
    data = db.execute(
        'SELECT i.id, c.name as college, i.inspection_date, i.inspector, i.remarks '
        'FROM Inspections i JOIN Colleges c ON i.college_id=c.id'
    ).fetchall()
    return render_template('inspections.html', inspections=data)

@app.route('/add_inspection', methods=['GET', 'POST'])
def add_inspection():
    db = get_db()
    colleges = db.execute('SELECT id, name FROM Colleges').fetchall()
    if request.method == 'POST':
        college_id = request.form['college_id']
        date = request.form['inspection_date']
        inspector = request.form['inspector']
        remarks = request.form['remarks']
        if not college_id or not date:
            flash('College and date are required.')
        else:
            db.execute('INSERT INTO Inspections (college_id, inspection_date, inspector, remarks) VALUES (?, ?, ?, ?)',
                       (college_id, date, inspector, remarks))
            db.commit()
            return redirect(url_for('inspections'))
    return render_template('add_inspection.html', colleges=colleges)

@app.route('/criteria', methods=['GET', 'POST'])
def criteria():
    db = get_db()
    if request.method == 'POST':
        name = request.form['criterion_name']
        max_score = request.form['max_score']
        desc = request.form['description']
        if not name or not max_score:
            flash('Name and max score are required.')
        else:
            db.execute('INSERT INTO Criteria (criterion_name, max_score, description) VALUES (?, ?, ?)',
                       (name, max_score, desc))
            db.commit()
            return redirect(url_for('criteria'))
    items = db.execute('SELECT * FROM Criteria').fetchall()
    return render_template('criteria.html', criteria=items)

@app.route('/inspection_ratings', methods=['GET', 'POST'])
def inspection_ratings():
    db = get_db()
    inspections = db.execute('SELECT id, inspection_date FROM Inspections').fetchall()
    criteria_list = db.execute('SELECT id, criterion_name FROM Criteria').fetchall()
    if request.method == 'POST':
        inspection_id = request.form['inspection_id']
        criterion_id = request.form['criterion_id']
        score = request.form['score']
        remarks = request.form['remarks']
        if not inspection_id or not criterion_id or not score:
            flash('All fields except remarks are required.')
        else:
            db.execute('INSERT INTO Inspection_Ratings (inspection_id, criterion_id, score, remarks) VALUES (?, ?, ?, ?)',
                       (inspection_id, criterion_id, score, remarks))
            db.commit()
            return redirect(url_for('inspection_ratings'))
    ratings = db.execute(
        'SELECT r.id, i.inspection_date, c.criterion_name, r.score, r.remarks '
        'FROM Inspection_Ratings r '
        'JOIN Inspections i ON r.inspection_id=i.id '
        'JOIN Criteria c ON r.criterion_id=c.id'
    ).fetchall()
    return render_template('add_inspection_rating.html', inspections=inspections, criteria=criteria_list, ratings=ratings)

if __name__ == '__main__':
    app.run(debug=True)
