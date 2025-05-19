// 获取当前日期的前一日
const today = new Date();
today.setDate(today.getDate() - 1);
const queryEndDate = today.toISOString().split('T')[0]; // 格式化为 YYYY-MM-DD

// 创建一个全局变量来存储结果和状态
window.fetchTemRes = [];
window.fetchComplete = false;
window.fetchResult = null;
let activeRequests = 0;

// 延迟函数（返回Promise）
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// 定义函数来递归获取所有页的数据
async function fetchAllPages(querywhere, pageIndex = 0) {
    activeRequests++;
    try {
        let body;
        if (querywhere === "G") {
            body = `query_where=${querywhere}&queryStartDate=0000-01-01&queryEndDate=9999-12-31&queryType=2&pageIndex=${pageIndex}`;
        } else if (querywhere === "H") {
            body = `query_where=${querywhere}&queryStartDate=0000-01-01&queryEndDate=${queryEndDate}&pageIndex=${pageIndex}`;
        }

        let success = false;
        let attempt = 0;
        let data = null;

        // 请求重试逻辑
        while (attempt < 3 && !success) {
            try {
                const response = await fetch('https://kyfw.12306.cn/otn/queryOrder/queryMyOrder', {
                    method: 'POST',
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
                    },
                    body: body
                });

                if (!response.ok) throw new Error(`HTTP错误! 状态码: ${response.status}`);
                data = await response.json();
                success = true;
            } catch (error) {
                attempt++;
                if (attempt >= 3) {
                    throw new Error(`请求失败，已达最大重试次数 (${error.message})`);
                }
                console.log(`请求失败，${3 - attempt}次重试机会剩余，2秒后重试...`);
                await delay(2000);
            }
        }

        // 处理成功响应
        if (data.httpstatus && data.data && data.data.OrderDTODataList) {
            const results = data;
            const total = data.data.order_total_number;

            window.fetchTemRes = window.fetchTemRes.concat(results);
            console.log(`[${querywhere}] 获取第${pageIndex + 1}页，当前总数: ${window.fetchTemRes.length}`);

            if (window.fetchTemRes.length < total) {
                // 生成随机延迟（0.1-1.5秒）
                const randomDelay = Math.floor(Math.random() * 1400) + 100;
                await delay(randomDelay);
                await fetchAllPages(querywhere, pageIndex + 1);
            } else {
                console.log(`[${querywhere}] 所有数据获取完成`);
            }
        } else {
            throw new Error('响应数据格式异常');
        }
    } catch (error) {
        console.error(`[${querywhere}] 第${pageIndex + 1}页获取失败:`, error.message);
    } finally {
        activeRequests--;
        checkFetchComplete();
    }
}

// 检查 fetch 请求是否都已完成
function checkFetchComplete() {
    if (activeRequests === 0) {
        window.fetchComplete = true;
        processFetchResult();
    }
}

// 处理 fetch 结果的函数
function processFetchResult() {
    window.fetchResult = window.fetchTemRes;
    console.log('最终结果',window.fetchResult);
}

fetchAllPages("G");
fetchAllPages("H");


/*
// 获取当前日期的前一日
const today = new Date();
today.setDate(today.getDate() - 1);
const queryEndDate = today.toISOString().split('T')[0]; // 格式化为 YYYY-MM-DD

// 创建一个全局变量来存储结果和状态
window.fetchTemRes = [];
window.fetchComplete = false;
window.fetchResult = null;
let activeRequests = 0; // 跟踪当前活动的请求数量

// 定义函数来递归获取所有页的数据
function fetchAllPages(querywhere,pageIndex = 0) {
    activeRequests++;
    let body;
    if (querywhere === "G"){
        body = `query_where=${querywhere}&queryStartDate=0000-01-01&queryEndDate=9999-12-31&queryType=2&pageIndex=${pageIndex}` // 动态设置 pageIndex
    }
    else if (querywhere === "H"){
        body = `query_where=${querywhere}&queryStartDate=0000-01-01&queryEndDate=${queryEndDate}&pageIndex=${pageIndex}` // 动态设置 pageIndex
    }

    fetch('https://kyfw.12306.cn/otn/queryOrder/queryMyOrder', {
        method: 'POST',
        headers: {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        },
        body: body
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json(); // 解析响应体为 JSON
    })
    .then(data => {
        if (data.httpstatus && data.data && data.data.OrderDTODataList) {
            const results = data;
            const total = data.data.order_total_number;

            // 将当前页的结果添加到全局结果数组中
            window.fetchTemRes = window.fetchTemRes.concat(results);

            console.log(`Fetched page ${pageIndex}, total results so far: ${window.fetchTemRes.length}`);
            // 如果当前页的结果数量小于总数，继续请求下一页
            if (window.fetchTemRes.length < total) {
                fetchAllPages(querywhere,pageIndex + 1); // 递归调用，获取下一页
            } else {
                console.log('All results fetched.');
            }
        } else {
            console.error('Unexpected response structure:', data);
        }
    })
    .catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
    })
    .finally(() => {
        activeRequests--; // 请求完成，减少活动请求计数
        checkFetchComplete(); // 每次请求完成后都检查是否所有请求完成
    });
};

// 检查 fetch 请求是否都已完成
function checkFetchComplete() {
    if (activeRequests === 0) {
        window.fetchComplete = true;
        processFetchResult();
    }
}

// 处理 fetch 结果的函数
function processFetchResult() {
    // 将 fetchTemRes 数组转换为 JSON 字符串并赋值给 fetchResult
    window.fetchResult = window.fetchTemRes;
    console.log(window.fetchResult);
    // 在这里进行后续操作
}

fetchAllPages("G");
fetchAllPages("H");
*/


/*
// 创建一个全局变量来存储结果
window.fetchResult = null;

fetch('https://kyfw.12306.cn/otn/queryOrder/queryMyOrder', {
    method: 'POST',
    headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8" // 这是表单数据常用的内容类型
    },
    body: `query_where=H&queryStartDate=2000-01-01&queryEndDate=${queryEndDate}` // 将 URLSearchParams 对象转换为字符串并作为请求体发送
})
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json(); // 解析响应体为 JSON
})
.then(data => {
    window.fetchResult = data; // 处理解析后的 JSON 数据
})
.catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
});
*/
