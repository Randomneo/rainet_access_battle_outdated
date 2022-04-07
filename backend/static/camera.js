import Vec2 from './vec.js';

class Camera {
    static offset = 4;

    static getPos(pos) {
        return new Vec2(pos.x + this.offset, pos.y + this.offset);
    }
    static getX(x) {
        return x + this.offset;
    }
    static getY(y) {
        return y + this.offset;
    }
}


export default Camera;
