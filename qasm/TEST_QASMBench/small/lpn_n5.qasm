// Name of Experiment: LPN circuit 2 v1

OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[5];

h q[0];
cz q[0], q[1];

