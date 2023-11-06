import abc

class DesktopRepository(abc.ABC):
    @abc.abstractmethod
    def get_desktops(self):
        pass

    @abc.abstractmethod
    def get_desktop(self, desktop_id):
        pass

    @abc.abstractmethod
    def create_desktop(self, desktop):
        pass

    @abc.abstractmethod
    def update_desktop(self, desktop_id, desktop):
        pass

    @abc.abstractmethod
    def delete_desktop(self, desktop_id):
        pass