import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from labs import release
p=argparse.ArgumentParser(description='Local release-gate state machine; no cluster deployment')
p.add_argument('--candidate',default='demo-v1');p.add_argument('--state',default='release-state.json');p.add_argument('--checks',default=str(Path(__file__).with_name('checks-pass.json')));a=p.parse_args()
print(json.dumps(release(a.state,a.candidate,json.loads(Path(a.checks).read_text(encoding='utf-8'))),indent=2))
