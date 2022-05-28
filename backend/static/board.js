import {
    BaseGameObject,
    Virus,
    Link,
    Enemy,
    Exit,
} from './GameObject.js';
import { Events, getMousePos } from './event.js';
import { Vec2 } from './vec.js';
import Camera from './camera.js';
import { Scene } from './scene.js';
import { mouse } from './mouse.js';




export class Board extends BaseGameObject {
    constructor(pos, size) {
        super();
        let self = this;
        this.pos = pos;
        this.lineWidth = 1;
        this.fillStyle = '#000';
        this.setsize(size);
        this.handle_click = true;


        this.board = [];
        for (let i = 0; i < 8; i++) {
            this.board.push([]);
            for (let j = 0; j < 8; j++) {
                this.board[i].push(null);
            }
        }
        // prepare stage events
        Events.handlers('board.setcard').set('set_card', function (card) {
            mouse.setCursor(card);
        });
        Events.handlers('canvas.mousemove').set('show_board_cursor', function (data) {
            Events.trigger('board.mousemove', {board: self, mouse_pos: getMousePos(data.this, data.event)});
        });
        Events.handlers('board.check_start').set('check_start', function () {self.checkBeforeStart();});
        Events.trigger('board.prepare', self);


        // Clear before game
        Events.handlers('game.start').set('board_before_start', function () {
            self.enemy_turn = false;
            Events.handlers('board.setcard').delete('set_card');
            Events.handlers('canvas.mousemove').delete('show_board_cursor');
            Events.handlers('board.start').delete('check_start');

            Events.handlers('canvas.mousemove').set('move_card', function (data) {
                if (!self.card)
                    return;
                self.card.pos = getMousePos(data.this, data.event);
                self.card.pos.x -= 25;
                self.card.pos.y -= 25;
            });
            self.canvasClick(function (arg) {self.in_game_clicked(arg);});
            Events.trigger('board.start', self);
        });
        Events.handlers('board.start').set('spawn_enemies', function () {
            let enemy_poses = [
                [0, 0], [1, 0], [2, 0], [3, 1], [4, 1], [5, 0], [6, 0], [7, 0],
            ];
            for (let pos of enemy_poses) {
                pos = new Vec2(pos[0], pos[1]);
                let enemy = new Enemy();
                enemy.pos = self.toGlobal(pos);
                self.board[pos.x][pos.y] = enemy;
            }
        });

    }

    checkBeforeStart() {
        if (this.viruses().length >= 4 && this.links().length >= 4) {
            Events.trigger('game.start');
        } else {
            console.log('can\'t start game');
        }
    }

    setsize(size) {
        this.size = size;
        this.rectSize = new Vec2(this.size.x/8, this.size.y/8);
    }

    in_game_clicked(mouse_pos) {
        let board_pos = this.toBoard(mouse_pos);
        if (!this.card) {
            if (
                this.enemy_turn
                    || !this.board[board_pos.x][board_pos.y]
                    || !this.board[board_pos.x][board_pos.y].movable
            )
                return;
            this.card = this.board[board_pos.x][board_pos.y];
            this.card.selectToMove(board_pos);
            this.board[this.card.board_pos.x][this.card.board_pos.y] = null;
        } else {
            if (!this.card.validMove(board_pos)) {
                return;
            }
            if (this.board[board_pos.x][board_pos.y]) {
                console.log('owerlapping skip');
                return;
            }
            if (!board_pos.eq(this.card.board_pos)) {
                console.log('player moved');
            }

            this.card.pos = this.toGlobal(board_pos);
            this.board[board_pos.x][board_pos.y] = this.card;
            this.card = null;
        }
    }

    clicked(mouse_pos) {
        if (!mouse.cursor) {
            return;
        }
        this.add(mouse.cursor.copy(), mouse_pos);
    }

    cards() {
        let cards = this.board.reduce((acc, val) => acc.concat(val), []).filter(x => x);
        return cards;
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
        for (let i = 0; i <= this.size.x; i += this.rectSize.x) {
            context.fillRect(
                Camera.getX(i + this.pos.x - this.lineWidth / 2),
                Camera.getY(this.pos.y - this.lineWidth / 2),
                this.lineWidth,
                this.size.y + this.lineWidth,
            );
        }
        for (let i = 0; i <= this.size.y; i += this.rectSize.y) {
            context.fillRect(
                Camera.getX(this.pos.x - this.lineWidth / 2),
                Camera.getY(i + this.pos.y - this.lineWidth / 2),
                this.size.x + this.lineWidth,
                this.lineWidth,
            );
        }
    }

    isFieldAllowed(gameobject, board_pos) {
        return this.board[board_pos.x][board_pos.y] === null
            || this.board[board_pos.x][board_pos.y].constructor !== gameobject.constructor;
    }
    isLimitAllowed(gameobject) {
        return (mouse.cursor.constructor === Virus && this.viruses().length < 4)
            || (mouse.cursor.constructor === Link && this.links().length < 4);
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

        if (this.board[board_pos.x][board_pos.y] instanceof Exit)
            return;
        if (
            this.isFieldAllowed(gameobject, board_pos)
                && this.isLimitAllowed()
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
