from dispatch.view import View
from dispatch.response import *
from auth.decorators import *
from models.user import User
from models.group import Group
from models.repository import Repository
from template.shortcuts import evaluate
from models.options import Options

class Ajax(View):
	"""Ajax view, for global ajax requests, like list users/groups/repositories"""
	@login_required
	def handler(self, req, path):
		o = Options()

		# we only handle ajax requests
		if not req.is_ajax():
			return Redirect(o.url_path('base_url_submin'))

		if 'listAll' in req.post:
			return self.listAll(req)
		if 'listUsers' in req.post:
			return self.listUsers(req)
		if 'listGroups' in req.post:
			return self.listGroups(req)
		if 'listRepositories' in req.post:
			return self.listRepositories(req)

		return XMLStatusResponse('', False, 'Unknown command')

	def listUsers(self, req):
		session_user = req.session['user']
		try:
			users = User.list(session_user)
			return XMLTemplateResponse("ajax/listusers.xml", {'users': users})
		except Exception, e:
			return XMLStatusResponse('listUsers', False, 'Failed to get a list: %s' % e)

	def listGroups(self, req):
		try:
			groups = Group.list(req.session['user'])
			return XMLTemplateResponse("ajax/listgroups.xml", {'groups': groups})
		except Exception, e:
			raise
			return XMLStatusResponse('listGroups', False, 'Failed to get a list: %s' % e)

	def listRepositories(self, req):
		try:
			repos = Repository.list(req.session['user'])
			variables = {'repositories': repos}
			return XMLTemplateResponse("ajax/listrepositories.xml", variables)
		except Exception, e:
			raise
			return XMLStatusResponse('listRepositories', False, 'Failed to get a list: %s' % e)

