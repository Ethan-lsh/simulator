#include <math.h>
#include "QuEST.h"
#include <time.h>
#include <stdio.h>
#ifndef M_PI
#define M_PI 3.14159265
#endif

int main(int argc, char *argv[]) {
    QuESTEnv env = createQuESTEnv();
    Qureg qubits = createQureg(19, env);
    int measured[19];


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
    hadamard(qubits, 3);
    hadamard(qubits, 4);
    hadamard(qubits, 5);
    hadamard(qubits, 6);
    hadamard(qubits, 7);
    hadamard(qubits, 8);
    hadamard(qubits, 9);
    hadamard(qubits, 10);
    hadamard(qubits, 11);
    hadamard(qubits, 12);
    hadamard(qubits, 13);
    hadamard(qubits, 14);
    hadamard(qubits, 15);
    hadamard(qubits, 16);
    hadamard(qubits, 17);
    pauliX(qubits, 18);
    hadamard(qubits, 18);
    controlledNot(qubits, 0, 18);
    hadamard(qubits, 0);
    controlledNot(qubits, 1, 18);
    hadamard(qubits, 1);
    controlledNot(qubits, 2, 18);
    hadamard(qubits, 2);
    controlledNot(qubits, 3, 18);
    hadamard(qubits, 3);
    controlledNot(qubits, 4, 18);
    hadamard(qubits, 4);
    controlledNot(qubits, 5, 18);
    hadamard(qubits, 5);
    controlledNot(qubits, 6, 18);
    hadamard(qubits, 6);
    controlledNot(qubits, 7, 18);
    hadamard(qubits, 7);
    controlledNot(qubits, 8, 18);
    hadamard(qubits, 8);
    controlledNot(qubits, 9, 18);
    hadamard(qubits, 9);
    controlledNot(qubits, 10, 18);
    hadamard(qubits, 10);
    controlledNot(qubits, 11, 18);
    hadamard(qubits, 11);
    controlledNot(qubits, 12, 18);
    hadamard(qubits, 12);
    controlledNot(qubits, 13, 18);
    hadamard(qubits, 13);
    controlledNot(qubits, 14, 18);
    hadamard(qubits, 14);
    controlledNot(qubits, 15, 18);
    hadamard(qubits, 15);
    controlledNot(qubits, 16, 18);
    hadamard(qubits, 16);
    controlledNot(qubits, 17, 18);
    hadamard(qubits, 17);
    measured[0] = measure(qubits, 0);
    measured[1] = measure(qubits, 1);
    measured[2] = measure(qubits, 2);
    measured[3] = measure(qubits, 3);
    measured[4] = measure(qubits, 4);
    measured[5] = measure(qubits, 5);
    measured[6] = measure(qubits, 6);
    measured[7] = measure(qubits, 7);
    measured[8] = measure(qubits, 8);
    measured[9] = measure(qubits, 9);
    measured[10] = measure(qubits, 10);
    measured[11] = measure(qubits, 11);
    measured[12] = measure(qubits, 12);
    measured[13] = measure(qubits, 13);
    measured[14] = measure(qubits, 14);
    measured[15] = measure(qubits, 15);
    measured[16] = measure(qubits, 16);
    measured[17] = measure(qubits, 17);

    finish = clock();

    duration = (double)(finish-start) * pow(10,3);
    printf("Time: %f \n", duration);

    destroyQureg(qubits, env);
    destroyQuESTEnv(env);
    return 0;
}
