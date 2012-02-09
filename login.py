import pygtk
pygtk.require('2.0')
import gtk

import logging

import multiprocessing

from broadcast import BroadcastClient
from broadcast.signals import teacher_discovered

import gobject

class LoginApp:
    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('Login')
        self.liststore = gtk.ListStore(str)
        print len(self.liststore)
        #self.liststore.append(['first'])
        #print len(self.liststore)
        self.treeview = gtk.TreeView(self.liststore)
        self.treeview_column = gtk.TreeViewColumn('Available Teachers')
        self.treeview.append_column(self.treeview_column)
        #gobject.timeout_add(1, self.handle_teacher_discovery_event)
        teacher_discovered.connect(self.handle_teacher_discovery_event)
        self.cell = gtk.CellRendererText()
        self.treeview_column.pack_start(self.cell, True)
        self.treeview_column.add_attribute(self.cell, 'text', 0)
        self.window.add(self.treeview)
        self.window.show_all()

    def handle_teacher_discovery_event(self, signal, sender):
        #self.liststore.append(['parent'])
        #model = self.treeview.get_model()
        #model.append(('parenrnerer',))
        #print len(self.liststore)
        #print sender
        #print signal
        #print 'New teacher available'
        #gobject.timeout_add(1, self.handle_teacher_discovery_event)
        self.add_teacher()

    def add_teacher(self):
        self.liststore.append(['parent'])


if __name__ == "__main__":
    app = LoginApp()
    multiprocessing.log_to_stderr(logging.DEBUG)
    message = 'bcastserver'
    datagram_size = len(message)
    client = BroadcastClient(65535, datagram_size)
    client.start()
    gtk.main()
    client.join()
