from foo import system

if system.get_os() == "Windows":
    from win32event import CreateMutex
    from win32api import CloseHandle, GetLastError
    from winerror import ERROR_ALREADY_EXISTS
else:
    import os, commands

class SingleInstance(object):

    def __init__(self):
        self.last_error = False

        if system.get_os() == "Windows":
            self.mutex_name = 'foo_{D0E858DF-985E-4907-B7FB-8D732C3FC3B9}'
            self.mutex = CreateMutex(None, False, self.mutex_name)
            self.last_error = GetLastError()
        else:
            self.pid_path = '/tmp/foo.pid'
            if os.path.exists(self.pid_path):
                pid = open(self.pid_path, 'r').read().strip()
                pid_running = commands.getoutput('ls /proc | grep %s' % pid)

                if pid_running:
                    self.last_error = True

            if not self.last_error:
                f = open(self.pid_path, 'w')
                f.write(str(os.getpid()))
                f.close()

    def is_running(self):
        if system.get_os() == "Windows":
            return (self.last_error == ERROR_ALREADY_EXISTS)
        else:
            return self.last_error

    def __del__(self):
        if system.get_os() == "Windows":
            if self.mutex:
                CloseHandle(self.mutex)
        else:
            if not self.last_error:
                os.unlink(self.pid_path)
