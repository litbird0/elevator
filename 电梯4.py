import sys, time, msvcrt
from datetime import datetime

class Elevator:
    def __init__(self):
        #初始化
        self.list_num = [-1]*6
        self.inopen = 0  #开门键（电梯里）
        self.open = 0     #开门功能
        self.close = 0    #关门功能
        self.outup = 0       #上行键（电梯外）
        self.force_outup = 0  #为1时，忽略电梯外按下的上行键
        self.outdown = 0     #下行键（电梯外）
        self.force_outdown = 0  #为1时，忽略电梯外按下的下行键
        self.direction = -1 #方向（向下为0；向上为1,停止为-1）
        self.now = 0        #现在到达的楼层
        self.count = 0      #已经按下的楼层数
        self.help = 0       #按铃求助功能
        self.heavy = 0      #载重
        self.weight = 0     #输入的重量
        self.alarm = 0      #警报功能
        self.cancel = 0     #手动取消按键
        self.start = 0      #自动回停的条件：计时开始
        self.end = 0        #自动回停的条件：计时结束
        self.floor = []     #输入的楼层
        self.rreturn = 0    #自动回停标志
        
 #开门函数,sound==1:开启语音提示
    def Open(self,sound):
        self.close = 0
        self.open = 1
        print("开门")
        if sound:
            self.Sound()
        time.sleep(2)

        print('self.count:',self.count)
        print('self.direction:',self.direction)
        print('self.now:',self.now)
        print('self.list_num:',self.list_num)

        if self.rreturn:
            self.Close()

        else:
       #输入重量的变化
            self.weight = input('请输入重量的变化：')
            if self.weight!='':
                self.weight = self.weight.split(',')
                self.Heavy(self.weight)
            self.Close()
            self.open = 0
            self.rreturn = 0

 #关门函数   
    def Close(self):
        if self.close:
            pass
        else:
            self.close = 1
            print("关门")
            time.sleep(2)

 #开门和关门；只要按下关门键，就关门
    def Open_or_Close(self):
        if self.close==1:
            self.close = 0
            self.Close()
        elif (self.inopen==1
            or (self.direction==0 and self.outdown==1)
            or (self.direction==1 and self.outup==1)):
            self.Open()

 #语音提示函数
    def Sound(self):   
        print("%d楼到了~~"%(self.now+1))
        self.list_num[self.now] = -1
        self.count -= 1
        self.flag = 0       #没有楼层按下的标志
        for each in self.list_num:
            if each!=-1:
                self.flag = 1
        if not self.flag:
            self.direction = -1   #没有楼层按下，暂时停在该楼层

 #按铃求助函数
    def Help(self):
        self.help = 1
        print("求助！求助！")
        time.sleep(3)
        self.help = 0
            

 #电梯外上行键
    def OutUp(self,aim):
        if not self.force_outup:
            print("电梯外上行")
            self.outup = 1
            self.Button(aim)
            self.outup = 0   #自动取消按下
        
 #电梯外下行键
    def OutDown(self,aim):
        if not self.force_outdown:
            print('电梯外下行')
            self.outdown = 1
            self.Button(aim)
            self.outdown = 0   #自动取消按下

 #按键函数
    def Button(self,aim):    
        #原来停止，最先按下的楼层决定运行方向
        if self.direction==-1:
            if aim==self.now:
                self.Open(0)  #不开语音提示
            else:
                if aim>self.now:
                    self.direction = 1  #确定方向：上行
                    print('确定方向为上行')
                    if self.list_num[aim]==-1:
                        self.list_num[aim] = aim
                        self.count += 1
                else:
                    self.direction = 0  #确定方向：下行
                    print('确定方向为下行')
                    if self.list_num[aim]==-1:
                        self.list_num[aim] = aim
                        self.count += 1

        #原来上行，如果按下下行键，忽略；否则不忽略
        elif self.direction==1:
            if not self.outdown:
                if aim>self.now:
                    if self.list_num[aim]==-1:
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
                    if self.list_num[aim]==-1:
                        self.list_num[aim] = aim
                        self.count += 1
                else:
                    pass
            else:
                pass
        print('按键')
        print('self.count:',self.count)
        print('aim:',aim)
        print('self.direction:',self.direction)
        print('self.now:',self.now)
        print('self.list_num:',self.list_num)

 #手动取消楼层按键函数
    def Cannel(self,aim):      
        if self.list_num[aim]!=-1:       #原来是按下状态
            
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
            self.cancel = 1
            self.count -= 1

        print('取消')
        print('aim:',aim)
        print('self.count',self.count)
        print('self.direction:',self.direction)
        print('self.now:',self.now)
        print('self.list_num:',self.list_num)

 #忽略电梯外按键函数
    def Ignore_out(self,judge):
        print("忽略电梯外按键")
        if judge:
            if self.direction==1:
                if self.now<self.next:
                    self.force_outup = 1     #忽略电梯外按下的上行键
            if self.direction==0:
                if self.now>self.next:
                    self.force_downup = 1    #忽略电梯外按下的下行键

 #计算载重函数
    def Heavy(self,list_add_weight):     #list_add_weight:变化重量的列表
        for i in range(len(list_add_weight)):
            list_add_weight[i] = float(list_add_weight[i])
        self.heavy += sum(list_add_weight)
        print(self.heavy)
        if self.heavy>=630:
            self.alarm = 1
            print("已超重~~")
            self.Open(0)            
        elif self.heavy>530 and self.heavy<630:
            print("hhh")
            if self.direction==1:
                for each in self.list_num[self.now+1:]:
                    if each>=0:
                        self.next = each
                        break
                if self.next-self.now>1:
                    self.Ignore_out(1)
            elif self.direction==0:
                for each in self.list_num[:self.now]:
                    if each>=0:
                        self.next = each
                        break
                if self.now-self.next>1:
                    self.Ignore_out(1)
        else:
            self.force_outup = 0
            self.force_outdown = 0

 #监听输入函数
    def ReadInput(self,caption,default,timeout=3):  #超时3秒没有输入则跳过
        start_time = time.time()
       # sys.stdout.write('%s(%s):'%(caption, default));
        input=''
        while True:
            if msvcrt.kbhit():     #键盘按下返回1，否则返回0
                chr = msvcrt.getche()
                if ord(chr) == 13: # enter_key
                    break
                #elif ord(chr) >= 32: #space_char
                else:
                    input += str(chr)
                    print('')
                    #print('写入')
            elif (len(input) == 0 and (time.time() - start_time) > timeout):
               # print('超时')
                break

        print('')  # needed to move to next line
        if len(input) > 0:
            return input
        else:
            return default
        

 #转换输入，控制按键
    def Trans(self):
        self.a=self.ReadInput("",'')[1:]
        self.b = self.a.replace("'",'')
        self.b = self.b.split('b')
        self.floor += self.b
        while True:
            if len(self.floor):

                #电梯内按下楼层
                if (self.floor[0]=='1'
                    or self.floor[0]=='2'
                    or self.floor[0]=='3'
                    or self.floor[0]=='4'
                    or self.floor[0]=='5'
                    or self.floor[0]=='6'):
                    self.Cannel(int(self.floor[0])-1)
                    if not self.cancel:
                        self.Button(int(self.floor[0])-1)
                    self.cancel = 0

                #电梯内按下开门
                elif self.floor[0]=='o':
                    self.inopen = 1
                    self.Open_or_Close()
                    self.inopen = 0

                #电梯内按下关门
                elif self.floor[0]=='c':
                    self.close = 1
                    self.Open_or_Close()

                #电梯外按下上行
                elif self.floor[0]=='u':
                    if (self.floor[1]=='1'
                        or self.floor[1]=='2'
                        or self.floor[1]=='3'
                        or self.floor[1]=='4'
                        or self.floor[1]=='5'
                        or self.floor[1]=='6'):
                        self.OutUp(int(self.floor[1])-1)
                        del self.floor[1]

                #电梯外按下下行
                elif self.floor[0]=='d':
                    if (self.floor[1]=='1'
                        or self.floor[1]=='2'
                        or self.floor[1]=='3'
                        or self.floor[1]=='4'
                        or self.floor[1]=='5'
                        or self.floor[1]=='6'):
                        self.OutDown(int(self.floor[1])-1)
                        del self.floor[1]

                #按下求助
                elif self.floor[0]=='h':
                    self.Help()

                del self.floor[0]

            else:
                break
                
 
if __name__=='__main__':
    e = Elevator()
    e.start = datetime.now()
    while True:
        e.Trans()     #可输入按键

        #自动回停
        if not e.start:
            e.start = datetime.now()
        e.end = datetime.now()
        if e.end.minute-e.start.minute>=1:
            if e.now>0:
                e.list_num[0] = 0
                e.direction = 0
                e.rreturn = 1
                print("自动回停")
        
        #电梯上行
        if e.direction==1:
            e.start = 0
            time.sleep(2)
            while True:
                e.Open(0)
                e.now += 1
                e.Trans()    #可输入按键
                if e.list_num[e.now]==e.now:  #到达楼层
                    e.Open(1)
                    break

        #电梯下行
        if e.direction==0:
            e.start = 0
            time.sleep(2)
            while True:
                e.Open(0)
                e.now -= 1
                e.Trans()    #可输入按键
                if e.list_num[e.now]==e.now:   #到达楼层
                    e.Open(1)
                    break

    
                    
        

