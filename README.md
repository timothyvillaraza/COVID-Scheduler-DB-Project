# COVID-Scheduler-DB-Project

AUTHORS: 
	Timothy Villaraza
	Kaylynn Arrington

DESCRIPTION:
	We used Django(Python) to create our web framework. We downloaded Postgresql to help us handle our database.

	This is a web application for a simple covid vaccine scheduler. This is our first experience with creating a database backend let alone a full on web application
	
SETUP:
	DATABSE: Postgre
		- Download Postgre
		- Download pgAdmin
			- Create a new database

	cs480proj/cs480proj/settings.py
		- Change the proper settings to connect to your database
	
	Dependencies:
		- pip install psycopg2                // Postgre library

	Commands to start server:
		- python manage.py makemigrations	  // Create SQL queries from Django's ORM
		- python manage.py migrate			  // Run the SQL queries on the database
		- python manage.py createsuperuser    // Creates a Super User to access the admin panel
		- python manage.py runserver		  // Runs the web application locally

Note:
  No time slots only exist when a nurse account joins one for the first time.
