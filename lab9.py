from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

web_app = Flask(__name__)
web_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts_database.sqlite'
database = SQLAlchemy(web_app)

class Person(database.Model):
    person_id = database.Column(database.Integer, primary_key=True)
    full_name = database.Column(database.String(100), nullable=False)
    telephone = database.Column(database.String(20), nullable=False)

@web_app.route('/register', methods=['POST'])
def register_person():
    full_name = request.form['full_name']
    telephone = request.form['telephone']
    
    # Check if the person already exists in the database
    person_exists = Person.query.filter((Person.full_name == full_name) | (Person.telephone == telephone)).first()
    if person_exists:
        return "Entry already exists in the directory."

    new_entry = Person(full_name=full_name, telephone=telephone)
    database.session.add(new_entry)
    database.session.commit()
    return redirect(url_for('show_directory'))

@web_app.route('/directory')
def show_directory():
    directory_entries = Person.query.all()
    return render_template('directory.html', directory_entries=directory_entries)

@web_app.route('/reset', methods=['POST'])
def reset_directory():
    Person.query.delete()
    database.session.commit()
    return redirect(url_for('show_directory'))

if __name__ == '__main__':
    with web_app.app_context():
        database.create_all()
    web_app.run(debug=True)
