from flask import Flask, jsonify, render_template, request, redirect, url_for
from Models import db, Post, User, Category
from werkzeug.utils import secure_filename
from AzureBlobStorage import AzureBlobStorageManager
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os


load_dotenv()
STORAGE_ACCOUNT = os.getenv('STORAGE_ACCOUNT')
STORAGE_CONTAINER = os.getenv('STORAGE_CONTAINER')
SAS_TOKEN = os.getenv('SAS_TOKEN')
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/posts', methods=['GET'])
def posts():
    # Check the 'Accept' header in the request
    content_type = request.headers.get('Accept')
    if 'application/json' in content_type:
        posts = Post.query.all()
        posts_list = [{'id': post.id, 'title': post.title, 'html_content':post.html_content} for post in posts]
        return jsonify(posts_list)
    else:
        # Return HTML if the 'Accept' header does not specify JSON
        return redirect(url_for('index'))

@app.route('/posts', methods=['POST'])
def insert_post():
    # Check the 'Accept' header in the request
    content_type = request.headers.get('Accept')
    if 'application/json' in content_type:
        post_data = request.json
        if not post_data['title']:
            return "Invalid Request", 400
        new_post = Post(title=post_data['title'],html_content=post_data['html_content'], user_id=post_data['user_id'], category_id=post_data['category_id'])
        db.session.add(new_post)
        db.session.commit()
        return jsonify(title=post_data['title'],html_content=post_data['html_content']), 201
    else:
        return "Invalid Request", 400
    
@app.route('/posts/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def post(id):
    # Check the 'Accept' header in the request
    content_type = request.headers.get('Accept')
    post = Post.query.get_or_404(id)
    post.author = User.query.filter_by(id=post.user_id).first().name

    if request.method == 'GET':
        if 'application/json' in content_type:
            return jsonify(id=post.id, title=post.title, html_content=post.html_content)
        else:
            # Return HTML if the 'Accept' header does not specify JSON
            return render_template('post.html', id=post.id, title=post.title, html_content=post.html_content, created_at=post.created_at, author=post.author)
        
    elif request.method == "PUT":
        if 'application/json' in content_type:
            post_data = request.json
            post.title = post_data['title']
            post.html_content = post_data['html_content']
            post.category_id = post_data['category_id']
            db.session.commit()
            return jsonify(message="Updated Successfully"), 202
        
    elif request.method == 'DELETE':
        # Delete a specific item
        db.session.delete(post)
        db.session.commit()
        return jsonify(message="Deleted Successfully"), 204


@app.route('/', methods=['GET']) 
@app.route('/<int:page_id>', methods=['GET'])
@app.route('/categories/<int:category_id>', methods=['GET'])
def index(page_id=1, category_id=False):
    if category_id:
        posts = db.paginate(Post.query.filter_by(category_id=category_id).order_by(Post.created_at.desc()), max_per_page=5, page=page_id)
    else:
        posts = db.paginate(db.select(Post).order_by(Post.created_at.desc()), max_per_page=5, page=page_id)
    pages = posts.iter_pages()
    print(pages)
    return render_template('main.html', page_id=page_id, posts=posts, categories=Category().query.all())

@app.route('/admin/edit_post', methods=['GET'])
@app.route('/admin/edit_post/<int:post_id>', methods=['GET'])
@login_required
def add_post(post_id=False):
    categories = Category.query.all()
    if post_id:
        post = Post.query.filter_by(id=post_id).first()
        return render_template('editpost.html', post=post, categories=categories)
    else:
        return render_template('editpost.html', post=False, categories=categories)
    
@app.route('/categories', methods=['GET', 'POST'])
def categories():
    # Check the 'Accept' header in the request
    content_type = request.headers.get('Accept')
    if request.method == 'POST':
        category_data = request.json
        new_category = Category(name=category_data['name'])
        db.session.add(new_category)
        db.session.commit()
        return jsonify(id=new_category.id, name=new_category.name), 201
    if request.method == 'GET':
        if 'application/json' in content_type:
            categories = Category.query.all()
            categories = [{'id': category.id, 'name': category.name} for category in categories]
            return jsonify(categories)
        else:
            return "Invalid Request", 400
        
@app.route('/categories/<int:id>', methods=['DELETE', 'PUT'])
def category(id):
    # Check the 'Accept' header in the request
    content_type = request.headers.get('Accept')
    category = Category.query.get_or_404(id)
    if request.method == 'DELETE':
        db.session.delete(category)
        db.session.commit()
        return jsonify(message="Deleted Successfully"), 204
    if request.method == 'PUT':
        if 'application/json' in content_type:
            category_data = request.json
            category.name = category_data['name']
            db.session.commit()
            return jsonify(message="Updated Successfully"), 202
        else:
            return "Invalid Request", 400

@app.route('/img_upload', methods=['POST'])
@login_required
def img_upload():
    # check if the post request has the file part
        if 'file' not in request.files:
            return "Invalid Request", 400
        file = request.files['file']
        if file.filename == '':
            return "Invalid Request", 400
        if file and allowed_file(file.filename):
            storage_manager = AzureBlobStorageManager(sas_token = SAS_TOKEN, account_url=STORAGE_ACCOUNT)
            file.filename = secure_filename(file.filename)
            if storage_manager.does_blob_exist('img', file.filename):
                file.filename =  storage_manager.generate_random_filename(lenght=6,filename=file.filename)
            try:
                storage_manager.upload_blob_stream(container_name="img", file=file)
                file_url = STORAGE_ACCOUNT + "/" + STORAGE_CONTAINER +"/"+file.filename
                return jsonify(file_url=file_url), 201
            except:
                return "Invalid Request", 400

@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
        
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        # Check if the username is already taken
        if User.query.filter_by(username=username).first():
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password=password).decode('utf-8')
        new_user = User(name=name, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('index'))
    
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

 
if __name__ == '__main__':
    app.run(debug=True)