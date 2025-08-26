(function () {
    console.log('SHA1 钩子已启动')
    var _SHA = CryptoJS.SHA1;
    CryptoJS.SHA1 = function (data) {
        console.log('SHA1 捕获到明文数据:', data)
        console.log('SHA1 捕获到密文数据:', _SHA(data))
        debugger;
        // 使用原始eval执行代码
        return _SHA(data);
    };
})();