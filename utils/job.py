from threading import Thread
from kivy.event import EventDispatcher
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from utils.i18n import _
from utils.info_ctl import info_ctl
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty


class Job(EventDispatcher,Thread):
    __stereotype__ = StringProperty('job')
    controller=ObjectProperty(None)
    job_id=''
    job_events=('on_job_init','on_job_finished','on_job_error','on_job_finally','on_feedback_init','on_feedback_loop','on_feedback_finished')
    def on_controller(self,sender,value):
        for k in self.job_events:
            if hasattr(self.controller,k+self.job_id):
                self.bind(**{k:getattr(self.controller,k+self.job_id)})
    def on_job_init(self,*largs):
        pass
    def on_job_finished(self,*largs):
        pass
    def on_job_error(self,*largs):
        pass
    def on_job_finally(self,*largs):
        pass
    def on_feedback_init(self,*largs):
        pass
    def on_feedback_loop(self,*largs):
        pass
    def on_feedback_finished(self,*largs):
        pass
    def __init__(self,**kwargs):
        super(Job,self).__init__(**kwargs)
        for k in self.job_events:
            self.register_event_type(k)
        self.job_state=None
        self.str_error=""
        self.str_traceback=""
        self.str_feedback=""

    def start_job(self,*args,**kwargs):
        self.args_job = args
        self.kwargs_job = kwargs
        self.dispatch('on_job_init')
        self.job_state='running'
        self.start()
        Clock.schedule_once(self.check_finished,0.5)
    
    def run(self):
        self.do_job(*self.args_job,**self.kwargs_job)


    def do_job(self,*largs,**kwargs):
        raise "Not implemented"


    def check_finished(self,dt):
        if self.job_state=='finished':
            self.dispatch('on_job_finished')
            self.dispatch('on_job_finally')
            return
        if self.job_state=='error':
            self.dispatch('on_job_error')
            self.dispatch('on_job_finally')
            return
        self.dispatch('on_feedback_init')
        Clock.schedule_once(self.feedback_loop,0.2) 
    
    def feedback_loop(self,dt):
        self.dispatch('on_feedback_loop')
        if self.job_state=='running':
            Clock.schedule_once(self.feedback_loop,0.2)
        else:
            self.dispatch('on_feedback_finished')
            if self.job_state=='finished':
                self.dispatch('on_job_finished')
                self.dispatch('on_job_finally')
                return
            if self.job_state=='error':
                self.dispatch('on_job_error')
                self.dispatch('on_job_finally')
                return

Builder.load_string('''
<CargandoLayout>:
    pb:pb
    ProgressBar:
        id:pb
        max: 100
        value:0
''')

class CargandoLayout(BoxLayout):
    __stereotype__ = StringProperty('widget')
    pb=ObjectProperty()

class JobLoading(Job): 
    def on_feedback_init(self,*largs):
        from utils.format import get_format
        self.e=CargandoLayout()
        self.e.lbl=_('Cargando')
        self.popup = Popup(title_size=get_format('font14'),title=_('Cargando'),
                      content=self.e,
                      size_hint=(None, None), size=(400, 150),auto_dismiss=False)
        self.popup.open()
    def on_feedback_loop(self,*largs):
        self.e.pb.value=(self.e.pb.value+5)%self.e.pb.max

    def on_job_init(self,*largs):
        import gc
        print "job_collecting",str(gc.collect())
        self.controller.screen_manager.all_widgets_disabled=True
    
    def on_job_finally(self,*largs):
        self.controller.screen_manager.all_widgets_disabled=False

    def on_job_error(self,*largs):
        info_ctl.error(_('Error'),self.str_error,self.str_traceback)

    def on_feedback_finished(self,*largs):
        self.popup.dismiss()

