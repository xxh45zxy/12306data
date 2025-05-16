// 初始化一个空对象来存储所有返回的 JSON 数据
const allData = {};

// 创建一个全局变量来存储结果
window.fetchResult = null;

// 定义一个函数来接收传入的 JSON 字符串
function init(jsonString) {
    try {
        // 将 JSON 字符串解析为 JavaScript 对象或数组
        const trade_info_list = jsonString[0];
        // 创建一个数组来存储所有的 Promise
        const promises = trade_info_list.map((info, index) => {
            const [queryType, tradeId] = info;
            
            // 执行 fetch 请求并返回一个 Promise
            return fetch('https://cx.12306.cn/tlcx/memberInfo/PointDetailQuery', {
                method: 'POST',
                headers: {
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
                },
                body: `queryType=${encodeURIComponent(queryType)}&trade_id=${encodeURIComponent(tradeId)}`
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(data => {
                // 将返回的 JSON 数据存储到 allData 对象中
                allData[index] = data;
                return data; // 确保 Promise 解析为 data
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
                return null; // 在错误情况下返回一个 null，避免 Promise 被拒绝
            });
        });

        // 使用 Promise.all 等待所有请求完成
        Promise.all(promises)
            .then(() => {
                window.fetchResult = JSON.stringify(allData, null, 2);
            });
    } catch (error) {
        console.error("Error parsing JSON:", error);
    }
}

/*
用于app remote webview debug console
// 初始化一个空对象来存储所有返回的 JSON 数据
const allData = {};

// 创建一个全局变量来存储结果
window.fetchResult = null;

// 封装 AlipayJSBridge.call 为一个返回 Promise 的函数
function callAlipayJSBridge(operationType, requestData) {
    return new Promise((resolve, reject) => {
        AlipayJSBridge.call(
            'rpcWithBaseDTO',
            {
                "headers": {},
                "httpGet": false,
                "signType": -1,
                "requestData": requestData,
                "operationType": operationType
            },
            function(result) {
                if (result) {
                    resolve(result);
                } else {
                    reject(new Error('AlipayJSBridge call failed: ' + (result ? JSON.stringify(result) : 'Unknown error')));
                }
            }
        );
    });
}

// 定义一个函数来接收传入的 JSON 字符串
function init(jsonString) {
    try {
        // 传入的是已经解析的数组
        const trade_info_list = jsonString;
        // 如果 jsonString 已经是数组，直接使用 trade_info_list = jsonString;

        // 检查 trade_info_list 是否为数组
        if (!Array.isArray(trade_info_list)) {
            console.error("Input data is not an array");
            return;
        }

        // 创建一个数组来存储所有的 Promise
        const promises = trade_info_list.map((info, index) => {
            const [queryType, tradeId] = info;

            // 使用封装后的函数执行 AlipayJSBridge 请求
            return callAlipayJSBridge(
                'com.cars.otsmobile.memberInfo.pointDetailQuery',
                [{ "_requestBody": { "trade_id": tradeId, "query_type": queryType } }]
            )
            .then(data => {
                // 将返回的 JSON 数据存储到 allData 对象中
                allData[index] = data;
                return data; // 确保 Promise 解析为 data
            })
            .catch(error => {
                console.error('There has been a problem with your AlipayJSBridge operation:', error);
                return null; // 在错误情况下返回一个 null，避免 Promise 被拒绝
            });
        });

        // 使用 Promise.all 等待所有请求完成
        Promise.all(promises)
            .then(() => {
                window.fetchResult = allData;
                console.log("All requests completed. Data stored in window.fetchResult.");
            });
    } catch (error) {
        console.error("Error parsing JSON:", error);
    }
}
*/