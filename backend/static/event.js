import { Vec2 } from './vec.js';


class Handlers {
    constructor() {
        this.handlers = {};
    }

    get(handler) {
        return this.handlers[handler];
    }
    set (handler, func) {
        this.handlers[handler] = func;
    }

    delete(handler) {
        delete this.handlers[handler];
    }

    trigger(data) {
        for (let [func_name, func] of Object.entries(this.handlers)) {
            func(data);
        }
    }
}



export function getMousePos(context, event) {
    return new Vec2(
        event.clientX - context.getBoundingClientRect().left,
        event.clientY - context.getBoundingClientRect().top,
    );
}


export class Events {
    static events = {};

    static handlers(event) {
        if (Events.events[event] === undefined) {
            Events.events[event] = new Handlers();
        }
        return Events.events[event];
    }

    static trigger(event, data=null) {
        if (event in Events.events)
            Events.events[event].trigger(data);
        else
            console.log('Skiping event ' + event + ' no handlers');
    }
}
