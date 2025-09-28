import json  
import pandas as pd
from general_func import *


def railwaycommorderdata(file_name,check_id,sort_id,input_type,*input_json_data):

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
                data = json.loads(input_json)
            else:
                data = input_json_data[0]
              
            # 初始化一个空列表来存储转换后的数据行  
            rows = []
            # print("o1")
            
            # 遍历orderList中的每个项目
            for order in data["results"]:
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
                                new_key = f"{key}_{i}"  
                                if item is None:
                                    item = ""
                                elif isinstance(item, dict):
                                    for key_t, value_t in item.items():
                                        key_ts = new_key + "_" + key_t
                                        if value_t is None:
                                            order_new[key_ts] = ""
                                        else:
                                            order_new[key_ts] = str(value_t)
                                else:
                                    order_new[new_key] = str(item)

                    else:  
                        # 如果值不是列表，则直接添加原始的键值对  
                        order_new[key] = str(value)
                                
                rows.append(order_new)  

            # print("o2")  
            # 将行列表转换为DataFrame  
            df_new = pd.DataFrame(rows)  
            all_new_data = pd.concat([all_new_data, df_new], ignore_index=True)
            # print("o3")'''

      
        except json.JSONDecodeError:  
            print("输入的JSON数据格式错误，请重新输入。")

    save_csv(file_name,check_id,sort_id,existing_data,all_new_data,1,'last')


if __name__ == '__main__':
    
    file_name_1 = get_file_path("railwaybaggage.csv")
    check_id_1 = "billCode"
    sort_id_1 = "details_1_scantime"

    railwaycommorderdata(file_name_1,check_id_1,sort_id_1,1)

    print("已完成。")
