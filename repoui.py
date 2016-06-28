#!/bin/env python
# -*- coding: utf-8 -*-

# Set default encoding to UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import config
from db import get_session, User
from hashlib import sha512

#import sqlite3
import re
import random
import string
import json
import smtplib
from datetime import date
from flask import Flask, render_template, request, Response, redirect, url_for, session
app = Flask(__name__)
app.secret_key = config.sessionkey


def init():
    db = get_session()
    if db.query(User).count():
        return

    # Add default admin
    salt = passwdgen()
    user = User(
        username='admin',
        firstname='Administrator',
        lastname='',
        email='admin@example.com',
        country='DE',
        city='City',
        organization='Org',
        created=date.today(),
        admin=True,
        access=True)
    user.password_set('123')
    db.add(user)
    db.commit()


@app.route('/', methods=['POST', 'GET'])
def home():
    user, passwd = request.form.get('username'), request.form.get('password')
    if user:
        u = get_session().query(User).filter(User.username==user)
        if not u.count() or not u[0].password_verify(passwd):
            return redirect(url_for('error', e='loginerror'))
        session['login'] = (u[0].username, u[0].admin, u[0].access)


    # Don't accept self set users
    user = None
    try:
        user, admin, repoaccess = session.get('login')
    except:
        pass

    if user and repoaccess:
        return render_template('login.html', config=config, username=user,
                admin=admin)

    # No login? Show start page:
    return render_template('index.html', config=config)


@app.route('/opencast.repo', methods=['GET', 'POST'])
@app.route('/opencast-testing.repo', methods=['GET', 'POST'])
def repofile():
    if not request.authorization:
        return '', 401
    user, passw = request.authorization.username, request.authorization.password
    if not user:
        return '', 401
    try:
        u = get_session().query(User).filter(User.username==user,
                                             User.access==True)
        if not (u.count() and u[0].password_verify(passwd)):
            return '', 400
    except:
        return '', 500

    # Get specs
    tpl     = request.path.lstrip('/')
    os      = request.form.get('os', 'el')
    version = request.form.get('version', '6')

    return render_template(tpl, user=user, passwd=passwd, os=os,
            version=version)


@app.route('/auth', methods=['GET'])
def auth():
    try:
        user, passwd = request.authorization.username, request.authorization.password
        u = get_session().query(User).filter(User.username==user,
                                             User.access==True)
        if u.count() and u[0].password_verify(passwd):
            session['login'] = (user, passwd)
            return '' # 200 OK
    except:
        pass
    return Response('', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})



@app.route('/msg/<e>')
def error(e):
    try:
        msg = getattr(config, e)
        return render_template('message.html', config=config, message=msg)
    except:
        return '', 400


@app.route('/forgot', methods=['GET','POST'])
def forgot():
    # TODO
    email = request.form.get('email')
    if not email:
        return render_template('forgot.html', config=config)

    data = None
    with sqlite3.connect('users.db') as con:
        cur = con.cursor()
        cur.execute('''select username, password from user
                where email=? and repoaccess''', (email,))
        data = cur.fetchall()

    if not data:
        return redirect(url_for('error', e='forgotmailerror'))

    # Send mail
    header  = 'From: %s\n' % config.mailsender
    header += 'To: %s\n' % email
    header += 'Subject: %s\n\n' % config.forgotmailtopic
    message = header + config.forgotmailtext
    for username, password in data:
        message += '\nusername: %s'   % username
        message += '\npassword: %s\n' % password

    server = smtplib.SMTP('smtp.serv.uos.de')
    server.sendmail(
            config.mailsender,
            email,
            message)
    server.quit()
    return redirect(url_for('error', e='forgotsuccess'))


@app.route('/terms')
@app.route('/impressum')
@app.route('/success')
def serve():
    tpl = request.path.lstrip('/')
    return render_template(tpl + '.html', config=config)


@app.route('/admin', methods=['GET', 'POST'])
@app.route('/admin/<who>', methods=['GET', 'POST'])
def admin(who='new'):
    username, admin, repoaccess = [None]*3
    try:
        username, admin, repoaccess = session.get('login')
    except:
        pass
    if not username or not admin:
        return redirect(url_for('home'))

    # Handle save option
    if request.form:
        with sqlite3.connect('users.db') as con:
            cur = con.cursor()
            user = unicode(request.form.get('user'))
            action = request.form.get('action')
            cur.execute(u'''select repoaccess, email, password, firstname, lastname
                    from user where username=?''', (user,))
            data = cur.fetchone()
            if data:
                if action in (u'admin', u'user') and not data[0]:
                    registrationmail(user, data[1], data[2], data[3], data[4])
                if action == u'user':
                    cur.execute(u'update user set repoaccess=1, admin=0 where username=?', (user,))
                elif action == u'admin':
                    cur.execute(u'update user set repoaccess=1, admin=1 where username=?', (user,))
                elif action == u'delete':
                    cur.execute(u'delete from user where username=?', (user,))
                    reason = request.form.get(u'reason')
                    deletemail(user, data[1], data[3], data[4], reason)
                con.commit()

    user = []
    # Get user
    user = get_session().query(User).order_by(User.username.asc())

    if who == 'new':
        user = user.filter(User.access==False)
        return render_template('adminnew.html', config=config, user=user,
                newusercount=user.count())
    return render_template('adminall.html', config=config, user=user,
            newusercount=len([ u for u in user if not u.access]),
            usercount=user.count())


@app.route('/access/<who>/<ref>', methods=['GET'])
def access(who, ref):
    username, admin, repoaccess = [None]*3
    try:
        username, admin, repoaccess = session.get('login')
    except:
        pass
    if not username or not admin:
        return redirect(url_for('home'))

    db = get_session()
    db.query(User).filter(User.username==who).update({'access':True})
    db.commit()

    return redirect(url_for('admin', who=ref))


@app.route('/delete/<who>/<ref>', methods=['GET'])
def delete(who, ref):
    username, admin, repoaccess = [None]*3
    try:
        username, admin, repoaccess = session.get('login')
    except:
        pass
    if not username or not admin:
        return redirect(url_for('home'))

    db = get_session()
    db.query(User).filter(User.username==who).delete()
    db.commit()

    return redirect(url_for('admin', who=ref))


@app.route('/csv', methods=['GET'])
def csv():
    username, admin, repoaccess = [None]*3
    try:
        username, admin, repoaccess = session.get('login')
    except:
        pass
    if not username or not admin:
        return redirect(url_for('home'))

    attr = [a for a in User.__dict__.keys()
            if not (a.startswith('_') or a.startswith('pass') or
                    a.startswith('serial'))]
    csv = ', '.join(attr) + '\n'

    # Get user
    user = get_session().query(User).order_by(User.username.asc())
    for u in user:
        userdata = [getattr(u, a) or '' for a in attr]
        csv += ', '.join(['"%s"' % x for x in userdata]) + '\n'
    return Response(csv, content_type='application/octet-stream')



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/storeuser', methods=['POST'])
def storeuser():
    if request.form.get('terms') != 'agree':
        return redirect(url_for('error', e='termsofuseuerror'))

    if request.form.get('url'):
        return redirect(url_for('error', e='boterror'))

    if not re.match(r'^[^@]+@[^@]+\.[^@]+$', request.form.get('email')):
        return redirect(url_for('error', e='emailerror'))

    if not re.match(r'^[a-z]+$', request.form.get('user')):
        return redirect(url_for('error', e='userexistserror'))

    for field in ['firstname', 'lastname', 'country', 'city', 'organization']:
        if not request.form.get(field):
            return redirect(url_for('error', e='requirederror'))

    db = get_session()
    db.add(User(
        username=request.form.get('user'),
        firstname=request.form.get('firstname'),
        lastname=request.form.get('lastname'),
        email=request.form.get('email'),
        country=request.form.get('country'),
        city=request.form.get('city'),
        organization=request.form.get('organization'),
        department=request.form.get('department'),
        created=date.today(),
        usage=request.form.get('usage'),
        learned=request.form.get('learn-about'),
        admin=False,
        access=False))
    db.commit()

    # Send registration mail to admin
    header  = 'From: %s\n' % request.form.get('email')
    header += 'To: %s\n' % config.adminmailadress
    header += 'Subject: %s\n\n' % (
            config.adminmailtopic % {'username' : request.form.get('user')})
    message = header + ( config.adminmailtext % {
        'username'  : request.form.get('user'),
        'firstname' : request.form.get('firstname'),
        'lastname'  : request.form.get('lastname') })

    server = smtplib.SMTP('smtp.serv.uos.de')
    for to in config.adminmailadress:
        server.sendmail(request.form.get('email'), to, message)
    server.quit()
    return redirect(url_for('success'))


def passwdgen():
    chars = string.letters + string.digits
    return ''.join([random.choice(chars) for _ in range(16)])


def registrationmail(username, email, password, firstname, lastname):
    header  = 'From: %s\n' % config.mailsender
    header += 'To: %s\n' % email
    header += 'Subject: %s\n\n' % config.mailtopic
    message = header + config.mailtext % {
            'firstname' : firstname,
            'lastname'  : lastname,
            'username'  : username,
            'password'  : password}

    server = smtplib.SMTP('smtp.serv.uos.de')
    server.sendmail(config.mailsender, email, message)
    server.quit()


def deletemail(username, email, firstname, lastname, reason):

    text = reason

    header  = 'From: %s\n' % config.mailsender
    header += 'To: %s\n' % email
    header += 'Subject: OpencastRepo Accound has been Deleted\n\n'
    message = header + text

    server = smtplib.SMTP('smtp.serv.uos.de')
    server.sendmail(config.mailsender, email, message)
    server.quit()


if __name__ == "__main__":
    init()
    app.run(debug=True)
