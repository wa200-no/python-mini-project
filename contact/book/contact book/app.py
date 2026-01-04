from flask import Flask, render_template, request, jsonify
import csv
import os

app = Flask(__name__)
CSV_FILE = 'Book1.csv'

def read_contacts():
    contacts = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contacts.append(row)
    return contacts

def write_contacts(contacts):
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['username', 'contact'])
        writer.writeheader()
        writer.writerows(contacts)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts', methods=['GET'])
def get_all():
    return jsonify(read_contacts())

@app.route('/contact/<username>', methods=['GET'])
def get_contact(username):
    for c in read_contacts():
        if c['username'] == username:
            return jsonify(c)
    return jsonify({'error': 'User not found'}), 404

@app.route('/add', methods=['POST'])
def add_contact():
    data = request.json
    contacts = read_contacts()
    contacts.append({
        'username': data['username'],
        'contact': data['contact']
    })
    write_contacts(contacts)
    return jsonify({'message': 'Contact added'})

@app.route('/delete/<username>', methods=['DELETE'])
def delete_contact(username):
    contacts = read_contacts()
    contacts = [c for c in contacts if c['username'] != username]
    write_contacts(contacts)
    return jsonify({'message': 'Contact deleted'})

if __name__ == '__main__':
    app.run(debug=True)