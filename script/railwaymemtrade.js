// 创建一个全局变量来存储结果
window.fetchResult = null;

fetch('https://cx.12306.cn/tlcx/memberInfo/pointSimpleQuery', {
    method: 'POST',
    headers: {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"// 这是表单数据常用的内容类型
    },
    body: "queryType=0&queryStartDate=10000000&queryEndDate=99999999&pageIndex=0" // 将 URLSearchParams 对象转换为字符串并作为请求体发送
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