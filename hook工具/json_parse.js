(function () {
    var old_parse = JSON.parse;
    JSON.parse = function (params) {
        if (params['password']) {
            console.log(params);
            debugger;
        } else {
            return old_parse(params);
        }// 不改变原有的执行逻辑
    }
})();

