import urllib
from lib.utils import mimport
iif = mimport('lib.utils').iif
html = mimport('lib.html')
mod_authz = mimport('lib.authz')

def _getauthz(input):
	SubmergeEnv = input.req.get_options()['SubmergeEnv']

	import ConfigParser
	cp = ConfigParser.ConfigParser()
	cp.read(SubmergeEnv)
	try:
		authz_file = cp.get('svn', 'authz_file')
	except ConfigParser.NoSectionError, e:
		print e, 'in', SubmergeEnv
		return

	return mod_authz.Authz(authz_file)

def _select(user, permission):
	checked = ' selected="selected"'
	select = '<select name="%s">' % urllib.quote(user)
	select += '\n\t\t\t<option value=""%s>-</option>' % iif(permission == '', checked, '')
	select += '\n\t\t\t<option value="r"%s>r</option>' % iif(permission == 'r', checked, '')
	select += '\n\t\t\t<option value="rw"%s>rw</option>' % iif(permission == 'rw', checked, '')
	select += '\n\t\t</select>'
	return select

def handler(input):
	authz = _getauthz(input)

	print html.header('Permissions')
	print '<h2>Permissions</h2>'
	print '<table>'
	print '\t<thead>'
	print '\t\t<th style="width: 150px" align="left">user / group</th>'
	print '\t\t<th align="left">Permission</th>'
	print '\t</thead>'

	paths = authz.paths()
	paths.sort()
	for repos, path in paths:
		print '<form action="./authz/edit" method="post">'
		print '\t<input type="hidden" name="path" value="%s%s" />' % \
				(iif(repos is not None, urllib.quote(str(repos) + ':'), ''), 
				urllib.quote(path))
		print '\t<tr>'
		print '\t\t<th colspan="2" align="left" ' +\
			'style="border-top: 1px solid #000">%s - %s</th>' % \
			(iif(repos, repos, ''), path)
		print '\t</tr>'
		permissions = authz.permissions(repos, path)
		permissions.sort()
		for user, permission in permissions:
			print '\t<tr>'
			print '\t\t<td><a href="./authz/edit/?repos=%s&path=%s&user=%s">%s</a></td>' % \
					(urllib.quote(str(repos)), urllib.quote(path), 
							urllib.quote(user), user)
			print '\t\t<td>%s</td>' % _select(user, permission)
			print '\t</tr>'
		print '\t<tr>'
		print '\t\t<td colspan="2" align="right">'
		print '\t\t\t<input type="submit" value="Save %s%s" />' %\
				(iif(repos is not None, str(repos) + ':', ''), path)
		print '\t\t</td>\n\t</tr>'
		print '</form>'
	print '</table>'

	print html.footer()

def edit(input):
	authz = _getauthz(input)
	pass