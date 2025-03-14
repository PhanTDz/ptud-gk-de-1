from flask import Flask, render_template, request, redirect, url_for, flash, session, g
import sqlite3
import random
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from init_db import init_db
from functools import wraps

app = Flask(__name__, instance_relative_config=True)
app.config['DATABASE'] = os.path.join(app.instance_path, 'blog.db')
app.secret_key = 'your_secret_key'

# Định nghĩa login_required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            flash('Vui lòng đăng nhập để tiếp tục', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'db'):
        g.db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
    with app.app_context():
        init_db()

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE id = ?', (user_id,)
        ).fetchone()

@app.context_processor
def utility_processor():
    return dict(g=g)

@app.template_filter('format_datetime')
def format_datetime(value):
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return value
    return value.strftime('%Y-%m-%d %H:%M')

# Route mặc định chuyển hướng đến trang login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Trang chủ được bảo vệ
@app.route('/home')
@login_required
def home():
    db = get_db()
    posts = db.execute('''
        SELECT p.*, u.username, 
        (SELECT COUNT(*) FROM follows WHERE post_id = p.id) as follow_count,
        (SELECT COUNT(*) FROM saved_posts WHERE post_id = p.id) as save_count
        FROM posts p 
        JOIN users u ON p.author_id = u.id 
        ORDER BY p.created_at DESC
    ''').fetchall()
    
    formatted_posts = []
    for post in posts:
        post_dict = dict(post)
        if isinstance(post_dict['created_at'], str):
            post_dict['created_at'] = datetime.strptime(post_dict['created_at'], '%Y-%m-%d %H:%M:%S')
        formatted_posts.append(post_dict)
    
    return render_template('home.html', posts=formatted_posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        
        if user and check_password_hash(user['password'], password):
            session.clear()
            session['user_id'] = user['id']
            session['is_actor'] = user['is_actor']
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_actor = 1 if 'is_actor' in request.form else 0
        db = get_db()
        
        try:
            db.execute('INSERT INTO users (username, password, is_actor) VALUES (?, ?, ?)',
                      (username, generate_password_hash(password), is_actor))
            db.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists')
    return render_template('register.html')

@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if not session.get('is_actor'):
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image_url = f"https://picsum.photos/800/400?random={random.randint(1, 1000)}"
        
        db = get_db()
        db.execute('''
            INSERT INTO posts (title, content, image_url, author_id)
            VALUES (?, ?, ?, ?)
        ''', (title, content, image_url, session['user_id']))
        db.commit()
        flash('Post created successfully!')
        return redirect(url_for('home'))
        
    return render_template('create_post.html')

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    if not session.get('is_actor'):
        return redirect(url_for('home'))
    
    db = get_db()
    post = db.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    
    if post['author_id'] != session['user_id']:
        flash('You can only edit your own posts!')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        db.execute('''
            UPDATE posts 
            SET title = ?, content = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, content, post_id))
        db.commit()
        flash('Post updated successfully!')
        return redirect(url_for('post_detail', post_id=post_id))
        
    return render_template('edit_post.html', post=post)

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_detail(post_id):
    db = get_db()
    post = db.execute('''
        SELECT p.*, u.username,
        (SELECT COUNT(*) FROM follows WHERE post_id = p.id) as follow_count
        FROM posts p 
        JOIN users u ON p.author_id = u.id 
        WHERE p.id = ?
    ''', (post_id,)).fetchone()
    
    comments = db.execute('''
        SELECT c.*, u.username 
        FROM comments c 
        JOIN users u ON c.user_id = u.id 
        WHERE c.post_id = ?
        ORDER BY c.created_at DESC
    ''', (post_id,)).fetchall()
    
    is_following = False
    if g.user:
        follow = db.execute('''
            SELECT * FROM follows 
            WHERE user_id = ? AND post_id = ?
        ''', (g.user['id'], post_id)).fetchone()
        is_following = follow is not None
    
    if request.method == 'POST' and g.user:
        content = request.form['content']
        db.execute('INSERT INTO comments (content, post_id, user_id) VALUES (?, ?, ?)',
                  (content, post_id, g.user['id']))
        db.commit()
        return redirect(url_for('post_detail', post_id=post_id))
    
    return render_template('post_detail.html', 
                         post=post, 
                         comments=comments, 
                         is_following=is_following)

@app.route('/my_saved_posts')
@login_required
def my_saved_posts():
    db = get_db()
    posts = db.execute('''
        SELECT p.*, u.username, 
        (SELECT COUNT(*) FROM follows WHERE post_id = p.id) as follow_count,
        1 as is_saved
        FROM posts p 
        JOIN users u ON p.author_id = u.id
        JOIN saved_posts sp ON p.id = sp.post_id
        WHERE sp.user_id = ?
        ORDER BY sp.created_at DESC
    ''', (g.user['id'],)).fetchall()
    
    return render_template('saved_posts.html', posts=posts)

@app.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    if not session.get('is_actor'):
        return redirect(url_for('home'))
    
    db = get_db()
    db.execute('DELETE FROM comments WHERE post_id = ?', (post_id,))
    db.execute('DELETE FROM follows WHERE post_id = ?', (post_id,))
    db.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    db.commit()
    return redirect(url_for('home'))

@app.route('/follow/<int:post_id>')
@login_required
def follow_post(post_id):
    db = get_db()
    try:
        db.execute('INSERT INTO follows (user_id, post_id) VALUES (?, ?)',
                  (session['user_id'], post_id))
        db.commit()
    except sqlite3.IntegrityError:
        db.execute('DELETE FROM follows WHERE user_id = ? AND post_id = ?',
                  (session['user_id'], post_id))
        db.commit()
    return redirect(url_for('post_detail', post_id=post_id))

@app.route('/save_post/<int:post_id>')
@login_required
def save_post(post_id):
    db = get_db()
    try:
        saved = db.execute('''
            SELECT * FROM saved_posts 
            WHERE user_id = ? AND post_id = ?
        ''', (g.user['id'], post_id)).fetchone()
        
        if saved:
            db.execute('''
                DELETE FROM saved_posts 
                WHERE user_id = ? AND post_id = ?
            ''', (g.user['id'], post_id))
            flash('Post removed from saved posts.', 'success')
        else:
            db.execute('''
                INSERT INTO saved_posts (user_id, post_id)
                VALUES (?, ?)
            ''', (g.user['id'], post_id))
            flash('Post saved successfully!', 'success')
        
        db.commit()
    except sqlite3.Error as e:
        flash('An error occurred while saving the post.', 'error')
        print(e)
    
    if request.referrer and 'saved_posts' in request.referrer:
        return redirect(url_for('my_saved_posts'))
    return redirect(url_for('post_detail', post_id=post_id))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    init_app(app)
    app.run(debug=True) 