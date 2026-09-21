#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--nodes',required=True); p.add_argument('--edges',required=True); p.add_argument('--allowlist',required=True); p.add_argument('--receipt',required=True); a=p.parse_args()
nodes=json.loads(Path(a.nodes).read_text()); edges=json.loads(Path(a.edges).read_text()); allow=set(json.loads(Path(a.allowlist).read_text()))
ids=[n['id'] for n in nodes]; ids_set=set(ids); edge_keys=[]; broken=[]; unknown=[]
for e in edges:
    k=e.get('edge_key') or (e['source_id'],e['relationship_type'],e['target_id']); edge_keys.append(str(k))
    if e['source_id'] not in ids_set or e['target_id'] not in ids_set: broken.append(e)
    if e['relationship_type'] not in allow: unknown.append(e)
r={'node_count':len(nodes),'edge_count':len(edges),'duplicate_node_ids':len(ids)-len(ids_set),'duplicate_edge_keys':len(edge_keys)-len(set(edge_keys)),'broken_endpoints':len(broken),'unknown_relationship_types':len(unknown)}
r['pass']=all(r[k]==0 for k in ['duplicate_node_ids','duplicate_edge_keys','broken_endpoints','unknown_relationship_types'])
Path(a.receipt).write_text(json.dumps(r,indent=2)+'\n'); print(json.dumps(r,indent=2)); sys.exit(0 if r['pass'] else 1)
