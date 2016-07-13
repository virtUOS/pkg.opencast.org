# -*- coding: utf-8 -*-
database='sqlite:///user.db'

# LOGIN
sessionkey = 'bdkfHvkVt(r8%ZGIUZGTRHg'

# EMAIL TO USER */

repourl = 'https://pkg.opencast.org'
accessmailsender = "no-reply@uni-osnabrueck.de"
accessmailsubject = "Opencast Package Repository"
accessmailtext = '''Hello %(firstname)s %(lastname)s,
Welcome to the Opencast Package Repository.
Here are your credentials for the repo:

    Username: %(username)s
    Password: %(password)s

For more information, please visit
 ''' + repourl

# EMAIL TO ADMIN */

adminurl          = repourl + "/admin"
adminmailadress   = ['lkiesow@uos.de', 'rrolf@uos.de']
adminmailsubject = "%(username)s registered on Opencast Package Repository"
adminmailtext     = '''Hello Admin,
%(username)s (%(firstname)s %(lastname)s) signed-up for the Opencast Package
Repository. To review this registration, visit:

''' + adminurl

# EMAIL FORGOT PASSWORD */

forgotmailsubject = 'Reset Password for Opencast Repository'
forgotmailtext = '''Hello %(firstname)s %(lastname)s,
it seems like you want to reset your password for the Opencast Package
Repository. To do so, follow the following link within the next 24h:

  ''' + repourl + '''%(resetlink)s

If you did not initiate this process, please just ignore this e-mail.
'''

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
