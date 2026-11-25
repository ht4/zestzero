from app.playground import simulate, matrix
from app.main import app
from fastapi.testclient import TestClient

def test_all_corrected_scenarios():
    rows=matrix()['scenarios']
    assert len(rows)==96
    assert all(r['passed'] for r in rows if r['version']=='corrected')
    assert any(not r['passed'] for r in rows if r['version']=='baseline')

def test_cross_matter():
    bad=simulate('baseline','analyst-a','pricing','document')
    good=simulate('corrected','analyst-a','pricing','document')
    assert not bad['passed'] and bad['observed']['sources']==['B-1']
    assert good['passed'] and not good['observed']['text']

def test_revoked_summary():
    assert not simulate('baseline','analyst-b','pricing','revoked')['passed']
    assert simulate('corrected','analyst-b','pricing','revoked')['passed']

def test_current_source_and_abstention():
    assert simulate('corrected','analyst-a','notice','document')['observed']['sources']==['A-2']
    assert simulate('corrected','reviewer','budget','document')['observed']['status']=='abstain'

def test_api_and_invalid_input():
    c=TestClient(app)
    params=dict(version='corrected',user='analyst-a',topic='pricing',operation='document')
    assert c.get('/api/playground',params=params).json()==simulate(**params)
    assert c.get('/api/playground',params={**params,'user':'real-user'}).status_code==422
