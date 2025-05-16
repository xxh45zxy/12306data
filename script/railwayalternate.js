// 创建一个全局变量来存储结果和状态
window.fetchTemRes = [];
window.fetchComplete = false;
window.fetchResult = null;
let activeRequests = 0; // 跟踪当前活动的请求数量

// 定义函数来递归获取所有页的数据
function fetchAllPages(queryurl,pageno = 0) {
    activeRequests++;

    fetch(queryurl, {
        method: 'POST',
        headers: {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        },
        body: `query_start_date=0000-00-00&query_end_date=9999-99-99&page_no=${pageno}`
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json(); // 解析响应体为 JSON
    })
    .then(data => {
        if (data.httpstatus && data.data && data.data.list && data.data.list[0].total_page) {
            const results = data;
            const total = data.data.list[0].total_page;

            // 将当前页的结果添加到全局结果数组中
            window.fetchTemRes = window.fetchTemRes.concat(results);

            console.log(`Fetched page ${pageno}, total results so far: ${window.fetchTemRes.length}`);
            // 如果当前页数小于总页数，继续请求下一页
            if (pageno + 1 < total) {
                fetchAllPages(queryurl,pageno + 1); // 递归调用，获取下一页
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

fetchAllPages("https://kyfw.12306.cn/otn/afterNateOrder/queryUnHonourHOrder");
fetchAllPages("https://kyfw.12306.cn/otn/afterNateOrder/queryProcessedHOrder");

/*
// 第一个 fetch 请求
fetch('https://kyfw.12306.cn/otn/afterNateOrder/queryUnHonourHOrder', {
    method: 'POST',
    headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    },
    body: "query_start_date=0000-00-00&query_end_date=9999-99-99"
})
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
})
.then(data => {
    window.fetchTemRes.push(data);
    checkFetchComplete();
})
.catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
    checkFetchComplete();
});

// 第二个 fetch 请求
fetch('https://kyfw.12306.cn/otn/afterNateOrder/queryProcessedHOrder', {
    method: 'POST',
    headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    },
    body: "query_start_date=0000-00-00&query_end_date=9999-99-99"
})
.then(response => {
    if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
    }
    return response.json();
})
.then(data => {
    window.fetchTemRes.push(data);
    checkFetchComplete();
})
.catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
    checkFetchComplete();
});

// 检查两个 fetch 请求是否都已完成
function checkFetchComplete() {
    if (window.fetchTemRes.length === 2) {
        window.fetchComplete = true;
        processFetchResults();
    }
}

// 处理 fetch 结果的函数
function processFetchResults() {
    // 将 fetchTemRes 数组转换为 JSON 字符串并赋值给 fetchResult
    window.fetchResult = window.fetchTemRes;
    console.log( window.fetchResult);
    // 在这里进行后续操作
}
*/