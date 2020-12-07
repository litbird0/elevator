import time
from datetime import datetime

class Elevator:
    def __init__(self):
        #初始化
        self.list_num = [-1]*6
        self.inopen = 0  #开门键（电梯里）
        self.open = 0     #开门功能
        self.close = 0    #关门功能
        self.outup = 0       #上行键（电梯外）
        self.outdown = 0     #下行键（电梯外）
        self.direction = -1 #方向（向下为0；向上为1,停止为-1）
        self.now = 0        #现在到达的楼层
        self.count = 0      #已经按下的楼层数
        self.help = 0       #按铃求助功能
        self.heavy = 0      #载重
        self.weight = 0     #输入的重量
        self.alarm = 0      #警报功能
        self.start = 0      #自动回停的条件：计时开始
        self.end = 0        #自动回停的条件：计时结束
        

 #拼接键盘输入的字符（数字）函数
    def Add_weight(self,each_weight):
        global self.weight
        self.weight += each_weight

 #删除操作函数
    def Del_weight(self):
        global self.weight
        weight = weight[:-1]

 #开门函数,sound:是否语音提示
    def Open(self,sound):    
        self.open = 1
        if sound:
            Sound()
        time.sleep(5)

       #开始监听键盘
        self.weight = ''
        while True:
            keyboard.add_hotkey('0',self.Add_weight,args=('0'))
            keyboard.add_hotkey('1',self.Add_weight,args=('1'))
            keyboard.add_hotkey('2',self.Add_weight,args=('2'))
            keyboard.add_hotkey('3',self.Add_weight,args=('3'))
            keyboard.add_hotkey('4',self.Add_weight,args=('4'))
            keyboard.add_hotkey('5',self.Add_weight,args=('5'))
            keyboard.add_hotkey('6',self.Add_weight,args=('6'))
            keyboard.add_hotkey('7',self.Add_weight,args=('7'))
            keyboard.add_hotkey('8',self.Add_weight,args=('8'))
            keyboard.add_hotkey('9',self.Add_weight,args=('9'))
            keyboard.add_hotkey(',',self.Add_weight,args=(','))
            keyboard.add_hotkey('+',self.Add_weight,args=('+'))
            keyboard.add_hotkey('-',self.Add_weight,args=('-'))
            keyboard.add_hotkey('backspace',self.Del_weight)
            recorded = keyboard.record(until='enter')    #按下回车键，停止监听
            if recorded!=[]:
                break
        if self.weight!='':
            self.weight = self.weight.split(',')
            self.Heavy(self.weight)
        self.Close()

 #关门函数   
    def Close(self):     
        self.close = 1
        time.sleep(2)
        self.Heavy()

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

 #按铃求助按键函数
    def Help(self):
        self.help = 1
        time.sleep(10)
        self.help = 0
            

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
                    if each>=0:
                        self.top_flag = 0
                if self.top_flag:
                    self.none_flag = 1   #判断已经到达的和要取消的楼层之间有没有楼层按下
                    for each in self.list_num[self.now+1:aim]:
                        if each>=0:
                            self.none_flag = 0
                    if self.none_flag:
                        self.list_num[aim-1] = aim

            #原来下行
            if self.direction==0:      
                self.least_flag = 1      #判断是否是原来要到达的最低层
                for each in self.list_num[:aim]:
                    if each>=0:
                        self.least_flag = 0
                if self.least_flag:
                    self.none_flag = 1   #判断已经到达的和要取消的楼层之间有没有楼层按下
                    for each in self.list_num[aim+1:self.now]:
                        if each>=0:
                            self.none_flag = 0
                    if self.none_flag:
                        self.list_num[aim-1] = aim

            #取消所按楼层
            self.list_num[aim] = -1

 #忽略电梯外按键函数
    def Ignore_out(self,judge):
        if judge:
            if direction==1:
                if self.now<self.next:
                    self.outup = 0
            if direction==0:
                if self.now>self.next:
                    self.downup = 0

 #计算载重函数
    def Heavy(self,list_add_weight):     #list_add_weight:变化重量的列表
        for i in range(len(list_add_weight)):
            list_add_weight[i] = float(list_add_weight[i])
        self.heavy += sum(list_add_weight)
        if self.heavy>=630:
            self.alarm = 1
            self.Open(0)            ###之后还有输入载重变化
            self.Heavy(list_add_weight)
        elif self.heavy>530 and self.heavy<630:
            if self.direction==1:
                for each in list_num[self.now+1:]:
                    if each>=0:
                        self.next = each
                        break
                if self.next-self.now>1:
                    self.Ignore_out(1)
            elif self.direction==0:
                for each in list_num[:self.now]:
                    if each>=0:
                        self.next = each
                        break
                if self.now-self.next>1:
                    self.Ignore_out(1)
        else:
            pass

 #自动回停函数
    def Return_first(self):
        if self.direction==-1:  
            if self.now==0:      #原来停在一楼，忽略
                pass
            else while self.inopen==0\     #按键状态没有变化
                    and self.open==0\     
                    and self.close==0\    
                    and self.outup==0\       
                    and self.outdown==0\     
                    and self.count==0\      
                    and self.help==0\       
                    and self.heavy<10\      
                    and self.alarm==0:
                        if self.start==0:
                            self.start = datetime.now() #计时开始
                        else:
                            self.end = datetime.now()
                        if self.end.min-self.start.min>=10:    #持续10分钟
                            self.list_num[0] = 0
                            self.direction = 0
                            break
                
                    else:                       #按键有变化，计时重新开始
                        self.start = 0
                
 #拼接键盘输入的字符（数字）函数
    def Add_floor(self,num):
        global floor
        floor += num

 #删除操作函数
    def Del(self):
        global floor
        floor = floor[:-1]
    
if __name__=='__main__':
    e = Elevator()
    while True:
        if keyboard.read_key==' ':      #按下空格键，开始监听键盘
            floor = ''
            keyboard.add_hotkey('0',e.Add_floor,args=('0'))
            keyboard.add_hotkey('1',e.Add_floor,args=('1'))
            keyboard.add_hotkey('2',e.Add_floor,args=('2'))
            keyboard.add_hotkey('3',e.Add_floor,args=('3'))
            keyboard.add_hotkey('4',e.Add_floor,args=('4'))
            keyboard.add_hotkey('5',e.Add_floor,args=('5'))
            keyboard.add_hotkey('6',e.Add_floor,args=('6'))
            keyboard.add_hotkey('7',e.Add_floor,args=('7'))
            keyboard.add_hotkey('8',e.Add_floor,args=('8'))
            keyboard.add_hotkey('9',e.Add_floor,args=('9'))
            keyboard.add_hotkey(',',e.Add_floor,args=(','))
            keyboard.add_hotkey(';',e.Add_floor,args=(';'))
            keyboard.add_hotkey('backspace',e.Del_floor)
            recorded = keyboard.record(until='enter')    #按下回车键，停止监听
        else:
            pass

        floor = floor[1:].split(';')
        for i in range(len(floor)):
            floor[i] = floor[i].split(',')
        #floor:[[电梯内按下的楼层],[电梯外按下上行键的楼层],[电梯外按下下行键的楼层]]

    
  
        

    
                    
        
