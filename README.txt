Prerequisites:
-Have an active IDE, e.g. Pycharm, Visual Studio Code
-Have all the required libraries, mentioned in "requirements.txt" already installed
-Have a DataBase architecture app, e.g. MySQL Workbench
-Have a Browser application

How to start the API:
-Open the DataBase app and run the queries from CreateTheDB.txt => that creates the DB
-Open the Project's package within the IDE; the directory of the loading should be the same as
the directory where "main.py" is situated
-Make sure that the correct credentials are used to connect to the DataBase
(credentials are stored in data/database.py)
-Go to the IDE's Terminal (for the project) and write in the terminal "uvicorn main:app"; press enter
-If all the prerequisites up to now are satisfied, several rows should appear in the terminal,
one of which will print an active URL (e.g. http://127.0.0.1:8000)
-Open the URL in the Browser; specify to the end of the link "/docs"
(so it looks like http://127.0.0.1:8000/docs, if you are using localhost)
-The FastAPI interface should appear, giving access to all the available API endpoints
-If you want to stop the API, just click Ctrl+c in the terminal

-Have fun testing the application :D
