import sqlite3
import os
from werkzeug.security import generate_password_hash

def init_db():
    # Đảm bảo thư mục instance tồn tại
    if not os.path.exists('instance'):
        os.makedirs('instance')

    # Đường dẫn đến database
    DB_PATH = os.path.join('instance', 'blog.db')
    
    # Kết nối đến database (sẽ tạo mới nếu chưa tồn tại)
    conn = sqlite3.connect(DB_PATH)
    db = conn.cursor()

    # Tạo các bảng nếu chưa tồn tại
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_actor INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            image_url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            author_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES users (id)
        );

        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        );

        CREATE TABLE IF NOT EXISTS follows (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (post_id) REFERENCES posts (id),
            UNIQUE(user_id, post_id)
        );

        CREATE TABLE IF NOT EXISTS saved_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            post_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (post_id) REFERENCES posts (id),
            UNIQUE(user_id, post_id)
        );
    ''')

    # Kiểm tra xem bảng users có dữ liệu chưa
    user_count = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]

    # Chỉ thêm dữ liệu mẫu nếu bảng users trống
    if user_count == 0:
        print("Adding sample data...")
        
        # 1. Tạo tài khoản mẫu
        users_data = [
            ('actor1', 'password123', 1),
            ('actor2', 'password123', 1),
            ('user1', 'password123', 0),
            ('user2', 'password123', 0),
        ]

        for username, password, is_actor in users_data:
            try:
                db.execute(
                    'INSERT INTO users (username, password, is_actor) VALUES (?, ?, ?)',
                    (username, generate_password_hash(password), is_actor)
                )
            except sqlite3.IntegrityError:
                print(f"User {username} already exists, skipping...")

        # 2. Tạo bài post mẫu
        posts_data = [
            ('First Blog Post', 'This is the content of the first blog post. It contains some sample text.', 
             'https://picsum.photos/800/400?random=1', 1),
            ('Travel Experience', 'Sharing my amazing travel experience in Japan. The culture, food, and people were amazing!', 
             'https://picsum.photos/800/400?random=2', 1),
            ('Tech Review', 'A detailed review of the latest smartphone. Pros, cons, and everything you need to know.', 
             'https://picsum.photos/800/400?random=3', 2),
            ('Cooking Tips', 'Essential cooking tips and tricks that every beginner should know.', 
             'https://picsum.photos/800/400?random=4', 2),
        ]

        for title, content, image_url, author_id in posts_data:
            db.execute('''
                INSERT INTO posts (title, content, image_url, author_id)
                VALUES (?, ?, ?, ?)
            ''', (title, content, image_url, author_id))

        # 3. Tạo comment mẫu
        comments_data = [
            ('Great post!', 1, 3),
            ('Very informative, thanks for sharing!', 1, 4),
            ('I learned a lot from this.', 2, 3),
            ('Looking forward to more posts like this!', 2, 4),
        ]

        for content, post_id, user_id in comments_data:
            db.execute('''
                INSERT INTO comments (content, post_id, user_id)
                VALUES (?, ?, ?)
            ''', (content, post_id, user_id))

        # 4. Tạo follows mẫu
        follows_data = [
            (3, 1),
            (3, 2),
            (4, 1),
        ]

        for user_id, post_id in follows_data:
            try:
                db.execute('INSERT INTO follows (user_id, post_id) VALUES (?, ?)',
                          (user_id, post_id))
            except sqlite3.IntegrityError:
                print(f"Follow relationship already exists, skipping...")

        # 5. Tạo saved posts mẫu
        saved_posts_data = [
            (3, 1),
            (3, 3),
            (4, 2),
        ]

        for user_id, post_id in saved_posts_data:
            try:
                db.execute('INSERT INTO saved_posts (user_id, post_id) VALUES (?, ?)',
                          (user_id, post_id))
            except sqlite3.IntegrityError:
                print(f"Saved post relationship already exists, skipping...")

        print("Sample data added successfully!")
    else:
        print("Database already contains data, skipping sample data creation.")

    # Lưu thay đổi và đóng kết nối
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("\nTài khoản mẫu (nếu chưa tồn tại):")
    print("Actor accounts:")
    print("- Username: actor1, Password: password123")
    print("- Username: actor2, Password: password123")
    print("User accounts:")
    print("- Username: user1, Password: password123")
    print("- Username: user2, Password: password123") 