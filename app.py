import os

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Set the configuration options for the database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# Initialize the SQLAlchemy object
db = SQLAlchemy(app)

# Add context to the app
app.app_context().push()

# Define the database model
class Entreprise(db.Model):
    __tablename__ = 'entreprises'

    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    marque = db.Column(db.String(100), nullable=False)
    numero = db.Column(db.String(100), nullable=False)
    date_fab = db.Column(db.DateTime(timezone=True), server_default=db.func.now())

    # Define a method to save the object to the database
    def save(self):
        db.session.add(self)
        db.session.commit()

    # Define a method to return a string representation of the object
    def __repr__(self):
        return f'<Entreprise {self.id}>'

# Create the database tables
db.create_all()

# Define the route for the home page
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Retrieve the form data and create a new object
        mod = request.form.get('model')
        mrq = request.form.get('marque')
        num = request.form.get('numero')
        data = Entreprise(model=mod, marque=mrq, numero=num)
        data.save()
        # Redirect to the home page
        return redirect(url_for('index'))

    # Retrieve all the data from the database
    all_data = Entreprise.query.all()
    # Render the home page template with the data
    return render_template('index.html', data=all_data)

# Define the route for deleting an object
@app.route('/delete/<int:id>')
def delete1(id):
    # Retrieve the object to be deleted and delete it from the database
    data = Entreprise.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    # Redirect to the home page
    return redirect(url_for('index'))

# Define the route for editing an object
@app.route('/<int:id>/edit/', methods = ['GET', 'POST'])
def edit(id):
    # Retrieve the object to be edited
    data = Entreprise.query.get_or_404(id)
    if request.method == 'POST':
        # Retrieve the form data and update the object
        mod = request.form.get('model')
        mrq = request.form.get('marque')
        num = request.form.get('numero')
        data.model = mod
        data.marque = mrq
        data.numero = num
        data.save()
        # Redirect to the home page
        return redirect(url_for('index'))
    # Render the edit page template with the data
    return render_template('edit.html', data=data)

# Define the route for displaying the home page
@app.route('/home')
def home():
    return render_template('home.html')

# Define the route for displaying the about page
@app.route('/about')
def about():
    return render_template('about.html')

# Run the application
if __name__ == '__main__':
    app.run(debug=True)