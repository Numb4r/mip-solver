#include <cstddef>
#include <cstdlib>
#include <iostream>
#include <limits>
#include <stdexcept>
#include <cxxopts.hpp>
#include "solvers.h"


int main(int argc, char** argv) {

    cxxopts::Options options(argv[0], "MIP solver");
    options.positional_help("FILE")
            .add_options()
                ("h,help", "Show this help message and exit.", cxxopts::value<bool>())
                ("file", "Path to file with MIP data.", cxxopts::value<std::string>())
                ("verbose", "Display log of the optimization process.", cxxopts::value<bool>())
                ("seed", "Seed to initialize the random number generator.", cxxopts::value<int>()->default_value("0"))
                ("threads", "Number of threads to use.", cxxopts::value<int>()->default_value("1"))
                ("time-limit", "Time limit in seconds.", cxxopts::value<int>()->default_value(std::to_string(std::numeric_limits<int>::max())));
                ("positional", "Other positional arguments.", cxxopts::value<std::vector<std::string>>());

    options.parse_positional({ "file", "positional" });

    try {

        auto args = options.parse(argc, argv);

        // Show usage, if "help" flag is active
        if (args.count("help")) {
            std::cout << options.help() << std::endl;
            return EXIT_SUCCESS;
        }

        // Check if input data file were set
        if (args.count("file") == 0) {
            throw std::invalid_argument("Missing arguments.");
        }

        // Get args
        std::string file = args["file"].as<std::string>();
        bool verbose = (args.count("verbose") > 0);
        int seed = args["seed"].as<int>();
        int threads = args["threads"].as<int>();
        int time_limit = args["time-limit"].as<int>();

        // Set MIP solver
        // std::string solver_str = args["solver"].as<std::string>();
        orcs::Solver solver;
        solver = orcs::Solver::GUROBI;
        

        // Run the MIP solver
        orcs::Result result = orcs::solve(file, solver, seed, threads, time_limit, verbose);

        // Print result
        if (result.status == orcs::Status::OPTIMAL) {
            std::cout << "Status: optimal" << std::endl;
            std::cout << "Objective: " << result.objective << std::endl;
            std::cout << "Runtime (ms): " << result.runtime_ms << std::endl;

        } else if (result.status == orcs::Status::FEASIBLE) {
            std::cout << "Status: feasible" << std::endl;
            std::cout << "Objective: " << result.objective << std::endl;
            std::cout << "Runtime (ms): " << result.runtime_ms << std::endl;

        } else {
            std::cout << "Status: Unknown" << std::endl;
        }

    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        std::cerr << "Type the following command for a correct usage." << std::endl;
        std::cerr << argv[0] << " --help" << std::endl << std::endl;
        return EXIT_FAILURE;

    } catch (...) {
        std::cerr << "Unexpected error." << std::endl;
        std::cerr << "Type the following command for a correct usage." << std::endl;
        std::cerr << argv[0] << " --help" << std::endl << std::endl;
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
