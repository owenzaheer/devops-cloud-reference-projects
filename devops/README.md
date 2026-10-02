# Local cloud-operations labs

Python 3.12+. Install `python -m pip install -r requirements.txt`, then run `python -m pytest -q` from this folder. Each project contains a runnable `lab.py --help` entry point and a precise explanation of the local exercise.

Implemented: authenticated encrypted backup/restore, SQLite integrity and tenant checks, deterministic Decimal cost/capacity models, atomic release decisions and failure fixtures. Terraform and Kubernetes examples describe the deployment boundary; there is no live AWS, cluster, IAM or cloud backup integration. Release input checks are explicit fixtures rather than measured cluster telemetry. See the verification report for executed checks.
