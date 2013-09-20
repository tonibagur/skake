import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, BooleanProperty,ListProperty,DictProperty,NumericProperty,StringProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

from kivy.event import EventDispatcher


Builder.load_file('utils/grid.kv')

class DataGrid(BoxLayout):
    '''
    Important properties of this class are:
        Header related properties:
           header_height: Absolute height of the header
           header_height_hint: Relative height of the header
           Possible uses:
                1) header_height=0 and header_height_hint=x: The header adjusts his height acording to the size of his parent
                2) header_height_hint=x header_height_hint=None: The header height is absolutely set up.
    '''
    __stereotype__ = StringProperty('widget')
    header=ObjectProperty(None)
    body=ObjectProperty(None)
    adapter=ObjectProperty(None)
    cols_data=ListProperty(None)
    header_height=NumericProperty(0)
    header_height_hint=NumericProperty(0.05,allownone=True)
    header_visible=BooleanProperty(True)
    item_selection=BooleanProperty(False)
    item_selection_callback=ObjectProperty(None)
    

    def on_adapter(self,sender,value):
        if value:
            self.cols_data=value.cols_data
    def refreshData(self):
        self.body.refreshData()

class DataGridHeader(GridLayout):
    __stereotype__ = StringProperty('widget')
    adapter=ObjectProperty()
    allow_resize=False
    def on_adapter(self,sender,value):
        self.clear_widgets()
        if value and self.parent.header_visible:
            for c in self.adapter.cols_data:
                self.add_widget(self.adapter.get_col_widget(c))


class DataGridBody(ScrollView):
    __stereotype__ = StringProperty('widget')
    view=ObjectProperty()
    num_cols=NumericProperty()
    adapter=ObjectProperty()
    
    def refreshData(self):
        if self.adapter.always_refresh:
            self.view.clear_widgets()
        num_children = len(self.view.children)
        if self.adapter.data:
            num_elem=0
            for d in self.adapter.data:
                if num_elem<num_children:
                    w=self.view.children[num_children-num_elem-1]
                    #w.clear_widgets()
                    self.adapter.get_row_widget(d,num_elem,w)
                else:
                    self.view.add_widget(self.adapter.get_row_widget(d,num_elem))
                num_elem=num_elem+1
            if num_elem<num_children:
                c=self.view.children[:num_children-num_elem]
                for e in c:
                    self.view.remove_widget(e)
        else:
            self.view.clear_widgets()

    def on_adapter(self,sender,value):
        if value:
            self.refreshData()
    

class DataGridField(GridLayout):
    __stereotype__ = StringProperty('widget')
    selection_enabled=BooleanProperty(False)
    selected=BooleanProperty(False)
    item_selection_callback=ObjectProperty(None)
    row=ObjectProperty(None)
    allow_resize=True

    def on_touch_down(self,touch):
        super(DataGridField,self).on_touch_down(touch)
        if self.collide_point(touch.pos[0],touch.pos[1]) and self.selection_enabled:
            self.selected=True
    def on_touch_up(self,touch):
        super(DataGridField,self).on_touch_up(touch)
        if not self.selection_enabled:
            return
        fire=False
        if self.selected and self.collide_point(touch.pos[0],touch.pos[1]):
            fire=True
        self.selected=False
        if fire:
            if self.item_selection_callback:
                self.item_selection_callback(self.row)
                
num_chars={}

def get_num_chars(size,font):
    global num_chars
    if size in num_chars:
        return num_chars[size]
    l=Label(text='')
    l.texture_update()
    t=1
    while l.texture_size[0]<size:
        #print l.texture_size[0]
        l.text='A'*t
        l.texture_update()
        t+=1
    num_chars[size]=t+1
    return t+1
    
from collections import defaultdict
length_letter=defaultdict(lambda:defaultdict(int))
#print length_letter['font12']['A']

def get_length_letter(letter,font):
    x=length_letter[font][letter]
    if x>0:
        return x
    else:
        tam=10
        t=letter*tam
        l=Label(text=t)
        l.texture_update()
        x=float(l.texture_size[0])/float(tam)
        length_letter[font][letter]=x
        #print font,letter,x
        return x

class TextRectangle(BoxLayout):
    __stereotype__ = StringProperty('widget')
    label=ObjectProperty(None)
    rect_color=ListProperty([0.2, 0.2, 0.2, 1])
    text=StringProperty('')
    method='fast' # fast or exact
    resize_level=NumericProperty(1)
    
    def get_parent_to_resize(self):
        if self.resize_level==1:
            return self.parent
        elif self.resize_level==2:
            return self.parent.parent
        elif self.resize_level==3:
            return self.parent.parent.parent
    
    def change_parent_size(self,height_texture):
        if hasattr(self,'count'):
            self.count+=1
        else:
            self.count=1
        if hasattr(self.get_parent_to_resize(),'allow_resize') and self.get_parent_to_resize().allow_resize:
            margin=30
            if (max(70,height_texture+margin) > self.get_parent_to_resize().size[1]) or (self.count>1 and self.last_size+margin==self.get_parent_to_resize().size[1]):
                self.get_parent_to_resize().size=(self.get_parent_to_resize().size[0],max(70,height_texture+margin))
        self.last_size=height_texture
    
    def format_text_fast(self,s,size,font_size):
        res=""
        last_seen=0
        max_seen=get_num_chars(size,font_size)
        for c in s:
            if c=='\n' or c==' ':
                last_seen=0
            else:
                last_seen+=1
            if last_seen >max_seen:
                c+='\n'
                last_seen=0
            res+=c
        return res
        
    def format_text_exact(self,s,size,font_size):
        res=""
        size2=0
        for c in s:
            res+=c
            if c!='\n':
                size2+=get_length_letter(c,font_size)
            else:
                size2=0
            if size2>size+5:
                res+='\n'
                size2=0
        return res

        
    def format_text(self,s,size,font_size):
        return self.format_text_exact(s,size,font_size)

class DataGridAdapter(EventDispatcher):
    __stereotype__ = StringProperty('adapter')
    cols_data = ListProperty([('col0','Columna 0',0.2),('col1','Columna 1',0.3),('col2','Columna 2',0.5)])
    data = ListProperty([{'col0':str(i*0),'col1':str(i*1),'col2':'a\nb\nc\n'+'d '*100+'\ne\nf\ng\nh' if i%5==0 else str(i*2)} for i in range(10)])
    grid=ObjectProperty()
    always_refresh=False

    def get_col_widget(self,col):
        return TextRectangle(rect_color=[0.2, 0.2, 1, 1],text=col[1],size_hint_x=col[2])

    def get_element(self,row,col,num_elem,f=None):
        #Caso de elemento m2o, devuelve el name
        if not f:
            if row[col[0]] and str(type(row[col[0]])) == "<type 'list'>" and len(row[col[0]]) > 1:
                return TextRectangle(rect_color=[0.2, 0.2, 0.2, 1],text=str(row[col[0]][1]),size_hint_x=col[2])
            elif not row[col[0]]:
                return TextRectangle(rect_color=[0.2, 0.2, 0.2, 1],text='',size_hint_x=col[2])
            return TextRectangle(rect_color=[0.2, 0.2, 0.2, 1],text=str(row[col[0]]),size_hint_x=col[2])
        else:
            w=self.get_col_element(col,f)
            if row[col[0]] and str(type(row[col[0]])) == "<type 'list'>" and len(row[col[0]]) > 1:
                w.text=str(row[col[0]][1])
                return w
            elif not row[col[0]]:
                w.text=''
                return w
            w.text=str(row[col[0]])
            return w
    def get_col_element(self,col,f):
        index=self.cols_data.index(col)
        return f.children[len(f.children)-index-1]
    
    def get_row_widget(self,row,num_elem,f=None):
        if not f:
            f=DataGridField(selection_enabled=self.grid.item_selection,row=row,item_selection_callback=self.grid.item_selection_callback)
            f.size=(0,60)
            for c in self.cols_data:
                rect=self.get_element(row,c,num_elem)
                f.add_widget(rect)
        else:
            for c in self.cols_data:
                self.get_element(row,c,num_elem,f)
        return f
    def on_data(self,instance,value):
        self.grid.refreshData()

    def refresh_data(self):
        self.grid.refreshData()

class DataGridAExample(DataGridAdapter):
    cols_data = ListProperty([('col0','Columna 0',0.2),('col1','Columna 1',0.6),('col3','Columna 3',0.2)])
    data = ListProperty([{'col0':str(i*0),'col1':str(i*1),'col3':'a\nb\nc\n'+'d '*100+'\ne\nf\ng\nh' if i%5==0 else str(i*2)} for i in range(10)])

class Main(App):

    def build(self):
        # fields,col_hints,data,class,adapter
        #self.root=DataGrid(header_height_hint=0.2)
        self.root=DataGrid(header_height_hint=0.2)
        self.root.adapter=DataGridAExample(grid=self.root)
        self.root.adapter.data = [{'col0':str(i*0),'col1':str(i*1),'col3':'a\nb\nc\n'+'d '*100+'\ne\nf\ng\nh' if i%5==0 else str(i*2)} for i in range(10)]
        return self.root


if __name__ in ('__main__', '__android__'):
    app = Main()
    app.run()
