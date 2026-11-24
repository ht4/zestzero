"""Reproducible checks, decision rules and audit evidence."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
from app.sandbox import Sandbox, CASE

# References are indicative, not a complete conformity assessment.
CHECKS = [
 ('ZZ-01','Authorized retrieval','medium','ISO A.5.15 / AISVS 5.2.2','Confirm legitimate users can retrieve the current contract.'),
 ('ZZ-02','Cross-matter isolation','critical','ISO A.5.15 / AISVS 5.2.2','Enforce the requesting identity at retrieval.'),
 ('ZZ-03','Derived summary isolation','critical','ISO A.5.15 / OWASP RAG','Recheck source permissions when reading generated content.'),
 ('ZZ-04','Revoked access to summary','high','ISO A.5.18 / OWASP RAG','Invalidate or reauthorize stored content after revocation.'),
 ('ZZ-05','Revoked access to source','high','ISO A.5.18 / OWASP RAG','Apply current grants on every retrieval.'),
 ('ZZ-06','Current contract version','high','ISO A.5.33 / document integrity','Exclude superseded clauses; preserve source identifiers.'),
 ('ZZ-07','Unsupported assertion','medium','OWASP RAG / output validation','Abstain when no supporting document exists.'),
 ('ZZ-08','Public context retrieval','medium','ISO A.5.15 / AISVS 5.2.2','Keep permitted public context available.'),
 ('ZZ-09','Unknown identity denied','high','ISO A.5.16 / AISVS 5.2.2','Reject identities not in the laboratory directory.')
]

def evaluate(corrected):
    out=[]
    for i,(ident,name,severity,control,action) in enumerate(CHECKS):
        s=Sandbox(corrected)
        if i==0:
            r=s.query('analyst-a','notice'); ok=r['status']=='answered' and all(x.startswith('A-') for x in r['sources']) and bool(r['sources']); expected='Authorized document returned'
        elif i==1:
            r=s.query('analyst-a','pricing'); ok=r['status']!='answered' and not r['sources'] and not r['text']; expected='No restricted source or content returned'
        elif i==2:
            s.save_summary('analyst-b','pricing','summary-b'); r=s.read_summary('analyst-a','summary-b'); ok=r['status']=='denied' and not r['sources'] and not r['text']; expected='Derived summary denied across matters'
        elif i==3:
            s.save_summary('analyst-b','pricing','summary-b'); s.revoke('analyst-b','B'); r=s.read_summary('analyst-b','summary-b'); ok=r['status']=='denied' and not r['sources'] and not r['text']; expected='Previously authorized summary denied after revocation'
        elif i==4:
            s.revoke('analyst-b','B'); r=s.query('analyst-b','pricing'); ok=r['status']!='answered' and not r['sources'] and not r['text']; expected='Source not returned after revocation'
        elif i==5:
            r=s.query('analyst-a','notice'); ok=r['sources']==['A-2'] and '60 days' in r['text']; expected='Active amendment A-2 (60 days)'
        elif i==6:
            r=s.query('analyst-a','budget'); ok=r['status']=='abstain' and not r['sources'] and not r['text']; expected='Abstain when no supporting document exists'
        elif i==7:
            r=s.query('analyst-a','public'); ok=r['status']=='answered' and r['sources']==['P-1']; expected='Public reference P-1 returned'
        else:
            r=s.query('unknown','notice'); ok=r['status']=='denied' and not r['sources'] and not r['text']; expected='Unknown identity denied'
        # Never export document contents; record a fingerprint for reproducibility.
        observed={'status':r['status'],'source_ids':r['sources'],'content_returned':bool(r['text']),'content_sha256':sha256(r['text'].encode()).hexdigest() if r['text'] else None}
        row={'id':ident,'name':name,'severity':severity,'control':control,'expected':expected,'observed':observed,'passed':bool(ok),'action':action,'owner':'Security / Engineering (proposed)','review':'pending human validation'}
        row['evidence_sha256']=sha256(json.dumps(row,sort_keys=True).encode()).hexdigest()
        out.append(row)
    failed=[r for r in out if not r['passed']]
    decision='BLOCK' if any(r['severity'] in ('critical','high') for r in failed) else ('REVIEW' if failed else 'READY FOR HUMAN REVIEW')
    return {'version':'corrected' if corrected else 'baseline','executed_at':datetime.now(timezone.utc).isoformat(),'total':len(out),'passed':len(out)-len(failed),'failed':len(failed),'decision':decision,'checks':out}

def snapshot():
    return {'case':{k:CASE[k] for k in ('title','context','sources')},'runs':{v:evaluate(v=='corrected') for v in ('baseline','corrected')},'scope':'Synthetic laboratory, deterministic extractive retrieval; no real LLM, authentication, or third-party testing.'}

if __name__=='__main__':
    dest=Path(__file__).resolve().parents[1]/'site/results.json'
    dest.write_text(json.dumps(snapshot(),indent=2)+'\n')
    print(dest)
