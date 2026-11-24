"""ContractNLI evidence-ranking benchmark. Not an entailment or legal advice model."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import random
import re
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'https://stanfordnlp.github.io/contract-nli/'
LABELS = {'Entailment', 'Contradiction'}
TOKEN = re.compile(r"[a-z]{2,}")
STOP = set('the a an of to in and or for by as is be are that this with shall may it on from at'.split())


def words(text):
    return [w for w in TOKEN.findall(text.lower()) if w not in STOP]


def load_split(archive, name):
    with ZipFile(archive) as z:
        matches = [i for i in z.infolist() if i.filename.rsplit('/', 1)[-1] == name + '.json']
        if len(matches) != 1 or matches[0].file_size > 100_000_000:
            raise ValueError(f'Expected exactly one reasonable-sized {name}.json in original ZIP')
        return json.loads(z.read(matches[0]))


def groups(split):
    for d in split['documents']:
        spans = [words(d['text'][a:b]) for a, b in d['spans']]
        annotations = d['annotation_sets'][0]['annotations']
        for key, ann in sorted(annotations.items()):
            if ann['choice'] not in LABELS:
                continue  # evidence retrieval is undefined for NotMentioned
            gold = set(ann['spans'])
            if not gold or min(gold) < 0 or max(gold) >= len(spans):
                raise ValueError(f'Invalid evidence annotation in document {d["id"]}')
            yield str(d['id']), key, words(split['labels'][key]['hypothesis']), spans, gold


def feature(key, query, span):
    # Hypothesis-specific and shared features; no annotation, document ID or split in inputs.
    common = set(query).intersection(span)
    return ' '.join(['shared_'+w for w in span] + [key.replace('-', '_')+'_'+w for w in span] + ['overlap_'+w for w in sorted(common)]) or 'empty_span'


def baseline_score(query, span):
    q, s = set(query), set(span)
    return len(q & s) / max(1, len(q))


def train_model(split):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    rng = random.Random(42)
    x, y = [], []
    for _, key, q, spans, gold in groups(split):
        negatives = [i for i in range(len(spans)) if i not in gold]
        selected = sorted(gold) + rng.sample(negatives, min(len(negatives), 5*len(gold)))
        for i in selected:
            x.append(feature(key, q, spans[i]))
            y.append(int(i in gold))
    model = make_pipeline(TfidfVectorizer(token_pattern=r'(?u)\b\w+\b', max_features=60000, sublinear_tf=True), LogisticRegression(max_iter=300, class_weight='balanced', random_state=42))
    model.fit(x,y)
    return model, len(y)


def top(scores, k=3):
    return sorted(range(len(scores)), key=lambda i: (-scores[i], i))[:k]


def evaluate_model(train, test):
    def ids(s): return {str(d['id']) for d in s['documents']}
    def hashes(s): return {sha256(d['text'].encode()).hexdigest() for d in s['documents']}
    if ids(train) & ids(test) or hashes(train) & hashes(test):
        raise ValueError('Train/test overlap: benchmark stopped')
    model, n = train_model(train)
    metrics = {k:{'hit1':0., 'hit3':0., 'recall3':0.} for k in ('lexical','trained')}
    examples = []
    count = 0
    for doc, key, q, spans, gold in groups(test):
        scores = model.predict_proba([feature(key,q,s) for s in spans])[:,1]
        ranks = {'lexical':top([baseline_score(q,s) for s in spans]), 'trained':top(scores)}
        for mode, rank in ranks.items():
            found = set(rank) & gold
            metrics[mode]['hit1'] += int(bool(rank and rank[0] in gold))
            metrics[mode]['hit3'] += int(bool(found))
            metrics[mode]['recall3'] += len(found)/len(gold)
        count += 1
        if len(examples) < 8:
            examples.append({'document_id':doc,'hypothesis_id':key,'gold_span_ids':sorted(gold),'ranked_span_ids':ranks['trained'],'hit_at_3':bool(set(ranks['trained']) & gold)})
    if not count: raise ValueError('No annotated evidence queries in test split')
    for scores in metrics.values():
        for k in scores: scores[k] = round(scores[k]/count, 6)
    return {'status':'measured','dataset':'ContractNLI','source':SOURCE,'license':'CC BY 4.0','model':'TF-IDF + supervised logistic regression','train_documents':len(train['documents']),'test_documents':len(test['documents']),'train_span_pairs':n,'test_queries':count,'metrics':metrics,'examples':examples,'scope':'Evidence retrieval on official train/test splits; excludes NotMentioned; no entailment classification, LLM or legal advice. No raw document text exported.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('archive',type=Path,help='Original ContractNLI ZIP downloaded after reading its terms')
    args=p.parse_args()
    train,test=(load_split(args.archive,name) for name in ('train','test'))
    print(f'Loaded {len(train["documents"])} train and {len(test["documents"])} test contracts.',flush=True)
    result=evaluate_model(train,test)
    result['archive_sha256']=sha256(args.archive.read_bytes()).hexdigest()
    result['executed_at']=datetime.now(timezone.utc).isoformat()
    import sklearn
    result['sklearn_version']=sklearn.__version__
    dest=ROOT/'site/benchmark.json'
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('examples',)},indent=2))
    print(dest)

if __name__=='__main__': main()
