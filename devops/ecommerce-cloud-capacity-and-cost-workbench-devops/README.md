# Ecommerce Cloud Capacity and Cost Workbench

Independent local capacity lab with synthetic inputs. No cloud resources or charges are created.

From this folder, after installing `../requirements.txt`, run `python lab.py --help`, then `python lab.py`. Run `python -m pytest -q` from the parent `devops` directory.

Models required instance counts, utilization and normalized costs from explicitly supplied throughput and unit-cost inputs. `--rps`, `--capacity`, `--target`, `--unit-cost`, `--hours` select the scenario. Prices are arbitrary modeled units, not current AWS prices. `capacity.tf` shows the same model as a resource-free Terraform planning exercise.

## Review the code

[Architecture and failure boundaries](ARCHITECTURE.md). Shared workflow modules and tests are in the parent stack folder. This repository is intended for source review; no hosted application is required.
