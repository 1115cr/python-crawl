(function () {
    console.log('MD5 钩子已启动')
    var _MD5 = window.CryptoJS.MD5;
    window.CryptoJS.MD5l = function (data) {
        console.log('MD5 捕获到数据:', data)
        debugger;
        // 使用原始eval执行代码
        return _MD5(data);
    };
})();