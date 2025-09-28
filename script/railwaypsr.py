import json  
import pandas as pd
from general_func import *


def railwaypsrdata(file_name,check_id,sort_id,input_type,*input_json_data):

    existing_data = read_existing_data(file_name)

    # 不断从用户那里获取JSON输入，直到用户直接回车  
    all_new_data = pd.DataFrame()  # 用于存储所有新输入的数据

    count_data = 0
    
    while True:

        count_data += 1
        if count_data>1 and input_type == 0:
            break

        if input_type == 1:
            
            input_json = manual_input()
            
            if not input_json.strip():  # 如果用户输入的是空字符串或只有空格  
                break  
 
        try:  
            # 尝试解析JSON数据
            if input_type == 1:
                data_s = [json.loads(input_json)]
            else:
                data_s = input_json_data[0]
              
            # 初始化一个空列表来存储转换后的数据行  
            rows = []
            # print("o1")
              
            # 遍历orderList中的每个项目
            for data in data_s:

                for order in data['data']['psr']['results']:
                    
                    order_new = {}
                    
                    for key, value in order.items():

                        if value is None:
                            order_new[key] = ""
                        elif isinstance(value, list):
                            if value == []:
                                order_new[f"{key}_1"] = ""

                            # 如果值是列表，则拆分列表并添加新的键值对
                            else:
                                for i, item in enumerate(value, start=1):
                                    if item is None:
                                        item = ""
                                    new_key = f"{key}_{i}"  
                                    order_new[new_key] = str(item)

                                if key == "orderinfo" and len(value) == 2:
                                    order_new["orderinfo_3"] = order_new["orderinfo_2"]
                                    order_new["orderinfo_2"] = ""
                        else:  
                            # 如果值不是列表，则直接添加原始的键值对  
                            order_new[key] = str(value)
                                    
                    rows.append(order_new)  

            # print("o2")  
            # 将行列表转换为DataFrame  
            df_new = pd.DataFrame(rows)  
            all_new_data = pd.concat([all_new_data, df_new], ignore_index=True)
            # print("o3")
    
        except json.JSONDecodeError:  
            print("输入的JSON数据格式错误，请重新输入。")  

    save_csv(file_name,check_id,sort_id,existing_data,all_new_data,1,'last')


if __name__ == '__main__':
    
    file_name_1 = "railwaypsr.csv"
    check_id_1 = "ext_ticket_no"
    sort_id_1 = "local_start_time"

    railwaymemtradedata(file_name_1,check_id_1,sort_id_1,1)

    print("已完成。")

'''
Use the js code shown below in the browser console.

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
    console.log(data); // 处理解析后的 JSON 数据
})
.catch(error => {
    console.error('There has been a problem with your fetch operation:', error);
});

'''

