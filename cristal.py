
from general import GeneralStatement
from process import XYZListen, XYZRespond

class Cristal(object):

    def __init__(self):
        super().__init__()
        self.xyz_respond = XYZRespond()
        self.xyz_listen = XYZListen()
        self.general_statement = GeneralStatement(self.xyz_respond, self.xyz_listen)
    
    def get_model_path(self) -> str:
        from pocketsphinx import get_model_path
        model_path = get_model_path()
        return model_path

    def run(self):
        self.xyz_listen.run()

if __name__=='__main__':
    cristal = Cristal()
    cristal.run()