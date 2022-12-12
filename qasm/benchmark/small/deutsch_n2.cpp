#include <math.h>
#include "QuEST.h"
#include <stdio.h>
#include <time.h>

#ifndef M_PI
#define M_PI 3.14159265
#endif

int main(int argc, char *argv[]) {
    QuESTEnv env = createQuESTEnv();
    Qureg qubits = createQureg(2, env);
    int measured[2];

    printf("-------------------------------------------------------\n");
    printf("Running QuEST tutorial:\n\t deutsch_n2.cpp \n");
    printf("-------------------------------------------------------\n");
    reportQuESTEnv(env);

    initZeroState(qubits);


    clock_t start, finish;
    double duration;


    start = clock();

    hadamard(qubits, 0);
    pauliX(qubits, 1);
    hadamard(qubits, 1);
    controlledNot(qubits, 0, 1);
    hadamard(qubits, 0);

    finish = clock();

    duration = (double)(finish-start) * pow(10,3);
    printf("Time: %f \n", duration);

    destroyQureg(qubits, env);
    destroyQuESTEnv(env);
    return 0;
}
