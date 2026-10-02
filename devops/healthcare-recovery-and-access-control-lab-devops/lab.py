import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from labs import recover
p=argparse.ArgumentParser(description='Encrypted recovery drill with synthetic SQLite records')
p.add_argument('--output',default='drill-output');p.add_argument('--role',default='recovery-operator');p.add_argument('--simulate-corruption',action='store_true');a=p.parse_args()
print(json.dumps(recover(a.output,a.role,a.simulate_corruption),indent=2))
