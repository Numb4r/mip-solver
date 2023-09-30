#include "solvers.h"
#include "utils.h"
#include <stdexcept>
#include <cxxtimer.hpp>
#include <gurobi_c++.h>




orcs::Result orcs::solve(const std::string& filename, Solver solver, int seed, int threads, int time_limit, bool verbose) {

    // Calls Gurobi solver
    
    return gurobi(filename, seed, threads, time_limit, verbose);
    
}
  

orcs::Result orcs::gurobi(const std::string& filename, int seed, int threads, int time_limit, bool verbose) {
    
    // Keep results
    Result result { Status::UNKNOWN, 0, 0 };

    // Gurobi solver
    GRBEnv* env = nullptr;
    try {

        // Load problem data
        env = new GRBEnv();
        GRBModel model(*env, filename);

        // Configure the solver
        model.getEnv().set(GRB_IntParam_LogToConsole, (verbose ? 1 : 0));
        model.getEnv().set(GRB_IntParam_OutputFlag, (verbose ? 1 : 0));
        model.getEnv().set(GRB_IntParam_Threads, threads);
        model.getEnv().set(GRB_IntParam_Seed, seed);
        model.getEnv().set(GRB_DoubleParam_TimeLimit, (double) time_limit);

        // Solve the problem
        cxxtimer::Timer timer(true);
        model.optimize();
        timer.stop();

        // Get result
        if (model.get(GRB_IntAttr_SolCount) > 0) {
            
            if (model.get(GRB_DoubleAttr_MIPGap) < 1e-5) {
                result.status = Status::OPTIMAL;
            } else {
                result.status = Status::FEASIBLE;
            }

            result.objective = model.get(GRB_DoubleAttr_ObjVal);
            result.runtime_ms = timer.count<std::chrono::milliseconds>();
        };

    } catch (const GRBException& e) {
        if (env != nullptr) delete env;
        std::string msg = orcs::utils::format("Gurobi exception: %s", e.getMessage().c_str());
        throw std::runtime_error(msg);

    } catch (...) {
        if (env != nullptr) delete env;
        throw std::runtime_error("Unexpected error.");
    }

    // Deallocate resources
    if (env != nullptr) delete env;

    return result;
}



