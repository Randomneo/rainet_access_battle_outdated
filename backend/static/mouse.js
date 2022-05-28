import { BaseGameObject } from './GameObject.js';
import { Events } from './event.js';


class Mouse extends BaseGameObject {
    constructor() {
        super();
        this.card = null;
        this.cursor = null;
        self = this;

        Events.handlers('board.mousemove').set('mouse_cursor', function(data) {
            let board = data.board;
            if (!mouse.cursor)
                return;
            let board_pos = board.toBoard(data.mouse_pos);
            if (board_pos.inRect(-1, -1, 8, 8)) {
                self.cursor.visible = true;
                self.cursor.pos = board.toGlobal(board_pos);
            } else {
                self.cursor.visible = false;
            }
        });
        Events.handlers('mouse.setcard').set('set_card', function (card) {
            self.setCursor(card);
            self.cursor.z = -1;
            self.cursor.visible = false;
        });
        Events.handlers('game.start').set('mouse_before_start', function () {
            self.cursor = null;
            Events.handlers('mouse.setcard').delete('set_card');
            Events.handlers('board.mousemove').set('mouse_cursor', function(data) {
                if (!self.cursor)
                    return;
                self.cursor.pos = data.mouse_pos;
                self.cursor.pos.x -= 25;
                self.cursor.pos.y -= 25;
            });
        });
    }

    setCursor(gameObject) {
        this.cursor = gameObject.copy();
    }

    child_draw() {
        return [this.cursor];
    }

    draw(context) {
        // no extra draw for mouse
    }
}

export var mouse = new Mouse();
