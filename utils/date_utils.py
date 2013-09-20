import datetime
from datetime import timedelta
#from pytz import timezone
from kivy.properties import StringProperty

class DateUtils:
    __stereotype__ = StringProperty('other')
    
    def get_hores_dif(self, tz1, tz2, fecha = False):
        return 7
        tz_1 = timezone(tz1)
        tz_2 = timezone(tz2)
        time_aux = None
        now = datetime.datetime.now()
        if not fecha:
            time_aux = now
        else:
            time_aux = fecha.split(".")
            time_aux = time_aux[0]
            time_aux = datetime.datetime.strptime(time_aux, '%Y-%m-%d %H:%M:%S')
        loc_dt = tz_2.localize(time_aux, is_dst = True)
        loc_dt_off = loc_dt.utcoffset()
        loc_hours = loc_dt_off.days * 24
        loc_hours += loc_dt_off.seconds / 3600
        hora_ext = loc_dt.astimezone(tz_1)
        hora_ext_off = hora_ext.utcoffset()
        hora_ext_hours = hora_ext_off.days * 24
        hora_ext_hours += hora_ext_off.seconds / 3600
        hores_dif = hora_ext_hours - loc_hours
        return hores_dif
    
    def get_horas_serv(self,date,date_format = "%Y-%m-%d %H:%M:%S"):
        delta = self.get_hores_dif("Europe/Madrid","EST")
        date_orig = datetime.datetime.strptime(str(date), date_format)
        date_final = date_orig - timedelta(hours=delta)
        date_str = date_final.strftime('%d-%m-%y %H:%M')
        return date_str
    
    #Convierte formato de date_format a date_format_final
    def cambiar_formato_fecha(self, date,date_format = "%Y-%m-%d %H:%M:%S",date_format_final = "%d-%m-%y %H:%M:%S"):
        date_datetime = datetime.datetime.strptime(str(date), date_format)
        date_str = date_datetime.strftime(date_format_final)
        return date_str



