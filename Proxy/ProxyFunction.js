function proxy_test(obj) {

    return new Proxy(obj, {
        get: function (target, property, receiver) {
            //debugger;
            console.log("get: ", obj, property,target[property]);
            return target[property];
        },
        set: function (target, property, value) {
            //debugger;
            console.log("set: ", obj, property);
            return Reflect.set(...arguments);
        },
    })
}

window = proxy_test(window);
document = proxy_test(document);
navigator = proxy_test(navigator);
screen = proxy_test(screen);
history = proxy_test(history);
location = proxy_test(location);