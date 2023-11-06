"""
from typing import Optional


class Desktop:
    def __init__(
            self,
            os_id: int,
            alias: str=Optional[str]
    ):
        self.os_id = os_id
        self.alias = alias

    def __repr__(self):
        return f'<Desktop {self.os_id} {self.alias}>'

    def __str__(self):
        return f'{self.os_id} {self.alias}'

    def dict(self):
        return {
            'os_id': self.os_id,
            'alias': self.alias
        }
    
    def set_alias(self, alias: str):
        self.alias = alias

    @staticmethod
    def new_from_dict(dict: dict):
        return Desktop(
            os_id=dict['os_id'],
            alias=dict.get('alias')
        )
    
"""

# Path: app/model/test/desktop.py
import unittest

from app.model.desktop import Desktop


class TestDesktop(unittest.TestCase):

    def test_desktop(self):
        desktop = Desktop(1)
        self.assertEqual(desktop.os_id, 1)
        self.assertEqual(desktop.alias, None)

    def test_desktop_with_alias(self):
        desktop = Desktop(1, 'Ubuntu')
        self.assertEqual(desktop.os_id, 1)
        self.assertEqual(desktop.alias, 'Ubuntu')

    def test_desktop_set_alias(self):
        desktop = Desktop(1)
        desktop.set_alias('Ubuntu')
        self.assertEqual(desktop.os_id, 1)
        self.assertEqual(desktop.alias, 'Ubuntu')

    def test_desktop_dict(self):
        desktop = Desktop(1, 'Ubuntu')
        self.assertEqual(desktop.dict(), {
            'os_id': 1,
            'alias': 'Ubuntu'
        })

    def test_desktop_new_from_dict(self):
        desktop = Desktop.new_from_dict({
            'os_id': 1,
            'alias': 'Ubuntu'
        })
        self.assertEqual(desktop.os_id, 1)
        self.assertEqual(desktop.alias, 'Ubuntu')

    def test_desktop_new_from_dict_without_alias(self):
        desktop = Desktop.new_from_dict({
            'os_id': 1
        })
        self.assertEqual(desktop.os_id, 1)
        self.assertEqual(desktop.alias, None)

    def test_desktop_repr(self):
        desktop = Desktop(1, 'Ubuntu')
        self.assertEqual(repr(desktop), '<Desktop 1 Ubuntu>')

    def test_desktop_str(self):
        desktop = Desktop(1, 'Ubuntu')
        self.assertEqual(str(desktop), '1 Ubuntu')

    def test_desktop_reversible_to_dict(self):
        desktop = Desktop(1, 'Ubuntu')
        self.assertEqual(desktop.dict(), Desktop.new_from_dict(desktop.dict()).dict())
