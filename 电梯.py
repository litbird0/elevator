import time

class Elevator:
    def __init__(self):
        self.list_num = [-1]*6

    def button(self,num):    #按下按键或者取消按键
        if not self.list_num[num]:
            self.list_num[num] = num   #按下按键
        else:
            self.list_num[num] = -1    #取消按键
        
    def up(self,now,num):    #上行；now:目前楼层；num:按下的楼层
        if now<num and num!=6:     #按键按下不忽略的楼层
            self.button(num)
        else:
            pass                   #忽略

        for self.each_num in self.list_num[now:]:
            if self.each_num>0:
                self.arrive(self.each_num)
                time.sleep(5)     #上升过程（延时5秒）
        
    def down(self,now,num):   #下行
        if now>num and num!=1:    #按键按下不忽略的楼层
            self.button(num)
        else:
            pass                  #忽略

        for self.each_num in self.list_num[:now]:
            if self.each_num>0:
                self.arrive(self.each_num)
                time.sleep(5)     #下降过程（延时5秒）

    def arrive(self,now):    #到达
        self.button(now)            #取消到达楼层的按键
        print("%d楼倒了"%now)
        time.sleep(5)          #等待5秒

    def auto_stop(self,now):   #自动回停
        self.up(now,3)
        self.dowm(now,3)
        
    
