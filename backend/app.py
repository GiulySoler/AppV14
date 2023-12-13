from flask import Flask, jsonify, request, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow
import json
from werkzeug.utils import secure_filename
import os 


app = Flask(__name__)
 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:''@localhost/flask' # Configurar acesso ao meu Mysql.

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) 
ma = Marshmallow(app)

app.app_context().push() # at PYTHON command 

camimg = 'C:/Users/giuly/Desktop/Sam/App/server/public/images'

app.config['UPLOAD'] = camimg


class Articles(db.Model):  # Modelo de banco de dados.
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    alarme = db.Column(db.Integer)
    images = db.Column(db.Text())
    

    def __init__(self, title, body, alarme, date, images):
        self.title = title
        self.body = body
        self.alarme = alarme
        self.date = date
        self.images = images
        

class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body', 'date', 'alarme', 'images')

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)


@app.route('/get/<id>/', methods = ['GET']) # Rota para pegar informações de acordo com o id no meu banco de dados.
def get_details(id):
    article = Articles.query.get(id)
    return article_schema.jsonify(article)        


@app.route('/get/', methods = ['GET']) # Rota para pegar todas informações do banco de dados.
def get_article():

    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)

    return jsonify(results)  

@app.route('/get/onlytrue/', methods = ['GET']) # Rota para pegar informações de alarme ativos.
def get_alarme_true():

    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    b = []
    for i in results:
        if ((i['alarme']) == 1):
            a = i
            b.append(a)
    c = json.dumps(b)

    return (c)  

@app.route('/add/', methods = ['POST']) # Rota para adicionar informações ao meu banco de dados.
def add_article():
    title = request.json['title']
    body = request.json['body']
    alarme = 0

    articles = Articles(title, body, alarme)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)

@app.route('/update/<id>/', methods = ['PUT']) # Rota para alterar o banco de dados.
def update_article(id):
    article = Articles.query.get(id)

    title = request.json['title']
    body = request.json['body']

    article.title = title
    article.body = body

    db.session.commit()
    return article_schema.jsonify(article)

@app.route('/delete/<id>/', methods = ['DELETE']) # Rota para deletar um dado no banco
def article_delete(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()

    return article_schema.jsonify(article)

@app.route('/alarme/<id>/', methods = ['PUT']) # Rota para alterar o valor do alarme dos dados 
def update_alarme(id):
    article = Articles.query.get(id)
    alarme = request.json['alarme']
    article.alarme = alarme
    article.date = datetime.datetime.now()
    db.session.commit()
    return article_schema.jsonify(article)

@app.route('/upload/', methods = ['POST'])
def upload_img():
    a = request.files['image']
    filename = secure_filename(a.filename) + '0.jpeg'
    os.remove(os.path.join(app.config['UPLOAD'], filename))
    a.save(os.path.join(app.config['UPLOAD'], filename))
    send_from_directory(app.config['UPLOAD'], filename)
    
    return ("done")

@app.route('/images/<path:path>', methods = ['GET'])
def serve_static(path):
    return send_from_directory(app.config['UPLOAD'], path)

if __name__ == "__main__" : 
    app.run()
