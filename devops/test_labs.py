import pytest
from labs import recover,capacity,release

def test_backup_integrity_tenant_checks_and_permissions(tmp_path):
    with pytest.raises(PermissionError):recover(tmp_path,'viewer')
    r=recover(tmp_path)
    assert r['records']==2 and r['integrity']=='ok' and r['cloudResourcesCreated']==0
    assert (tmp_path/'backup.enc').read_bytes()!= (tmp_path/'synthetic-source.db').read_bytes()

def test_tampered_backup_cannot_be_restored(tmp_path):
    with pytest.raises(ValueError,match='integrity'):recover(tmp_path,corrupt=True)
    assert not (tmp_path/'synthetic-restored.db').exists()

def test_capacity_rounding_cost_and_invalid_input():
    r=capacity(101,100,.5,.20)
    assert r['instances']==3 and r['estimatedCost']=='14.40'
    assert capacity(0,100,.5,0)['instances']==1
    for args in [(1,0,.5,1),(-1,100,.5,1),(1,100,1.1,1),(1,100,.5,-1),('NaN',100,.5,1)]:
        with pytest.raises(ValueError):capacity(*args)

def test_release_gate_rejection_preserves_active_version(tmp_path):
    p=tmp_path/'release.json';checks=dict.fromkeys(['authorization','tenantIsolation','rollback','functional','latency'],True)
    assert release(p,'v1',checks)['active']=='v1'
    rejected=release(p,'v2',{**checks,'authorization':False})
    assert rejected['active']=='v1' and rejected['history'][-1]['decision']=='rejected'
    with pytest.raises(ValueError):release(p,'v3',{'functional':True})
    assert release(p,'v3',checks)['active']=='v3'
