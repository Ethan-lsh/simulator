OPENQASM 2.0;
include "qelib1.inc";
qreg q[14];
cx q[4],q[2];
cx q[13],q[12];
cx q[12],q[13];
cx q[13],q[12];
cx q[3],q[0];
cx q[7],q[5];
cx q[5],q[7];
cx q[7],q[5];
rz(3.3239611) q[8];
cz q[6],q[11];
cx q[10],q[1];
cx q[1],q[10];
cx q[10],q[1];
h q[9];
cz q[11],q[10];
h q[2];
y q[4];
cz q[5],q[8];
x q[9];
cx q[6],q[13];
cx q[13],q[6];
cx q[6],q[13];
y q[12];
t q[7];
cz q[1],q[3];
x q[0];
h q[6];
cx q[5],q[12];
cx q[12],q[5];
cx q[5],q[12];
x q[4];
t q[7];
cx q[1],q[3];
sdg q[8];
id q[10];
cz q[13],q[0];
t q[2];
s q[9];
y q[11];
cx q[7],q[5];
cx q[5],q[7];
cx q[7],q[5];
cx q[12],q[8];
cx q[8],q[12];
cx q[12],q[8];
cx q[4],q[11];
x q[10];
u1(0.14497786) q[0];
rx(1.9079876) q[6];
t q[13];
rz(6.2333091) q[1];
h q[2];
s q[9];
rx(4.9106528) q[3];
cx q[10],q[8];
rx(5.3865838) q[13];
u1(4.8516907) q[9];
sdg q[3];
rz(0.27133334) q[6];
sdg q[0];
cx q[1],q[12];
cz q[2],q[11];
cz q[7],q[5];
rx(6.0077441) q[4];
z q[10];
cx q[6],q[0];
sdg q[12];
h q[13];
cx q[11],q[3];
cx q[3],q[11];
cx q[11],q[3];
cz q[5],q[2];
cx q[4],q[8];
cz q[1],q[7];
s q[9];
cz q[6],q[10];
tdg q[3];
h q[1];
cx q[5],q[12];
cx q[12],q[5];
cx q[5],q[12];
cz q[9],q[0];
tdg q[11];
rx(0.56364168) q[8];
tdg q[7];
x q[4];
h q[2];
x q[13];
cz q[7],q[8];
y q[0];
tdg q[6];
rx(3.0028867) q[13];
rx(4.4492071) q[1];
cx q[2],q[5];
cx q[5],q[2];
cx q[2],q[5];
cx q[3],q[11];
cx q[11],q[3];
cx q[3],q[11];
cx q[9],q[12];
cx q[12],q[9];
cx q[9],q[12];
tdg q[10];
u1(1.3029603) q[4];
cx q[5],q[12];
cx q[6],q[1];
cx q[1],q[6];
cx q[6],q[1];
cx q[8],q[13];
cx q[10],q[4];
rz(1.3062627) q[11];
cx q[0],q[3];
cx q[3],q[0];
cx q[0],q[3];
cz q[9],q[7];
z q[2];
cx q[2],q[10];
cx q[10],q[2];
cx q[2],q[10];
t q[7];
s q[8];
cz q[11],q[12];
cx q[1],q[0];
cz q[13],q[4];
z q[3];
cx q[5],q[6];
cx q[6],q[5];
cx q[5],q[6];
u1(0.57798555) q[9];
sdg q[13];
rx(1.1639844) q[7];
id q[8];
h q[12];
x q[4];
z q[9];
sdg q[10];
cx q[11],q[1];
cx q[1],q[11];
cx q[11],q[1];
s q[2];
cx q[3],q[6];
cx q[6],q[3];
cx q[3],q[6];
tdg q[5];
rx(3.255749) q[0];
s q[2];
z q[10];
cz q[5],q[6];
cx q[1],q[8];
cx q[8],q[1];
cx q[1],q[8];
rx(5.3737578) q[3];
y q[12];
cz q[9],q[4];
x q[0];
sdg q[11];
rx(2.7076215) q[7];
u1(0.043372523) q[13];
rx(0.89318887) q[10];
cx q[7],q[9];
cx q[9],q[7];
cx q[7],q[9];
rz(3.8529107) q[13];
cz q[1],q[8];
cx q[6],q[5];
cx q[2],q[3];
rx(4.3207474) q[11];
cz q[12],q[4];
x q[0];
s q[0];
cz q[9],q[2];
cx q[4],q[5];
cx q[8],q[6];
y q[10];
cz q[13],q[3];
cx q[7],q[1];
u1(3.2247366) q[11];
tdg q[12];