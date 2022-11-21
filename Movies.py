from flask import Flask, render_template, request, redirect, url_for
from wtforms import Form, StringField, SubmitField, BooleanField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
import psycopg2
import sys



app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Gandalf2000@localhost/postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://reciswppitzyjv:b7ffc0c1c62473e33382989a3a9c8f01d66f8871d4ef168619b93cacbb4d63d6@ec2-3-216-167-65.compute-1.amazonaws.com:5432/dbp4to3fkiqb1e'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class Movies(db.Model):
    movie_id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(300))
    genre = db.Column(db.String(50))
    year = db.Column(db.Integer)
    director = db.Column(db.String(300))
    child = db.relationship('MyList', backref='parent')


class MyList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    has_watched = db.Column(db.Boolean)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))

app.context_processor
def base():
    form = SearchForm()
    return dict(form=form)


class SearchForm(Form):
        searchData = StringField("searchData")

class CheckForm(Form):
        checkform_boolean = BooleanField("checkbox")
        checkform_Id = StringField("")

@app.route('/')
def index():
    #return render_template('movies.html')
    return redirect(url_for('movies'))


@app.route('/watch_list')
def watch_list():
    watch_list_data = MyList.query.all()

    watch_movie_list = []
    for watch_row in watch_list_data:
        movie = Movies.query.filter(Movies.movie_id == watch_row.movie_id).first()
        watch_movie_list.append(movie)

    #my_movie_data = Movies.query.filter(Movies.movie_id.in_(my_movie_ids)).all()
    return render_template('watch_list.html', my_movie_data=watch_movie_list)


@app.route('/addToList', methods=["POST"])
def addToList():
    print("add-preloop", file=sys.stderr)
    add_form_movie_ids = request.form.getlist("add_checkbox")
    for add_form_movie_id in add_form_movie_ids:
        print("add"+add_form_movie_id, file=sys.stderr)
        list = MyList(id=add_form_movie_id, has_watched=False, movie_id=add_form_movie_id)
        db.session.add(list)
        db.session.commit()

    return redirect(url_for('watch_list'))

@app.route('/removeFromList', methods=["POST"])
def removeFromList():
    print("remove-preloop", file=sys.stderr)
    remove_form_movie_ids = request.form.getlist("remove_checkbox")
    for remove_form_movie_id in remove_form_movie_ids:
        print("remove:"+remove_form_movie_id, file=sys.stderr)
        db.session.query(MyList).filter(MyList.movie_id==remove_form_movie_id).delete()
        db.session.commit()

    return redirect(url_for('watch_list'))



@app.route('/movies')
def movies():
    allMovies = Movies.query.all()
    return render_template('movies.html', allMovies=allMovies)



@app.route('/watch_history')
def watch_history():
    return render_template('watch_history.html')



@app.route('/search_Filter', methods=["POST"])
def search_Filter():

    myForm = SearchForm(request.form)
    if request.method == 'POST':
        search = request.form.get('searchData', False)
        data = Movies.query.filter(Movies.title.contains(search))

        return render_template("search_Filter.html", myForm=myForm, data=data)
