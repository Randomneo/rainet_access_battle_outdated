from abc import ABC
from abc import abstractmethod


class ActionValidationError(Exception):
    ...


class ActionValidator(ABC):

    @abstractmethod
    def validate(self, data):
        pass


class SetLayoutValidator(ActionValidator):

    def validate_field(self, i, j, field):
        allowed_poses = (
            (7, 0),
            (7, 1),
            (7, 2),
            (6, 3),
            (6, 4),
            (7, 5),
            (7, 6),
            (7, 7),
        )
        is_virus = field.startswith('virus')
        is_link = field.startswith('link')
        if (is_virus or is_link) and (i, j) not in allowed_poses:
            raise ActionValidationError('not valid virus/link pos')

        if is_virus:
            return 1, 0
        if is_link:
            return 0, 1
        return 0, 0

    def validate(self, data):
        viruses = 0
        links = 0
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                virus, link = self.validate_field(i, j, item)
                viruses += virus
                links += link
        if not (viruses == 4 and links == 4):
            raise ActionValidationError('Not valid cards count')
