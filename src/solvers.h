#ifndef MIP_SOLVER_PREDICTION_SOLVERS_H
#define MIP_SOLVER_PREDICTION_SOLVERS_H

#include <string>
#include <tuple>

namespace orcs {

    /**
     * MIP solvers.
     */
    enum class Solver : int {
        GUROBI,
    };

    /**
     * Optimization status.
     * 
     */
    enum class Status : int {
        UNKNOWN,
        OPTIMAL,
        FEASIBLE
    };

    /**
     * Data structure to store relevant results.
     */
     struct Result {
         Status status;
         double objective;
         unsigned long long runtime_ms;
     };

    /**
     * Solve a MIP problem.
     * @param filename Path to the file with the problem data.
     * @param solver Define which MIP solver to use.
     * @param seed Seed to initialize the random number generator.
     * @param threads Number of threads the solver is allowed to use.
     * @param time_limit Maximum runtime in seconds.
     * @param verbose Verbosity mode.
     * @return A Result structure with relevant data.
     */
    Result solve(const std::string& filename, Solver solver, int seed, int threads, int time_limit, bool verbose);

    Result gurobi(const std::string& filename, int seed, int threads, int time_limit, bool verbose);
    

}

#endif
