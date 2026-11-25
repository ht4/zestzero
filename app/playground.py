"""Interactive, synthetic-only scenario runner. No external services."""
from datetime import datetime, timezone
from itertools import product
from pathlib import Path
import json
from app.sandbox import Sandbox

VERSIONS = ('baseline', 'corrected')
USERS = ('analyst-a', 'analyst-b', 'reviewer', 'unknown')
TOPICS = ('notice', 'pricing', 'budget', 'public')
OPERATIONS = ('document', 'summary', 'revoked')

def simulate(version, user, topic, operation):
    if not (version in VERSIONS and user in USERS and topic in TOPICS and operation in OPERATIONS):
        raise ValueError('Unsupported synthetic scenario')
    sandbox = Sandbox(version == 'corrected')
    # Only predefined synthetic inputs are available. Summary authored by the
    # authorized reviewer; revocation applies to the selected restricted matter.
    matter = {'notice': 'A', 'pricing': 'B'}.get(topic)
    if operation == 'document':
        result = sandbox.query(user, topic)
    else:
        sandbox.save_summary('reviewer', topic, 'demo-summary')
        if operation == 'revoked' and matter and user in sandbox.grants:
            sandbox.revoke(user, matter)
        result = sandbox.read_summary(user, 'demo-summary')
    # Independent expectation from the fictional access policy, not the
    # returned result or Sandbox.allowed(). Public context requires a known ID.
    grants = {'analyst-a': ('A',), 'analyst-b': ('B',), 'reviewer': ('A','B')}
    authorized = user in grants and (topic == 'public' or matter in grants[user])
    if operation == 'revoked' and matter:
        authorized = False
    expected_source = {'notice':'A-2','pricing':'B-1','public':'P-1'}.get(topic)
    if authorized and expected_source:
        passed = result['status']=='answered' and result['sources']==[expected_source] and bool(result['text'])
        expectation = 'current_source'
    else:
        passed = result['status'] in ('denied','abstain') and not result['sources'] and not result['text']
        expectation = 'no_content'
    return dict(version=version,user=user,topic=topic,operation=operation,expected=expectation,
                expected_source=expected_source if authorized else None,passed=passed,observed=result)

def matrix():
    return {'scope':'Synthetic public demonstration; not production authentication or LLM inference.',
            'executed_at':datetime.now(timezone.utc).isoformat(),
            'scenarios':[simulate(*args) for args in product(VERSIONS, USERS, TOPICS, OPERATIONS)]}

if __name__ == '__main__':
    dest=Path(__file__).resolve().parents[1]/'site/playground.json'
    dest.write_text(json.dumps(matrix(), indent=2)+'\n')
    print(dest)
