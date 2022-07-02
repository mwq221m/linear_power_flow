import pandapower as pp
import pandas as pd
lines_data=pd.read_excel('test.xlsx')
nodes_data=pd.read_excel('test.xlsx',sheet_name=1)
net=pp.create_empty_network()
vb=110;sb=100;zb=vb**2/sb#例题给定的标幺值已经给定了sb 要更换必须做相应换算
for i in range(len(nodes_data)):
    pp.create_bus(net,vn_kv=110,index=i+1)
for i in range(len(lines_data)):
    temp=lines_data.iloc[i]
    start=temp['起始节点']
    start=int(start)
    end=temp['终止节点']
    end=int(end)
    r=temp['r']*zb
    x=temp['x']*zb
    pp.create_line_from_parameters(net,from_bus=start,to_bus=end,length_km=1,r_ohm_per_km=r,x_ohm_per_km=x,c_nf_per_km=0,max_i_ka=10,in_service=True)

pp.create_gen(net,bus=2,p_mw=20,vm_pu=1.03)
pp.create_load(net,bus=2,p_mw=50,q_mvar=20)
pp.create_load(net,bus=3,p_mw=60,q_mvar=25)
pp.create_ext_grid(net,bus=1,vm_pu=1.05,va_degree=0)
pp.runpp(net)
print(net.res_bus)
print(net.res_line)

