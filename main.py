# pendulum datetime plugin ??
# ajastamine APScheduler
import sys
import os
import json
import time
from graphqlclient import GraphQLClient
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from pygame import mixer

client = GraphQLClient('https://api.graph.cool/simple/v1/cj7ebm8yt0m9s0114ngjezyec')
now = time.localtime()
mixer.init()
sisse = mixer.Sound("1.wav")
valja = mixer.Sound("2.wav")
sees = client.execute(
    '''
query {allOnoffs {isSees}} 

'''
)
ajad = client.execute('''
query {allHelins {
  bell
  hour
  minute
}}

''')
print('Hetkel on kell: %s' % datetime.now())
parsed_sees = json.loads(sees)
playing = parsed_sees['data']['allOnoffs'][0]['isSees']
parsed_ajad = json.loads(ajad)
# print(parsed_ajad['data']['allHelins'])
helinate_arv = len(parsed_ajad['data']['allHelins'])
print ('helinate arv on: ' + str(helinate_arv))
# print(parsed_ajad['data']['allHelins'][0])

def tick(x):
    print('Tick! Kell on praegu: %s' % datetime.now())
    print('Helin on ' + str(x % 2))
# sisse ja v2ljahelinaga variant
    # if x%2 == 1:
    #     sisse.play()
    #
    # else:
    #     valja.play()
# ainult sissehelinaga
    sisse.play()


if __name__ == '__main__' and playing:
    scheduler = BackgroundScheduler()
    for x in range(helinate_arv):
        scheduler.add_job(tick, 'cron',[x], day_of_week='mon-fri', hour=parsed_ajad['data']['allHelins'][x]['hour'],
                          minute=parsed_ajad['data']['allHelins'][x]['minute'], end_date='2018-06-06')
    scheduler.start()
    scheduler.print_jobs()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
