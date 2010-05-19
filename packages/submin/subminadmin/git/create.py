import os
import sys
import commands

from submin.models import options

def run(reponame):
	if not reponame.endswith(".git"):
		reponame += ".git"

	reposdir = options.env_path('git_dir') + reponame

	old_path = os.environ["PATH"]
	os.environ["PATH"] = options.value("env_path")
	cmd = 'GIT_DIR="%s" git --bare init' % str(reposdir)
	(exitstatus, outtext) = commands.getstatusoutput(cmd)
	os.environ["PATH"] = old_path

	if exitstatus != 0:
		raise PermissionError(
			"External command 'GIT_DIR=\"%s\" git --bare init' failed: %s" % \
					(name, outtext))