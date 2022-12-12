#include <math.h>
#include "QuEST.h"
#include <time.h>
#include <stdio.h>
#ifndef M_PI
#define M_PI 3.14159265
#endif

int main(int argc, char *argv[]) {
    QuESTEnv env = createQuESTEnv();
    Qureg qubits = createQureg(23, env);
    int measured[23];


    printf("-------------------------------------------------------\n");
    printf("Running QuEST tutorial:\n\t teleportation_n3.cpp \n");
    printf("-------------------------------------------------------\n");
    reportQuESTEnv(env);

    initZeroState(qubits);

    clock_t start, finish;
    double duration;

    start = clock();

    hadamard(qubits, 0);
    controlledNot(qubits, 0, 1);
    controlledNot(qubits, 1, 2);
    controlledNot(qubits, 2, 3);
    controlledNot(qubits, 3, 4);
    controlledNot(qubits, 4, 5);
    controlledNot(qubits, 5, 6);
    controlledNot(qubits, 6, 7);
    controlledNot(qubits, 7, 8);
    controlledNot(qubits, 8, 9);
    controlledNot(qubits, 9, 10);
    controlledNot(qubits, 10, 11);
    controlledNot(qubits, 11, 12);
    controlledNot(qubits, 12, 13);
    controlledNot(qubits, 13, 14);
    controlledNot(qubits, 14, 15);
    controlledNot(qubits, 15, 16);
    controlledNot(qubits, 16, 17);
    controlledNot(qubits, 17, 18);
    controlledNot(qubits, 18, 19);
    controlledNot(qubits, 19, 20);
    controlledNot(qubits, 20, 21);
    controlledNot(qubits, 21, 22);
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
    measured[18] = measure(qubits, 18);
    measured[19] = measure(qubits, 19);
    measured[20] = measure(qubits, 20);
    measured[21] = measure(qubits, 21);
    measured[22] = measure(qubits, 22);

    finish = clock();

    duration = (double)(finish-start) * pow(10,3);
    printf("Time: %f \n", duration);

    destroyQureg(qubits, env);
    destroyQuESTEnv(env);
    return 0;
}
