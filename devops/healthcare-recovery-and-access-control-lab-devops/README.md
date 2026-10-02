# Healthcare Recovery and Access Control Lab

Independent local recovery lab with synthetic inputs. No cloud resources or charges are created.

From this folder, after installing `../requirements.txt`, run `python lab.py --help`, then `python lab.py`. Run `python -m pytest -q` from the parent `devops` directory.

Creates a consistent SQLite snapshot, encrypts it with a fresh local Fernet key, verifies its authenticated integrity, restores a separate database and checks record count and tenant filtering. `--simulate-corruption` rejects an altered backup. Key and database artifacts are excluded from Git. This is a local rehearsal, not an AWS/Kubernetes disaster-recovery deployment.

## Architecture

[Architecture and failure boundaries](ARCHITECTURE.md). Shared workflow modules and tests are in the parent stack folder.
