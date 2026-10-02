# Education Application Delivery Platform

Independent local delivery lab with synthetic inputs. No cloud resources or charges are created.

From this folder, after installing `../requirements.txt`, run `python lab.py --help`, then `python lab.py`. Run `python -m pytest -q` from the parent `devops` directory.

Applies explicit functional, latency, authorization, tenant isolation and rollback checks to an atomically saved release state. Failed gates retain the previously active version. Use `--checks checks-fail.json` to observe rejection. Kubernetes manifests are examples requiring a locally built image and cluster; they have not been applied or validated against a live cluster.

## Review the code

[Architecture and failure boundaries](ARCHITECTURE.md). Shared workflow modules and tests are in the parent stack folder. This repository is intended for source review; no hosted application is required.
