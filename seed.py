from app import create_app
from app.extensions import db
from app.models import User

app = create_app()

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

    users = []

    for i in range(20):
        print("**all good**")
        user = User(username=names[i],
                    email=emails[i])
        print("**done**")
        users.append(user)
    db.session.add_all(users)
    db.session.commit()
