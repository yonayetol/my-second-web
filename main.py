from flask import Flask, request, url_for, render_template, redirect
import sqlalchemy
from sqlalchemy.orm import declarative_base, sessionmaker, mapped_column, Mapped
import requests
import json

api_key = "e9b3141006a27070f11351d087fe33b1"

app = Flask(__name__)
db = sqlalchemy.create_engine("sqlite:///the_Sec.db")
Base = declarative_base()
Session = sessionmaker(bind=db)

class Movie(Base):
    __tablename__ = "Movies"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    year: Mapped[str]
    description: Mapped[str]
    rating: Mapped[float]  
    review: Mapped[str]
    image_url: Mapped[str]
    ranking: Mapped[int]

Base.metadata.create_all(db)

@app.route("/")
def front_page():
    with Session() as session:
        all_movies = session.query(Movie).all()
    return render_template("index.html", movies=all_movies)

@app.route("/update", methods=['POST'])
def upgrade():
    the_id = request.form['id_carrier']
    with Session() as session:
        movie = session.query(Movie).filter_by(id=the_id).first()
        if request.form['place'] == 'hello':
            the_rate = float(request.form['the_new_rating'])
            the_review = request.form['the_new_review']
            movie.rating = the_rate
            movie.review = the_review
            session.commit()
            return redirect(url_for('front_page'))
    return render_template('the_update.html', movie=movie)

@app.route("/delete", methods=["POST"])
def Delete():
    if request.method == 'POST':
        the_id = request.form['id_carrier']
        with Session() as session:
            book_to_be_deleted = session.query(Movie).filter_by(id=the_id).first()
            session.delete(book_to_be_deleted)
            session.commit()
    return redirect(url_for('front_page'))

@app.route("/add", methods=['POST', 'GET'])
def adding_movies():
    if request.method == 'POST':
        if request.form['add'] == '0':
            the_dict = json.loads(request.form['the_instance'])  # Safely parse the JSON string
            year = the_dict.get('release_date', 'Unknown')
            new_movie = Movie(
                title=the_dict['title'],
                description=the_dict['overview'],
                image_url=f"https://image.tmdb.org/t/p/w500{the_dict['poster_path']}",
                review="None",
                rating=0,
                year=year,
                ranking=0
            )
            with Session() as session:
                session.add(new_movie)
                session.commit()
            return redirect(url_for('front_page'))
        else:
            title = request.form['add']
            response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}")
            if response.status_code == 200:
                new_response = response.json()['results']
                return render_template('select.html', reason=new_response)
            else:
                return redirect(url_for('front_page'))
    return render_template('find_movie.html')

if __name__ == "__main__":
    app.run(debug=True)
