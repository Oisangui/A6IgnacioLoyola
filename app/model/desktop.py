from typing import Optional


class Desktop:
    def __init__(
            self,
            os_id: int,
            alias: Optional[str]=None
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
    