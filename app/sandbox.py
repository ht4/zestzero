"""Isolated synthetic legal retrieval fixture. No real user authentication or LLM."""
from dataclasses import dataclass
from pathlib import Path
import json

CASE = json.loads((Path(__file__).resolve().parents[1] / 'data/case.json').read_text())

@dataclass(frozen=True)
class Document:
    id: str
    matter: str
    topic: str
    version: int
    text: str
    active: bool

class Sandbox:
    def __init__(self, corrected: bool):
        self.corrected = corrected
        self.docs = [Document(**d) for d in CASE['documents']]
        self.grants = {'analyst-a': {'A'}, 'analyst-b': {'B'}, 'reviewer': {'A','B'}}
        self.summaries = {}

    def allowed(self, user, doc):
        return user in self.grants and (doc.matter == 'PUBLIC' or doc.matter in self.grants[user])

    def revoke(self, user, matter):
        self.grants[user].discard(matter)

    def query(self, user, topic):
        if user not in self.grants:
            return {'status':'denied','text':'','sources':[]}
        candidates = [d for d in self.docs if d.topic == topic]
        if self.corrected:
            candidates = [d for d in candidates if self.allowed(user,d) and d.active]
        if not candidates:
            if not self.corrected and topic == 'budget':
                return {'status':'answered','text':'Unsupported synthetic estimate: 50000.','sources':[]}
            return {'status':'abstain','text':'','sources':[]}
        chosen = sorted(candidates, key=lambda d:d.version, reverse=self.corrected)[0]
        return {'status':'answered','text':chosen.text,'sources':[chosen.id]}

    def save_summary(self, user, topic, key):
        result = self.query(user,topic)
        if result['status'] == 'answered':
            self.summaries[key] = {'owner':user, **result}
        return result

    def read_summary(self, user, key):
        summary = self.summaries.get(key)
        if not summary or user not in self.grants:
            return {'status':'denied','text':'','sources':[]}
        if self.corrected:
            docs = {d.id:d for d in self.docs}
            if not summary['sources'] or not all(s in docs and self.allowed(user,docs[s]) and docs[s].active for s in summary['sources']):
                return {'status':'denied','text':'','sources':[]}
        return {k:summary[k] for k in ('status','text','sources')}
