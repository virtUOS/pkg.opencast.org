db_username="matterhorn-rpms"
db_password="j5QV9DCj4vd5bu8h"
database="matterhorn-rpms"

# LOGIN

sessionkey = 'bdkfHvkVt(r8%ZGIUZGTRHg'

# EMAIL TO USER */

repourl      = "http://www.lernfunk.de/repo/"
mailsender   = "virtuos@uni-osnabrueck.de"
mailtopic    = "Registration Matterhorn RPM Repo"
mailtext     = '''Hello %(firstname)s %(lastname)s,
Welcome to the Matterhorn RPM Repository.
Here are your credentials for the repo:
	
	Username: %(username)s
	Password: %(password)s
	
You will find more information if you login under ''' + repourl

# EMAIL TO ADMIN */

adminurl          = "http://www.lernfunk.de/repo/admin/"
#adminmailadress  = "rrolf@uni-osnabrueck.de"
adminmailadress   = "lkiesow@uos.de"
adminmailtopic    = "%(username)s registered on Matterhorn CentOS Repo"
adminmailtext     = "Hello Admin, \n%(username)s (%(firstname)s %(lastname)s) registered to the Matterhorn RPM Repo.\n\nVisit " + adminurl + " to activate his account."

# EMAIL FORGOT PASSWORD */

mailsender = 'no-reply@virtuos.uos.de'
forgotmailtopic  = 'Your password for Matterhorn Repository'
forgotmailtext   = '''Hello,
your login for the Matterhorn RPM Repository:
'''

# TEXT SUCCESSFULL/ERROR REGESTRATION PAGE */

successtext     = '''Thank you for signing up! Your request will be reviewed
		and you will get your login after approval.'''
userexistserror = ('Sign-up failed', '''We are sorry, but a user with this
		username already exists. Please choose another username.''')
emailerror = ('Sign-up failed', '''You are required to use a valid email
		address for registration.''')
captchaerror    = ('Sign-up failed', '''There was an error during the sign up
		process. Please try again.''')
dberror         = ('Database error', '''An error occurred. The connection to
		the database could not be established. This should not have happened.
		Please report this and try again later.''')
loginerror      = ('Log-in failed', '''The log-in failed. Please verify that
		you used the correct username and password and try again.''')
forgotmailerror = ('Password recovery failed', '''There is no active user with
		the given mail address. Please make sure you entered the address
		correctly.''')


# TEXT SIGNUP INFO TEXT */

signupinfotext = "With signing up you will get free access to Matterhorn Repo for CentOS and Fedora."

# TEXT FORGOTTEN PASSWORD SENT */

passwordsenttext = "We sent a mail with your password to you."
