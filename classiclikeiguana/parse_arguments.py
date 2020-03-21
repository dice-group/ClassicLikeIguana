def parse_arguments() -> str:
    import argparse
    import os

    parser = argparse.ArgumentParser(description='An IGUANA spin-off for benchmarking fast commandline interfaces.')
    parser.add_argument('configfile', metavar='config file', type=str, nargs='?',
                        help='A yaml file providing the configuration for the benchmark.')

    args = parser.parse_args()

    if args.configfile is None:
        print("Please provide the path to a config file as commandline argument.")
        if not os.path.exists('config.yaml'):
            with open('config.yaml', 'w') as config_file:
                config_file.write(
                    '''
#  name of the triple store
triplestore: rdf3x
# command to start the interactive terminal
command: ./rdf3xembedded swdfdb
# line start that indicates that the triple store is ready to receive queries 
initFinished: RDF-3X protocol 1 
# line start that indicates a success
queryFinished: \\.
# line starts that indicate a failure
queryError:
- failure
- 'parse error:'
- internal error plan generation failed
# name of the dataset
dataset: swdf
# a file that contains a query in each line
queryFile: swdf.txt
# maximum duration a query may be processed (ms)
timeout: 180000
# total time the benchmark will be executed (ms)
timelimit: 360000
                    '''
                )

            print("A config file template 'config.yaml' was generated at {}.".format(os.getcwd()))
        exit(0)
    return str(args.configfile)
