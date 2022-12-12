#include <math.h>
#include "QuEST.h"

#include <time.h>
#include <stdio.h>


#ifndef M_PI
#define M_PI 3.14159265
#endif

int main(int argc, char *argv[]) {
    QuESTEnv env = createQuESTEnv();
    Qureg qubits = createQureg(14, env);
    int measured[14];


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
    pauliX(qubits, 13);
    hadamard(qubits, 13);
    controlledNot(qubits, 0, 13);
    hadamard(qubits, 0);
    controlledNot(qubits, 1, 13);
    hadamard(qubits, 1);
    controlledNot(qubits, 2, 13);
    hadamard(qubits, 2);
    controlledNot(qubits, 3, 13);
    hadamard(qubits, 3);
    controlledNot(qubits, 4, 13);
    hadamard(qubits, 4);
    controlledNot(qubits, 5, 13);
    hadamard(qubits, 5);
    controlledNot(qubits, 6, 13);
    hadamard(qubits, 6);
    controlledNot(qubits, 7, 13);
    hadamard(qubits, 7);
    controlledNot(qubits, 8, 13);
    hadamard(qubits, 8);
    controlledNot(qubits, 9, 13);
    hadamard(qubits, 9);
    controlledNot(qubits, 10, 13);
    hadamard(qubits, 10);
    controlledNot(qubits, 11, 13);
    hadamard(qubits, 11);
    controlledNot(qubits, 12, 13);
    hadamard(qubits, 12);
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

    finish = clock();

    duration = (double)(finish-start) * pow(10,6);
    printf("Time: %f \n", duration);
    
    destroyQureg(qubits, env);
    destroyQuESTEnv(env);
    return 0;
}
