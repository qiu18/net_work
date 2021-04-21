# 导入窗体模块
import tkinter
# 导入mysql模块
import pymysql
# 导入时钟模块
import time
# 导入线程模块
import threading
# 导入抓取窗口消息模块
from tkinter.messagebox import askyesno


# 创建一个thinter时钟模块
class Timer:
    def __init__(self,wnd,ms,call):
        """ tkinter窗口定时执行某函数

        :param wnd: tkinter窗口
        :param ms: 重复执行间隔时间（毫秒）
        :param call: 重复执行的函数
        """
        self.__wnd = wnd
        self.__ms = ms
        self.__call = call
        self.__running = False

    def start(self):
        if not self.__running:
            self.__wnd.after(0,self.__on__timer)
            self.__running = True

    def stop(self):
        if self.__running:
            self.__running = False

    def is_running(self):
        return self.__running

    def __on__timer(self):
        if self.__running:
            self.__call()
            self.__wnd.after(self.__ms,self.__on__timer)


# 连接数据路
def get_conn():
    return pymysql.Connect(
        host='192.168.250.3',
        port=3307,
        user='sxgdwl',
        password='13515990222',
        database='Net_work',
        charset='utf8'
    )


# 查询表
def query_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        return cursor.fetchall()
    finally:
        conn.close()


# 根据oid获取网口状态(是否在线、光功率)



# 插入或更新mysql数据库
def insert_or_update_data(sql):
    conn = get_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()


# 从Mysql获取端口数据
def get_port_data():
    text_log.delete(1.0, 'end')
    text_log.insert('end', '开始刷新数据******' + '\n')
    sql = 'select * from host'
    datas = query_data(sql)
    lendata = len(datas)
    for i in range(lendata):
        datass = datas[i]
        host_id = datass['host_id']
        host_name = datass['host_name']
        # print(host_id)
        sql = 'SELECT * from host_port WHERE host_id = ' + str(host_id)
        host_oid_date = query_data(sql)
        lenhost_oid_date = len(host_oid_date)
        for ii in range(lenhost_oid_date):
            oid_date = host_oid_date[ii]
            port_oid = oid_date['port_oid']
            port_name = oid_date['port_name']
            port_date = snmpget(port_oid)
            port_starte = port_date[0][1]
            port_rx_power = port_date[1][1]
            # 取mysql格式当前时间
            log_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if port_starte == 1:
                upsql = "update host_port SET port_state = '" + str(port_starte) + "',port_rx_power = '" + str(port_rx_power) + "',log_time = '" + str(log_time) + "' WHERE port_oid = '" + str(port_oid) + "'"
                insert_or_update_data(upsql)
                insql = "INSERT INTO host_log (host_name,host_id,log_time,port_name,post_oid,port_rx_power,port_state) VALUES ('" + host_name + "','" + str(host_id) + "','" + str(log_time) + "','" + port_name + "','" + str(port_oid) + "','" + str(port_rx_power) + "','" + str(port_starte) + "')"
                insert_or_update_data(insql)
            else:
                upsql = "update host_port SET port_state = '" + str(port_starte) + "',log_time = '" + str(log_time) + "' WHERE port_oid = '" + str(port_oid) + "'"
                insert_or_update_data(upsql)
                insql = "INSERT INTO host_log (host_name,host_id,log_time,port_name,post_oid,port_state) VALUES ('" + host_name + "','" + str(host_id) + "','" + str(log_time) + "','" + port_name + "','" + str(port_oid) + "','" + str(port_starte) + "')"
                insert_or_update_data(insql)
            print_text = str(log_time) + '|' + str(port_oid) + '|' + str(port_starte) + '|' + str(port_rx_power)
            text_log.insert('end',print_text + '\n')


def get_data_threading():
    thread = threading.Thread(target=get_port_data)
    thread.start()


def start_get_oid():
    btn_start.config(state='disabled')
    btn_stop.config(state='normal')
    time_js.start()


def stop_get_oid():
    btn_start.config(state='normal')
    btn_stop.config(state='disabled')
    time_js.stop()


# 关闭窗口时弹出选项
def close_window():
    ans = askyesno(title='警告', message='真的要关闭窗口?')
    if ans:
        global stop_perform
        stop_perform = 1
        root.destroy()
    else:
        return


root = tkinter.Tk()
root.title('交换机OID采集器')
root.geometry('400x600')
root.iconbitmap('123.ico')
time_js = Timer(root,10000,get_data_threading)
btn_start = tkinter.Button(root, text='开始采集', command=start_get_oid)
btn_start.place(x=10, y=10)
btn_stop = tkinter.Button(root, text='停止采集',state='disabled',command=stop_get_oid)
btn_stop.place(x=75, y=10)
text_log = tkinter.Text(root,width=53,height=41)
text_log.place(x=10, y=50)
root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()


