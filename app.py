from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'phi_protection_tool_secret_key'

# Database connection
def get_db_connection():
    conn = sqlite3.connect('phi_compliance.db')
    conn.row_factory = sqlite3.Row
    return conn

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Vendor submission form
@app.route('/add_vendor', methods=['GET', 'POST'])
def add_vendor():
    if request.method == 'POST':
        vendor_name = request.form['vendor_name']
        contact = request.form['contact']
        encryption = request.form['encryption']
        data_destruction = request.form['data_destruction']
        access_control = request.form['access_control']
        audit_logs = request.form['audit_logs']
        incident_response = request.form['incident_response']
        subcontractor_compliance = request.form['subcontractor_compliance']
        employee_training = request.form['employee_training']
        date_submitted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO vendors (vendor_name, contact, encryption, data_destruction, access_control, audit_logs, incident_response, subcontractor_compliance, employee_training, date_submitted)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (vendor_name, contact, encryption, data_destruction, access_control, audit_logs, incident_response, subcontractor_compliance, employee_training, date_submitted))
        conn.commit()
        conn.close()

        flash('Vendor information has been submitted successfully!', 'success')
        return redirect(url_for('vendor_list'))

    return render_template('vendor_form.html')

# Vendor dashboard/list
@app.route('/vendors')
def vendor_list():
    conn = get_db_connection()
    vendors = conn.execute('SELECT * FROM vendors').fetchall()
    conn.close()
    return render_template('vendor_list.html', vendors=vendors)

# View vendor report
@app.route('/report/<int:vendor_id>')
def compliance_report(vendor_id):
    conn = get_db_connection()
    vendor = conn.execute('SELECT * FROM vendors WHERE id = ?', (vendor_id,)).fetchone()
    conn.close()
    return render_template('compliance_report.html', vendor=vendor)

if __name__ == '__main__':
    app.run(debug=True)
