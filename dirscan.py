import re
import time
import aiohttp
import asyncio
import threading
import tkinter as tk
import async_timeout
from urllib.parse import urlparse


class Scanner:
    def __init__(self):
        self.window  = tk.Tk()
        self.window.title('小葵目录扫描器 Code by:xi4okv')
        self.window.geometry('800x800')
        #Label
        self.L1 = tk.Label(self.window , text="Url:")
        self.L1.place( x=10,y=10)
        #输入URL
        self.E1 = tk.Entry(self.window , width = 50, bd = 2)
        self.E1.place( x=40,y=10)
        #Label
        self.L2 = tk.Label(self.window , text="Timeout:")
        self.L2.place( x=450,y=10)
        #输入超时时间
        self.E2 = tk.Entry(self.window , width = 5, bd = 2)
        self.E2.place( x=510,y=10)
        #开始按钮
        self.B = tk.Button(self.window , text ="扫描", command = self.change_form_state)
        self.B.place( x=400,y=8)
        #显示结果
        self.M = tk.Text(self.window,width = 110, height=55)
        self.M.place(x=10,y=50)
        
        #默认扫描连接
        self.E1.insert(0,"https://www.baidu.com/")
        #默认超时
        self.E2.insert(0,2)

        with open("./dict/dict.txt") as f:
            self.data = f.readlines()
        
        self.window .mainloop()

    async def scan(self):
        url = self.E1.get()
        timeout = int(self.E2.get())
        up = urlparse(url)
        compile_rule = r'<title>.*</title>'
        sem = asyncio.Semaphore(20)  
        with (await sem):
            async with aiohttp.ClientSession() as session:
                for path in self.data:
                    path = path.strip()
                    async with async_timeout.timeout(timeout):
                        async with session.get(url + path) as resp:
                            content = await resp.text()
                            title_list = re.findall(compile_rule, content)
                            if title_list:
                                title = title_list[0]
                                title = title[7:-8]
                            else:
                                title = None
                            if resp.status != 404:
                                self.M.insert(tk.INSERT,str(resp.status) + "\t" + url + path + " ===> " + title + "\n")
                                self.M.see(tk.END)
                                self.M.update()
                self.M.insert(tk.INSERT,"End!\n")
                self.M.see(tk.END)
                self.M.update()




    def get_loop(self,loop):
        self.loop=loop
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()
        
    def change_form_state(self):
        coroutine = self.scan()
        new_loop = asyncio.new_event_loop()                        
        t = threading.Thread(target=self.get_loop,args=(new_loop,))  
        t.start()
 
        asyncio.run_coroutine_threadsafe(coroutine,new_loop)


if __name__ == '__main__':
    app = Scanner()
