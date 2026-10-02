"""Local synthetic recovery, capacity modeling and release gates. No cloud calls."""
import hashlib,json,math,sqlite3,tempfile,time
from decimal import Decimal,ROUND_HALF_UP
from pathlib import Path
from cryptography.fernet import Fernet,InvalidToken

def recover(directory,role='recovery-operator',corrupt=False):
    if role!='recovery-operator':raise PermissionError('Recovery-operator fixture role required')
    root=Path(directory).resolve();root.mkdir(parents=True,exist_ok=True)
    source=root/'synthetic-source.db';restored=root/'synthetic-restored.db'
    with sqlite3.connect(source) as db:
        db.execute('CREATE TABLE IF NOT EXISTS appointments(id TEXT PRIMARY KEY,tenant TEXT,resource TEXT)')
        db.executemany('INSERT OR IGNORE INTO appointments VALUES(?,?,?)',[('APPT-1','clinic-a','Room1'),('APPT-2','clinic-b','Room2')])
        db.commit()
    started=time.perf_counter()
    # SQLite backup API gives a consistent snapshot even if source WAL mode is used.
    with sqlite3.connect(source) as db,sqlite3.connect(root/'snapshot.db') as snap:db.backup(snap)
    original=(root/'snapshot.db').read_bytes();digest=hashlib.sha256(original).hexdigest()
    key=Fernet.generate_key();cipher=Fernet(key);encrypted=cipher.encrypt(original)
    (root/'backup.enc').write_bytes(encrypted);(root/'recovery.key').write_bytes(key)
    if corrupt:encrypted=encrypted[:-8]+b'corrupt!'
    try:plain=cipher.decrypt(encrypted)
    except InvalidToken:raise ValueError('Encrypted backup integrity check failed')
    if hashlib.sha256(plain).hexdigest()!=digest:raise ValueError('Snapshot checksum mismatch')
    restored.write_bytes(plain)
    with sqlite3.connect(restored) as db:
        integrity=db.execute('PRAGMA integrity_check').fetchone()[0]
        count=db.execute('SELECT count(*) FROM appointments').fetchone()[0]
        tenant_a=db.execute('SELECT id FROM appointments WHERE tenant=?',('clinic-a',)).fetchall()
    if integrity!='ok' or count!=2 or tenant_a!=[('APPT-1',)]:raise ValueError('Restore verification failed')
    report={'mode':'local synthetic drill','encrypted':True,'sha256':digest,'records':count,'tenantChecks':'passed','integrity':integrity,'elapsedSeconds':round(time.perf_counter()-started,4),'cloudResourcesCreated':0}
    (root/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    return report

def capacity(requests_per_second,capacity_per_instance,target_utilization,unit_cost_per_hour,hours=24):
    rps=Decimal(str(requests_per_second));throughput=Decimal(str(capacity_per_instance));target=Decimal(str(target_utilization));cost=Decimal(str(unit_cost_per_hour));duration=Decimal(str(hours))
    if not rps.is_finite() or not throughput.is_finite() or not target.is_finite() or not cost.is_finite() or not duration.is_finite():raise ValueError('Finite inputs required')
    if rps<0 or throughput<=0 or not Decimal('0')<target<=1 or cost<0 or duration<=0:raise ValueError('Invalid capacity model inputs')
    count=max(1,math.ceil(rps/(throughput*target)))
    spend=(Decimal(count)*cost*duration).quantize(Decimal('.01'),rounding=ROUND_HALF_UP)
    utilization=rps/(throughput*count)
    return {'mode':'user-supplied synthetic cost model','instances':count,'utilization':str(utilization.quantize(Decimal('.0001'))),'estimatedCost':str(spend),'unitCostPerHour':str(cost),'hours':str(duration),'currency':'arbitrary modeled units','cloudResourcesCreated':0}

def release(state_path,candidate,checks):
    root=Path(state_path).resolve();root.parent.mkdir(parents=True,exist_ok=True)
    before=json.loads(root.read_text(encoding='utf-8')) if root.exists() else {'active':'baseline','history':[]}
    if not isinstance(candidate,str) or not candidate or len(candidate)>100:raise ValueError('Candidate identifier required')
    required={'authorization','tenantIsolation','rollback','functional','latency'}
    if set(checks)!=required or any(type(v) is not bool for v in checks.values()):raise ValueError('Explicit boolean values for all release checks required')
    passed=all(checks.values())
    after={'active':candidate if passed else before['active'],'history':before['history']+[{'candidate':candidate,'checks':checks,'decision':'promoted' if passed else 'rejected','previous':before['active']}]}
    temporary=root.with_suffix('.pending');temporary.write_text(json.dumps(after,indent=2)+'\n',encoding='utf-8');temporary.replace(root)
    return after
