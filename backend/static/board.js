import { BaseGameObject, Virus, Link } from './GameObject.js';
import { Events, getMousePos } from './event.js';
import { Vec2 } from './vec.js';
import Camera from './camera.js';
import { Scene } from './scene.js';




export class Board extends BaseGameObject {
    constructor(pos, size) {
        super();
        let self = this;
        this.pos = pos;
        this.lineWidth = 1;
        this.fillStyle = '#000';
        this.setsize(size);
        this.card = null;
        console.log(this.rectSize);
        this.handle_click = true;


        this.board = [];
        for (let i = 0; i < 8; i++) {
            this.board.push([]);
            for (let j = 0; j < 8; j++) {
                this.board[i].push(null);
            }
        }
        // prepare stage events
        Events.handlers('board.setcard').set('set_card', function (card) { self.setCard(self, card); });
        Events.handlers('canvas.mousemove').set('show_board_cursor', function (data) {
            if (!self.card)
                return;
            self.cursor = self.card.copy();
            self.cursor.z = -1;
            Scene.namedObjects['cursor'] = self.cursor;

            let board_pos = self.toBoard(getMousePos(data.this, data.event));
            if (Board.isPosOn(board_pos)) {
                self.cursor.visible = true;
                self.cursor.pos = self.toGlobal(board_pos);
            } else {
                self.cursor.visible = false;
            }
        });
        Events.handlers('board.system.start').set('check_start', function () {self.checkBeforeStart();});

        // Clear before game
        Events.handlers('game.start').set('board_before_start', function () {
            self.cursor = null;
            self.card = null;
            Events.handlers('board.setcard').delete('set_card');
            Events.handlers('canvas.mousemove').delete('show_board_cursor');
            Events.handlers('board.system.start').delete('check_start');
        });

    }

    checkBeforeStart() {
        if (this.viruses().length >= 4 && this.links().length >= 4) {
            Events.trigger('game.start');
        } else {
        }
    }

    setsize(size) {
        this.size = size;
        this.rectSize = new Vec2(this.size.x/8, this.size.y/8);
    }

    setCard(self, card) {
        self.card = card;
    }

    clicked(mouse_pos) {
        if (!this.card) {
            return;
        }
        this.add(this.card.copy(), mouse_pos);
    }

    cards() {
        return this.board.reduce((acc, val) => acc.concat(val), []).filter(x => x);
    }

    viruses() {
        return this.cards().filter(x => x.constructor === Virus);
    }

    links() {
        return this.cards().filter(x => x.constructor === Link);
    }

    child_draw() {
        return this.cards();
    }

    draw(context) {

        context.fillStyle = this.fillStyle;
        for (let i = 0; i <= this.size.x; i+=this.rectSize.x) {
            context.fillRect(
                Camera.getX(i + this.pos.x - this.lineWidth / 2),
                Camera.getY(this.pos.y - this.lineWidth / 2),
                this.lineWidth,
                this.size.y + this.lineWidth,
            );
        }
        for (let i = 0; i <= this.size.y; i+=this.rectSize.y) {
            context.fillRect(
                Camera.getX(this.pos.x - this.lineWidth / 2),
                Camera.getY(i + this.pos.y - this.lineWidth / 2),
                this.size.x + this.lineWidth,
                this.lineWidth,
            );
        }
    }

    static isPosOn(pos) {
        return (
            pos.x < 8 && pos.x >= 0
            && pos.y < 8 && pos.y >= 0
        );
    }

    isFieldAllowed(gameobject, board_pos) {
        return this.board[board_pos.x][board_pos.y] === null
            || this.board[board_pos.x][board_pos.y].constructor !== gameobject.constructor;
    }
    isLimitAllowed(gameobject) {
        return (this.card.constructor === Virus && this.viruses().length < 4)
            || (this.card.constructor === Link && this.links().length < 4);
    }
    isPosAllowed(board_pos) {
        let allowed_poses = [
            [0, 7],
            [1, 7],
            [2, 7],
            [3, 6],
            [4, 6],
            [5, 7],
            [6, 7],
            [7, 7],
        ];
        return allowed_poses.some(e => e[0] === board_pos.x && e[1] === board_pos.y);
    }


    add(gameobject, pos=null) {
        if (pos === null)
            pos = gameobject.pos;

        let board_pos = this.toBoard(pos);


        if (
            this.isFieldAllowed(gameobject, board_pos)
                && this.isLimitAllowed(gameobject)
                && this.isPosAllowed(board_pos)
        ) {
            this.board[board_pos.x][board_pos.y] = gameobject;
            gameobject.visible = true;
        } else {
            this.board[board_pos.x][board_pos.y] = null;
        }

        gameobject.pos = this.toGlobal(board_pos);
    }

    toGlobal(pos) {
        return new Vec2(
            (pos.x) * (this.size.x/8) + this.pos.x,
            (pos.y) * (this.size.y/8) + this.pos.y,
        );
    }

    toBoard(pos) {
        let newX = Math.floor((pos.x - this.pos.x)/(this.size.x/8));
        let newY = Math.floor((pos.y - this.pos.y)/(this.size.y/8));
        return new Vec2(newX, newY);
    }
}
