OPENQASM 2.0;
include "qelib1.inc";
qreg q[4];
cz q[1],q[0];
s q[2];
y q[3];
z q[1];
rx(3.6450344) q[3];
u3(4.6594306,4.6562326,2.4458921) q[2];
rz(4.252048) q[0];
cx q[3],q[0];
u2(1.5739575,0.50630448) q[2];
x q[1];
tdg q[0];
z q[2];
cu1(3.5419809) q[1],q[3];
