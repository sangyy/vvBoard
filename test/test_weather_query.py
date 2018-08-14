import requests
from lxml import html
import re
import time

from xugu import LED

url = "http://www.weather.com.cn/weather/101280601.shtml"
led = LED(13)
r = re.compile("\d+")

def warnig_single():
    """
    闪烁LED灯持续一个小时
    :return: 
    """
    for i in range(3600):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)

def working_single():
    """
    LED 灯常亮一个小时
    :return: 
    """
    for i in range(3600):
        led.on()
        time.sleep(1)

def failed_single():
    """
    LED灯熄灭10秒
    :return: 
    """
    led.off()
    time.sleep(10)

def check_threhold(tem):
    """
    检测阈值，如果温度超过阈值，则闪烁LED灯，否则LED灯常亮，如果没有获取到温度，则LED灯是熄灭状态
    :param tem: 
    :return: 
    """
    threhold = 30
    if tem is None:
        failed_single()
    elif tem > threhold:
        warnig_single()
    else:
        working_single()

while 1:
    # 爬取中国天气网获取深圳市的气温
    body = requests.get(url)
    if body.ok:
        tree = html.fromstring(body.content)
        # 根据网页结构定位到当天的气温
        for item in tree.xpath('//ul[@class="t clearfix"]//'
                               'li[@class="sky skyid lv2 on"]//p[@class="tem"]'):
            tem = item.text_content()
            rt = r.findall(tem)
            if rt:
                tem = int(rt[0])
            else:
                tem = None
            check_threhold(tem)
            break
    else:
        failed_single()
