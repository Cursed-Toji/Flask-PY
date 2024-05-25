from flask import Flask, render_template, request, redirect, url_for
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

# Inicialização do banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
