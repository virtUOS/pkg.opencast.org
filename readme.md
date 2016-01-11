UI For Opencast RPM Repository
==============================

Get things running
------------------

Launch the repo UI, this will automatically create the SQLite database:

    python repoui.py

Now add an administrative user to the database:

    sqlite3 users.db
    sqlite> insert into user (username, password, email, admin, repoaccess) values ('admin', '123', 'virtmm@uos.de', 1, 1);
