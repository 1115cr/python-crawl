(function () {
    console.log('AES 钩子已启动')
    var _aes = window.CryptoJs.AES.encrypt();
    window.CryptoJS.AES.encrypt = function (data, key, iv) {
        console.log('AES 捕获到明文数据:', data)
        console.log('AES 捕获到key数据:', key)
        console.log('AES 捕获到iv:', iv)
        debugger;
        // 使用原始eval执行代码
        return _aes(data, key, iv);
    };
})();