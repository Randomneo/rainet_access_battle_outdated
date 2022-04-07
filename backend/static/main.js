import Camera from './camera.js';
import Vec2 from './vec.js';


let gameObjects = [];

class BaseGameObject {
    draw(context) {
        console.log('implement draw');
    }
}

class GameObject extends BaseGameObject {
    constructor(pos, size, fillStyle) {
        super();
        this.pos = pos;
        this.size = size;
        this.fillStyle = fillStyle;
    }

    draw(context) {
        context.fillStyle = this.fillStyle;
        context.fillRect(
            Camera.getPos(this.pos).x,
            Camera.getPos(this.pos).y,
            this.pos.x + this.size.x,
            this.pos.y + this.size.y,
        );
    }
}

class Board extends BaseGameObject {
    constructor(size, fillStyle) {
        super();
        this.lineWidth = 6;
        this.rectSize = new Vec2(100, 100);
        this.size = size;
        this.fillStyle = fillStyle;
    }
    draw(context) {
        context.fillStyle = this.fillStyle;
        for (let i = 0; i <= this.size.x; i+=this.rectSize.x) {
            context.fillRect(
                Camera.getX(i - this.lineWidth / 2),
                Camera.getY(- this.lineWidth / 2),
                this.lineWidth,
                this.size.y + this.lineWidth,
            );
        }
        for (let i = 0; i <= this.size.x; i+=this.rectSize.x) {
            context.fillRect(
                Camera.getX(- this.lineWidth / 2),
                Camera.getY(i - this.lineWidth / 2),
                this.size.x + this.lineWidth,
                this.lineWidth,
            );
        }
    }
}


function draw(context, gameObjects) {
    console.log(gameObjects);

    gameObjects.forEach(function(gameObject) {
        gameObject.draw(context);
    });
}


class Game {
    constructor() {
        this.mapSize = new Vec2(800, 800);
        this.canvas = document.querySelector('#gamecanvas');
        this.context = this.canvas.getContext('2d');
        this.canvas.width = this.mapSize.x + Camera.offset * 2;
        this.canvas.height = this.mapSize.y + Camera.offset * 2;

        // load level
        let gameObject = new GameObject(new Vec2(50, 50), new Vec2(50, 50), '#f00');
        let bord = new Board(this.mapSize, '#000');
        gameObjects.push(gameObject);
        gameObjects.push(bord);

        // first draw
        draw(this.context, gameObjects);
    }

    static start() {
        let game = new this();
    }
}


export default Game;
