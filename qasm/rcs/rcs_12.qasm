OPENQASM 2.0;
include "qelib1.inc";
qreg q[12];
s q[7];
cx q[6],q[3];
cx q[3],q[6];
cx q[6],q[3];
cz q[8],q[10];
cx q[2],q[1];
u1(0.5901865) q[4];
cx q[9],q[0];
cx q[5],q[11];
cz q[4],q[3];
y q[8];
cz q[5],q[1];
cz q[11],q[6];
cz q[0],q[10];
cx q[7],q[2];
cx q[2],q[7];
cx q[7],q[2];
tdg q[9];
t q[9];
sdg q[5];
x q[8];
cx q[7],q[10];
cx q[10],q[7];
cx q[7],q[10];
cz q[1],q[2];
cx q[4],q[0];
cx q[0],q[4];
cx q[4],q[0];
cx q[11],q[3];
id q[6];
t q[1];
t q[2];
cx q[11],q[3];
cx q[3],q[11];
cx q[11],q[3];
cx q[9],q[4];
cx q[4],q[9];
cx q[9],q[4];
u1(5.2438851) q[5];
cz q[7],q[6];
t q[0];
u1(2.9220637) q[10];
id q[8];
s q[8];
h q[10];
rx(5.7959938) q[11];
t q[5];
x q[1];
id q[4];
u1(4.0815595) q[7];
s q[9];
y q[0];
cx q[6],q[2];
tdg q[3];
cx q[6],q[3];
cz q[1],q[7];
rx(0.33320643) q[0];
y q[11];
t q[9];
rz(2.8827741) q[4];
rz(5.4840564) q[10];
x q[8];
cx q[2],q[5];
cx q[5],q[2];
cx q[2],q[5];
cz q[5],q[4];
tdg q[10];
u1(4.5833205) q[2];
sdg q[9];
h q[11];
cx q[0],q[8];
cx q[8],q[0];
cx q[0],q[8];
z q[1];
cz q[3],q[6];
y q[7];
rx(1.8486094) q[0];
cx q[7],q[6];
cx q[6],q[7];
cx q[7],q[6];
cx q[2],q[4];
cx q[4],q[2];
cx q[2],q[4];
id q[3];
z q[5];
rx(1.6032335) q[9];
cz q[10],q[1];
t q[8];
x q[11];
cx q[10],q[7];
cx q[1],q[6];
cx q[8],q[5];
cx q[5],q[8];
cx q[8],q[5];
cx q[2],q[11];
tdg q[4];
cx q[9],q[3];
cx q[3],q[9];
cx q[9],q[3];
z q[0];
z q[9];
cz q[10],q[11];
cz q[5],q[1];
cx q[3],q[2];
cx q[2],q[3];
cx q[3],q[2];
x q[8];
cx q[0],q[6];
cx q[6],q[0];
cx q[0],q[6];
y q[4];
rx(1.2016961) q[7];
cx q[3],q[4];
cx q[6],q[2];
cx q[2],q[6];
cx q[6],q[2];
cx q[1],q[11];
cx q[11],q[1];
cx q[1],q[11];
x q[10];
cx q[7],q[0];
cz q[8],q[9];
x q[5];
y q[11];
cx q[9],q[6];
cx q[6],q[9];
cx q[9],q[6];
cx q[4],q[3];
cx q[3],q[4];
cx q[4],q[3];
cz q[1],q[5];
z q[7];
cz q[10],q[8];
cx q[2],q[0];
