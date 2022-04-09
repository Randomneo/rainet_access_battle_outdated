export class Scene {
    static gameObjects = [];
    static namedObjects = {};

    static draw(context) {
        let to_draw = [...Scene.gameObjects];
        to_draw.push(...Object.values(Scene.namedObjects));
        to_draw.push(
            ...to_draw
                .map(x => x.child_draw())
                .reduce((acc, val) => acc.concat(val), [])
                .filter(x => x)
        );
        to_draw = to_draw.filter(x => x.visible);
        to_draw.sort(x => x.z);
        to_draw.forEach(function(gameObject) {
            gameObject.draw(context);
        });
    }
}
