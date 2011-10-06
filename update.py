import os
import subprocess

for path, directories, files in os.walk('.'):
    for directory in directories:
        subdirectory = os.path.join(path, directory)
        for subpath, subdirectories, subfiles in os.walk(subdirectory):

            if '.git' in subdirectories:
	        print 'Found git repository at: %s' % subpath
	        os.chdir(subpath)
	        subprocess.Popen('/usr/bin/git pull', shell=True)
	        os.chdir('..')
		break

            if '.svn' in subdirectories:
		print 'Found subversion repository at: %s' % subpath
		command = '/usr/bin/svn up %s' % subpath
		subprocess.Popen(command, shell=True)
		break

            if '.bzr' in subdirectories:
		print 'Found bazar repository at: %s' % subpath
                os.chdir(subpath)
                subprocess.Popen('/usr/bin/bzr pull', shell=True)
                os.chdir('..')
		break

	    if '.hg' in subdirectories:
		print 'Found mercurial repository at: %s' % subpath
                os.chdir(subpath)
                subprocess.Popen('/usr/bin/hg pull', shell=True)
                os.chdir('..')
                break
    break
