'''
Progress Bar
============

.. versionadded:: 1.0.8

.. image:: images/progressbar.jpg
    :align: right

The :class:`ProgressBar` widget is used to visualize progress of some task.
Only horizontal mode is supported, vertical mode is not available yet.

The progress bar has no interactive elements, It is a display-only widget.

To use it, simply assign a value to indicate the current progress::

    from kivy.uix.progressbar import ProgressBar
    pb = ProgressBar(max=1000)

    # this will update the graphics automatically (75% done):
    pb.value = 750

'''

__all__ = ('MyProgressBar', )

from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty, AliasProperty,StringProperty
from kivy.lang import Builder

Builder.load_file('utils/progress.kv')

class TextProgressBar(RelativeLayout):
    __stereotype__ = StringProperty('widget')
    value=NumericProperty(0)
    

class MyProgressBar(Widget):
    '''Class for creating a Progress bar widget.

    See module documentation for more details.
    '''
    __stereotype__ = StringProperty('widget')
    
    def __init__(self, **kwargs):
        self._value = 0.
        super(MyProgressBar, self).__init__(**kwargs)

    def _get_value(self):
        return self._value

    def _set_value(self, value):
        value = max(0, min(self.max, value))
        if value != self._value:
            self._value = value
            return True

    value = AliasProperty(_get_value, _set_value)
    '''Current value used for the slider.

    :data:`value` is a :class:`~kivy.properties.AliasProperty`, than returns the
    value of the progressbar. If the value is < 0 or > :data:`max`, it will be
    normalized to thoses boundaries.

    .. versionchanged:: 1.6.0
        The value is now limited between 0 to :data:`max`
    '''

    def get_norm_value(self):
        d = self.max
        if d == 0:
            return 0
        return self.value / float(d)

    def set_norm_value(self, value):
        self.value = value * self.max

    value_normalized = AliasProperty(get_norm_value, set_norm_value,
                                     bind=('value', 'max'))
    '''Normalized value inside the 0-max to 0-1 range::

        >>> pb = MyProgressBar(value=50, max=100)
        >>> pb.value
        50
        >>> slider.value_normalized
        0.5

    :data:`value_normalized` is an :class:`~kivy.properties.AliasProperty`.
    '''

    max = NumericProperty(100.)
    '''Maximum value allowed for :data:`value`.

    :data:`max` is a :class:`~kivy.properties.NumericProperty`, default to 100.
    '''

class MultiProgressBar(Widget):
    __stereotype__ = StringProperty('widget')
    verde=NumericProperty(0.)
    naranja=NumericProperty(0.)
    azul=NumericProperty(0.)
    roja=NumericProperty(0.)
    roja_disc=NumericProperty(0.)
    barra1=StringProperty('verde')
    barra2=StringProperty('naranja')
    barra3=StringProperty('azul')
    value1=NumericProperty(0)
    value2=NumericProperty(0)
    value3=NumericProperty(0)
    min_visible_value=NumericProperty(0.05)
    
    def on_verde(self,*largs,**kwargs):
        self.refresh_orden_barras()
    def on_naranja(self,*largs,**kwargs):
        self.refresh_orden_barras()
    def on_azul(self,*largs,**kwargs):
        self.refresh_orden_barras()
    
    def refresh_orden_barras(self):
        s = sorted([(self.verde,'verde'),(self.naranja,'naranja'),(self.azul,'azul')],reverse=True)
        self.barra1=s[0][1]
        self.barra2=s[1][1]
        self.barra3=s[2][1]
        self.value1=min((s[0][0] if s[0][0] >= self.min_visible_value else 0),1)
        self.value2=min((s[1][0] if s[1][0] >= self.min_visible_value else 0),1)
        self.value3=min((s[2][0] if s[2][0] >= self.min_visible_value else 0),1)

if __name__ == '__main__':

    from kivy.base import runTouchApp
    runTouchApp(MyProgressBar())

