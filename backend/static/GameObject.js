import Camera from './camera.js';
import { Events, getMousePos } from './event.js';
import { Vec2 } from './vec.js';


export class BaseGameObject {
    constructor () {
        this.visible = true;
        this.object_id = Math.floor(Math.random() * 100000);
        this._name = 'base_game_object_' + this.object_id;
        this.canvasClick();
        this.z = 0;
    }

    draw(context) {
        console.log('implement draw');
    }

    clicked(mouse_pos) {
        console.log('implement clicked');
    }

    child_draw() {}

    canvasClick() {
        let self = this;
        Events.handlers('canvas.click').set(
            self._name,
            function (data) {
                if (!self.handle_click)
                    return;
                let mouse_pos = getMousePos(data.this, data.event);
                if (
                    mouse_pos.x > self.pos.x
                    && mouse_pos.x < self.pos.x + self.size.x
                    && mouse_pos.y > self.pos.y
                    && mouse_pos.y < self.pos.y + self.size.y
                ) {
                    self.clicked(mouse_pos);
                }
            },
        );
    }
}


export class GameObject extends BaseGameObject {
    constructor(pos, size, fillStyle) {
        super();
        this.pos = pos;
        this.size = size;
        this.fillStyle = fillStyle;
    }

    draw(context) {
        context.fillStyle = this.fillStyle;
        context.fillRect(
            this.pos.x,
            this.pos.y,
            this.pos.x + this.size.x,
            this.pos.y + this.size.y,
        );
    }
}


export class Card extends BaseGameObject {
    constructor() {
        super();
        this.pos = new Vec2(0, 0);
        this.size = new Vec2(50, 50);
        this.visible = false;
        this.z = -10;
    }

    mousePosToBoard(pos) {
        return new Vec2(
            Math.min(
                Math.max(
                    Math.floor((pos.x - Camera.offset)/100),
                    0,
                ),
                7,
            )*100 + Camera.offset,
            Math.min(
                Math.max(
                    Math.floor((pos.y - Camera.offset)/100),
                    0,
                ),
                7,
            )*100 + Camera.offset,
        );
    }

    draw(context) {
        context.fillStyle = this.fillStyle;
        context.fillRect(
            this.pos.x,
            this.pos.y,
            this.size.x,
            this.size.y,
        );
    }

    copy() {
        return Object.create(
            Object.getPrototypeOf(this),
            Object.getOwnPropertyDescriptors(this)
        );
    }
}


export class Virus extends Card {
    constructor() {
        super();
        this.fillStyle = '#f4f';
    }
}


export class Link extends Card {
    constructor() {
        super();
        this.fillStyle = '#44f';
    }
}
