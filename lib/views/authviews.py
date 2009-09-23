import os

from dispatch.view import View
from dispatch.response import Response, Redirect
from views.error import ErrorResponse
from template.shortcuts import evaluate
from config.authz.htpasswd import NoMD5PasswordError
from models.user import User, UnknownUserError
from models.options import Options

class Login(View):
	def handler(self, request, path):
		o = Options()
		if not request.post:
			return self.evaluate_form(o)
		username = request.post.get('username', '')
		password = request.post.get('password', '')

		invalid_login = True
		try:
			user = User(username)
			invalid_login = False
		except UnknownUserError, e:
			pass

		try:
			if not user.check_password(password):
				return self.evaluate_form(o, 'Not a valid username and password combination')
		except NoMD5PasswordError, e:
			return self.evaluate_form(config, str(e))

		if invalid_login:
			return self.evaluate_form(o, 'Not a valid username and password combination')


		url = '/'
		if 'redirected_from' in request.session:
			url = request.session['redirected_from']

		user.is_authenticated = True
		request.session['user'] = user
		request.session.save()
		return Redirect(url)


	def evaluate_form(self, options, msg=''):
		localvalues = {}
		localvalues['msg'] = msg
		base_url = options.value('base_url_submin')
		if base_url[-1] != '/':
			base_url += '/'
		localvalues['base_url'] = base_url
		return Response(evaluate('login.html', localvalues))


class Logout(View):
	def handler(self, request, path):
		if 'user' in request.session:
			request.session['user'].is_authenticated = False
			del request.session['user']
		url = '/'
		if 'redirected_from' in request.session:
			url = request.session['redirected_from']
		return Redirect(url)

