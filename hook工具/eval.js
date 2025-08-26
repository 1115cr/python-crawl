(function () {
    var old_eval = window.eval;
    window.eval = function (params) {
        if (typeof params === 'string' && params.indexOf('X-Apikey') !== -1) {
            console.log('eval 捕获到包含 x-apikey 的代码:', params);
            debugger;
        }
        // 使用原始eval执行代码
        return old_eval.apply(this, arguments);
    };
})();