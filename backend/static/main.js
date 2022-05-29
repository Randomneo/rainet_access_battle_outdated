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
} from './GameObject.js';
import { mouse } from './mouse.js';
import { GameOrchestrator } from './gameorchestrator.js';
import { GameStack } from './gamestack.js';


let startButtons = {
    virus: {
        pos: [500, 200],
        size: [100, 50],
        type: VirusButton,
    },
    link: {
        pos: [700, 200],
        size: [100, 50],
        type: LinkButton,
    },
    start: {
        pos: [550, 500],
        size: [200, 70],
        type: StartButton,
    },
};


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
        this.gameorchestrator = new GameOrchestrator(board);

        Scene.gameObjects.push(board);
        Scene.gameObjects.push(mouse);
    }

    bindSocket(socket) {
        if (socket.readyState !== 1)
            console.log('wrong socket status!');
        this.gameorchestrator.bindSocket(socket);
    }

    loadStartButtons() {
        for (const i in startButtons) {
            let button = startButtons[i];
            Scene.namedObjects[i+'_button'] = new button.type(
                new Vec2(button.pos[0], button.pos[1]),
                new Vec2(button.size[0], button.size[1]),
            );
        }
    }

    clearStartButtons() {
        for (const i in startButtons) {
            delete Scene.namedObjects[i+'_button'];
        }
    }

    planStage() {
        this.loadStartButtons();

        OwnExit.create_default_at(OwnExit, [new Vec2(3, 7), new Vec2(4, 7)]);
        EnemyExit.create_default_at(EnemyExit, [new Vec2(3, 0), new Vec2(4, 0)]);

    }

    cleanPlanStage() {
        this.clearStartButtons();
    }

    gameStage() {
        this.cleanPlanStage();
        let gamestack = new GameStack();
        Scene.gameObjects.push(gamestack);
    }

    draw() {
        this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
        Scene.draw(this.context);
    }

    start() {
        let self = this;
        Events.handlers('game.start').set('start', function () { self.gameStage(); });

        this.canvas.onmousemove = function (event) {
            Events.trigger('canvas.mousemove', {'this': this, 'event': event});
        };
        this.canvas.onmouseout = function (event) {
            Events.trigger('canvas.mouseout', {'this': this, 'event': event});
        };
        this.canvas.onclick = function (event) {
            Events.trigger('canvas.click', {'this': this, 'event': event});
        };

        setInterval(function () { self.draw(); }, 10);
    }
}


export default Game;
