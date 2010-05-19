import os

from submin.models import options
from submin.models import user

def run():
	env_path = options.env_path()
	filename = os.path.expanduser("~/.ssh/authorized_keys")

	www_key_file = env_path + "conf" + "id_dsa.pub"
	if not www_key_file.exists():
		raise Exception("Could not find the submin ssh-key. Please run submin-admin init-git")
	key_fp = open(str(www_key_file))
	www_key = key_fp.readline().strip()
	key_fp.close()

	fp = open(str(filename), "w+")
	fp.write('command="submin-admin \'%s\' git admin" %s\n' % \
			(env_path, www_key))
	userlist = user.list(user.FakeAdminUser())
	for x in userlist:
		u = user.User(x)
		ssh_keys = u.ssh_keys()
		if not ssh_keys:
			continue
		for ssh_key in ssh_keys:
			fp.write('command="submin-admin \'%s\' git user %s" %s\n' % \
					(env_path, u, ssh_key["key"]))
	fp.close()