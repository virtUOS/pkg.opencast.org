#!/bin/env python
# -*- coding: utf-8 -*-

# Set default encoding to UTF-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import config

import sqlite3
import random
import string
import json
import smtplib
from datetime import date
from flask import Flask, render_template, request, Response, redirect, url_for, session
app = Flask(__name__)
app.secret_key = config.sessionkey

with sqlite3.connect('users.db') as con:
	cur = con.cursor()
	cur.execute('''create table if not exists user(
		username      TEXT PRIMARY KEY,
		firstname     TEXT,
		lastname      TEXT,
		password      TEXT,
		email         TEXT,
		country       TEXT,
		city          TEXT,
		company       TEXT,
		department    TEXT,
		created       TEXT,
		usematterhorn BOOL,
		installations TEXT,
		adoptiontime  TEXT,
		admin         BOOL,
		repoaccess    BOOL,
		deleteaccess  TEXT,
		comment       TEXT)''')
	con.commit()


@app.route('/', methods=['POST', 'GET'])
def home():
	user, passwd = request.form.get('username'), request.form.get('password')
	if user:
		try:
			with sqlite3.connect('users.db') as con:
				cur = con.cursor()
				cur.execute('''select username, admin, repoaccess from user
						where username=? and password=? and repoaccess''',
						(user, passwd))
				data = cur.fetchone()
				if not data:
					return redirect(url_for('error', e='loginerror'))
				session['login'] = data
		except:
			return redirect(url_for('error', e='loginerror'))


	# Don't accept self set users
	user = None
	try:
		user, admin, repoaccess = session.get('login')
	except:
		pass
	if user:
		return render_template('login.html', config=config, username=user,
				admin=admin)

	# No login? Show start page:
	return render_template('index.html', config=config)


@app.route('/matterhorn.repo', methods=['GET', 'POST'])
@app.route('/matterhorn-testing.repo', methods=['GET', 'POST'])
def repofile():
	if not request.authorization:
		return '', 401
	user, passwd = request.authorization.username, request.authorization.password
	if not user:
		return '', 401
	try:
		with sqlite3.connect('users.db') as con:
			cur = con.cursor()
			cur.execute('''select username from user
					where username=? and password=? and repoaccess''',
					(user, passwd))
			if not cur.fetchone():
				return '', 400
	except:
		return '', 401

	# Get specs
	tpl     = request.path.lstrip('/')
	os      = request.form.get('os', 'el')
	version = request.form.get('version', '6')

	print tpl, user, passwd, os
	return render_template(tpl, user=user, passwd=passwd, os=os,
			version=version)


@app.route('/auth', methods=['GET'])
def auth():
	try:
		user, passwd = request.authorization.username, request.authorization.password
		if session.get('login') == (user, passwd):
			return '' # 200 OK
		with sqlite3.connect('users.db') as con:
			cur = con.cursor()
			cur.execute('''select username from user
					where username=? and password=? and repoaccess''',
					(user, passwd))
			data = cur.fetchone()
			if data:
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


@app.route('/signup')
def signup():
	randa = random.randrange(1, 49)
	randb = random.randrange(1, 49)
	randr = randa + randb
	return render_template('signup.html', config=config, rand=(randa, randb, randr))


@app.route('/success')
def success():
	return render_template('success.html', config=config)


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
		print request.form
		with sqlite3.connect('users.db') as con:
			cur = con.cursor()
			for k, v in request.form.iteritems():
				cur.execute('''select repoaccess, email, password, firstname, lastname
						from user where username=?''', (k,))
				data = cur.fetchone()
				if data and v in ('admin', 'user') and not data[0]:
					registrationmail(k, data[1], data[2], data[3], data[4])
				if v == 'user':
					cur.execute('update user set repoaccess=1, admin=0 where username=?', (k,))
				elif v == 'admin':
					cur.execute('update user set repoaccess=1, admin=1 where username=?', (k,))
				elif v == 'delete':
					cur.execute('delete from user where username=?', (k,))
			con.commit()


	user = []
	# Get user
	with sqlite3.connect('users.db') as con:
		cur = con.cursor()
		cur.execute('select * from user where not repoaccess' if who == 'new' else 'select * from user')
		user = cur.fetchall()

	if who == 'new':
		return render_template('adminnew.html', config=config, user=user,
				newusercount=len(user))
	user.sort(key=lambda u: u[0].lower())
	return render_template('adminall.html', config=config, user=user,
			newusercount=len([ u for u in user if not u[14]]),
			usercount=len(user))



@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))


@app.route('/storeuser', methods=['POST'])
def storeuser():
	if request.form.get('agreebox') != 'agree':
		return redirect(url_for('error', e='termsofuseuerror'))

	if request.form.get('captcha') != request.form.get('correct_result'):
		return redirect(url_for('error', e='captchaerror'))

	email = request.form.get('email')
	if not ( email and '@' in email and '.' in email.split('@')[-1] ):
		return redirect(url_for('error', e='emailerror'))

	if not request.form.get('user'):
		return redirect(url_for('error', e='userexistserror'))

	try:
		with sqlite3.connect('users.db') as con:
			cur = con.cursor()
			cur.execute('''insert into user
					values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (
						request.form.get('user'),
						request.form.get('firstname'),
						request.form.get('lastname'),
						passwdgen(),
						request.form.get('email'),
						request.form.get('country'),
						request.form.get('city'),
						request.form.get('company'),
						request.form.get('department'),
						str(date.today()),
						request.form.get('usematterhorn'),
						request.form.get('installations'),
						request.form.get('adoptiontime'),
						False, False, '', ''))
			con.commit()
	except sqlite3.IntegrityError:
		return redirect(url_for('error', e='userexistserror'))
	except:
		return redirect(url_for('error', e='dberror'))

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
	server.sendmail(
			request.form.get('email'),
			config.adminmailadress,
			message)
	server.quit()
	return redirect(url_for('success'))


def passwdgen():
	chars = string.letters + string.digits
	passwd = ''
	for i in xrange(10):
		passwd += chars[random.randrange(0, len(chars))]
	return passwd


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


if __name__ == "__main__":
	app.run(debug=True)
