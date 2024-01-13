Clone the Repository:
Open a terminal or command prompt. Makue sure to go to master branch
Run git clone https://github.com/rishabh-jain28/pushowl.git.

Navigate to the Directory:
Change into the OwlLibrary directory using cd OwlLibrary.

Activate Virtual Environment:
On Linux/Mac: Run source pushowl/bin/activate. 
On Windows: Run pushowl\Scripts\activate.

Install Dependencies:
Run pip install -r owllibrary/requirements.txt.

Configure Environment Variables:
Copy the env.sample file to .env in the owllibrary directory.
Update the .env file with your database credentials.

Apply Database Migrations:
Run python manage.py migrate.

Create Superuser:
Run python manage.py createsuperuser and follow the prompts to create an admin user.

Run the Server:
Start the server with python manage.py runserver.

Access Admin Panel:
Open your browser and go to http://localhost:8000/admin/. Log in with the superuser credentials.


API Endpoints
Use the following URLs to interact with the API:

Get All Books:
Go to http://localhost:8000/api/books/ in your browser or use a tool like curl or Postman.

Get Books by Author:
Visit http://localhost:8000/api/author-books/?author={author_name}.



Borrow a Book:
Make a POST request to http://localhost:8000/api/borrow-book/?bookname={book_name} with the provided data:

json_data
{
  "username": "{username}"
}


Return a Book:
Make a POST request to http://localhost:8000/api/return-book/?bookname={book_name} with the provided data:

json_data
{
  "username": "{username}"
}

Remember to replace {username}, {author_name}, and {book_name} with actual values during testing.


