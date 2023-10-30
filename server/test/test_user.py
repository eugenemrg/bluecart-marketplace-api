import pytest
from projectapp.models import User
from projectapp.config import db, app
# from faker import Faker


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
        yield client
        db.drop_all()

def test_create_users(client):
    with app.app_context():
        User.query.delete()

        emails = [
            "johndoe123@gmail.com",
            "sarah.smith@gmail.com",
            "gamer4life@gmail.com",
            "naturelover@gmail.com",
            "codinggeek@gmail.com",
            "musicfan@gmail.com",
            "fitnessjunkie@gmail.com",
            "bookworm@gmail.com",
            "travelbug@gmail.com",
            "foodie@gmail.com",
            "techwizard@gmail.com",
            "artlover@gmail.com",
            "fashionista@gmail.com",
            "hiker@gmail.com",
            "petlover@gmail.com",
            "scienceenthusiast@gmail.com",
            "moviebuff@gmail.com",
            "soccerstar@gmail.com",
            "eachbum@gmail.com",
            "historybuff@gmail.com"
        ]

        names = [
            "John Doe",
            "Sarah Smith",
            "GameR4Life",
            "Nature Lover",
            "Coding Geek",
            "Music Fan",
            "Fitness Junkie",
            "Book Worm",
            "Travel Bug",
            "Foodie Galore",
            "Tech Wizard",
            "Art Lover",
            "Fashionista",
            "Hiker Adventures",
            "Pet Lover",
            "Science Enthusiast",
            "Movie Buff",
            "Soccer Star",
            "Beach Bum",
            "History Buff"

        ]

        for i in range(len(emails)):
            user = User(username=names[i], email=emails[i])
            db.session.add(user)

        db.session.commit()

        assert User.query.count() == len(emails)

def test_query_users(client):
    with app.app_context():
        users = User.query.all()

        assert len(users) >= 0