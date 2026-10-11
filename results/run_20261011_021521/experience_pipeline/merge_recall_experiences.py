import json, pathlib
strict=pathlib.Path('experiments/unused_attack_mitigation/experiences/llm_judgments.jsonl')
delta=pathlib.Path('experiments/unused_attack_mitigation/experiences_recall_delta/llm_judgments.jsonl')
out=pathlib.Path('experiments/unused_attack_mitigation/llm_judgments_recall.jsonl')
merged={}
for p in (strict,delta):
    if p.exists():
        for line in p.open():
            r=json.loads(line)
            gid=str(r['graph_id'])
            prev=merged.get(gid)
            if prev is None or (prev.get('error') and not r.get('error')):
                merged[gid]=r
with out.open('w') as h:
    for r in merged.values(): h.write(json.dumps(r,ensure_ascii=False)+'\n')
ok=sum(1 for r in merged.values() if not r.get('error'))
adm=sum(1 for r in merged.values() if not r.get('error') and (r.get('llm_judgment') or {}).get('is_reusable_experience') is True)
print('merged rows:',len(merged),'ok:',ok,'admitted:',adm)
