import csv
import os

def read_trip_info(file_path_list):
    trade_info_list = []
    
    for file_path in file_path_list:
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    sequence_no_0 = row.get('sequence_no')
                    if sequence_no_0:
                        trade_info_list.append(sequence_no_0)
                    sequence_no_1 = row.get('sequenceNo')
                    if sequence_no_1:
                        trade_info_list.append(sequence_no_1)
        except FileNotFoundError:
            print(f"警告：文件未找到 {file_path}，已跳过")
        except Exception as e:
            print(f"处理文件 {file_path} 时发生错误：{str(e)}")
            
    
    trade_info_list = [element for element in list(set(trade_info_list)) if element]

    return trade_info_list

if __name__ == "__main__":

    print('Must have railwaytrip.csv and railway_psr.csv before using this script.')

    file_path_list = []

    # 获取当前脚本的目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # 构建上级目录的路径
    parent_directory = os.path.join(current_directory, '..')
    
    # 构建文件的完整路径
    file_path_list.append(os.path.join(parent_directory, 'railwaypsr.csv'))
    file_path_list.append(os.path.join(parent_directory, 'railwaytrip.csv'))
    file_path_list.append(os.path.join(parent_directory, 'railwayalternate.csv'))
    file_path_list.append(os.path.join(parent_directory, 'railwaymemtrade.csv'))
    file_path_list.append(os.path.join(parent_directory, 'railwaymemtradedetail.csv'))
    file_path_list.append(os.path.join(parent_directory, 'railwayinvoice.csv'))
    trade_info = read_trip_info(file_path_list)
    print(trade_info)
    print(len(trade_info))


'''
If you want to get railway trip detail,
use this script to get a list of trade id,
and use the js code shown below in the browser console.
The json data returned by the website
should be processed in the railwaytripdetail.py script.

const trade_info_list = [List that you just generated]

// 初始化一个空对象来存储所有返回的 JSON 数据
const allData = {};

// 创建一个数组来存储所有的 Promise
const promises = trade_info_list.map((info, index) => {
    const seqno = info[0];
    
    // 执行 fetch 请求并返回一个 Promise
    return fetch('https://kyfw.12306.cn/otn/orderdetail/queryOrderDetail', {
        method: 'POST',
        headers: {
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        },
        body: `sequence_no=${encodeURIComponent(seqno)}`
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
