import { BaseGameObject } from './GameObject.js';
import { Events } from './event.js';


class Mouse extends BaseGameObject {
    constructor() {
        super();
        this.card = null;
        this.cursor = null;
        self = this;

        Events.handlers('board.mousemove').set('draw_cursor', function(data) {
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
    }

    setCursor(gameObject) {
        this.cursor = gameObject.copy();
        this.cursor.z = -1;
        this.cursor.visible = false;
    }

    child_draw() {
        return [this.cursor];
    }

    draw(context) {
        // no extra draw for mouse
    }
}

export var mouse = new Mouse();
