import csv
import os

def read_trade_info(file_path):
    trade_info_list = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                trade_type = row.get('trade_type')
                trade_id = row.get('trade_id')
                if trade_type and trade_id:
                    trade_info_list.append([trade_type, trade_id])
    except FileNotFoundError:
        print(f"警告：文件未找到 {file_path}，已跳过")
    except Exception as e:
        print(f"处理文件 {file_path} 时发生错误：{str(e)}")
    
    return trade_info_list

if __name__ == "__main__":

    print('Must have railwaymemtrade.csv before using this script.')

    # 获取当前脚本的目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # 构建上级目录的路径
    parent_directory = os.path.join(current_directory, '..')
    
    # 构建文件的完整路径
    file_path = os.path.join(parent_directory, 'railwaymemtrade.csv')
    trade_info = read_trade_info(file_path)
    print(trade_info)


'''
If you want to get railway member trade detail,
use this script to get a list of trade id,
and use the js code shown below in the browser console.
The json data returned by the website
should be processed in the railwaymemtradedetail.py script.

const trade_info_list = [List that you just generated]

// 初始化一个空对象来存储所有返回的 JSON 数据
const allData = {};

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
        console.log(`Fetched data for index ${index}:`, data);
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
        console.log('All data:', JSON.stringify(allData, null, 2));
    });

'''
