'''
Purpose of this file is to preview some arch solution and write them somewere

Time line:
   draw                      draw                  draw
    | mouseclick    mousemove |         some other  |
--> |----event-------event----|------------event----|-->

there is drawing every strict time interval during that interval could
happen any amount of events
'''


class Event:
    def __init__(self, owner):
        self.owner = owner

    def __call__(self, trigger):
        # do something
        return None


class Camera:
    ...


class GameObject:
    board_pos = ...
    visible = bool
    events = dict[str:Event]


class Card:
    selected = bool


class Level:
    level = 8*8

    def add(self, obj, pos):
        ...

    def move(self, obj, pos_start, pos_end):
        ...


class Scene:
    camera = Camera()

    level = 8*8
    stage = [
        1,  # place units
        2,  # game itself
    ]
    this_turn = bool

    prepare_mouse_click_events = []
    game_mouse_click_events = []

    # change on stage change
    current_stage_click_events = ...

    def handle_on_mouse_click(self, trigger_info):
        for event in self.current_stage_click_events:
            event(trigger_info)

    def set_stage_prepare(self):
        # sets events and everything to handle stage 1
        yield
        # unsets all

    def set_stage_game(self):
        # sets events and everything to handle stage 2
        yield
        # unsets all


class Game:
    scene = Scene()
