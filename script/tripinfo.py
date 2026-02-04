import csv
import os
from datetime import datetime, timedelta

def read_trip_info(file_path_list, time_limit):
    trade_info_list = []

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
                            seq_value = row.get('sequence_no')
                            create_time_str = row.get('create_time')
                            
                            if seq_value and create_time_str:
                                # 格式：20250210000353363
                                try:
                                    # 提取日期和时间部分
                                    create_time = datetime.strptime(create_time_str[:14], '%Y%m%d%H%M%S')
                                    
                                    # 如果时间在当前日期time_limit日以前，丢弃这一行
                                    if create_time >= cutoff_date:
                                        trade_info_list.append(seq_value)
                                except ValueError as e:
                                    print(f"解析create_time错误: {create_time_str}, 错误: {e}")
                                    continue
                            else:
                                continue

                        # 处理trip文件
                        elif 'trip' in filename:
                            seq_value = row.get('sequence_no')
                            order_date_str = row.get('order_date')
                            
                            if order_date_str:
                                try:
                                    # 格式: 2024-07-10 17:22:57
                                    order_date = datetime.strptime(order_date_str, '%Y-%m-%d %H:%M:%S')
                                    
                                    # 如果时间在当前日期time_limit日以前，丢弃这一行
                                    if order_date >= cutoff_date:
                                        trade_info_list.append(seq_value)
                                except ValueError as e:
                                    print(f"解析order_date错误: {order_date_str}, 错误: {e}")
                                    continue
                            else:
                                continue
                        
                        # 处理alternate文件
                        elif 'alternate' in filename:
                            seq_value = row.get('sequence_no')
                            reserve_time_str = row.get('reserve_time')
                            
                            if reserve_time_str:
                                try:
                                    # 格式: 2024-07-10
                                    reserve_time = datetime.strptime(reserve_time_str, '%Y-%m-%d')
                                    
                                    # 如果时间在当前日期time_limit日以前，丢弃这一行
                                    if reserve_time >= cutoff_date:
                                        trade_info_list.append(seq_value)
                                except ValueError as e:
                                    print(f"解析reserve_time错误: {reserve_time_str}, 错误: {e}")
                                    continue
                            else:
                                continue

                        # 处理memtrade文件
                        elif 'memtrade' in filename:
                            seq_value = row.get('sequence_no')
                            trade_time_str = row.get('trade_time')
                            
                            if trade_time_str:
                                try:
                                    if '.' in trade_time_str:
                                        # 格式: 2022-12-30 12:05:12.292495
                                        trade_time = datetime.strptime(trade_time_str, '%Y-%m-%d %H:%M:%S.%f')
                                    else:
                                        # 格式: 20221230
                                        trade_time = datetime.strptime(trade_time_str, '%Y%m%d')
                                    
                                    # 如果时间在当前日期time_limit日以前，丢弃这一行
                                    if trade_time >= cutoff_date:
                                        trade_info_list.append(seq_value)
                                except ValueError as e:
                                    print(f"解析trade_time错误: {trade_time_str}, 错误: {e}")
                                    continue
                            else:
                                continue
                        
                        # 处理memtradedetail文件
                        elif 'memtradedetail' in filename:
                            seq_value = row.get('sequence_no')
                            train_date_str = row.get('train_date')
                            
                            if train_date_str:
                                try:
                                    # 格式: 20240710
                                    train_date = datetime.strptime(train_date_str, '%Y%m%d')
                                    
                                    # 如果时间在当前日期time_limit日以前，丢弃这一行
                                    if train_date >= cutoff_date:
                                        trade_info_list.append(seq_value)
                                except ValueError as e:
                                    print(f"解析train_date错误: {train_date_str}, 错误: {e}")
                                    continue
                            else:
                                continue
                        
                        # 处理commreserve和ecardreserve文件
                        elif 'commreserve' in filename or 'ecardreserve' in filename:
                            seq_value = row.get('sequenceNo')
                            reserveTime_str = row.get('reserveTime')
                            
                            if seq_value and reserveTime_str:
                                # 格式：20250210000353363
                                try:
                                    # 提取日期和时间部分
                                    reserveTime = datetime.strptime(reserveTime_str[:14], '%Y%m%d%H%M%S')
                                    
                                    # 如果时间在当前日期time_limit日以前，丢弃这一行
                                    if reserveTime >= cutoff_date:
                                        trade_info_list.append(seq_value)
                                except ValueError as e:
                                    print(f"解析reserveTime错误: {reserveTime_str}, 错误: {e}")
                                    continue
                            else:
                                continue
                    else:
                        # 其他文件用原来的逻辑（无时间限制）
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
            
    # 去重并移除空值
    trade_info_list = [element for element in list(set(trade_info_list)) if element]

    return trade_info_list

if __name__ == "__main__":

    print('Must have railwaytrip.csv and railway_psr.csv before using this script.')

    # tripdetail查询时间限制
    time_limit = 80

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
    file_path_list.append(os.path.join(parent_directory, 'railwaycommreserve.csv'))
    file_path_list.append(os.path.join(parent_directory, 'railwayecardreserve.csv'))
    trade_info = read_trip_info(file_path_list, time_limit)
    print(trade_info)
    print(len(trade_info))