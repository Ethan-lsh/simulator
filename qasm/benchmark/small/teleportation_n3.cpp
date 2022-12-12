#include <math.h>
#include "QuEST.h"
#include <time.h>
#include <stdio.h>

#ifndef M_PI
#define M_PI 3.14159265
#endif

int main(int argc, char *argv[]) {
    QuESTEnv env = createQuESTEnv();
    Qureg qubits = createQureg(3, env);
    int measured[3];

    printf("-------------------------------------------------------\n");
    printf("Running QuEST tutorial:\n\t teleportation_n3.cpp \n");
    printf("-------------------------------------------------------\n");
    reportQuESTEnv(env);

    initZeroState(qubits);

    clock_t start, finish;
    double duration;


    start = clock();
    hadamard(qubits, 0);
    hadamard(qubits, 2);
    tGate(qubits, 0);
    controlledNot(qubits, 2, 1);
    hadamard(qubits, 0);
    sGate(qubits, 0);
    controlledNot(qubits, 0, 1);
    hadamard(qubits, 0);
    measured[0] = measure(qubits, 0);
    measured[1] = measure(qubits, 1);
    measured[2] = measure(qubits, 2);

    finish = clock();


    duration = (double)(finish-start) * pow(10,3);
    printf("Time: %f \n", duration);

    destroyQureg(qubits, env);
    destroyQuESTEnv(env);
    return 0;
}
