import { BaseGameObject, Virus, Link, Enemy } from './GameObject.js';
import { Vec2 } from './vec.js';
import { Events } from './event.js';

export class GameStack extends BaseGameObject {
    constructor() {
        super();
        let self = this;
        this.pos = new Vec2(500, 350);
        this.size = new Vec2(200, 200);
        this.boardStyle = '#000';
        this.handle_click = false;

        this.card_size = 35;
        this.margin = 10;

        this.user_stack = {
            virus: 0,
            link: 0,
        };
        // 'card_type' or { type: 'virus/link/unknown'}
        this.enemy_stack = [
        ];
        Events.handlers('stack.add.user').set('add_user', (type) => { self.user_stack[type]+=1; console.log(self); });
        Events.handlers('stack.add.enemy').set('add_enemy', (type) => { self.enemy_stack.push(type); console.log(self); });
    }

    draw(context) {
        context.strokeStyle = this.boardStyle;
        context.strokeRect(
            this.pos.x,
            this.pos.y,
            this.size.x,
            this.size.y,
        );
        context.beginPath();
        context.moveTo(
            this.pos.x,
            this.pos.y + this.size.y/2,
        );
        context.lineTo(
            this.pos.x + this.size.x,
            this.pos.y + this.size.y/2,
        );
        context.stroke();
        context.beginPath();
        context.moveTo(
            this.pos.x + this.size.x/2,
            this.pos.y + this.size.y/2,
        );
        context.lineTo(
            this.pos.x + this.size.x/2,
            this.pos.y + this.size.y,
        );
        context.stroke();

        this.draw_user_stack(context);
        this.draw_enemy_stack(context);
    }

    draw_user_stack(context) {

        let start_pos = new Vec2(
            this.pos.x + this.margin,
            this.pos.y + this.size.y/2 + this.margin,
        );
        for (let i=0; i<this.user_stack.virus; i++) {
            context.fillStyle = Virus.fillStyle;
            context.fillRect(
                start_pos.x + (i % 2 * (this.card_size + this.margin)),
                start_pos.y + (Math.floor(i/2) * (this.card_size + this.margin)),
                this.card_size,
                this.card_size,
            );
        }

        start_pos = new Vec2(
            this.pos.x + this.size.x/2 + this.margin,
            this.pos.y + this.size.y/2 + this.margin,
        );
        for (let i=0; i<this.user_stack.link; i++) {
            context.fillStyle = Link.fillStyle;
            context.fillRect(
                start_pos.x + (i % 2 * (this.card_size + this.margin)),
                start_pos.y + (Math.floor(i/2) * (this.card_size + this.margin)),
                this.card_size,
                this.card_size,
            );
        }
    }

    draw_enemy_stack(context) {
        let start_pos = new Vec2(
            this.pos.x + this.margin,
            this.pos.y + this.margin,
        );
        for (let [i, card] of this.enemy_stack.entries()) {
            switch (card) {
            case 'link': context.fillStyle = Link.fillStyle; break;
            case 'virus': context.fillStyle = Virus.fillStyle; break;
            default: context.fillStyle = Enemy.fillStyle; break;
            }

            context.fillRect(
                start_pos.x + (i % 4 * (this.card_size + this.margin)),
                start_pos.y + (Math.floor(i/4) * (this.card_size + this.margin)),
                this.card_size,
                this.card_size,
            );

        }
    }
}
