import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
class LinearPowerFlow():
    def __init__(self,lines_data,nodes_data):
        self.lines_data = lines_data
        self.nodes_data = nodes_data
        self.number_of_nodes=len(self.nodes_data)
        self.number_of_lines=len(self.lines_data)
        self.B=np.zeros((self.number_of_nodes,self.number_of_nodes))
        self.X = np.zeros((self.number_of_nodes, self.number_of_nodes))
        self.S=np.zeros((self.number_of_lines,self.number_of_nodes-1))
        self.p=np.zeros(self.number_of_nodes)
        #self.p_temporary=np.zeros(self.number_of_nodes)
        self.theta=np.zeros(self.number_of_nodes)
        #self.theta_temporary=np.zeros(self.number_of_nodes)
        self.slack_bus=1


    def read_lines_data(self):
        for i in range(len(self.lines_data)):
            temp=lines_data.iloc[i]
            status=temp['status']
            if status==0:
                continue
            start=temp['起始节点']
            start=int(start)
            #print(start)
            end=temp['终止节点']
            end=int(end)
            #print(end)
            x=temp['x']
            self.B[start-1,end-1]+=-1/x
            self.B[end-1,start-1]+=-1/x
            self.B[start-1,start-1]+=1/x
            self.B[end-1,end-1]+=1/x
        #self.X=np.linalg.inv(self.B)#此时B矩阵行列式为零 求逆矩阵有问题
        self.X[self.slack_bus:,self.slack_bus:]=np.linalg.inv(self.B[self.slack_bus:,self.slack_bus:])

    def read_nodes_data(self):
        for i in range(len(self.nodes_data)):
            temp=self.nodes_data.iloc[i]
            node=temp['节点']
            node=int(node)
            p=temp['p']
            self.p[node-1]=p








    def run_power_flow(self):
        temp_idx = [i for i in range(len(self.nodes_data)) if i != self.slack_bus-1]
        #print('temp_idx',temp_idx)
        # self.theta[temp_idx].reshape(-1,1)=np.linalg.inv(self.B[temp_idx,temp_idx])@self.p[temp_idx]
        #print('B',self.B[(temp_idx,temp_idx)])
        #print(self.p[temp_idx].reshape(-1,1))
        temp_vector =np.linalg.inv(self.B[self.slack_bus:,self.slack_bus:])@self.p[temp_idx].reshape(-1,1)#当平衡节点不为1号时这样写不对
        #temp_vector=temp_vector.reshape(1)
        #self.theta[temp_idx]=temp_vector
        for i in range(len(temp_vector)):
            temp_idx2=temp_idx[i]
            #self.theta[temp_idx2]=temp_vector[i]*180/np.pi#后续需要对支路功率进行计算 不能在这里换算成角度
            self.theta[temp_idx2] = temp_vector[i]

    def temp_sensitivity_calculation(self,idx):
        p_temp=np.zeros(self.number_of_nodes)
        p_temp[idx]=1
        theta_temp=np.zeros(self.number_of_nodes)
        line_sensitivity=np.zeros(self.number_of_lines)
        temp_idx = [i for i in range(len(self.nodes_data)) if i != self.slack_bus - 1]
        temp_vector = np.linalg.inv(self.B[self.slack_bus:, self.slack_bus:]) @ p_temp[temp_idx].reshape(-1, 1)
        for i in range(len(temp_vector)):
            temp_idx2=temp_idx[i]
            #self.theta[temp_idx2]=temp_vector[i]*180/np.pi#后续需要对支路功率进行计算 不能在这里换算成角度
            theta_temp[temp_idx2] = temp_vector[i]
        for i in range(self.number_of_lines):
            temp = self.lines_data.iloc[i]
            start = temp['起始节点']
            start = int(start)
            end = temp['终止节点']
            end = int(end)
            x = temp['x']
            power = (theta_temp[start - 1] - theta_temp[end - 1]) / x
            line_sensitivity[i]=power
        return line_sensitivity

    def sensitivity_calculation(self):
        for i in range(self.number_of_nodes-1):#平衡节点不参与
            line_sensitivity=self.temp_sensitivity_calculation(idx=i+1)
            self.S[:,i]=line_sensitivity










    def show_power_flow(self):
        mark='**************************'
        print(mark)
        for i in range(len(self.lines_data)):
            temp=self.lines_data.iloc[i]
            start=temp['起始节点']
            start=int(start)
            end=temp['终止节点']
            end=int(end)
            x=temp['x']
            power=(self.theta[start-1]-self.theta[end-1])/x
            print('从节点%s到节点%s的有功功率为%s'%(start,end,power))
        for i in range(len(self.nodes_data)):
            theta=self.theta[i]*180/np.pi
            print('%s号节点的相角为%s度'%(i+1,theta))
        print(mark)





lines_data=pd.read_excel('test.xlsx')
nodes_data=pd.read_excel('test.xlsx',sheet_name=1)
print(lines_data)
print(nodes_data)
test=LinearPowerFlow(lines_data=lines_data,nodes_data=nodes_data)
test.read_lines_data()
#print(test.B)
test.read_nodes_data()
#print(test.p)
test.run_power_flow()
#print(test.theta)
test.show_power_flow()
#sensitivity1=test.temp_sensitivity_calculation(idx=1)
#print(sensitivity1)
#sensitivity2=test.temp_sensitivity_calculation(idx=2)
#print(sensitivity2)
test.sensitivity_calculation()
print(test.S)
#test.sensitivity_calculation()
#print(test.S)
