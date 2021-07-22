from apscheduler.schedulers.blocking import BlockingScheduler
import requests
from pyquery import PyQuery as pq
import datetime


sched = BlockingScheduler()


def lineNotifyMessage(token, msg):

    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, params=payload)
    return r.status_code


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=6)
def scheduled_job():
    url = "https://jimchu-app-linebot.herokuapp.com/"
    res = requests.get(url)
    doc = pq(res.text)
    print(doc('h1').text())
    print(datetime.datetime.now().ctime())
    
    token = 'Qg1tV3SQkI9clpvzOViAzjxNUkczSQMwddf7H3YbiNU'
    message = '嗨! 我是小朱 現在時間: {}'.format(datetime.datetime.now().ctime())
    lineNotifyMessage(token, message)

sched.start()