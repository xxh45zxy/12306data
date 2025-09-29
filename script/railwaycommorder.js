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
            const query_type = info;
            
            // 执行 fetch 请求并返回一个 Promise
            return fetch('https://kyfw.12306.cn/otn/npQuery/queryFavorOrderMergeInfoNew', {
                method: 'POST',
                headers: {
                    "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
                },
                body: `query_type=${encodeURIComponent(query_type)}&page_index=0`
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