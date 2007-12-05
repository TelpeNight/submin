from template.shortcuts import evaluate_main
from dispatch.response import Response
from config.config import Config
from models.user import User
from models.group import Group
from authz.authz import Authz
from authz.htpasswd import HTPasswd

class Users(object):
	def handler(self, req, path, ajax=False):
		if ajax:
			return self.ajaxhandler(req, path)

		config = Config()

		authz = Authz(config.get('svn', 'authz_file'))
		htpasswd = HTPasswd(config.get('svn', 'access_file'))

		localvars = {}

		user = None
		authz_users = authz.users()
		username = ''
		if len(path) > 0:
			username = path[0]

		htpasswd_users = htpasswd.users()
		if username in htpasswd_users:
			email = ''
			if authz_users.has_key(username):
				if authz_users[username].has_key('email'):
					email = authz_users[username]['email']
			user = User(username, email)

		groups = []
		authz_groups = authz.groups()
		authz_groups.sort()
		for group in authz_groups:
			members = authz.members(group)
			groups.append(Group(group, members))

		localvars['user'] = user
		localvars['member_of'] = groups
		formatted = evaluate_main('users', localvars)
		return Response(formatted)

	def ajaxhandler(self, req, path):
		config = Config()
		authz = Authz(config.get('svn', 'authz_file'))

		success = False
		error = ''

		username = path[0]

		try:
			email = req.get.get('email')
			authz.setUserProp(username, 'email', email)
			success = True
		except Exception, e:
			error = 'Could not change email of user ' + username

		try:
			password = req.get.get('password')
			htpasswd = HTPasswd(config.get('svn', 'access_file'))
			htpasswd.change(username, password)
			htpasswd.flush()
			success = True
		except Exception, e:
			error = 'Could not change password of user ' + username

		if success:
			error = 'Success!'

		return Response(error)