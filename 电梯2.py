import time

class Elevator:
    def __init__(self):
        self.list_num = [-1]*6
        self.inopen = 0  #初始化开门键（电梯里）
        self.open = 0     #初始化开门功能
        self.close = 0    #初始化关门功能
        self.outup = 0       #初始化上行键（电梯外）
        self.outdown = 0     #初始化下行键（电梯外）
        self.direction = 0 #初始化方向（向下为0；向上为1,停止为-1）
        self.now = 0        #初始化现在到达的楼层

    def Open(self):     #开门函数
        self.open = 1
        time.sleep(5)
        self.Close()

    def Close(self):     #关门函数
        self.close = 1

    def Sound(self,now):    #语音提示函数
        print("%d楼到了~~"%(now+1))
        self.list[now] = -1

    def Button(self,now,aim):    #成功按下目标楼层函数
        self.count = 0
        for each_num in self.list_num:
            if each_num>0:
                self.count += 1
        if self.count==1:
            if aim==now:
                pass
            else:
                if aim>now:
                    self.direction = 1  #确定方向：上行
                    else:
                        self.direction = 0  #确定方向：下行
        if self.direction==1:
            if aim>now:
                self.list_num[aim] = aim
            else:
                pass
        if self.direction==0:
            if aim<now:
                self.list_num[aim] = aim
            else:
                pass

    def OutUp(self,aim):   #电梯外上行键
        self.Button(self.now,aim)
        self.outup = 0   #取消按下

    def OutDown(selg,aim):   #电梯外下行键
        self.Button(self.now,aim)
        self.outup = 0   #取消按下

    def Stop(self,now):       #原来停止函数
        if self.close==1:     #只要按下关门键，就关门
            self.Close()
        elif self.inopen==1 or (self.direction==0 and self.down==1) or (self.direction==1 and self.up==1):
            self.Open()
        

    
                    
        
