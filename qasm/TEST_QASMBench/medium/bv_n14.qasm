//@author Raymond Harry Rudy rudyhar@jp.ibm.com
//Bernstein-Vazirani with 14 qubits.
//Hidden string is 1111111111111
OPENQASM 2.0;
include "qelib1.inc";
qreg qr[14];
creg cr[13];
h qr[0];
h qr[1];
h qr[2];
h qr[3];
h qr[4];
h qr[5];
h qr[6];
h qr[7];
h qr[8];
h qr[9];
h qr[10];
h qr[11];
h qr[12];
x qr[13];
h qr[13];

cx qr[0], qr[13];
cx qr[1], qr[13];
cx qr[2], qr[13];
cx qr[3], qr[13];
cx qr[4], qr[13];
cx qr[5], qr[13];
cx qr[6], qr[13];
cx qr[7], qr[13];
cx qr[8], qr[13];
cx qr[9], qr[13];
cx qr[10], qr[13];
cx qr[11], qr[13];
cx qr[12], qr[13];

h qr[0];
h qr[1];
h qr[2];
h qr[3];
h qr[4];
h qr[5];
h qr[6];
h qr[7];
h qr[8];
h qr[9];
h qr[10];
h qr[11];
h qr[12];
