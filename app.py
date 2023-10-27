"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:password@localhost:5432/blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'


with app.app_context():
    connect_db(app)
    db.create_all()
    new_user5 = User(first_name="Pamela", last_name="Vegan", image_url="https://www.freeiconspng.com/uploads/face-head-woman-female-icon-23.png")
    db.session.add(new_user5)
    db.session.commit()



# **GET */ :*** Redirect to list of users. (We’ll fix this in a later step).
@app.route('/')
def root():
    """Homepage will redirect to the user list."""
    return redirect("/users")


# **GET */users :*** Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form.
@app.route('/users')
def users_index():
    """Show information for all users."""

    users = User.query.order_by(User.first_name, User.last_name).all()
    return render_template('users/index.html', users=users)


# **GET */users/new :*** Show an add form for users
@app.route('/users/new', methods=["GET"])
def users_add_form():
    """Display a form for adding a new user."""

    return render_template('users/add_user.html')


# **POST */users/new :*** Process the add form, adding a new user and going back to ***/users***
@app.route("/users/new", methods=["POST"])
def users_add():
    """Process the form submission for adding a new user."""

    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


# **GET */users/[user-id] :***Show information about the given user. Have a button to get to their edit page, and to delete the user.
@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show information about the given user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/show_user.html', user=user)


# **GET */users/[user-id]/edit :*** Show the edit page for a user. Have a cancel button that returns to the detail page for a user, and a save button that updates the user.
@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show the edit page for an existing user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


# **POST */users/[user-id]/edit :***Process the edit form, returning the user to the ***/users*** page.
@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Process the edit form for updating an existing user."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


# **POST */users/[user-id]/delete :*** Delete the user.
@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Process form for deleting an existing user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

