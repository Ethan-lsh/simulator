// Name of Experiment: lineair_solver_in_0 v3
// Description: 1bit lineair solver
Solver for a linear equation for one quantumbit

OPENQASM 2.0;
include "qelib1.inc";

qreg q[5];
creg c[5];

h q[1];
x q[3];
cx q[1],q[2];
h q[1];
h q[2];
h q[3];
cx q[3],q[2];
h q[2];
h q[3];
u3(-0.58,0,0) q[3];
h q[2];
h q[3];
cx q[3],q[2];
h q[2];
h q[3];
h q[1];
u3(0.58,0,0) q[3];
cx q[1],q[2];
h q[1];
measure q[1] -> c[1];
measure q[2] -> c[2];
measure q[3] -> c[3];
