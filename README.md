# BlueCart Marketplace API

One of the major issues facing the rapidly growing online shopping community is lack of a tool that is able to automatically compute the marginal benefit(MB) and the cost benefit (CB) analysis of purchasing product A from e-shop X; product B from e-shop Y, or product A and B all from e-shop X or e-shop Y.

This owes to the fact that both shops may have the same product, but the MB and CB are highly subjective to factors such as shipping costs which may differ from e-shop X to Y, consumer ratings for each products in the two stores, quality, price among others

This is the Python Flask API for the [BlueCart Marketplace Project](https://github.com/eugenemrg/bluecart-marketplace) that offers a possible solution to the issue.

# Setup Requirements
- Visual Studio Code, see [here](https://code.visualstudio.com/)
- Windows Subsystem for Linux (WSL), details [here](https://learn.microsoft.com/en-us/windows/wsl/install)
- Git and Github for version control and collaboration
- Python, the project uses `version 3.10.12`
- Pipenv, a Python virtualenv management tool, details [here](https://pipenv.pypa.io/en/latest/)
- Postgres for database management, details [here](https://www.postgresql.org/download/linux/)

# Installation
To run the Rental Management App locally:

- Clone/Download the repository
- Navigate into the project directory 
- Run `pipenv install` to install all required packages
- Update the database connection URI in `__init__.py`, read about configuring your database connection [here](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/config/)
- Run `pipenv shell` to activate the project virtualenv
- Run `flask 'app:create_app()' db init` to initialize the database
- Run `flask 'app:create_app()' db migrate -m 'Initial migration'` to complete the first database migration
- Run `flask 'app:create_app()' db upgrade` to create or upgrade the database tables
- Run `gunicorn 'app:create_app()'` to start the app

### API Documentation and Deployment

[Bluecart Marketplace API Deployment](https://bluecart-api.onrender.com)

# Packages

All the packages used for the project are available in the project's Pipfile.  
[Package details](/Pipfile)

# Languages and Tools
- Python
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) - A Python Web Framework
- [Gunicorn](https://gunicorn.org/) - A Python Web Server Gateway Interface HTTP server

# Contributing
Contributions are welcome. Reach out to any of the authors or our community to get on board.

# Author(s)
BlueCart Marketplace API was created by:

- Nicole Mugeshi
- Kenneth Mwangi 
- [Eugene Aduogo](https://github.com/eugenemrg/)
  
# Team
BlueCart Marketplace project members:

- [Eugene Aduogo](https://github.com/eugenemrg/)
- Kenneth Mwangi 
- Micah Barasa
- Nicole Mugeshi
- Victor Njoroge



# License
BlueCart Marketplace

Copyright (C) 2023

Licensed under GNUv3. See [license](/LICENSE)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
