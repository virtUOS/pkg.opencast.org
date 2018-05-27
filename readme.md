UI For Opencast RPM Repository
==============================

Get things running
------------------

Launch the repo UI, this will automatically create the SQLite database:

    python repoui.py

Now add an administrative user to the database:

    sqlite3 users.db
    sqlite> insert into user (username, password, email, admin, repoaccess) values ('admin', 'password', 'admin@example.com', 1, 1);

Afterwards, you should be able to login as user `admin` using the password
`password`.
