import { Vec2 } from './vec.js';
import { Board } from './board.js';
import { Events } from './event.js';
import { Scene } from './scene.js';
import {
    VirusButton,
    LinkButton,
    StartButton,
} from './button.js';



class Game {
    constructor() {
        let self = this;
        this.mapSize = new Vec2(400, 400);
        this.canvas = document.querySelector('#gamecanvas');
        this.context = this.canvas.getContext('2d');
        this.canvas.width = 900;
        this.canvas.height = 600;

        // load level
        let board = new Board(new Vec2(20, 150), this.mapSize.copy());
        Scene.gameObjects.push(board);
        this.planStage();
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
