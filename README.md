# COVID-Scheduler-DB-Project

AUTHORS:

	Timothy Villaraza
	Kaylynn Arrington

DESCRIPTION:

	This is a web application for a simple covid vaccine scheduler.
	
	This is our first experience with creating a database backend let alone a full web application
	Uses the Django (Python) web framework. We downloaded Postgresql to help us handle our local database.

SETUP:

	DATABASE:
		Postgre
		- Download Postgre
		- Download pgAdmin
			- Create a new database

	cs480proj/cs480proj/settings.py
		- Change the proper settings to connect to your database
	
	Dependencies:
		- pip install psycopg2			      // Postgre library

	How to start the project:
		Server Setup:
			1. python manage.py makemigrations    // Create SQL queries from Django's ORM
			2. python manage.py migrate	      // Run the SQL queries on the database
			3. python manage.py createsuperuser   // Creates a Super User to access the admin panel
			4. python manage.py runserver	      // Runs the web application locally
			
		Creating First Available Timeslot:
			At least one nurse acconut must exist for time slots to be created.
