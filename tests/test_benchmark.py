from app.benchmark import evaluate_model, load_split, top
import json
from zipfile import ZipFile
import pytest

def fixture(id, text):
    parts = text.split('|')
    start=0; spans=[]
    for part in parts:
        spans.append([start,start+len(part)]);start+=len(part)+1
    return {'documents':[{'id':id,'text':text,'spans':spans,'annotation_sets':[{'annotations':{'nda-1':{'choice':'Entailment','spans':[0]},'nda-2':{'choice':'NotMentioned','spans':[]}}}]}], 'labels':{'nda-1':{'hypothesis':'confidential records destroyed'},'nda-2':{'hypothesis':'payment'}}}

def test_benchmark_fixture():
    pytest.importorskip('sklearn')
    r=evaluate_model(fixture(1,'confidential records destroyed|office address|company contact'),fixture(2,'destroyed confidential files|office hours|phone contact'))
    assert r['test_queries']==1 and r['train_span_pairs']==3
    assert set(r['metrics'])=={'lexical','trained'}
    assert all(0<=x<=1 for v in r['metrics'].values() for x in v.values())
    assert 'confidential files' not in json.dumps(r)

def test_split_overlap():
    d=fixture(1,'confidential records destroyed|office address')
    with pytest.raises(ValueError,match='overlap'): evaluate_model(d,d)

def test_archive(tmp_path):
    path=tmp_path/'sample.zip';d=fixture(1,'one|two')
    with ZipFile(path,'w') as z:z.writestr('contract-nli/train.json',json.dumps(d))
    assert load_split(path,'train')==d
    with pytest.raises(ValueError):load_split(path,'test')

def test_ranking_ties(): assert top([0.2,0.5,0.5,0.1])==[1,2,0]
