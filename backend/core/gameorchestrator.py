from abc import ABC
from abc import abstractmethod
from logging import getLogger

log = getLogger(__name__)


class Action(ABC):
    type = None

    @staticmethod
    @abstractmethod
    def act(act_data=None):
        ...


class SetLayoutAction(Action):
    type = 'layout'

    @staticmethod
    def act(data):
        log.error('set layout action')
        log.error(data)
        return {
            'type': 'action',
            'action': 'set layout success',
        }


class MoveAction(Action):
    type = 'move'

    @staticmethod
    def act(data):
        log.error('move action')
        log.error(data)
        return {
            'type': 'action',
            'action': 'move enemy',
        }


actions = {action.type: action for action in Action.__subclasses__()}


class GameOrchestratorError(Exception):
    ...


class GameOrchestrator:

    @staticmethod
    def process_move(data):
        if 'type' not in data:
            raise GameOrchestratorError(f'No type in provided data {data}')
        if data['type'] not in actions:
            raise GameOrchestratorError('No action for provided type')

        return actions[data['type']].act(data['data'])
