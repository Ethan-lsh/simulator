#include <math.h>
#include "QuEST.h"
#include <time.h>
#include <stdio.h>
#ifndef M_PI
#define M_PI 3.14159265
#endif

int main(int argc, char *argv[]) {
    QuESTEnv env = createQuESTEnv();
    Qureg qubits = createQureg(8, env);
    int measured[8];


    printf("-------------------------------------------------------\n");
    printf("Running QuEST tutorial:\n\t %s\n", argv[0]);
    printf("-------------------------------------------------------\n");
    reportQuESTEnv(env);

    initZeroState(qubits);

    clock_t start, finish;
    double duration;

    start = clock();

    pauliX(qubits, 0);
    hadamard(qubits, 1);
    pauliX(qubits, 2);
    pauliX(qubits, 3);
    pauliX(qubits, 4);
    pauliX(qubits, 5);
    hadamard(qubits, 7);
    measured[6] = measure(qubits, 6);
    hadamard(qubits, 1);
    hadamard(qubits, 2);
    hadamard(qubits, 4);
    hadamard(qubits, 5);
    hadamard(qubits, 7);
    measured[0] = measure(qubits, 0);
    measured[3] = measure(qubits, 3);
    measured[1] = measure(qubits, 1);
    measured[2] = measure(qubits, 2);
    measured[4] = measure(qubits, 4);
    measured[5] = measure(qubits, 5);
    measured[7] = measure(qubits, 7);
    pauliX(qubits, 0);
    hadamard(qubits, 1);
    pauliX(qubits, 2);
    pauliX(qubits, 3);
    pauliX(qubits, 4);
    hadamard(qubits, 5);
    hadamard(qubits, 6);
    hadamard(qubits, 7);
    hadamard(qubits, 1);
    hadamard(qubits, 2);
    hadamard(qubits, 3);
    hadamard(qubits, 4);
    hadamard(qubits, 7);
    measured[0] = measure(qubits, 0);
    measured[5] = measure(qubits, 5);
    measured[6] = measure(qubits, 6);
    hadamard(qubits, 2);
    hadamard(qubits, 4);
    measured[1] = measure(qubits, 1);
    measured[3] = measure(qubits, 3);
    measured[7] = measure(qubits, 7);
    measured[2] = measure(qubits, 2);
    measured[4] = measure(qubits, 4);

    finish = clock();

    duration = (double)(finish-start) * pow(10,3);
    printf("Time: %f \n", duration);

    destroyQureg(qubits, env);
    destroyQuESTEnv(env);
    return 0;
}
