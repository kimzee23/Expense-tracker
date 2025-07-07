#  Expense Tracker App

A simple and powerful web-based application to help users manage their daily expenses, set budgets, and track spending habits effectively.

## Features

-  **User Authentication**  
  Secure registration and login functionality.

-  **Expense Management**  
  Add, update, and delete expenses with categories and descriptions.

-  **Budget Setting**  
  Set monthly budgets to manage your finances better.

-  **Insightful Reports**  
  Visualize spending through dynamic charts and summaries.

##  Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MongoDB
  
## Database

-	 **Database Integration**  
  Built with **MongoDB** for flexible and efficient data storage.

##	**Layered Architecture**  

  -	Clean and scalable structure using controller, service, repository, DTOs and model layers.
##	Api Endpoint:
-	http://localhost:5000/api/v1/
	
-	**Auth**
-	 Method  Endpoint            Description               
-	 POST    `/auth/register`    Register a new user       
-	 POST    `/auth/login`       Log in and receive token
-	 
-	 **Expense**
-	Method  Endpoint            Description                    
-	POST    `/expenses`         Add a new expense              
-	GET     `/expenses`         Get all expenses for the user  
-	GET     `/expenses/<id>`    Get a specific expense         
-	PUT     `/expenses/<id>`    Update an expense              
-	DELETE  `/expenses/<id>`    Delete an expense
	
-	**Budget**
-	Method  Endpoint           Description                    
-	POST    `/budget`         Set monthly budget             
-	GET     `/budget`         Get current month's budget

-	**Report**
-	 Method  Endpoint            Description                    
-	 GET    `/reports`         Get summary of expenses        

      
 
##	 Create and activate a virtual environment:
```run
python -m venv venv
source venv/bin/activate   
```
# On Windows: 
-	venv\Scripts\activate
  
##	Install dependencies:
```
pip install -r requirements.txt
 ``` 
##	Set environment variables (optional for development):
```
	export FLASK_APP=app.py
  export FLASK_ENV=development
```
##	On Windows (Command Prompt):
```
set FLASK_APP=app.py
set FLASK_ENV=development
```
##	Run the app:
```
flask run
```
## Clone the Repository

```git clone
git clone https://github.com/kimzee23/expense-tracker.git
cd expense-tracker
```

    

