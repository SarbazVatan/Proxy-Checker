#!/usr/bin/python
# -*- coding: utf-8 -*-
# proxy_checker by Sarbaz-Vatan
# Multi-Thread

import threading, Queue
import urllib2

print r'''
  ____                         ____ _               _             
 |  _ \ _ __ _____  ___   _   / ___| |__   ___  ___| | _____ _ __ 
 | |_) | '__/ _ \ \/ / | | | | |   | '_ \ / _ \/ __| |/ / _ \ '__|
 |  __/| | | (_) >  <| |_| | | |___| | | |  __/ (__|   <  __/ |   
 |_|   |_|  \___/_/\_\\__, |  \____|_| |_|\___|\___|_|\_\___|_|   
                      |___/    By: Sarbaz-Vatan
'''

input_queue = Queue.Queue()
url = 'http://google.com'
LIST = str(raw_input('\n\a[~]List: '))
thread = int(raw_input("\n[#]Thread: "))


def check_proxy(input_queue):
    while 1:
        prx = input_queue.get()
        try:
            proxy_handler = urllib2.ProxyHandler({'http': prx})
            opener = urllib2.build_opener(proxy_handler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib2.install_opener(opener)
            req = urllib2.Request("http://www.google.com")
            sock = urllib2.urlopen(req, timeout=7)
            rs = sock.read(1000)
            if '<title>Google</title>' in rs:
				print '[OK]', prx
				input_queue.task_done()
				kl = open('result.txt', 'a')
				kl.write(str(prx))
				kl.close()
        except urllib2.HTTPError, e:
            input_queue.task_done()

        except Exception, detail:
            print '[-]', prx
            input_queue.task_done()

def run_thread():
    global input_queue
    for x in range(thread):
        aa = threading.Thread(target=check_proxy, args=(input_queue,))
        aa.setDaemon(True)
        aa.start()
    for xx in open(LIST, 'r').readlines():
        input_queue.put(xx)
    input_queue.join()


if __name__ == '__main__':
    run_thread()
