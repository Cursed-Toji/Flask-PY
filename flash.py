from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de banco de dados
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        result = {}
        for key in self.mapper.c.keys():
            in getattr(self, key) is not None:
            result[key] = str(getattr(self, key))
        else:
            result[key] = getattr(self, key)

        return  result

@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@app.route('/post/add', methods=['POST'])
def add_post():
    try:
        form = request.form
        post = Post(title=form['title'], content=form['content'], author=form['author'])
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        return str(e)

    return redirect(url_for('home'))

@app.route('/post/<int:id>/del', methods=['POST'])
def delete_post(id):
    try:
        post = Post.query.get(id)
        if post:
            db.session.delete(post)
            db.session.commit()
    except Exception as e:
        return str(e)

    return redirect(url_for('home'))

@app.route('/post/<int:id>/edit', methods=['POST', 'GET'])
def edit_post(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        try:
            form = request.form
            post.title = form['title']
            post.content = form['content']
            post.author = form['author']
            db.session.commit()
        except Exception as e:
            return str(e)
        return redirect(url_for('home'))
    else:
        return render_template('edit.html', post=post)





########################################################

@app.route('/api/posts')
def api_lists_posts():
    posts = Post.query.all()
    return [post.to_dict() for post in posts]

# @app.route('/api/post/add', methods=['POST'])
# def api_add_post():
#     try:
#         form = request.form
#         post = Post(title=form['title'], content=form['content'], author=form['author'])
#         db.session.add(post)
#         db.session.commit()
#     except Exception as e:
#         return str(e)
#
#     return redirect(url_for('home'))
#
# @app.route('/api/post/<int:id>/del', methods=['POST'])
# def api_delete_post(id):
#     try:
#         post = Post.query.get(id)
#         if post:
#             db.session.delete(post)
#             db.session.commit()
#     except Exception as e:
#         return str(e)
#
#     return redirect(url_for('home'))
#
# @app.route('/post/<int:id>/edit', methods=['POST', 'GET'])
# def edit_post(id):
#     post = Post.query.get(id)
#     if request.method == 'POST':
#         try:
#             form = request.form
#             post.title = form['title']
#             post.content = form['content']
#             post.author = form['author']
#             db.session.commit()
#         except Exception as e:
#             return str(e)
#         return redirect(url_for('home'))
#     else:
#         return render_template('edit.html', post=post)
#


# Inicialização do banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
