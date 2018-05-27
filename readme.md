UI For Opencast RPM Repository
==============================

Get things running
------------------

Launch the repo UI, this will automatically create the SQLite database:

    % python repoui.py

Next create a password has for your initial user:

    % python -c 'from passlib.hash import pbkdf2_sha512; print(pbkdf2_sha512.encrypt("password"))'                                                               (git)-[master] [0]
    $pbkdf2-sha512$25000$i7EWIsTY21sLwfjfG2OMEQ$fvB.5FwxJam2PG0ECgokSf74syI5WPxW5h4XQN76nEmhW8sFGrrZ51EDep2VxnsDHVzlyCB4FsaafR5L18pW1Q

Finally, add an administrative user to the database:

    % sqlite3 user.db
    sqlite> insert into user (username, password, email, admin, repoaccess) values ('admin', '$pbkdf2-sha512$25000$i7EWI...', 'admin@example.com', 1, 1);

Afterwards, you should be able to login as user `admin` using the password
`password`.
