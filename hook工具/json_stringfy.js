(function () {
    var old_stringify = JSON.stringify;
    JSON.stringify = function (params) {
        if (params['password']) {
            console.log(params);
            debugger;
        } else {
            return old_stringify(params);
        }// 不改变原有的执行逻辑
    }
})();