import json  
import pandas as pd
import os

def get_file_path(file_name):
    # 获取当前脚本的目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # 构建上级目录的路径
    parent_directory = os.path.join(current_directory, '..')
    
    # 构建文件的完整路径
    file_name_1 = os.path.join(parent_directory, file_name)

    return file_name_1

def read_existing_data(file_name):
    
    # 读取现有的CSV文件（如果文件不存在，则创建一个空的DataFrame）  
    try:
        # 获取CSV文件的列名
        col_names = pd.read_csv(file_name, nrows=0).columns
        # 为每个列名创建一个字典，键是列名，值是str
        dtype_dict = {col: str for col in col_names}
        # 读取CSV文件，并指定dtype
        existing_data = pd.read_csv(file_name,dtype=dtype_dict,na_filter=False)
    except:
        existing_data = pd.DataFrame()

    return existing_data

def manual_input():
            
    print("请输入JSON数据，直接回车结束: ")
    
    lines = []  
    while True:  
        line = input() 
        if line == '':
            break  
        lines.append(line)  
      
    # 将列表转换为单个字符串，可以使用换行符'\n'作为分隔符  
    input_json = '\n'.join(lines)
    
    # input_json = input("请输入JSON数据（直接回车结束）: ")  

    return input_json

def handle_duplicate_old(data_original,check_id,keep_which):
    if check_id != '':
        # 检查并删除all_new_data中的重复项
        data_unique = data_original.drop_duplicates(subset=check_id, keep=keep_which)
    else:
        data_unique = data_original.drop_duplicates()
    return data_unique

def handle_duplicate_new(data_original,check_id,keep_which):
    if check_id == 'sequence_no':
        # 找出重复的 sequence_no
        duplicates = data_original[data_original.duplicated(subset=[check_id], keep=False)]
        
        if not duplicates.empty:
            # 按 sequence_no 分组
            grouped = duplicates.groupby(check_id)
            
            # 用于存储用户选择的结果
            to_keep = []
            
            for seq_no, group in grouped:
                # 按 order_date 降序排列
                group_sorted = group.sort_values(by='order_date', ascending=False)
                order_dates = group_sorted['order_date'].tolist()
                
                # 检查 order_date 是否全部相同
                if len(set(order_dates)) == 1:
                    # 如果 order_date 相同，按照 keep_which 参数去重
                    # print(f"检查到 {seq_no} 订单重复，且操作时间相同。")
                    to_keep_group = group_sorted.drop_duplicates(subset=check_id, keep=keep_which)  # 实际上这里 subset=[] 可以省略，因为已经按 sequence_no 分组
                    to_keep.extend(to_keep_group.to_dict('records'))  # 转换为字典列表以避免索引问题
                
                else:
                    # 打印提示信息
                    print(f"检查到 {seq_no} 订单重复，最新操作时间分别是 {', '.join(order_dates)}。")
                    user_input = input("输入回车仅保留最新项，输入0全部保留：").strip()
                    
                    if user_input == '':
                        # 保留最新项
                        to_keep.append(group_sorted.iloc[0])
                    elif user_input == '0':
                        # 保留所有项
                        to_keep.extend(group.to_dict('records'))  # 转换为字典列表以避免索引问题
            
            # 将保留的项转换为 DataFrame
            to_keep_df = pd.DataFrame(to_keep)
            
            # 从原始数据中移除重复项，并添加保留的项
            non_duplicates = data_original.drop_duplicates(subset=[check_id], keep=False)
            data_unique = pd.concat([non_duplicates, to_keep_df], ignore_index=True)
        else:
            # 如果没有重复项，直接去重（理论上不会执行，因为已经合并）
            data_unique = data_original.drop_duplicates(subset=[check_id], keep=keep_which)
    else:
        # 其他情况，正常去重
        if check_id != '':
            data_unique = data_original.drop_duplicates(subset=check_id, keep=keep_which)
        else:
            data_unique = data_original.drop_duplicates()
    return data_unique
    
def save_csv(file_name,check_id,sort_id,existing_data,all_new_data,sort_ok,keep_which = 'first'):

    original_row_count = len(existing_data)
    modified_row_count = 0
    new_row_count = 0
    
    if not all_new_data.empty:

        # print("o4")

        # all_new_data[check_id] = all_new_data[check_id].astype(str)

        all_new_data_unique = handle_duplicate_old(all_new_data,check_id,keep_which)
        
        '''
        if check_id != '':
            # 检查并删除all_new_data中的重复项
            all_new_data_unique = all_new_data.drop_duplicates(subset=check_id, keep=keep_which)
        else:
            all_new_data_unique = all_new_data.drop_duplicates()'''
            
        # 将新的唯一数据与现有数据合并
        combined_data = pd.concat([existing_data, all_new_data_unique], ignore_index=True)  

        combined_data_unique = handle_duplicate_new(combined_data,check_id,keep_which)

        '''
        if check_id != '':
            # 再次检查并删除重复项 
            combined_data_unique = combined_data.drop_duplicates(subset=check_id, keep=keep_which)
        else:
            combined_data_unique = combined_data.drop_duplicates()'''

        if sort_ok == 1:
            # 根据tradeNo列进行升序排列
            combined_data_sorted = combined_data_unique.sort_values(by=sort_id)
        else:
            combined_data_sorted = combined_data_unique
          
        # 将合并后的数据写入CSV文件（实际上是替换原文件，但包含了所有旧数据和新数据）  
        combined_data_sorted.to_csv(file_name, index=False, encoding = "utf-8-sig")  

        modified_row_count = len(combined_data_sorted)
        new_row_count = modified_row_count - original_row_count

    print("原有%d行，现有%d行，新增%d行。"%(original_row_count,modified_row_count,new_row_count))
