#include <math.h>
#include "QuEST.h"
#include <time.h>
#include <stdio.h>
#ifndef M_PI
#define M_PI 3.14159265
#endif

void ccx(Qureg qubits, const int q1, const int q2, const int q3) {
    hadamard(qubits, q3);
    controlledNot(qubits, q2, q3);
    phaseShift(qubits, q3, -M_PI/4);
    controlledNot(qubits, q1, q3);
    tGate(qubits, q3);
    controlledNot(qubits, q2, q3);
    phaseShift(qubits, q3, -M_PI/4);
    controlledNot(qubits, q1, q3);
    tGate(qubits, q2);
    tGate(qubits, q3);
    controlledNot(qubits, q1, q2);
    hadamard(qubits, q3);
    tGate(qubits, q1);
    phaseShift(qubits, q2, -M_PI/4);
    controlledNot(qubits, q1, q2);
}

int main(int argc, char *argv[]) {
    QuESTEnv env = createQuESTEnv();
    Qureg qubits = createQureg(6, env);
    int measured[6];

    printf("-------------------------------------------------------\n");
    printf("Running QuEST tutorial:\n\t teleportation_n3.cpp \n");
    printf("-------------------------------------------------------\n");
    reportQuESTEnv(env);

    initZeroState(qubits);

    clock_t start, finish;
    double duration;

    start = clock();

    hadamard(qubits, 0);
    hadamard(qubits, 1);
    hadamard(qubits, 2);
    controlledNot(qubits, 2, 4);
    pauliX(qubits, 3);
    controlledNot(qubits, 2, 3);
    ccx(qubits, 0, 1, 3);
    pauliX(qubits, 0);
    pauliX(qubits, 1);
    ccx(qubits, 0, 1, 3);
    pauliX(qubits, 0);
    pauliX(qubits, 1);
    hadamard(qubits, 2);
    pauliX(qubits, 3);
    hadamard(qubits, 0);
    hadamard(qubits, 1);
    measured[0] = measure(qubits, 0);
    measured[1] = measure(qubits, 1);
    measured[2] = measure(qubits, 2);
    measured[3] = measure(qubits, 3);
    measured[4] = measure(qubits, 4);
    measured[5] = measure(qubits, 5);

    finish = clock();

    duration = (double)(finish-start) * pow(10,3);
    printf("Time: %f \n", duration);
    
    destroyQureg(qubits, env);
    destroyQuESTEnv(env);
    return 0;
}
