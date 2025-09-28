from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time
from webdrivermanager_cn.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import sys
import os
 
# 获取当前脚本的目录
current_directory = os.path.dirname(os.path.abspath(__file__))
 
# 添加下级目录到 sys.path
sys.path.append(os.path.join(current_directory, 'script'))

from general_func import *
from railwaypsr import railwaypsrdata
from railwaytrip import railwaytripdata
from railwaytripdetail import railwaytripdetaildata
from railwayalternate import railwayalternatedata
from railwaymemtrade import railwaymemtradedata
from railwaymemtradedetail import railwaymemtradedetaildata
from railwayinvoice import railwayinvoicedata
from railwaycomminvoice import railwaycomminvoicedata
from railwaynotice import railwaynoticedata
from railwaycommorder import railwaycommorderdata
from railwaycommreserve import railwaycommreservedata
from tripinfo import read_trip_info
from memtradeinfo import read_trade_info
from extnoinfo import read_extno_info

def wait_for_js_variable(driver, variable_name):
    def condition(driver):
        return driver.execute_script(f"return {variable_name} !== null && typeof {variable_name} !== 'undefined';")
    return condition

def url_contains(driver, partial_url):
    def condition(driver):
        return partial_url in driver.current_url
    return condition

def element_not_present(driver, locator):
    def condition(driver):
        try:
            element = driver.find_element(*locator)
            return False
        except Exception:
            return True
    return condition

def dataprocess(driver,dataname,*query_list):
    try:
        # 执行 js
        with open(f'./script/railway{dataname}.js', 'r', encoding='utf-8') as file:
            js_code = file.read()
            
        # 执行 JavaScript 并获取返回的 JSON 数据
        if query_list:
            json_list = json.dumps(query_list)
            driver.execute_script(f"{js_code}; init({json_list});")
        else:
            driver.execute_script(js_code)
        # result = driver.execute_script("return window.fetchResult;")
        # 等待 JavaScript 中的异步操作完成
        try:
            WebDriverWait(driver, 60).until(wait_for_js_variable(driver, "window.fetchResult"))
            result = driver.execute_script("return window.fetchResult;")
            if query_list:
                result = json.loads(result)
        except Exception as e:
            print(f"Failed to get fetch result: {e}")

        # 将返回的 JSON 数据作为参数传入 myfunction
        globals()[f'railway{dataname}data'](
            globals()[f'file_name_{dataname}'],
            globals()[f'check_id_{dataname}'],
            globals()[f'sort_id_{dataname}'],
            0,
            result)
        print(f'{dataname} data completed.')
    except Exception as e:
        print(f"{dataname} data got something wrong: ")
        print(e)


def main():

    # 判断浏览器类型
    browser_type = input("If you are using Edge, enter 1. If you are using Chrome, just press Enter. Other browsers are not currently supported.")

    if browser_type == "1":
        from selenium.webdriver.edge.service import Service as EdgeService
        driver = webdriver.Edge(service = EdgeService(EdgeChromiumDriverManager(url='https://msedgedriver.microsoft.com', latest_release_url='https://msedgedriver.microsoft.com/LATEST_RELEASE').install()))
    else:
        from selenium.webdriver.chrome.service import Service as ChromeService
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # 打开登录页，自动选择扫码登录
    driver.get("https://kyfw.12306.cn/otn/resources/login.html")
    element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li.login-hd-account a"))
        )
    element.click()
    
    # 等待登录完成
    print("Please login.")
    WebDriverWait(driver, 120).until(
        url_contains(driver, "https://kyfw.12306.cn/otn/view/index.html")
    )
    # print("If ok, press Enter to continue...")
    # input()
    
    # 本人车票身份核验
    driver.get("https://kyfw.12306.cn/otn/view/personal_travel.html")
    print("Please scan the QR code to complete identity verification.")
    # locator = (By.CSS_SELECTOR, "div.c[style='display: none']")
    # WebDriverWait(driver, 120).until(element_not_present(driver, locator))
    print("If ok, press Enter to continue...")
    input()
       
    # 本人车票数据
    dataprocess(driver,"psr")
    
    # 火车票订单数据
    driver.get("https://kyfw.12306.cn/otn/view/train_order.html")
    dataprocess(driver,"trip")
    element_0 = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//li[@data-type="1"]/a[text()="历史订单"]'))
    )
    element_0.click()
    tripinfolist = read_trip_info([file_name_psr,file_name_trip,file_name_alternate,file_name_memtrade,file_name_memtradedetail,file_name_invoice])
    time.sleep(0.5)
    dataprocess(driver,"tripdetail",tripinfolist)
    
    # 候补订单数据
    dataprocess(driver,"alternate")
    
    # 会员积分数据
    driver.get("https://cx.12306.cn/tlcx/jfinformation.html") # https://cx.12306.cn/tlcx/welcome.html
    dataprocess(driver,"memtrade")
    memtradeinfolist = read_trade_info(file_name_memtrade)
    dataprocess(driver,"memtradedetail",memtradeinfolist)

    # 电子发票身份核验
    '''driver.get("https://kyfw.12306.cn/otn/view/invoice_index.html")

    element_1 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#toolbar_Div > div.wrapper.content > div.center-box > div > div.panel-remind.remind02.remind03 > div.remind-con > div.remind-btns > a.btn.btn-secondary.verfifyModal.w150"))
        )
    element_1.click()

    time.sleep(1)

    if "https://kyfw.12306.cn/otn/view/invoice_ticket_list.html" in driver.current_url:
        pass
    else:
        WebDriverWait(driver, 120).until(
            url_contains(driver, "https://kyfw.12306.cn/otn/view/invoice_ticket_list.html")
        )
        # print("Please scan the QR code to complete identity verification. If ok, press Enter to continue...")
        # input()'''
    driver.get("https://kyfw.12306.cn/otn/view/invoice_ticket_list.html")
    
    # 电子发票数据
    dataprocess(driver,"invoice")

    # 计次定期票电子发票数据
    driver.get("https://kyfw.12306.cn/otn/view/invoice_commutationTicket_list.html")
    dataprocess(driver,"comminvoice")

    # 行程信息提示数据
    extnoinfolist = read_extno_info([file_name_psr,file_name_trip,file_name_alternate,file_name_memtrade,file_name_memtradedetail,file_name_invoice])
    time.sleep(0.5)
    dataprocess(driver,"notice",extnoinfolist)

    # 计次定期票数据
    driver.get("https://kyfw.12306.cn/otn/view/commutation_order.html")
    dataprocess(driver,"commorder",[0,1,2,3,4,5,6,7,8,9])
    dataprocess(driver,"commreserve",[0,1,2,3,4,5,6,7,8,9])

    input("Press Enter to continue...")

    # driver.quit()

if __name__ == "__main__":

    file_name_psr = "railwaypsr.csv"
    check_id_psr = "ext_ticket_no"#trade_no
    sort_id_psr = "local_start_time"
    file_name_trip = "railwaytrip.csv"
    check_id_trip = "sequence_no"
    sort_id_trip = "order_date"#start_train_date_page
    file_name_tripdetail = "railwaytripdetail.csv"
    check_id_tripdetail = ""
    sort_id_tripdetail = "operate_time"
    file_name_alternate = "railwayalternate.csv"
    check_id_alternate = "reserve_no"
    sort_id_alternate = "trace_id"
    file_name_memtrade = "railwaymemtrade.csv"
    check_id_memtrade = "trade_id"
    sort_id_memtrade = "trade_time"
    file_name_memtradedetail = "railwaymemtradedetail.csv"
    check_id_memtradedetail = "trade_id"
    sort_id_memtradedetail = "train_date"
    file_name_invoice = "railwayinvoice.csv"
    check_id_invoice = "ext_ticket_no"
    sort_id_invoice = "local_start_time"
    file_name_comminvoice = "railwaycomminvoice.csv"
    check_id_comminvoice = "orderId"
    sort_id_comminvoice = "saleTime"
    file_name_notice = "railwaynotice.csv"
    check_id_notice = "ext_ticket_no"
    sort_id_notice = "local_start_time"
    file_name_commorder = "railwaycommorder.csv"
    check_id_commorder = "orderId"
    sort_id_commorder = "saleTime"
    file_name_commreserve = "railwaycommreserve.csv"
    check_id_commreserve = "sequenceNo"
    sort_id_commreserve = "reserveTime"

    main()
