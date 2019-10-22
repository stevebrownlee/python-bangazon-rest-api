# Bangazon Platform API

There are a couple steps to run this server. After you clone the repo, cd into it and perform the following steps:
1. Run this command: ```python -m venv bangazonenv``` _(if you are on Windows, this is the only command needs to be run in Windows Command Line, not Git Bash)_
1. Run `source ./bangazonenv/Scripts/activate` on Windows, or `source bangazonenv/bin/activate` on OSX.
1. In the root directory run the following command
    `pip install -r requirements.txt`
1. Execute `./seed_data.sh`

Now that your database is set up all you have to do is run the command:

```sh
python manage.py runserver
```
