content_st = """
#include <benchmark/benchmark.h>
#include <chrono>

template <typename T>
uint64_t Run_Batch_Min_Benchmark(int b
                                 , int n
                                 , T fun)
{
    std::chrono::time_point<std::chrono::system_clock> start_time_point, end_time_point;
    std::chrono::duration<double> fun_elapsed_seconds, loop_elapsed_seconds;
    uint64_t min_time = std::numeric_limits<uint64_t>::max();
    for (int i = 0; i < b; i++)
    {
        start_time_point = std::chrono::system_clock::now();
        for (int j = 0; j < n; j++)
        {
            fun();
        }
        fun_elapsed_seconds = std::chrono::system_clock::now() - start_time_point;

        // time the for loop to remove the overhead noise
        start_time_point = std::chrono::system_clock::now();
        for (int j = 0; j < n; j++) { benchmark::DoNotOptimize(j); } // { asm volatile(""); } // volatile the variable so that cpp O3 is not going to optimiz it
        loop_elapsed_seconds = std::chrono::system_clock::now() - start_time_point;

        uint64_t cur_run_time = static_cast<uint64_t>(fun_elapsed_seconds.count() * 1000 * 1000 + 0.5); // get nano second
        cur_run_time -= static_cast<uint64_t>(loop_elapsed_seconds.count() * 1000 * 1000 + 0.5); // remove loop overhead
        if (min_time > cur_run_time)
            min_time = cur_run_time;
    }
    return min_time;
}

static void BM_StringCreation(benchmark::State& state) {
    for (auto _ : state)
        std::string empty_string;
}
// Register the function as a benchmark
BENCHMARK(BM_StringCreation);

// Define another benchmark
static void BM_StringCopy(benchmark::State& state) {
    std::string x = "hello";
    for (auto _ : state)
        std::string copy(x);
}
BENCHMARK(BM_StringCopy);

BENCHMARK_MAIN();
"""
