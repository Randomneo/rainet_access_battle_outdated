export class Vec2 {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
    copy() {
        return new Vec2(this.x, this.y);
    }

    eq(other) {
        return this.x === other.x && this.y === other.y;
    }

    inRect(x1, y1, x2, y2) {
        return this.x > x1
            && this.x < x2
            && this.y > y1
            && this.y < y2;
    }
}

export default Vec2;
