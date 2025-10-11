// 创建一个全局变量来存储结果和状态
window.fetchTemRes = [];
window.fetchComplete = false;
window.fetchResult = null;
window.nowtotal = 0;
let activeRequests = 0; // 跟踪当前活动的请求数量

// 定义函数来递归获取所有页的数据
function fetchAllPages(pageIndex = 1) {
    activeRequests++;
    fetch('https://kyfw.12306.cn/otn/psr/query', {
        method: 'POST',
        headers: {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        },
        body: `from_date=00000000&end_date=99999999&pageIndex=${pageIndex}` // 动态设置 pageIndex
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json(); // 解析响应体为 JSON
    })
    .then(data => {
        if (data.httpstatus && data.data && data.data.psr) {
            const results = data;
            total = data.data.psr.total;

            // 将当前页的结果添加到结果数组中
            window.fetchTemRes = window.fetchTemRes.concat(results);

            window.nowtotal += data.data.psr.results.length
            console.log(`Fetched page ${pageIndex}, total results so far: ${window.nowtotal}`);
            // 如果当前页的结果数量小于总数，继续请求下一页
            if (window.nowtotal < total) {
                fetchAllPages(pageIndex + 1); // 递归调用，获取下一页
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

fetchAllPages();

/*
fetch('https://kyfw.12306.cn/otn/psr/query', {
    method: 'POST',
    headers: {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"// 这是表单数据常用的内容类型
    },
    body: "from_date=00000000&end_date=99999999&pageIndex=1" // 将 URLSearchParams 对象转换为字符串并作为请求体发送
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