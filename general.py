import abc
from process import XYZListen, XYZRespond

class Statement(abc.ABC):

    @abc.abstractmethod
    def clean(self):
        pass

    @abc.abstractmethod
    def respond(self):
        pass

class GeneralStatement(Statement):

    def __init__(self, xyz_respond: XYZRespond = None, xyz_listen: XYZListen = None):
        super().__init__()
        self.xyz_respond = xyz_respond
        self.xyz_listen = xyz_listen

    def clean(self, statement):
        statement = statement.replace("wikipedia", "")
        return statement

    def respond(self, statement):
        text = self.clean(statement)
        self.xyz_respond.run(text)
