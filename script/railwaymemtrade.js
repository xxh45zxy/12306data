// 创建一个全局变量来存储结果
window.fetchResult = null;

// 获取当前日期并计算一年前的日期
const today = new Date();
const oneYearAgo = new Date(today.getFullYear() - 1, today.getMonth(), today.getDate());
 
// 格式化为YYYYMMDD字符串（补零处理）
const year = oneYearAgo.getFullYear();
const month = String(oneYearAgo.getMonth() + 1).padStart(2, '0'); // 月份补零
const day = String(oneYearAgo.getDate()).padStart(2, '0');         // 日期补零
 
const startDate = `${year}${month}${day}`;

fetch('https://cx.12306.cn/tlcx/memberInfo/pointSimpleQuery', {
    method: 'POST',
    headers: {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"// 这是表单数据常用的内容类型
    },
    body: `queryType=0&queryStartDate=${startDate}&queryEndDate=99999999&pageIndex=0` // 将 URLSearchParams 对象转换为字符串并作为请求体发送
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