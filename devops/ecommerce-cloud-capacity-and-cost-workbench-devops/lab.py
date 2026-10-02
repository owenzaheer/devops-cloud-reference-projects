import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from labs import capacity
p=argparse.ArgumentParser(description='Synthetic capacity/cost model; no real cloud prices or API calls')
p.add_argument('--rps',default='101');p.add_argument('--capacity',default='100');p.add_argument('--target',default='.5');p.add_argument('--unit-cost',default='.20');p.add_argument('--hours',default='24');a=p.parse_args()
print(json.dumps(capacity(a.rps,a.capacity,a.target,a.unit_cost,a.hours),indent=2))
