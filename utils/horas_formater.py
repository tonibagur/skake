from kivy.properties import StringProperty

class HorasFormater:
    __stereotype__ = StringProperty('other')
    def format_horas(self,h):
        hores=int(h)
        resta=h-hores 
        return str(hores).zfill(2) + ':' + str(abs(int(resta*60))).zfill(2)    
