import pandapower as pp
import pandapower.networks as pn
net=pn.case9()
pp.runpp(net)
