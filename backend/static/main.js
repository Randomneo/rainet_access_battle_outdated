import { Vec2 } from './vec.js';
import { Board } from './board.js';
import { Events } from './event.js';
import { Scene } from './scene.js';
import {
    VirusButton,
    LinkButton,
    StartButton,
} from './button.js';
import {
    OwnExit,
    EnemyExit,
    Enemy,
} from './GameObject.js';



class Game {
    constructor() {
        let self = this;
        this.mapSize = new Vec2(400, 400);
        this.canvas = document.querySelector('#gamecanvas');
        this.context = this.canvas.getContext('2d');
        this.canvas.width = 900;
        this.canvas.height = 600;

        // load level
        this.planStage();
        let board = new Board(new Vec2(20, 150), this.mapSize.copy());
        Scene.gameObjects.push(board);
        Events.handlers('game.start').set('start', function () { self.gameStage(); });

        this.canvas.onmousemove = function (event) {
            Events.trigger('canvas.mousemove', {'this': this, 'event': event});
        };
        this.canvas.onmouseout = function (event) {
            Events.trigger('canvas.mouseout');
        };
        this.canvas.onclick = function (event) {
            Events.trigger('canvas.click', {'this': this, 'event': event});
        };

        setInterval(function () { self.draw(); }, 10);
    }

    planStage() {
        Scene.namedObjects['virus_button'] = new VirusButton(new Vec2(500, 200), new Vec2(100, 50));
        Scene.namedObjects['link_button'] = new LinkButton(new Vec2(700, 200), new Vec2(100, 50));
        Scene.namedObjects['start_button'] = new StartButton(new Vec2(550, 500), new Vec2(200, 70));
        OwnExit.create_default_at(OwnExit, [new Vec2(3, 7), new Vec2(4, 7)]);
        EnemyExit.create_default_at(EnemyExit, [new Vec2(3, 0), new Vec2(4, 0)]);

        Events.handlers('board.start').set('spawn_enemies', function (board) {
            let enemy_poses = [
                [0, 0], [1, 0], [2, 0], [3, 1], [4, 1], [5, 0], [6, 0], [7, 0],
            ];
            for (let pos of enemy_poses) {
                pos = new Vec2(pos[0], pos[1]);
                let enemy = new Enemy();
                enemy.pos = board.toGlobal(pos);
                board.board[pos.x][pos.y] = enemy;
            }
        });
    }

    cleanPlanStage() {
        delete Scene.namedObjects['virus_button'];
        delete Scene.namedObjects['link_button'];
        delete Scene.namedObjects['start_button'];
    }

    gameStage() {
        this.cleanPlanStage();
    }

    draw() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        Scene.draw(this.context);
    }

    static start() {
        let game = new this();
    }
}


export default Game;
