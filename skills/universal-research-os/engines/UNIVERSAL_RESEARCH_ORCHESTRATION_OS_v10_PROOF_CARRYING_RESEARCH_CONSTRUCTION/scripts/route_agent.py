#!/usr/bin/env python3
import argparse,json
ap=argparse.ArgumentParser();ap.add_argument('situation',choices=['dispatch','child','admission','audit','repair','promote','production-pipeline','reconcile','global-seal','release','migrate']);a=ap.parse_args()
m={'dispatch':'modules/dispatcher','child':'modules/child_runtime','admission':'modules/control_plane','audit':'modules/audit_os_v6_proof_carrying_construction','repair':'modules/repair','promote':'modules/production_release','production-pipeline':'scripts/run_child_production_pipeline.py','reconcile':'modules/reconciliation','global-seal':'modules/global_semantic_evidence_seal','release':'modules/release','migrate':'migration'}
print(json.dumps({'module':m[a.situation]},indent=2))
