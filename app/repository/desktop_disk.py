import json
from typing import List, cast
from app.model.desktop import Desktop
from app.model.desktop_repository import DesktopRepository
import uuid


class DesktopDisk(DesktopRepository):
    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        try:
            open(self.file_path, 'r').close()
        except FileNotFoundError:
            # Write {"data": [] }
            self._save_data([])

    def _read_data(self)->List[dict]:
        with open(self.file_path, 'r') as f:
            json_obj = json.load(f)
        return cast(List[dict], json_obj["data"])

    def _save_data(self, data: List[dict]):
        with open(self.file_path, 'w') as f:
            json.dump({'data': data}, f)

    def get_desktops(self):
        data =  self._read_data()
        desktops = []
        for desktop in data:
            desktops.append(Desktop.from_dict(desktop))
        return desktops

    def get_desktop(self, desktop_id):
        data = self._read_data()
        for desktop in data:
            if desktop['os_id'] == desktop_id:
                return Desktop.new_from_dict(desktop)
            if desktop.get('alias') == desktop_id:
                return Desktop.new_from_dict(desktop)
        return None

    def create_desktop(self, desktop: Desktop):
        data = self._read_data()
        for d in data:
            if d['os_id'] == desktop.os_id:
                raise Exception('Desktop already exists')
            if d.get('alias') == desktop.alias:
                raise Exception('Desktop already exists')
        desktop_dict = desktop.dict()
        desktop_dict['_id'] = str(uuid.uuid4().hex)
        data.append(desktop.dict())
        self._save_data(data)

    def update_desktop(self, desktop_id, desktop):
        data = self._read_data()
        for i, d in enumerate(data):
            if d['os_id'] == desktop_id:
                data[i] = desktop.dict()
                self._save_data(data)
                return
        raise Exception('Desktop not found')

    def delete_desktop(self, desktop_id):
        data = self._read_data()
        for i, d in enumerate(data):
            if d['os_id'] == desktop_id:
                del data[i]
                self._save_data(data)
                return
        raise Exception('Desktop not found')
