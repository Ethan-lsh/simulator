OPENQASM 2.0;
include "qelib1.inc";
qreg q0[25];
creg c0[5];
x q0[21];
x q0[20];
x q0[16];
ccx q0[20],q0[15],q0[1];
ccx q0[20],q0[16],q0[4];
ccx q0[20],q0[17],q0[7];
ccx q0[20],q0[18],q0[10];
ccx q0[20],q0[19],q0[13];
ccx q0[1],q0[2],q0[3];
cx q0[1],q0[2];
ccx q0[0],q0[2],q0[3];
ccx q0[4],q0[5],q0[6];
cx q0[4],q0[5];
ccx q0[3],q0[5],q0[6];
ccx q0[7],q0[8],q0[9];
cx q0[7],q0[8];
ccx q0[6],q0[8],q0[9];
ccx q0[10],q0[11],q0[12];
cx q0[10],q0[11];
ccx q0[9],q0[11],q0[12];
cx q0[13],q0[14];
cx q0[12],q0[14];
ccx q0[9],q0[11],q0[12];
cx q0[10],q0[11];
ccx q0[10],q0[11],q0[12];
cx q0[10],q0[11];
cx q0[9],q0[11];
ccx q0[6],q0[8],q0[9];
cx q0[7],q0[8];
ccx q0[7],q0[8],q0[9];
cx q0[7],q0[8];
cx q0[6],q0[8];
ccx q0[3],q0[5],q0[6];
cx q0[4],q0[5];
ccx q0[4],q0[5],q0[6];
cx q0[4],q0[5];
cx q0[3],q0[5];
ccx q0[0],q0[2],q0[3];
cx q0[1],q0[2];
ccx q0[1],q0[2],q0[3];
cx q0[1],q0[2];
cx q0[0],q0[2];
ccx q0[20],q0[15],q0[1];
ccx q0[20],q0[16],q0[4];
ccx q0[20],q0[17],q0[7];
ccx q0[20],q0[18],q0[10];
ccx q0[20],q0[19],q0[13];
ccx q0[21],q0[15],q0[4];
ccx q0[21],q0[16],q0[7];
ccx q0[21],q0[17],q0[10];
ccx q0[21],q0[18],q0[13];
ccx q0[1],q0[2],q0[3];
cx q0[1],q0[2];
ccx q0[0],q0[2],q0[3];
ccx q0[4],q0[5],q0[6];
cx q0[4],q0[5];
ccx q0[3],q0[5],q0[6];
ccx q0[7],q0[8],q0[9];
cx q0[7],q0[8];
ccx q0[6],q0[8],q0[9];
ccx q0[10],q0[11],q0[12];
cx q0[10],q0[11];
ccx q0[9],q0[11],q0[12];
cx q0[13],q0[14];
cx q0[12],q0[14];
ccx q0[9],q0[11],q0[12];
cx q0[10],q0[11];
ccx q0[10],q0[11],q0[12];
cx q0[10],q0[11];
cx q0[9],q0[11];
ccx q0[6],q0[8],q0[9];
cx q0[7],q0[8];
ccx q0[7],q0[8],q0[9];
cx q0[7],q0[8];
cx q0[6],q0[8];
ccx q0[3],q0[5],q0[6];
cx q0[4],q0[5];
ccx q0[4],q0[5],q0[6];
cx q0[4],q0[5];
cx q0[3],q0[5];
ccx q0[0],q0[2],q0[3];
cx q0[1],q0[2];
ccx q0[1],q0[2],q0[3];
cx q0[1],q0[2];
cx q0[0],q0[2];
ccx q0[21],q0[15],q0[4];
ccx q0[21],q0[16],q0[7];
ccx q0[21],q0[17],q0[10];
ccx q0[21],q0[18],q0[13];
ccx q0[22],q0[15],q0[7];
ccx q0[22],q0[16],q0[10];
ccx q0[22],q0[17],q0[13];
ccx q0[1],q0[2],q0[3];
cx q0[1],q0[2];
ccx q0[0],q0[2],q0[3];
ccx q0[4],q0[5],q0[6];
cx q0[4],q0[5];
ccx q0[3],q0[5],q0[6];
ccx q0[7],q0[8],q0[9];
cx q0[7],q0[8];
ccx q0[6],q0[8],q0[9];
ccx q0[10],q0[11],q0[12];
cx q0[10],q0[11];
ccx q0[9],q0[11],q0[12];
cx q0[13],q0[14];
cx q0[12],q0[14];
ccx q0[9],q0[11],q0[12];
cx q0[10],q0[11];
ccx q0[10],q0[11],q0[12];
cx q0[10],q0[11];
cx q0[9],q0[11];
ccx q0[6],q0[8],q0[9];
cx q0[7],q0[8];
ccx q0[7],q0[8],q0[9];
cx q0[7],q0[8];
cx q0[6],q0[8];
ccx q0[3],q0[5],q0[6];
cx q0[4],q0[5];
ccx q0[4],q0[5],q0[6];
cx q0[4],q0[5];
cx q0[3],q0[5];
ccx q0[0],q0[2],q0[3];
cx q0[1],q0[2];
ccx q0[1],q0[2],q0[3];
cx q0[1],q0[2];
cx q0[0],q0[2];
ccx q0[22],q0[15],q0[7];
ccx q0[22],q0[16],q0[10];
ccx q0[22],q0[17],q0[13];
ccx q0[23],q0[15],q0[10];
ccx q0[23],q0[16],q0[13];
ccx q0[1],q0[2],q0[3];
cx q0[1],q0[2];
ccx q0[0],q0[2],q0[3];
ccx q0[4],q0[5],q0[6];
cx q0[4],q0[5];
ccx q0[3],q0[5],q0[6];
ccx q0[7],q0[8],q0[9];
cx q0[7],q0[8];
ccx q0[6],q0[8],q0[9];
ccx q0[10],q0[11],q0[12];
cx q0[10],q0[11];
ccx q0[9],q0[11],q0[12];
cx q0[13],q0[14];
cx q0[12],q0[14];
ccx q0[9],q0[11],q0[12];
cx q0[10],q0[11];
ccx q0[10],q0[11],q0[12];
cx q0[10],q0[11];
cx q0[9],q0[11];
ccx q0[6],q0[8],q0[9];
cx q0[7],q0[8];
ccx q0[7],q0[8],q0[9];
cx q0[7],q0[8];
cx q0[6],q0[8];
ccx q0[3],q0[5],q0[6];
cx q0[4],q0[5];
ccx q0[4],q0[5],q0[6];
cx q0[4],q0[5];
cx q0[3],q0[5];
ccx q0[0],q0[2],q0[3];
cx q0[1],q0[2];
ccx q0[1],q0[2],q0[3];
cx q0[1],q0[2];
cx q0[0],q0[2];
ccx q0[23],q0[15],q0[10];
ccx q0[23],q0[16],q0[13];
ccx q0[24],q0[15],q0[13];
ccx q0[1],q0[2],q0[3];
cx q0[1],q0[2];
ccx q0[0],q0[2],q0[3];
ccx q0[4],q0[5],q0[6];
cx q0[4],q0[5];
ccx q0[3],q0[5],q0[6];
ccx q0[7],q0[8],q0[9];
cx q0[7],q0[8];
ccx q0[6],q0[8],q0[9];
ccx q0[10],q0[11],q0[12];
cx q0[10],q0[11];
ccx q0[9],q0[11],q0[12];
cx q0[13],q0[14];
cx q0[12],q0[14];
ccx q0[9],q0[11],q0[12];
cx q0[10],q0[11];
ccx q0[10],q0[11],q0[12];
cx q0[10],q0[11];
cx q0[9],q0[11];
ccx q0[6],q0[8],q0[9];
cx q0[7],q0[8];
ccx q0[7],q0[8],q0[9];
cx q0[7],q0[8];
cx q0[6],q0[8];
ccx q0[3],q0[5],q0[6];
cx q0[4],q0[5];
ccx q0[4],q0[5],q0[6];
cx q0[4],q0[5];
cx q0[3],q0[5];
ccx q0[0],q0[2],q0[3];
cx q0[1],q0[2];
ccx q0[1],q0[2],q0[3];
cx q0[1],q0[2];
cx q0[0],q0[2];
ccx q0[24],q0[15],q0[13];