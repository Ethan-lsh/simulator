OPENQASM 2.0;
include "qelib1.inc";
qreg q[6];
t q[5];
y q[4];
z q[2];
cz q[3],q[1];
z q[0];
cx q[0],q[2];
cx q[2],q[0];
cx q[0],q[2];
sdg q[5];
rx(3.7894489) q[4];
cx q[3],q[1];
rx(3.9833591) q[3];
z q[4];
y q[0];
h q[5];
cz q[2],q[1];
tdg q[3];
s q[2];
t q[0];
cz q[4],q[1];
x q[5];
cz q[5],q[4];
z q[3];
cz q[1],q[2];
x q[0];
cx q[2],q[1];
cx q[1],q[2];
cx q[2],q[1];
cz q[3],q[4];
cz q[0],q[5];
