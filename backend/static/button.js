import { Vec2 } from './vec.js';
import { Events, getMousePos } from './event.js';
import { BaseGameObject, Virus, Link } from './GameObject.js';

export class Text extends BaseGameObject {
    constructor(text, pos, color='#000', style='30px Arial', offset=null) {
        super();
        this.text = text;
        this.pos = pos;
        this.color = color;
        this.style = style;
        if (offset) {
            this.offset = offset;
        } else {
            this.offset = new Vec2(0, 0);
        }
    }

    draw(context) {
        context.fillStyle = '#000';
        context.font = '30px Arial';
        context.fillText(
            this.text,
            this.pos.x + this.offset.x,
            this.pos.y + this.offset.y,
        );
    }
}

export class Button extends BaseGameObject {
    constructor(pos, size, text='button') {
        super();
        this.handle_click = true;
        this.pos = pos;
        this.size = size;
        this.text = new Text(text, pos.copy());
        this.text.offset = new Vec2(10, 35);
        this.text.z = this.z + 1;
    }

    child_draw() {
        return [this.text];
    }

    draw(context) {
        context.beginPath();
        context.rect(this.pos.x, this.pos.y, this.size.x, this.size.y);
        context.stroke();
    }
}

class CardSelector extends Button {
    constructor(pos, size, text) {
        super(pos, size, text);
        this.selected = false;
        this.active_color = '#cce';
        let self = this;
        Events.handlers('cardselector.unselect').set(self._name, function () {
            self.selected = false;
        });

        Events.handlers('game.start').set('card_clear', function () {
            Events.handlers('cardselector.unselect').delete(self._name);
        });
    }

    clicked (mouse_pos) {
        let self = this;
        Events.trigger('cardselector.unselect');
        this.selected = true;
        Events.trigger('board.setcard', this.cursor.copy());
    }

    draw(context) {
        if (this.selected) {
            context.fillStyle = this.active_color;
            context.fillRect(
                this.pos.x,
                this.pos.y,
                this.size.x,
                this.size.y,
            );
        }
        context.beginPath();
        context.rect(this.pos.x, this.pos.y, this.size.x, this.size.y);
        context.stroke();
    }
}

export class VirusButton extends CardSelector {
    constructor(pos, size) {
        super(pos, size, 'Virus');
        this.cursor = new Virus();
        this.active_color = '#e4e';
    }
}

export class LinkButton extends CardSelector {
    constructor(pos, size) {
        super(pos, size, 'Link');
        this.cursor = new Link();
        this.active_color = '#44e';
    }
}

export class StartButton extends Button {
    constructor(pos, size) {
        super(pos, size, 'Start');
        this.text.offset.x = 65;
        this.text.offset.y = 45;
    }

    clicked() {
        Events.trigger('board.check_start');
    }

    draw(context) {
        context.fillStyle = '#cec';
        context.fillRect(
            this.pos.x,
            this.pos.y,
            this.size.x,
            this.size.y,
        );
        context.beginPath();
        context.rect(this.pos.x, this.pos.y, this.size.x, this.size.y);
        context.stroke();
    }
}
