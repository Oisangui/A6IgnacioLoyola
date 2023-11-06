"""
import json
from typing import List, cast
from uuid import UUID
from app.model.desktop import Desktop
from app.model.desktop_repository import DesktopRepository


class DesktopDisk(DesktopRepository):
    def __init__(self, file_path):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        try:
            open(self.file_path, 'r')
        except FileNotFoundError:
            open(self.file_path, 'w').close()

    def _read_file(self)->List[dict]:
        json_obj = json.load(open(self.file_path, 'r'))
        return cast(List[dict], json_obj)

    def get_desktops(self):
        data =  self._read_file()
        desktops = []
        for desktop in data:
            desktops.append(Desktop.from_dict(desktop))

    def get_desktop(self, desktop_id):
        data = self._read_file()
        for desktop in data:
            if desktop['os_id'] == desktop_id:
                return Desktop.from_dict(desktop)
            if desktop.get('alias') == desktop_id:
                return Desktop.from_dict(desktop)
        return None

    def create_desktop(self, desktop: Desktop):
        data = self._read_file()
        # Ensure it does not ensure already
        # With same alias or os_id
        data = self._read_file()
        for d in data:
            if d['os_id'] == desktop.os_id:
                raise Exception('Desktop already exists')
            if d.get('alias') == desktop.alias:
                raise Exception('Desktop already exists')
        desktop_dict = desktop.dict()
        desktop_dict['_id'] = str(UUID().hex)
        data.append(desktop.dict())
        json.dump(data, open(self.file_path, 'w'))

    def update_desktop(self, desktop_id, desktop):
        data = self._read_file()
        for i, d in enumerate(data):
            if d['os_id'] == desktop_id:
                data[i] = desktop.dict()
                json.dump(data, open(self.file_path, 'w'))
                return
        raise Exception('Desktop not found')

    def delete_desktop(self, desktop_id):
        data = self._read_file()
        for i, d in enumerate(data):
            if d['os_id'] == desktop_id:
                del data[i]
                json.dump(data, open(self.file_path, 'w'))
                return
        raise Exception('Desktop not found')
"""

# Path: app/repository/test/test_desktop_disk.py
import os
import unittest
from unittest.mock import patch
from app.model.desktop import Desktop
from app.repository.desktop_disk import DesktopDisk


class TestDesktopDisk(unittest.TestCase):

    def setUp(self):
        self.desktop_disk = DesktopDisk('test.json')

    def tearDown(self):
        import os
        os.remove('test.json')

    def test_desktop_disk(self):
        self.assertEqual(self.desktop_disk.file_path, 'test.json')

    def test_desktop_disk_ensure_file_exists(self):
        self.desktop_disk._ensure_file_exists()
        self.assertTrue(os.path.exists('test.json'))

    def test_desktop_disk_read_file(self):
        self.desktop_disk._ensure_file_exists()
        self.assertEqual(self.desktop_disk._read_data(), [])

    def test_desktop_disk_get_desktops(self):
        self.desktop_disk._ensure_file_exists()
        self.assertEqual(self.desktop_disk.get_desktops(), [])

    def test_desktop_disk_get_desktop(self):
        self.desktop_disk._ensure_file_exists()
        self.assertEqual(self.desktop_disk.get_desktop(1), None)

    def test_desktop_disk_create_desktop(self):
        self.desktop_disk._ensure_file_exists()
        self.desktop_disk.create_desktop(Desktop(1, 'Ubuntu'))
        # Here we only assert on fields alias and os_id
        # because _id is generated randomly
        self.assertEqual(self.desktop_disk.get_desktop(1).alias, 'Ubuntu')
        self.assertEqual(self.desktop_disk.get_desktop(1).os_id, 1)

    def test_desktop_disk_create_desktop_with_same_os_id(self):
        self.desktop_disk._ensure_file_exists()
        self.desktop_disk.create_desktop(Desktop(1, 'Ubuntu'))
        with self.assertRaises(Exception):
            self.desktop_disk.create_desktop(Desktop(1, 'Ubuntu'))

    def test_desktop_disk_create_desktop_with_same_alias(self):
        self.desktop_disk._ensure_file_exists()
        self.desktop_disk.create_desktop(Desktop(1, 'Ubuntu'))
        with self.assertRaises(Exception):
            self.desktop_disk.create_desktop(Desktop(2, 'Ubuntu'))

    def test_desktop_disk_update_desktop(self):
        self.desktop_disk._ensure_file_exists()
        self.desktop_disk.create_desktop(Desktop(1, 'Ubuntu'))
        self.desktop_disk.update_desktop(1, Desktop(1, 'Ubuntu 18.04'))
        self.assertEqual(self.desktop_disk.get_desktop(1).alias, 'Ubuntu 18.04')
        self.assertEqual(self.desktop_disk.get_desktop(1).os_id, 1)

    def test_desktop_disk_update_desktop_not_found(self):
        self.desktop_disk._ensure_file_exists()
        with self.assertRaises(Exception):
            self.desktop_disk.update_desktop(1, Desktop(1, 'Ubuntu 18.04'))

    def test_desktop_disk_delete_desktop(self):
        self.desktop_disk._ensure_file_exists()
        self.desktop_disk.create_desktop(Desktop(1, 'Ubuntu'))
        self.desktop_disk.delete_desktop(1)
        self.assertEqual(self.desktop_disk.get_desktop(1), None)

    def test_desktop_disk_delete_desktop_not_found(self):
        self.desktop_disk._ensure_file_exists()
        with self.assertRaises(Exception):
            self.desktop_disk.delete_desktop(1)

    def test_desktop_disk_get_desktop_by_alias(self):
        self.desktop_disk._ensure_file_exists()
        self.desktop_disk.create_desktop(Desktop(1, 'Ubuntu'))
        self.assertEqual(self.desktop_disk.get_desktop('Ubuntu').alias, 'Ubuntu')
        self.assertEqual(self.desktop_disk.get_desktop('Ubuntu').os_id, 1)

    def test_desktop_disk_get_desktop_by_alias_not_found(self):
        self.desktop_disk._ensure_file_exists()
        self.assertEqual(self.desktop_disk.get_desktop('Ubuntu'), None)
