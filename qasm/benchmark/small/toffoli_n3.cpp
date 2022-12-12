#include <math.h>
#include "QuEST.h"
#include <stdio.h>
#include <time.h>

#ifndef M_PI
#define M_PI 3.14159265
#endif

int main(int argc, char *argv[]) {
    QuESTEnv env = createQuESTEnv();
    Qureg qubits = createQureg(3, env);
    int measured[3];

    printf("-------------------------------------------------------\n");
    printf("Running QuEST tutorial:\n\t toffoli_n3.cpp \n");
    printf("-------------------------------------------------------\n");

    initZeroState(qubits);

    
    clock_t start, finish;
    double duration;

    
    start = clock();
    pauliX(qubits, 0);
    pauliX(qubits, 1);
    hadamard(qubits, 2);
    controlledNot(qubits, 1, 2);
    phaseShift(qubits, 2, -M_PI/4);
    controlledNot(qubits, 0, 2);
    tGate(qubits, 2);
    controlledNot(qubits, 1, 2);
    phaseShift(qubits, 2, -M_PI/4);
    controlledNot(qubits, 0, 2);
    phaseShift(qubits, 1, -M_PI/4);
    tGate(qubits, 2);
    controlledNot(qubits, 0, 1);
    hadamard(qubits, 2);
    phaseShift(qubits, 1, -M_PI/4);
    controlledNot(qubits, 0, 1);
    tGate(qubits, 0);
    sGate(qubits, 1);
    measured[0] = measure(qubits, 0);
    measured[1] = measure(qubits, 1);
    measured[2] = measure(qubits, 2);

    finish = clock();

    duration = (double)(finish - start) * pow(10, 3);
    printf("Time: %f\n", duration);


    /*
     * STUDY QUANTUM STATE
     */

    printf("\nCircuit output:\n");

    qreal prob;
    prob = getProbAmp(qubits, 7);
    printf("Probability amplitude of |111>: " REAL_STRING_FORMAT "\n", prob);

    prob = calcProbOfOutcome(qubits, 2, 1);
    printf("Probability of qubit 2 being in state 1: " REAL_STRING_FORMAT "\n", prob);

    int outcome = measure(qubits, 0);
    printf("Qubit 0 was measured in state %d\n", outcome);

    outcome = measureWithStats(qubits, 2, &prob);
    printf("Qubit 2 collapsed to %d with probability " REAL_STRING_FORMAT "\n", outcome, prob);

    showMemoryInfo();

    destroyQureg(qubits, env);
    destroyQuESTEnv(env);
    return 0;
}
