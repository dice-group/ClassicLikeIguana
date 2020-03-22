import yaml

from classiclikeiguana.execute import execute
from classiclikeiguana.parse_arguments import parse_arguments
from classiclikeiguana.write_result_file import write_result_file

config_file, debug_flag = parse_arguments()

with open(config_file, 'r') as file:
    cli_config = yaml.load(file, Loader=yaml.FullLoader)

start_datetime, execution_results = execute(cli_config, debug=debug_flag)

write_result_file(execution_results, cli_config, start_datetime)
