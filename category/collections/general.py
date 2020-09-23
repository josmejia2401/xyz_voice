import subprocess
from category.skill import AssistantSkill


def get_master_volume():
    stdout, stderr = subprocess.Popen('/usr/bin/amixer sget Master', shell=True, stdout=subprocess.PIPE).communicate()
    list_len = len(str(stdout).split('\n'))
    amixer_stdout = str(stdout).split('\n')[list_len - 1]
    find_start = amixer_stdout.find('[') + 1
    find_end = amixer_stdout.find('%]', find_start)
    return float(amixer_stdout[find_start:find_end])


def set_master_volume(volume):
    val = float(int(volume))
    proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE)
    proc.wait()

class UtilSkills(AssistantSkill):

    @classmethod
    def speech_interruption(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        """
        Stop assistant speech.
        """
        #stop_speaking = True
        pass

    @classmethod
    def increase_master_volume(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        # Limits: Playback 0 - 31
        step = 2
        volume = get_master_volume()
        if volume > 31:
            cls.response("El volumen de los altavoces ya es máximo")

        increased_volume = volume + step
        if increased_volume > 31:
            set_master_volume(31)
        else:
            set_master_volume(increased_volume)
            cls.response("Aumenté el volumen de los altavoces")

    @classmethod
    def reduce_master_volume(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        # Limits: Playback 0 - 31
        step = 2
        volume = get_master_volume()
        if volume < 0:
            cls.response("El volumen de los altavoces ya está silenciado")

        reduced_volume = volume - step
        if reduced_volume < 0:
            set_master_volume(0)
        else:
            set_master_volume(reduced_volume)
            cls.response("Bajé el volumen de los altavoces")

    @classmethod
    def mute_master_volume(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        # Limits: Playback 0 - 31
        volume = get_master_volume()
        if volume == 0:
            cls.response("El volumen de los altavoces ya está silenciado")
        else:
            set_master_volume(0)
            cls.response("Silencio los altavoces maestros")

    @classmethod
    def max_master_volume(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        # Limits: Playback 0 - 31
        volume = get_master_volume()
        if volume == 31:
            cls.response("El volumen de los altavoces ya es máximo")
        else:
            set_master_volume(31)
            cls.response("Pongo al máximo los altavoces maestros")
