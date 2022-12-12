#include <math.h>
#include "QuEST.h"
#include <time.h>
#include <stdio.h>

#ifndef M_PI
#define M_PI 3.14159265
#endif

int main(int argc, char *argv[]) {
    QuESTEnv env = createQuESTEnv();
    Qureg qubits = createQureg(5, env);
    int measured[5];
    printf("-------------------------------------------------------\n");
    printf("Running QuEST tutorial:\n\t qec_en_n5.cpp \n");
    printf("-------------------------------------------------------\n");
    reportQuESTEnv(env);

    initZeroState(qubits);

    clock_t start, finish;
    double duration;
    start = clock();

    hadamard(qubits, 0);
    hadamard(qubits, 1);
    hadamard(qubits, 2);
    hadamard(qubits, 3);
    hadamard(qubits, 4);
    tGate(qubits, 2);
    hadamard(qubits, 2);
    hadamard(qubits, 2);
    controlledNot(qubits, 1, 2);
    controlledNot(qubits, 0, 2);
    hadamard(qubits, 0);
    hadamard(qubits, 1);
    controlledNot(qubits, 3, 2);
    hadamard(qubits, 2);
    hadamard(qubits, 3);
    controlledNot(qubits, 3, 2);
    controlledNot(qubits, 0, 2);
    controlledNot(qubits, 1, 2);
    hadamard(qubits, 2);
    controlledNot(qubits, 4, 2);
    hadamard(qubits, 2);
    hadamard(qubits, 4);
    controlledNot(qubits, 4, 2);
    controlledNot(qubits, 1, 2);
    controlledNot(qubits, 3, 2);
    measured[2] = measure(qubits, 2);
    measured[4] = measure(qubits, 4);
    measured[0] = measure(qubits, 0);
    measured[1] = measure(qubits, 1);
    measured[3] = measure(qubits, 3);
    finish = clock();
    duration = (double)(finish-start) * pow(10,3);
    printf("Time: %f \n", duration);

    destroyQureg(qubits, env);
    destroyQuESTEnv(env);
    return 0;
}
