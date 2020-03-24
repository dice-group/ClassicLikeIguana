# ClassicLikeIguana (CLI)

Benchmarking tool for SPARQL triple stores with an interactive commandline interface. 

The output format is compatible with [IguanaResult2CSV](https://github.com/dice-group/IguanaResult2CSV)

*A tiny, specialized Python spin-off of the grown-up [IGUANA](iguana-benchmark.eu/).* 
 
## Installation
1. install [pypy3](https://www.pypy.org/download.html) (optional, you can also use any other python interpreter)
2. clone & change dir:
    ```shell script
    git clone https://github.com/dice-group/ClassicLatentIguana
    cd ClassicLikeIguana
    ```

## Run
Make sure you are in the folder, you just cloned. 
1. Generate an configuration template
    ```shell script
    ClassicLikeIguana.py
    ```
   The template is named `config.yaml`
2. Populate the template with the configuration you want to benchmark.
3. Run the benchmark:
   ```shell script
    ClassicLikeIguana.py your_benchmark_config.yaml
   ```
