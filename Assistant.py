import pygtk
pygtk.require('2.0')
import gobject
gobject.threads_init ()
import os,gtk,gio

class Assistant(gobject.GObject):
	
	__gsignals__ = {
		"switch-page" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
		"validate-page" : (gobject.SIGNAL_RUN_LAST, int, (gobject.TYPE_PYOBJECT,)),
	}
	
	builder = None
	__window = None
	__vbox_side_title = None
	__label_top_title = None
	__button_back = None
	__button_continue = None
	__nb = None
	__pages = []
	on_last_page_disable_continue = True
	
	VALIDATE_UNKNOWN, VALIDATE_SUCCESS, VALIDATE_FAIL = range(3)
	
	def __init__(self):
		gobject.GObject.__init__(self)
		#self.connect("validate-page",self.__validate_page_cb)
		
		self.builder = gtk.Builder()
		
		glade_prefix = ""
		try:
			glade_prefix = os.environ["GLADE_PREFIX"]
		except KeyError:
			print "No Glade Environment"
		
		
		self.builder.add_from_file(glade_prefix+"assistant.glade")
		self.window = self.builder.get_object("mainWindow")
		self.__vbox_side_title = self.builder.get_object("vboxSideTitle")
		self.__label_top_title = self.builder.get_object("labelTopTitle")
		self.__nb = self.builder.get_object("notebook")
		self.__button_back = self.builder.get_object("buttonBack")
		self.__button_continue = self.builder.get_object("buttonContinue")
		
		self.__button_back.connect("clicked", self.__click_back)
		self.__button_continue.connect("clicked", self.__click_continue)
		self.__nb.connect("switch-page",self.__nb_change_current_page_cb)
		
	def show(self):
		# Build
		
		for page in self.__pages:
			
			# Side Label
			page.side_label = gtk.Label()
			page.side_label.set_alignment(0,0.5)
			page.side_label.set_markup(page.title_side)
			
			self.__vbox_side_title.pack_start(page.side_label, expand=False, fill=True, padding=0)
			
			# Notebook Page
			self.__nb.append_page(page.widget,gtk.Label("Page"))
		
		self.__rejigger()
		
		# Show
		self.__vbox_side_title.show_all()
		self.window.show()
		
		
		
	def add_page(self,page):
		self.__pages.append(page)
		
		
		
	def __rejigger(self):
		for page in self.__pages:
			if page.is_selected:
				page.side_label.set_markup("<b>"+page.title_side+"</b>")
				self.__label_top_title.set_markup("<b> "+page.title_top+"</b>")
			else:
				if page.side_label:
					page.side_label.set_markup(page.title_side)
		
		last_page = self.__pages[len(self.__pages)-1]
		if last_page.is_selected and self.on_last_page_disable_continue:
			self.__button_continue.set_sensitive(False)
		else:
			self.__button_continue.set_sensitive(True)
		
	
	def __nb_change_current_page_cb(self, widget, data, pagenum):
		self.__button_back.set_sensitive(pagenum!=0)
		self.emit("switch-page",self.__pages[pagenum])
		
		i=0
		for page in self.__pages:
			page.is_selected = pagenum==i
			i+=1
		
		self.__rejigger()
	
	def __click_back(self, widget, data=None):
		#Do not validate to go back.
		#res = self.emit("validate-page",self.__pages[self.__nb.get_current_page()])
		#if res == self.VALIDATE_UNKNOWN or res == VALIDATE_SUCCESS:
		self.__nb.prev_page()
	
	def __click_continue(self, widget, data=None):
		res = self.emit("validate-page",self.__pages[self.__nb.get_current_page()])
		if res == self.VALIDATE_UNKNOWN or res == self.VALIDATE_SUCCESS:
			self.__nb.next_page()
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
