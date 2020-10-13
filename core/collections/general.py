import subprocess
from core.skill import AssistantSkill


def get_master_volume():
    #stdout, stderr = subprocess.Popen('/usr/bin/amixer sget Master', shell=True, stdout=subprocess.PIPE).communicate()
    stdout, stderr = subprocess.Popen('amixer -D pulse sget Master', shell=True, stdout=subprocess.PIPE).communicate()
    list_len = len(str(stdout).split('\n'))
    amixer_stdout = str(stdout).split('\n')[list_len - 1]
    find_start = amixer_stdout.find('[') + 1
    find_end = amixer_stdout.find('%]', find_start)
    return float(amixer_stdout[find_start:find_end])


def set_master_volume(volume):
    val = float(int(volume))
    #amixer -D pulse sset Master 0%
    #proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE)
    proc = subprocess.Popen('amixer -D pulse sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE)
    proc.wait()

class UtilSkills(AssistantSkill):

    @classmethod
    def speech_interruption(cls, ext = None, template = None, values = None, history = []):
        if not cls.get_activation():
            return
        cls.set_stop_speaking(True)
        
    
    @classmethod
    def current_master_volume(cls, ext = None, template = None, values = None, history = []):
        try:
            if not cls.get_activation():
                return
            volume = get_master_volume()
            if volume:
                response = template.format(str(volume) + " porciento de volumen")
            else:
                response = template.format("No se pudo encontrar el volumen")
            cls.response(response)
        except Exception as e:
            print("current_master_volume", e)
            response = template.format("No se pudo procesar el comando")
            cls.response(response)

    @classmethod
    def increase_master_volume(cls, ext = None, template = None, values = None, history = []):
        try:
            if not cls.get_activation():
                return
            step = 5
            volume = get_master_volume()
            if volume >= 100:
                r = template.format("El volumen de los altavoces ya es máximo")
                cls.response(r)
                return

            increased_volume = volume + step
            if increased_volume > 100:
                set_master_volume(100)
                r = template.format("Volumen al 100")
                cls.response(r)
                return
            else:
                set_master_volume(increased_volume)
                r = template.format("Aumenté el volumen de los altavoces")
                cls.response(r)
                return
        except Exception as e:
            print("increase_master_volume", e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)

    @classmethod
    def reduce_master_volume(cls, ext = None, template = None, values = None, history = []):
        try:
            if not cls.get_activation():
                return
            step = 5
            volume = get_master_volume()
            if volume < 0:
                r = template.format("El volumen de los altavoces está silenciado")
                cls.response(r)
                return
            reduced_volume = volume - step
            if reduced_volume < 0:
                set_master_volume(0)
                r = template.format("Volumen al 0")
                cls.response(r)
                return 
            else:
                set_master_volume(reduced_volume)
                r = template.format("Bajé el volumen de los altavoces")
                cls.response(r)
                return
        except Exception as e:
            print("reduce_master_volume", e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)

    @classmethod
    def mute_master_volume(cls, ext = None, template = None, values = None, history = []):
        try:
            if not cls.get_activation():
                return
            volume = get_master_volume()
            if volume == 0:
                r = template.format("El volumen de los altavoces ya está silenciado")
                cls.response(r)
                return
            else:
                set_master_volume(0)
                r = template.format("He Silenciado los altavoces maestros")
                cls.response(r)
                return
        except Exception as e:
            print("mute_master_volume", e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)

    @classmethod
    def max_master_volume(cls, ext = None, template = None, values = None, history = []):
        try:
            if not cls.get_activation():
                return
            volume = get_master_volume()
            if volume == 100:
                r = template.format("El volumen de los altavoces ya es máximo")
                cls.response(r)
                return
            else:
                set_master_volume(100)
                r = template.format("Se establece al máximo en los altavoces maestros")
                cls.response(r)
                return
        except Exception as e:
            print("max_master_volume", e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)
