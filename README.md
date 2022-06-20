# COVID-Scheduler-DB-Project

AUTHORS:

	Timothy Villaraza
	Kaylynn Arrington

DESCRIPTION:

	This is a web application for a simple covid vaccine scheduler.
	
	This is our first experience with creating a database backend let alone a full web application
	Uses the Django (Python) web framework. We downloaded Postgresql to help us handle our local database.

Admin vaccine inventory:
![image](https://user-images.githubusercontent.com/61322637/174668907-770bc54e-f5d9-43ca-95cc-506f31e6a550.png)

Patient Scheduled Appointments:
![image](https://user-images.githubusercontent.com/61322637/174669127-fd13de56-f762-4e7e-97bc-a650c3b66063.png)



Features:
	
	- Covid Vaccine Inventory and Scheduling
		- Supports multiple vaccines types
		- Tracks vaccine available and on hold inventory
		- Scheduling interacts with all account levels
		
	- User account roles and role based web page access
		- Admin level
			- Sets vaccine types and inventory
			- Can register and terminate nurse accounts
		- Nurse level
			- Nurses can set time slot availability
			- Nurses can see the patients that signed up for their time slots
		- Patient level
			- Patients can pick time slots for specificed vaccines
			- Edit account information
		- No account level
			- Register a patient account or sign in
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

Entitiy Relationship Diagram:
	![CS 480 ERD](https://user-images.githubusercontent.com/61322637/174665511-91baff42-bd94-48a2-bc9e-48ca060c1b15.png)

