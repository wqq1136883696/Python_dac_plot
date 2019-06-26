import time
import queue
from os import path
from threading import Thread
from StripeCameraComm import StpCaComm
from wyatt_modules import FileProcess as FP

rec_response = queue.Queue(9600)
thread_status = True


def receive(StpCaComm_connection):
    """接收消息"""
    while True:
        null_count = 0
        if thread_status:
            print("*****开始接收数据*****")
        while thread_status:
            response = StpCaComm_connection.receive_message()
            # print("Received: {}".format(response))
            if response != "":
                rec_response.put(response)
            if response == "":
                null_count += 1
            if null_count == 5:
                break
            time.sleep(0.1)
        # print("******停止接收消息。******")
        time.sleep(0.5)


def recv_response():
    """接收消息"""
    res = rec_response.get()
    return res


def read_response():
    """从队列中读取消息"""
    time.sleep(1)
    response = []
    while not rec_response.empty():
        res = rec_response.get(False)
        response.append(res)
        # print(response)
    if len(response) > 0:
        try:
            print(type(response[-1].split('\r')[-2][0]), response[-1].split('\r')[-2][0])

            if response[-1].split('\r')[-2][0] == '0':
                return True, response[-1][0]
            elif response[-1].split('\r')[-2][0] == '4':
                read_response()
            else:
                return False, response[-1][0]
        except IndexError:
            time.sleep(5)
            read_response()


def format_conversion(StrCaComm_connection, input_filename):
    """格式转换"""
    filename = input_filename
    my_path = path.splitext(filename)
    # print(my_path)
    StrCaComm_connection.send_command_get_response("ImgLoad(img,{})".format(filename))
    res = read_response()
    if res[0]:
        out_filename = my_path[0] + ".dac"
        StrCaComm_connection.send_command_get_response("ImgSave(Current,asciical,{},0)".format(out_filename))
        time.sleep(22)
        res = read_response()
        if res[0] or res[1] == '7':
            StrCaComm_connection.send_command_get_response("ImgDelete(All)")
            res = read_response()
            if res[0]:
                print("StrCaComm: [Converted: {}]".format(out_filename))


def main():
    global thread_status
    LENGTH = 135
    err_list = []

    client = StpCaComm()

    # 创建线程
    rec = Thread(target=receive, args=(client,))
    rec.setDaemon(False)
    rec.start()

    # 启动程序
    client.send_command_get_response("AppStart()")
    if read_response()[0]:
        pub_folder = r"G:\Group_Work\Wyatt_Experiment\NanoSheets\TW\tangbing_sample\ColdTemp\20190617\inter"
        sub_folder = FP.show_all_sub_folder(pub_folder, name=None)
        i = 1
        for folder in sub_folder:
            file_list = FP.show_file(folder, fmt='.img')
            if len(file_list) > 0:
                # print(file_list)
                for file in file_list:
                    print("-"*LENGTH)
                    filename = folder + "\\" + file
                    print("{} . Start converting [{}]".format(i, filename))
                    try:
                        format_conversion(client, input_filename=filename)
                    except Exception as err:
                        print("**********{} {}:{}**********".format(i, filename, err))
                        err_list.append("{}. {}".format(i, filename))
                    print("-"*LENGTH)
                    print("")
                    i += 1

    client.close()
    thread_status = False


if __name__ == '__main__':
    main()
