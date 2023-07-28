# Technoscape Backend (Django Rest Framework)

This is the tutorial to run the program.

---

## Current root directory

Your root directory should look like the following.

```
technoscape-backend\  <--This is the root directory
    backend\
        ...
    >.env.template
    >.gitignore
    >requirements.txt
    >steps.md
```

## Steps/Commands

> Note: Python virtual env docs can be found [here](https://docs.python.org/3/tutorial/venv.html).

1. Open a terminal and use the following command to create a virtual environment.

```
python -m venv venv
```

Now activate the virtual environment with the following command.

```
# windows machine (command prompt)
venv\Scripts\activate.bat

# mac/linux
source venv/bin/activate
```

You will know your virtual environment is active when your terminal displays the following:

```
(venv) path\to\project\technoscape-backend>
```

2. The project will rely on a whole bunch of 3rd party packages (requirements) to function. Install the project requirements. Add the following code to you terminal.

```
pip install -r requirements.txt
```

3. Create a env file to store information that is specific to our working environment. Use the following command in your terminal.

```
# windows machine
copy .env.example .env

#mac/linux
cp .env.example .env
```

4. Then, we will go to the working directory that is /backend. To do that, run the following command

```
cd backend
```

5. Run the following command to make and apply the migrations to the database
   > Note: I'm using PostgreSQL database, you should input your database credentials into your .env file

```
python manage.py makemigrations
python manage.py migrate
```

6. To run the server, run the following command
   > Note: The server will run through default port which is 8000, you can add the last argument to specify the port

```
python manage.py runserver
```

---
