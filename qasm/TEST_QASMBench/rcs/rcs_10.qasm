OPENQASM 2.0;
include "qelib1.inc";
qreg q[10];
cz q[7],q[2];
cx q[0],q[9];
cx q[9],q[0];
cx q[0],q[9];
cx q[1],q[8];
cx q[8],q[1];
cx q[1],q[8];
cx q[5],q[6];
cx q[6],q[5];
cx q[5],q[6];
y q[4];
tdg q[3];
t q[8];
s q[0];
z q[4];
s q[1];
h q[7];
s q[3];
x q[5];
cx q[6],q[9];
cx q[9],q[6];
cx q[6],q[9];
id q[2];
cx q[0],q[8];
h q[3];
cz q[5],q[2];
cx q[6],q[4];
cx q[4],q[6];
cx q[6],q[4];
cx q[1],q[7];
cx q[7],q[1];
cx q[1],q[7];
y q[9];
cz q[6],q[2];
sdg q[5];
cz q[4],q[8];
s q[3];
cx q[7],q[9];
cx q[9],q[7];
cx q[7],q[9];
cx q[1],q[0];
cx q[4],q[5];
cx q[5],q[4];
cx q[4],q[5];
x q[6];
cx q[3],q[0];
s q[9];
cx q[8],q[2];
cx q[2],q[8];
cx q[8],q[2];
tdg q[1];
id q[7];
z q[8];
cz q[7],q[3];
cz q[5],q[4];
rz(2.74546) q[2];
cx q[0],q[1];
cx q[1],q[0];
cx q[0],q[1];
id q[6];
t q[9];
cx q[3],q[4];
cx q[4],q[3];
cx q[3],q[4];
cx q[2],q[0];
t q[9];
cz q[5],q[1];
rx(0.23421374) q[7];
rx(3.520332) q[8];
tdg q[6];
cz q[3],q[8];
id q[1];
cz q[7],q[6];
cx q[2],q[5];
cz q[0],q[9];
tdg q[4];
z q[0];
rz(2.3280492) q[8];
cz q[1],q[6];
cx q[5],q[3];
cx q[2],q[7];
h q[4];
z q[9];
rx(0.87971547) q[7];
y q[6];
cx q[9],q[3];
rx(0.97744743) q[1];
sdg q[5];
cz q[2],q[8];
rx(1.0893066) q[0];
s q[4];
