import sys
import re
from Resource import *
from Processor import *


# 首先需要init才可执行之后的进程与资源分配操作
def system_init():
    processor_temp = Processor()
    resource_temp = Resource()
    processor_temp.create_process('init', 0)
    for x in processor_temp.get_running_list():
        print(x + " ", end='')
    return processor_temp, resource_temp


# 输入处理
def analysis(inputs):
    # 去除输入两边空格
    inputs = inputs.strip()
    # 去除输入中多个空格
    inputs = re.sub('[ ]+', ' ', inputs)
    # 解析用户输入
    xs = inputs.split(" ")
    if len(xs) == 3:
        # create process
        if xs[0] == 'cr':
            pid = xs[1]
            priority = xs[2]
            # 只能创建优先级为1或者2的进程，init进程的优先级为0
            if priority != '1' and priority != '2':
                print("invalid syntax:" + priority + ", type [1,2]")
                return 0
            processor.create_process(pid=pid, priority=priority)
        # request resource
        elif xs[0] == 'req':
            rid = xs[1]
            try:
                num = float(xs[2])
            except ValueError as e:
                print(e)
                return 0
            else:
                if num.is_integer() and abs(num) == num:
                    processor.request_resource(resource=resource, rid=rid, request_status=num)
                else:
                    print("error, the request number must be positive integer!")
                    return 0
        # release resource
        elif xs[0] == 'rel':
            rid = xs[1]
            try:
                num = float(xs[2])
            except ValueError as e:
                print(e)
                return 0
            else:
                if num.is_integer() and abs(num) == num:
                    processor.release_resource(resource=resource, rid=rid, release_status=num)
                else:
                    print("error, the release number must be positive integer!")
                    return 0
        else:
            print("invalid syntax" + xs[0])
            return 0
    elif len(xs) == 2:
        # show specified process
        if xs[0] == 'lp':
            pid = xs[1]
            processor.get_process_info(pid=pid)
            return 0
        # delete process
        elif xs[0] == 'de':
            # 不能删除 init 进程
            pid = xs[1]
            if pid == 'init':
                print("error, can not delete process init!")
                return 0
            processor.delete_process(resource=resource, pid=pid, time=0)
        # run file
        elif xs[0] == 'run':
            filename = xs[1]
            read_test_shell(filename)
        else:
            print("syntax occur")
            return 0
    else:
        # time out
        if inputs == 'to':
            processor.time_out()
        # list all process
        elif inputs == 'lp':
            running, ready, blocked = processor.get_running_list(), \
                                      processor.get_ready_list(), \
                                      processor.get_block_list()
            print("running: " + str(running))
            print("ready: " + str(ready))
            print("blocked: " + str(blocked))
            return 0
        # list all resources
        elif inputs == 'lr':
            request_list = resource.get_rl()
            [print(x) for x in request_list]
            return 0
        elif inputs == 'exit':
            return -1
        elif inputs == 'help':
            print("#################")
            print("process:")
            print("show [lp] | [lp <pid>] ")
            print("create [cr <pid> <priority>]")
            print("delete [de <pid>]")
            print("#################")
            print("resources:")
            print("request [req <rid> <number>]")
            print("release [rel <rid> <number>]")
            print("#################")
            print("dispatch:")
            print("time out [to]")
            print("#################")
            print("run test shell:")
            print("run [filename.txt]")
            print()
            return 0
        else:
            print("syntax occur")
            return 0
    for x in processor.get_running_list():
        # print("running:", x)
        print(x + " ", end='')


# 按行读取文本进shell
def read_test_shell(filename):
    try:
        file = open(filename)
        text_lines = file.readlines()
        for line in text_lines:
            analysis(line)
        file.close()
    except IOError as e:
        print(e.strerror)
        return 0
    else:
        file.close()
        return 0


# 主函数部分采用命令行参数读取文件内容
if __name__ == '__main__':
    processor, resource = system_init()
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        read_test_shell(filename)
    if len(sys.argv) == 1:
        while (True):
            X = input("")
            code = analysis(X)
            if code == -1:
                break