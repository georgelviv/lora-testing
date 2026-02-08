from lora_testing import (
  run, ExperimentDescription, logger, load_json,
  read_args, Args, LoraBase, get_backend,
  get_description
)

def main():
  args: Args = read_args()
  backend: LoraBase = get_backend(logger, args)
  config_suites = load_json("configs-suite.json")
  description: ExperimentDescription = get_description(backend, args)
  run(backend, description, configs_suite=config_suites, args=args)

if __name__ == "__main__":
  main()
