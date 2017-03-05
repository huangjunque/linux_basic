### Python 简单运维脚本 

##背景
最近在Windows 10上使用Linux子系统，发现它有一个非常坑爹的特点：Linux子系统是没有开机关机状态的，每次进入Bash shell就自动载入，退出后Linux子系统的所有进程都会被关闭，如果你撞了Mysql之类的服务要想随时运行的话就要保持Bash shell的随时开启，更坑的是这些服务并不会随之进入Bash shell而自动启动， 我只好写一个Python脚本用于管理这些服务。


##code python3

```
from os import system
from argparse import ArgumentParser

def start_service(service):
	system("service {} start".format(service))

def stop_service(service):
	system("service {} stop".format(service))
	
def restart_service(service):
	print(service)
	system("service {} restart".format(service))
	
def set_args():
	parser =ArgumentParser()
	parser.add_argument("service", help = "the service to be managed.")
	parser.add_argument("-s", "--start", help = "start the service(s).", action = "store_true")
	parser.add_argument("-r", "--restart", help = "restart the service(s).", action = "store_true")
	parser.add_argumet("-p", "--stop", help = "stop the service(s).", action = "store_true")
	return parser.parse_args()
	
def deal(args,services):
	global start_service, restart_service, stop_service
	services = services if not args.service else service if args.service == "all" else [args.service]
	operation = start_service if args.start else restart_service if args.restart else stop_service 
	for service in services:
		operation(service)
		
if __name__ == "__main__":
	deal(set_args(),manager_service())