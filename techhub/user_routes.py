
import json, os
from os.path import basename
from sqlalchemy.orm.exc import NoResultFound
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
from flask_login import current_user, login_required
from flask import * 
from flask_socketio import SocketIO, emit, join_room, leave_room
from markupsafe import escape
import re 
from flask_wtf.csrf import CSRFProtect
from techhub import app,csrf,socketio
from techhub.forms import *
from flask_login import login_required
from techhub.models import db,User,Category,Tag,Post,Contact,Comment

from sqlalchemy import func
from datetime import datetime

socketio = SocketIO(app)

def login_required(f):
    @wraps(f)  #this ensures that the details(meta data) about the original function f, that is decorated is still available..
    def login_check(*args, **kwargs):
        if session.get("userlogged") !=None:
            return f(*args,**kwargs)
        else:
            flash("Access Denied")
            return redirect (url_for('login'))
    return login_check

@app.route("/")
def homepage():
    user_id = session.get('userlogged')
    user = User.query.get(user_id)
    
    
    # Get the index of the latest post displayed on the main page
    latest_post_index = int(request.args.get('latest_post_index', 0))
    
    # Fetch the latest three posts, starting from the latest_post_index
    post = Post.query.order_by(Post.post_date.desc()).offset(latest_post_index).limit(3).all()
    
    return render_template("user/index.html", pagename="Home | TECH HUB", post=post, user=user, latest_post_index=latest_post_index)







@app.route("/user/post/")
def userpost():
    user_id = session.get('userlogged')
    user = User.query.get(user_id)
    latest_post_index = int(request.args.get('latest_post_index', 0) or 0)

    

    # Fetch the latest three posts, including the author's information
    post = Post.query.order_by(Post.post_date.desc()).offset(latest_post_index).all()

    return render_template("user/post.html", pagename="Post | TECH HUB", post=post, user=user, latest_post_index=latest_post_index)


@app.route('/post/comment/<int:id>', methods=['POST'])
@login_required
def post_comment(id):
    print("Route accessed") 
    # Get the user ID from the session
    user_id = session.get('userlogged')
    user = User.query.get(user_id)

    
    # Get the comment content from the form
    comment_content = request.form.get('comment_content')
    
    post = Post.query.get(id)
    if post:
        new_comment = Comment(user=user, post=post, response_text=comment_content)
        db.session.add(new_comment)
        db.session.commit()
        flash('Your comment has been posted.', 'success')
    else:
        flash('The specified post does not exist.', 'error')
    
    return redirect(url_for('userpost', id=id))  # Redirect to the story page





@app.route("/about/")
def about():
    user_id = session.get('userlogged')
    user = User.query.get(user_id)
    return render_template("user/about.html", pagename="About | TECH HUB", user=user)



@app.route("/post/<int:post_id>")
def view_post(post_id):
    user_id = session.get('userlogged')
    user = User.query.get(user_id)
    post = Post.query.get(post_id)
    if post:
        return render_template("user/viewpost.html", post=post,user=user)
    else:
        flash("Post not found", "error")
        return redirect(url_for("homepage"))






POST_IMAGE_PATH = "techhub/static/images/post"
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/user/new_post", methods=['GET', 'POST'])
def new_post():
    user_id = session.get('userlogged')
    user = User.query.get(user_id)

    if 'userlogged' not in session:
        flash('You need to log in to create a new post.', 'error')
        return redirect(url_for('login'))

    form = NewPostForm()
# ...

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        subcontent = form.subcontent.data
        image = request.files['image']

        if title and content and subcontent:
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(POST_IMAGE_PATH, filename)
                image.save(image_path)


                # Create a new post
                new_post = Post(title=title, content=content, subcontent=subcontent, image=os.path.basename(image_path), author_id=user_id)

                # Get selected categories and tags from the form
                selected_category_names = form.categories.data
                selected_category_names = [category.strip() for category in selected_category_names.split(',')]  # Correct this line
                selected_tag_names = form.tags.data.split(',')  # Split the tags

                # Associate the categories with the new post
                for category_name in selected_category_names:
                    category = Category.query.filter_by(name=category_name).first()
                    if not category:
                        category = Category(name=category_name)
                        db.session.add(category)
                    if category not in new_post.categories:
                        new_post.categories.append(category)

                # Associate the tags with the new post
                for tag_name in selected_tag_names:
                    tag = Tag.query.filter_by(name=tag_name.strip()).first()
                    if not tag:
                        tag = Tag(name=tag_name.strip())
                        db.session.add(tag)
                    if tag not in new_post.tags:
                        new_post.tags.append(tag)

                # Commit the session for the new post, categories, and tags
                db.session.add(new_post)
                db.session.commit()

                flash('Your post has been created!', 'success')
                return redirect(url_for('homepage'))
            else:
                flash('Invalid image file format. Please use .jpg, .jpeg, .png, or .gif.', 'error')
        else:
            flash('Title and content are required.', 'error')

    # ...


    return render_template("user/new_post.html", pagename="New Post | TECH HUB", form=form, user=user)











@app.route("/userlogin/", methods=['POST', 'GET'])
def login():
    form =LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()

        if user is not None and check_password_hash(user.password, password):
            session['userlogged'] = user.id
             # Set the session variable
            flash('Login successful', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid login. Please try again.', category='danger')

    return render_template("user/login.html", form=form, pagename="Login | TECH HUB")



@app.route("/register/", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template("user/registration.html", form=form, pagename="Registration | TECH HUB")
    else:
        if form.validate_on_submit():
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')  # Store the password securely
            password_hash = generate_password_hash(password, method='sha256')  # Hash the password
        

            # Create a new user instance
            new_user = User(username=username, email=email, password=password_hash,
                            first_name=first_name, last_name=last_name)

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            flash(f"{username} Your account has been created Succesfully..")
            return redirect(url_for('login'))

    return render_template("user/registration.html", form=form, pagename="Registration | TECH HUB")

@app.route("/dashboard" ,methods=['GET', 'POST'])
@login_required  # Ensure the user is logged in to access the dashboard
def dashboard():
     form = NewPostForm()
     if session.get('userlogged') is not None:
        id = session.get('userlogged')
        user = User.query.get(id)
        return render_template("user/dashboard.html", user=user, pagename="Dashboard | TECH HUB", form=form)
     else:
        flash('You need to login to access the page')
        return redirect(url_for('login'))


@app.route('/user/logout/')
def logout():
    user = None  # Initialize user as None

    if session.get('userlogged') is not None:
        user = session.get('userlogged')
        # Assuming you have a database model for users named MyUser
        user = User.query.get(user)

        session.pop('userlogged', None)
        flash('You have been logged out', category='success')

    return redirect(url_for('homepage'))




@app.route('/user/profile/update', methods=['POST', 'GET'])
def update_profile():
    user_id = session.get('userlogged')
    user = User.query.get(user_id)

    if request.method == 'GET':
        return render_template('user/profile.html', user=user)

    elif request.method == 'POST':
        last_name=request.form.get('first_name')
        first_name=request.form.get('last_name')
        new_email = request.form.get('email')
        bio = request.form.get('bio')
        new_password = request.form.get('password')
        profile_picture = request.files.get('profile_picture')
        # Update the user's email, bio, and password if provided
        if last_name:
            user.last_name = last_name
        if first_name:
            user.first_name = first_name
        if new_email:
            user.email = new_email
        if bio:
            user.bio = bio
        if new_password:
            new_password_hashed = generate_password_hash(new_password)
            user.password = new_password_hashed

        # Handle profile picture upload
       
        if profile_picture:
            filename = profile_picture.filename
            profile_picture.save(os.path.join(app.config['USER_PROFILE_PATH'], filename))
            user.profile_picture = filename

        db.session.commit()
        flash('Profile information has been updated successfully', category='success')
        return redirect(url_for('dashboard'))

    flash('User not found. Please log in again.', category='danger')
    return render_template('user/profile.html', user=user)


@app.route('/contact/', methods=['GET', 'POST'])
def contactus():

    user_id = session.get('userlogged')
    user = User.query.get(user_id)
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.form)
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            phone = form.phone.data
            message = form.message.data

            contact_entry = Contact(
                    contact_email=email,
                    contact_no=phone,
                    contact_message=message,
                    contact_name=name
                )

            db.session.add(contact_entry)
            db.session.commit()

            flash('Your message has been submitted successfully!', 'success')
            return redirect(url_for('contactus'))  # Redirect to a thank you or confirmation page

            
            # Handle the form data and database submission here
            # You can access the form data as shown above

        flash('Please fill out all the fields correctly.', 'error')
        # Redirect to a thank you or confirmation page

    return render_template('user/contact.html', form=form,  pagename="Contact Us | TECH HUB", user=user)


