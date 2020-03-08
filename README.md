# hockey_availability_trigger

Check the availability of future Stinky Socks hockey games, and email the user when a game becomes available.

# Setup
Create a virtualenv and use pip to install the requirements in `requirements.txt`
`virtualenv -p python3.6 venv`
`source venv/bin/activate`
`pip install --index-url https://pypi.python.org/simple/ -r requirements.txt`

Create a file where sqlite will save information. The script will modify this file.
`touch /path/to/sqlitefile.db`

Create a `credentials.py` file in the root directory, and specify your `gmail_user` and `gmail_password`, as well as the `sqlite_db_file` filepath. Don't worry, `credentials.py` is part of the `.gitignore`.

Run `run_check.py`

# OS X
You may have to first install sqlite
`brew install sqlite`
