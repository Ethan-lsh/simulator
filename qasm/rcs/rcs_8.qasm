OPENQASM 2.0;
include "qelib1.inc";
qreg q[8];
z q[1];
cz q[5],q[0];
u3(5.6043552,0.52028826,3.7526479) q[3];
cx q[6],q[7];
cx q[2],q[4];
cx q[4],q[2];
cx q[2],q[4];
u2(0.8768997,0.52350972) q[1];
cz q[7],q[5];
ch q[0],q[3];
ry(4.079108) q[6];
cu1(5.2960049) q[2],q[4];
ry(3.3630457) q[1];
cy q[0],q[5];
cx q[3],q[2];
ry(3.8365163) q[7];
cy q[6],q[4];
sdg q[7];
z q[3];
cu3(4.035155,0.027213155,6.098345) q[1],q[0];
cy q[4],q[2];
cy q[6],q[5];
x q[4];
cx q[7],q[2];
sdg q[0];
ch q[6],q[3];
x q[5];
u1(5.4271792) q[1];
ch q[7],q[3];
y q[0];
u2(0.54138273,3.409461) q[2];
ry(3.9381818) q[4];
rz(1.8034027) q[6];
cu3(6.1956898,2.5313568,2.4810138) q[1],q[5];
cx q[2],q[6];
cx q[6],q[2];
cx q[2],q[6];
cz q[0],q[1];
y q[3];
cy q[7],q[5];
h q[4];
sdg q[5];
ry(5.4717018) q[0];
cx q[3],q[1];
cx q[1],q[3];
cx q[3],q[1];
crz(3.4447097) q[4],q[6];
x q[2];
s q[7];