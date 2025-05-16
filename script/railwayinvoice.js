// 创建一个全局变量来存储结果和状态
window.fetchTemRes = [];
window.fetchComplete = false;
window.fetchResult = null;

// 第一个 fetch 请求
fetch('https://kyfw.12306.cn/otn/eInvoice/queryPsr', {
    method: 'POST',
    headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    },
    body: "from_date=10000000&end_date=99999999&pageIndex=0&ticket_type=&type=1"
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
fetch('https://kyfw.12306.cn/otn/eInvoice/queryPsr', {
    method: 'POST',
    headers: {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    },
    body: "from_date=10000000&end_date=99999999&pageIndex=0&ticket_type=&type=2"
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