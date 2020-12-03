import time

class Elevator:
    def __init__(self):
        self.list_num = [-1]*6
        self.inopen = 0  #初始化开门键（电梯里）
        self.open = 0     #初始化开门功能
        self.close = 0    #初始化关门功能
        self.outup = 0       #初始化上行键（电梯外）
        self.outdown = 0     #初始化下行键（电梯外）
        self.direction = -1 #初始化方向（向下为0；向上为1,停止为-1）
        self.now = 0        #初始化现在到达的楼层
        self.count = 0      #初始化已经按下的楼层数

#开门函数,sound:是否语音提示
    def Open(self,sound):    
        self.open = 1
        if sound:
            Sound()
        time.sleep(5)
        self.Close()

 #关门函数   
    def Close(self):     
        self.close = 1

#语音提示函数
    def Sound(self):   
        print("%d楼到了~~"%(self.now+1))
        self.list_num[self.now] = -1
        self.flag = 0       #没有楼层按下的标志
        for each in self.list_num:
            if each!=-1:
                self.flag = 1
        if not self.flag:
            self.direction = -1   #没有楼层按下，10分钟内电梯停在该楼层

 #电梯外上行键
    def OutUp(self,aim):   
        self.outup = 1
        self.Button(aim)
        self.outup = 0   #自动取消按下
        
 #电梯外下行键
    def OutDown(self,aim):   
        self.outdown = 1
        self.Button(aim)
        self.outdown = 0   #自动取消按下


 #按键函数
    def Button(self,aim):    
        
        #开门和关门；只要按下关门键，就关门
        if self.close==1:     
            self.Close()
        elif self.inopen==1 or (self.direction==0 and self.outdown==1) or (self.direction==1 and self.outup==1):
            self.Open()
        
        #原来停止，最先按下的楼层决定运行方向
        if self.direction==-1:
            if self.count==1:
                if aim==self.now:
                    self.Open(0)  #不开语音提示
                else:
                    if aim>self.now:
                        self.direction = 1  #确定方向：上行
                        self.list_num[aim] = aim
                        self.count += 1
                        else:
                            self.direction = 0  #确定方向：下行
                            self.list_num[aim] = aim
                            self.count += 1

        #原来上行，如果按下下行键，忽略；否则不忽略
        elif self.direction==1:
            if not self.outdown:
                if aim>self.now:
                    self.list_num[aim] = aim
                    self.count += 1
                else:
                    pass
            else:
                pass

        #原来下行，如果按下上行健，忽略；否则不忽略
        elif self.direction==0:
            if not self.outup:
                if aim<self.now:
                    self.list_num[aim] = aim
                    self.count += 1
                else:
                    pass
            else:
                pass


#手动取消楼层按键函数
    def Cannel(self,aim):      
        if self.list_num[aim]==1:       #原来是按下状态
            
            #原来上行
            if self.direction==1:      
                self.top_flag = 1      #判断是否是原来要到达的最高层
                for each in self.list_num[aim:]:
                    if each>0:
                        self.top_flag = 0
                if self.top_flag:
                    self.none_flag = 1   #判断已经到达的和要取消的楼层之间有没有楼层按下
                    for each in self.list_num[self.now+1:aim]:
                        if each>0:
                            self.none_flag = 0
                    if self.none_flag:
                        self.list_num[aim-1] = aim

            #原来下行
            if self.direction==0:      
                self.least_flag = 1      #判断是否是原来要到达的最低层
                for each in self.list_num[:aim]:
                    if each>0:
                        self.least_flag = 0
                if self.least_flag:
                    self.none_flag = 1   #判断已经到达的和要取消的楼层之间有没有楼层按下
                    for each in self.list_num[aim+1:self.now]:
                        if each>0:
                            self.none_flag = 0
                    if self.none_flag:
                        self.list_num[aim-1] = aim

            #取消所按楼层
            self.list_num[aim] = -1



            
            
            
    
   
        

    
                    
        
