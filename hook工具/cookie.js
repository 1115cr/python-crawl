(function () {
    var temp = null;
    Object.defineProperty(document, 'cookie', {
        get: function () {
            console.log('获取了cookie:', temp);
            return temp;
        },
        set: function (val) {
            temp = val;
            console.log('cookie:', val);
        }
    })
})()