OPENQASM 2.0;
include "qelib1.inc";
qreg q[8];
cx q[6],q[3];
cx q[2],q[0];
cx q[0],q[2];
cx q[2],q[0];
u1(4.6148987) q[5];
cx q[4],q[1];
x q[7];
u1(4.1993342) q[7];
rz(1.6639062) q[3];
cx q[5],q[6];
cx q[6],q[5];
cx q[5],q[6];
z q[4];
cx q[2],q[1];
id q[0];
cx q[2],q[4];
x q[3];
rx(4.7823617) q[6];
h q[0];
u1(0.15755723) q[7];
rz(2.3582636) q[5];
rz(6.0367375) q[1];
rz(0.38117512) q[4];
cx q[0],q[7];
u1(0.20927044) q[3];
h q[2];
rx(5.6817173) q[1];
cx q[6],q[5];
h q[7];
cx q[2],q[5];
cx q[3],q[6];
u1(3.2595893) q[4];
h q[0];
s q[1];
cx q[4],q[3];
cx q[3],q[4];
cx q[4],q[3];
t q[7];
z q[2];
t q[0];
cx q[5],q[6];
t q[1];
h q[3];
cx q[6],q[4];
cx q[4],q[6];
cx q[6],q[4];
id q[7];
cx q[2],q[1];
cx q[1],q[2];
cx q[2],q[1];
cz q[5],q[0];
rz(0.73492942) q[7];
h q[1];
t q[4];
rz(5.1094059) q[0];
rz(5.7293012) q[3];
cx q[5],q[6];
cx q[6],q[5];
cx q[5],q[6];
tdg q[2];
