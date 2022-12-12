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
    Qureg qubits = createQureg(11, env);
    int measured[11];

    printf("-------------------------------------------------------\n");
    printf("Running QuEST tutorial:\n\t \n");
    printf("-------------------------------------------------------\n");
    reportQuESTEnv(env);

    initZeroState(qubits);

    clock_t start, finish;
    double duration;
    
    start = clock();
    pauliZ(qubits, 0);
    hadamard(qubits, 9);
    hadamard(qubits, 0);
    controlledNot(qubits, 9, 10);
    controlledNot(qubits, 0, 3);
    controlledNot(qubits, 0, 6);
    controlledPhaseFlip(qubits, 0, 3);
    controlledPhaseFlip(qubits, 0, 6);
    hadamard(qubits, 0);
    hadamard(qubits, 3);
    hadamard(qubits, 6);
    pauliZ(qubits, 0);
    pauliZ(qubits, 3);
    pauliZ(qubits, 6);
    controlledNot(qubits, 0, 1);
    controlledNot(qubits, 3, 4);
    controlledNot(qubits, 6, 7);
    controlledNot(qubits, 0, 2);
    controlledNot(qubits, 3, 5);
    controlledNot(qubits, 6, 8);
    controlledPhaseFlip(qubits, 0, 1);
    controlledPhaseFlip(qubits, 3, 4);
    controlledPhaseFlip(qubits, 6, 7);
    controlledPhaseFlip(qubits, 0, 2);
    controlledPhaseFlip(qubits, 3, 5);
    controlledPhaseFlip(qubits, 6, 8);
    controlledNot(qubits, 0, 9);
    measured[9] = measure(qubits, 9);
    hadamard(qubits, 0);
    controlledNot(qubits, 9, 10);
    measured[0] = measure(qubits, 0);
    controlledPhaseFlip(qubits, 0, 10);
    controlledNot(qubits, 10, 1);
    controlledNot(qubits, 10, 2);
    controlledNot(qubits, 3, 4);
    controlledNot(qubits, 6, 7);
    controlledNot(qubits, 3, 5);
    controlledNot(qubits, 6, 8);
    controlledPhaseFlip(qubits, 10, 1);
    controlledPhaseFlip(qubits, 10, 2);
    controlledPhaseFlip(qubits, 3, 4);
    controlledPhaseFlip(qubits, 6, 7);
    controlledPhaseFlip(qubits, 3, 5);
    controlledPhaseFlip(qubits, 6, 8);
    ccx(qubits, 1, 2, 10);
    ccx(qubits, 5, 4, 3);
    ccx(qubits, 8, 7, 6);
    hadamard(qubits, 10);
    ccx(qubits, 1, 2, 10);
    hadamard(qubits, 3);
    hadamard(qubits, 6);
    hadamard(qubits, 10);
    ccx(qubits, 5, 4, 3);
    ccx(qubits, 8, 7, 6);
    hadamard(qubits, 10);
    hadamard(qubits, 3);
    hadamard(qubits, 6);
    pauliZ(qubits, 10);
    hadamard(qubits, 3);
    hadamard(qubits, 6);
    pauliZ(qubits, 3);
    pauliZ(qubits, 6);
    controlledNot(qubits, 10, 3);
    controlledNot(qubits, 10, 6);
    controlledPhaseFlip(qubits, 10, 3);
    controlledPhaseFlip(qubits, 10, 6);
    ccx(qubits, 3, 6, 10);
    hadamard(qubits, 10);
    ccx(qubits, 3, 6, 10);
    hadamard(qubits, 10);
    hadamard(qubits, 10);
    pauliZ(qubits, 10);
    measured[10] = measure(qubits, 10);
    finish = clock();

    duration = (double)(finish-start) * pow(10,3);
    printf("Time: %f \n", duration);


    destroyQureg(qubits, env);
    destroyQuESTEnv(env);
    return 0;
}
