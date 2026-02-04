import csv
import os
import re
from datetime import datetime, timedelta

def read_extno_info(file_path_list, time_limit):
    extno_info_list = []
    pattern = re.compile(r'^tickets_\d+_ext_ticket_no$')  # 编译正则表达式模式
    
    # 获取当前日期和时间
    now = datetime.now()
    cutoff_date = now - timedelta(days=time_limit)
    
    for file_path in file_path_list:
        try:
            filename = os.path.basename(file_path).lower()
            
            with open(file_path, mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                
                for row in csv_reader:
                    if time_limit > 0:
                        # 处理psr和invoice文件
                        if 'psr' in filename or 'invoice' in filename:
                            ext_value = row.get('ext_ticket_no')
                            create_time_str = row.get('create_time')
                            
                            if ext_value and create_time_str:
                                # 格式：20250210000353363
                                try:
                                    # 提取日期和时间部分
                                    create_time = datetime.strptime(create_time_str[:14], '%Y%m%d%H%M%S')
                                    
                                    # 如果时间在当前日期time_limit日以前，丢弃这一行
                                    if create_time >= cutoff_date:
                                        extno_info_list.append(ext_value)
                                except ValueError as e:
                                    print(f"解析create_time错误: {create_time_str}, 错误: {e}")
                                    continue
                            else:
                                continue
                        
                        # 处理trip文件
                        elif 'trip' in filename:
                            order_date_str = row.get('order_date')
                            
                            if order_date_str:
                                try:
                                    # 格式: 2024-07-10 17:22:57
                                    order_date = datetime.strptime(order_date_str, '%Y-%m-%d %H:%M:%S')
                                    
                                    # 如果时间在当前日期time_limit日以前，丢弃这一行所有值
                                    if order_date >= cutoff_date:
                                        # 动态匹配所有 tickets_数字_ext_ticket_no 字段
                                        for key in row.keys():
                                            if pattern.match(key):
                                                value = row.get(key)
                                                if value:  # 确保值非空
                                                    extno_info_list.append(value)
                                except ValueError as e:
                                    print(f"解析order_date错误: {order_date_str}, 错误: {e}")
                                    continue
                            else:
                                continue
                    
                    else:
                        # 其他文件用原来的逻辑（无时间限制）
                        ext_ticket_no_0 = row.get('ext_ticket_no')
                        if ext_ticket_no_0:
                            extno_info_list.append(ext_ticket_no_0)

                        # 动态匹配所有 tickets_数字_ext_ticket_no 字段
                        for key in row.keys():
                            if pattern.match(key):
                                value = row.get(key)
                                if value:  # 确保值非空
                                    extno_info_list.append(value)
                        
        except FileNotFoundError:
            print(f"警告：文件未找到 {file_path}，已跳过")
        except Exception as e:
            print(f"处理文件 {file_path} 时发生错误：{str(e)}")
    
    # 去重并移除空值
    extno_info_list = [element for element in list(set(extno_info_list)) if element]

    return extno_info_list

if __name__ == "__main__":
    print('Must have railwaytrip.csv and railway_psr.csv before using this script.')
    
    # notice查询时间限制
    time_limit = 80
    
    file_path_list = []

    # 获取当前脚本的目录
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    # 构建上级目录的路径
    parent_directory = os.path.join(current_directory, '..')
    
    # 构建文件的完整路径
    file_path_list.append(os.path.join(parent_directory, 'railwaypsr.csv'))
    file_path_list.append(os.path.join(parent_directory, 'railwaytrip.csv'))
    # file_path_list.append(os.path.join(parent_directory, 'railwayalternate.csv'))
    # file_path_list.append(os.path.join(parent_directory, 'railwaymemtrade.csv'))
    # file_path_list.append(os.path.join(parent_directory, 'railwaymemtradedetail.csv'))
    file_path_list.append(os.path.join(parent_directory, 'railwayinvoice.csv'))
    
    extno_info = read_extno_info(file_path_list, time_limit)
    print(extno_info)
    print(len(extno_info))