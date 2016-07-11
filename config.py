# -*- coding: utf-8 -*-
database='sqlite:///user.db'

# LOGIN

sessionkey = 'bdkfHvkVt(r8%ZGIUZGTRHg'

# EMAIL TO USER */

repourl      = 'http://pkg.opencast.org'
accessmailsender   = "no-reply@uni-osnabrueck.de"
accessmailsubject = "Opencast Package Repository"
accessmailtext     = '''Hello %(firstname)s %(lastname)s,
Welcome to the Opencast Package Repository.
Here are your credentials for the repo:

    Username: %(username)s
    Password: %(password)s

For more information, please visit
 ''' + repourl

# EMAIL TO ADMIN */

adminurl          = repourl + "admin"
adminmailadress   = ['lkiesow@uos.de', 'rrolf@uos.de']
adminmailadress   = ['lkiesow@uos.de']
adminmailsubject = "%(username)s registered on Opencast Package Repository"
adminmailtext     = '''Hello Admin,
%(username)s (%(firstname)s %(lastname)s) signed-up for the Opencast Package
Repository. To review this registration, visit:

''' + adminurl

# EMAIL FORGOT PASSWORD */

mailsender = 'no-reply@virtuos.uos.de'
forgotmailsubject = 'Reset Password for Opencast Repository'
forgotmailtext = '''Hello %(firstname)s %(lastname)s,
it seems like you want to reset your password for the Opencast Package
Repository. To do so, follow the following link within the next 24h:

  ''' + repourl + '''%(resetlink)s

If you did not initiate this process, please just ignore this e-mail.
'''

# TEXT SUCCESSFULL/ERROR REGESTRATION PAGE */

userexistserror = ('Sign-up failed', '''We are sorry, but a user with this
		username already exists. Please choose another username.''', 'Go back')
emailerror = ('Sign-up failed', '''You are required to use a valid email
		address for registration.''', 'Go back')
captchaerror    = ('Sign-up failed', '''There was an error during the sign up
		process. The equation was not solved correctly. Please try again.''',
		'Go back')
termsofuseuerror = ('Sign-up failed', '''There was an error during the sign up
		process. The terms of use have to be accepted. Please try again.''',
		'Go back')
dberror         = ('Database error', '''An error occurred. The connection to
		the database could not be established. This should not have happened.
		Please report this to lkiesow@uos.de and try again later.''', 'Go back')
loginerror      = ('Log-in failed', '''The log-in failed. Please verify that
		you used the correct username and password and try again.''', 'Go back')
forgotmailerror = ('Password recovery failed', '''There is no active user with
		the given mail address. Please make sure you entered the address
		correctly.''', 'Go back')
forgotsuccess = ('Success', '''A mail containing your login
		credentials has been sent to you.''', '')


# TEXT SIGNUP INFO TEXT */

signupinfotext = "With signing up you will get free access to Matterhorn Repo for CentOS and Fedora."

# TEXT FORGOTTEN PASSWORD SENT */

passwordsenttext = "We sent a mail with your password to you."

#TEXT DELETE MAIL
delete_reasons = [
        'Your request could not be accepted.',
        'Access for non-commercial organizations only.',
        'Invalid or incomplete data.',
        'Duplicated account'
        ]
deletemailsubject = "Registration: Opencast Package Repository"
deletemailtext = '''Hello %(firstname)s %(lastname)s,
we reviewed your registration and are sorry to say that access to the Opencast
Package Repository could not be granted. The reason for this decision is:

    %(reason)s

'''

# FORGOT PASSWORD
set_password_mail = '''Hello %(firstname)s %(lastname)s,
Welcome to the Opencast Package Repository.
Your access has been confirmed. The last step now is to set a password for your
account

    Username: %(username)s
    Password: %(password)s

For more information, please visit
 ''' + repourl
