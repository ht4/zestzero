from app.assurance import evaluate, snapshot
from app.sandbox import Sandbox
from app.main import app
from fastapi.testclient import TestClient

def test_baseline():
    r=evaluate(False); assert r['decision']=='BLOCK'; assert r['passed']==3; assert r['failed']==6

def test_corrected():
    r=evaluate(True); assert r['passed']==9 and r['failed']==0; assert r['decision']=='READY FOR HUMAN REVIEW'

def test_cross_matter():
    s=Sandbox(True); assert s.query('analyst-a','pricing')['text']==''

def test_revocation_summary():
    s=Sandbox(True); assert s.save_summary('analyst-b','pricing','b')['status']=='answered'; s.revoke('analyst-b','B'); assert s.read_summary('analyst-b','b')['status']=='denied'

def test_no_raw_content_in_evidence():
    import json
    r=json.dumps(snapshot()); assert 'CANARY-B-482' not in r; assert '72000' not in r

def test_stable_evidence():
    assert evaluate(True)['checks']==evaluate(True)['checks']

def test_current_version():
    assert Sandbox(True).query('analyst-a','notice')['sources']==['A-2']

def test_api():
    c=TestClient(app); assert c.get('/').status_code==200; assert c.get('/api/results').json()['runs']['corrected']['passed']==9
