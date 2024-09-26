import pandas as pd
from datetime import timedelta
import akshare as ak

def get_min(symbol):
    # 获取分钟级别的期权数据
    df = ak.option_sse_minute_sina(symbol=symbol) 
    return df

def is_in_time():
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M")
    if "09:30" <= formatted_time <= "12:00" or "13:00" <= formatted_time <= "15:30":
        return True
    else:
        return False
    
    
def strategy(stockcode, data, PositionInfo_dict):
	upper, middle, lower = talib.BBANDS(data['价格'].values, timeperiod=20, nbdevup=2, nbdevdn=2)
	dif, dea, macd = talib.MACD(data['价格'].values, fastperiod=12, slowperiod=26, signalperiod=9)
			# 判断是否突破布林轨道上轨且持仓中有MACD下穿, data['价格'][-1] <= middle[-1] or   日内卖出
	if PositionInfo_dict.__contains__(stockcode) and (data['价格'][-1] <= middle[-1] or dif[-1] <= dea[-1] or '14:59:00'.__eq__(data.index[-1])):
		# 执行卖出操作
		rec= PositionInfo_dict[stockcode]
		rec['收益']=data['价格'][-1]-rec['价格']
		PositionInfo_dict.pop(stockcode)
		log(f'{data.index[-1]} - sell {stockcode},profit:{rec["收益"]*10000*50}, dif:{dif[-1]}, dea: {dea[-1]}, upper: {upper[-1]}, middle:{middle[-1]}, price:{data["价格"][-1]}')		
		res.append(rec)
		return 'sell'
		# 布林宽度大于3%,and data['价格'][-3] <= upper[-3] ,and (upper[-1]-middle[-1])/middle[-1] > 0.03,and data['持仓'][-1] > 1000
	elif not PositionInfo_dict.__contains__(stockcode) and data['价格'][-1] > upper[-1] and dif[-1] > dea[-1] and data['持仓'][-1] > 500:
		PositionInfo_dict[stockcode] = {'时间':data.index[-1],'价格':data['价格'][-1]}
		# 执行买入操作
		log(f'{data.index[-1]} - buy {stockcode}, dif:{dif[-1]}, dea: {dea[-1]}, upper: {upper[-1]}, middle:{middle[-1]}, price:{data["价格"][-1]}')
		return 'buy'

	return ''

def buy(symbol, vol):
    print('{}- Buy {}, vol:{}'.format(time_util.ms(),symbol,vol))
    # 执行买入操作的代码
    pass

def sell(symbol, vol):
    print('{}- Sell {}, vol:{}'.format(time_util.ms(),symbol,vol))
    # 执行卖出操作的代码
    pass

import schedule
import time

def my_task():
    # log(f'{time_util.ms()}-开始执行任务[my_task]')
    if not is_in_time():
        # log("当前时间不在9:30-11:30之间，任务不执行")
        return
    # print("执行任务")
    df = option_data.get_min(symbol)
    df = df.set_index('时间')
    # print(df)
    flag = option_backtest.strategy(symbol, df, dict)
    if('sell'.__eq__(flag)):
			# 执行卖出操作
        option_order.sell(symbol,vol)   
    elif('buy'.__eq__(flag)):
		# 执行买入操作
        option_order.buy(symbol,vol)
    else:
      print(f'{time_util.ms()}-无买卖')
    
def job():
    log("执行定时任务job：", time.ctime())

def min():
   # 每5秒执行一次my_task函数
    schedule.every().seconds.do(my_task)
        
    # #每隔1秒执行一次job函数
    # schedule.every(10).seconds.do(job) 
    # #每隔10分钟执行一次job函数
    # schedule.every(10).minutes.do(job)
    # #每小时的整点执行job函数
    # schedule.every().hour.do(job)
    # #每天的14:30分执行job函数
    # schedule.every().day.at("14:30").do(job)
    # #随机地在每5到10分钟之间选择一个时间点执行job函数
    # schedule.every(5).to(10).minutes.do(job)
    # #每周一执行job函数
    # schedule.every().monday.do(job)
    # #每周三的13:15分执行job函数
    # schedule.every().wednesday.at("13:15").do(job)
    # #每个小时的第17分钟执行job函数
    # schedule.every().minute.at(":17").do(job)
def start():
    # 每5秒执行一次my_task函数
    schedule.every().minutes.do(my_task)

    while True:
        # 每一秒检查一次是否有需要执行的任务
        schedule.run_pending();
        time.sleep(1)
if __name__=='__main__':
    str='2023-12-31 03:40:10'
    #symbol="10007509"
    symbol="10007518"
    start()