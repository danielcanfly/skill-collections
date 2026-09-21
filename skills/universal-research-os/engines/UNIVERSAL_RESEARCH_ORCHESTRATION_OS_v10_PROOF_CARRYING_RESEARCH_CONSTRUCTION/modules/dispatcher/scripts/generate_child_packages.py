#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import argparse,csv,hashlib,json,re,shutil,zipfile
ROOT=Path(__file__).resolve().parents[1]
OS_ROOT=Path(__file__).resolve().parents[3]
AUDIT_CANONICAL=OS_ROOT/'modules/audit_os_v6_proof_carrying_construction'
RUNTIME=OS_ROOT/'modules/child_runtime'
PROOF=OS_ROOT/'modules/proof_carrying_construction'
REQ_CLASSES=['definition','comparison','how-to','decision/application','audit','source-provenance','multi-hop','adversarial']
ALLOWED_CLAIM_TYPES=['definition','formula','boundary','mechanism','driver','decision-rule','diagnostic-rule','audit-rule','case-fact','failure-mode','comparison','relationship','limitation','assumption','calculation','framework']
def w(p,s): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(s,encoding='utf-8')
def b(xs): return '\n'.join('- '+str(x) for x in xs)
def sha_text(s): return hashlib.sha256(s.encode()).hexdigest()
def csv_header(p,h): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(','.join(h)+'\n',encoding='utf-8')
def copytree(src,dst):
 for p in src.rglob('*'):
  rel=p.relative_to(src)
  if '__pycache__' in rel.parts or p.suffix in {'.pyc','.pyo'}: continue
  if p.is_dir(): (dst/rel).mkdir(parents=True,exist_ok=True)
  else: (dst/rel).parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,dst/rel)
def internal_tests(nodes):
 out=[]; i=1
 for n in nodes:
  qs=[('definition',n['definition_query']),('decision/application',n['decision_query']),('adversarial',n['failure_query'])]
  for j,(cl,q) in enumerate(qs):
   hold=(j==2); out.append({'test_id':f'RT{i:03d}','class':cl,'query':q,'expected_ids':[n['candidate_id']],'negative_ids':[n['negative_candidate_id']],'is_holdout':hold,'holdout':hold,'split':'holdout' if hold else 'development','notes':'Query, class, holdout flags and negative IDs are dispatcher-authored. Expected IDs may change only through approved node migration.','primary_source_binding_required':cl=='source-provenance'}); i+=1
 for idx,cl in enumerate(REQ_CLASSES): out[idx]['class']=cl
 return out
def auditor_tests(items):
 out=[]
 for t in items:
  x=dict(t); x.update({'split':'auditor-holdout','is_holdout':True,'holdout':True,'immutable_query':True,'immutable_expected_ids':True,'query_sha256':sha_text(t['query'])}); out.append(x)
 return out
def authority_tests(items):
 out=[]
 for t in items:
  x=dict(t); x.update({'class':'source-provenance','query_sha256':sha_text(t['query']),'primary_source_ids':[],'secondary_or_practitioner_negative_ids':[],'binding_status':'REQUIRED_BEFORE_FINALISATION','is_holdout':True,'holdout':True,'split':'auditor-holdout','immutable_query':True}); out.append(x)
 return out
def write_topic_docs(root,domain,c):
 nodes=c['expected_nodes']; modules=c['research_modules']; routes=c['mandatory_source_routes']; risks=c['semantic_risks'];
 w(root/'00_PASTE_THIS_PROMPT_FIRST.txt',f'''你正在執行一個已指定主題的 Knowledge OS 深度研究與 proof-carrying research construction 施工任務。這不是一般研究報告。\n\nSession ID：{c['session_id']}\n主題：{c['title']} / {c['title_en']}\nFinal output：`{c['final_output_name']}`\nCandidate version：`{c['candidate_version']}`
Pipeline production release：`{c.get('production_release_output_name', c['final_output_name'].replace('PRODUCTION_CANDIDATE','PRODUCTION_RELEASE'))}`\nEvidence-backed case minimum：{c['case_minimum']}\n\n# Mission\n{c['mission']}\n\n# Gate 0\n完整填寫 `24_GATE0_RESPONSE_TEMPLATE.md`。必須列出全部 modules、ownership、exclusions、expected nodes、source routes、semantic risks、exact schemas、case floor、八類 retrieval、locked auditor tests、source authority tests、candidate self-check followed by external independent semantic audit、final seal state machine與final filename。\n\n# 唯一 final sequence\n在 candidate 根目錄執行 `python qa/finalize_candidate.py . --case-min {c['case_minimum']} --output-zip ../{c['final_output_name']}`；Builder 完成後由 orchestration 執行 v10 admission、外部 Audit OS v6，並用 `promote_audited_candidate.py` 將 exact audited ZIP 提升為 production release。不得以 builder self-check 取代獨立審計。\n''')
 w(root/'01_TOPIC_MASTER_SPEC.md',f'''# Topic Master Spec\n\n- Domain: {domain['domain_title']} / {domain['domain_title_en']}\n- Session ID: `{c['session_id']}`\n- Topic: {c['title']}\n- English: {c['title_en']}\n- Candidate version: `{c['candidate_version']}`\n\n## Mission\n{c['mission']}\n\n## Canonical ownership\n{b(c['canonical_ownership'])}\n\n## Explicit exclusions\n{b(c['explicit_exclusions'])}\n\n## Core questions\n{chr(10).join(f'{i+1}. {q}' for i,q in enumerate(c['core_questions']))}\n\n## Evidence-backed case minimum\n{c['case_minimum']}\n\n## Final output\n`{c['final_output_name']}`\n''')
 parts=['# Research Content Blueprint','']
 for m in modules:
  parts += [f"## {m['module_id']}｜{m['title']}",'','### Must research',b(m['must_research']),'','### Must compare',b(m['must_compare']),'','### Required source families',b(m['source_families']),'','### Expected outputs',b(m['expected_outputs']),'']
 w(root/'02_RESEARCH_CONTENT_BLUEPRINT.md','\n'.join(parts))
 with (root/'03_EXPECTED_NODE_CATALOG.csv').open('w',encoding='utf-8',newline='') as f:
  wr=csv.writer(f);wr.writerow(['candidate_id','kind','title','definition_query','decision_query','failure_query','negative_candidate_id']);
  for n in nodes:wr.writerow([n[k] for k in ['candidate_id','kind','title','definition_query','decision_query','failure_query','negative_candidate_id']])
 w(root/'04_MANDATORY_SOURCE_SEEDS.md','# Mandatory Source Routes\n\n'+'\n\n'.join(f"## {r['route_id']}｜{r['source_family']}\n- Authority tier: `{r['authority_tier']}`\n- Target examples: {', '.join(r['target_examples'])}\n- Why required: {r['why_required']}\n- Challenge/limit query: {r['challenge_or_limit_query']}" for r in routes))
 w(root/'05_DEBATES_FAILURES_AND_COUNTEREXAMPLES.md','# Debates, Failures and Counterexamples\n\n'+b(c['debates']))
 w(root/'06_CASE_PLAN.md',f"# Case Plan\n\nMinimum evidence-backed cases: **{c['case_minimum']}**\n\nRequired types:\n{b(c['case_types'])}\n\nIllustrative or invented calculations do not count as evidence-backed cases.\n")
 w(root/'07_TOPIC_SEMANTIC_RISK_REGISTER.md','# Topic Semantic Risks\n\n'+'\n\n'.join(f"## {x['risk_id']}\n- Risk: {x['risk']}\n- Affected nodes: {', '.join(x['affected_nodes'])}\n- Preventive control: {x['preventive_control']}\n- Required evidence: {x['required_evidence']}" for x in risks))
 w(root/'08_DOMAIN_OWNERSHIP_MAP.md','# Domain Ownership Map\n\n## Owned here\n'+b(c['canonical_ownership'])+'\n\n## Excluded / external ownership\n'+b(c['explicit_exclusions'])+'\n')
 w(root/'09_EXECUTION_ORDER.md','# Execution Order\n\nGate 0 → Phase 1–10 → internal retrieval → locked auditor tests → source authority binding → semantic validators → candidate self-check followed by external independent semantic audit → idempotency → manifest last → ZIP → fresh-extraction Audit OS.\n')
 w(root/'11_ONE_SHOT_PHASE_1_TO_10_PLAN.md','# One-Shot Phase 1–10\n\n1 Scope lock\n2 Source landscape\n3 Acquisition and verification\n4 Atomic claims\n5 Canonicalisation/dedup\n6 Knowledge nodes\n7 Cases/counterexamples\n8 Graph and lineage\n9 Retrieval/semantic QA\n10 final seal and return.\n')
 w(root/'12_REQUIRED_SEARCH_QUERY_BANK.md','# Required Search Query Bank\n\n'+'\n\n'.join(f"## {m['module_id']}｜{m['title']}\n"+'\n'.join(f"- `{q}`" for q in [f'\"{m["title"]}\" official primary authority definition',f'\"{m["title"]}\" academic empirical evidence',f'\"{m["title"]}\" limitations criticism failure',f'\"{m["title"]}\" first-party case evidence']) for m in modules))
 with (root/'13_RESEARCH_MODULE_MATRIX.csv').open('w',encoding='utf-8',newline='') as f:
  wr=csv.writer(f);wr.writerow(['module_id','title','must_research','must_compare','source_families','expected_outputs','status']);
  for m in modules:wr.writerow([m['module_id'],m['title'],' | '.join(m['must_research']),' | '.join(m['must_compare']),' | '.join(m['source_families']),' | '.join(m['expected_outputs']),'NOT_STARTED'])
 for no,title,body in [
  (14,'CONTENT_COMPLETENESS_CHECKLIST','Every canonical node requires definition, boundary, variants, assumptions, mechanism, calculation/decision logic, data requirements, limitations, failure modes, counter-metrics, cases, lineage and retrieval coverage.'),
  (15,'GOLD_STANDARD_LESSONS','Do not trust all-green internal validators. Prevent all-support provenance, source-note boilerplate, parser-invisible holdouts, stale identities, duplicate merge trees and post-manifest mutation.'),
  (16,'SEMANTIC_PROVENANCE_CONTRACT','Allowed support values: support, partial-support, contextual-support, challenge. Direct support must establish the atomic claim within scope.'),
  (17,'SOURCE_METADATA_RECONCILIATION_CONTRACT','Separate verified year, effective/reporting date, accessed date, exact entity identity, rename/successor status, publisher, URL/DOI and access level.'),
  (18,'EXACT_PRODUCTION_SCHEMAS','Use the exact CSV headers supplied in the output skeleton. Do not rename or omit parser-consumed columns.'),
  (19,'TOPIC_SPECIFIC_SEMANTIC_RISK_REGISTER','Resolve every predeclared risk with claim IDs, source IDs, resolution, residual gap and status.'),
  (20,'EVIDENCE_BACKED_CASE_STANDARD','Cases require identifiable event/entity/context, traceable sources, mechanism, what was known at decision time, outcome and transfer limits.'),
  (21,'SOURCE_NOTE_PRODUCTION_PROFILE','Every source note requires source-specific findings, what it does not establish, method/population/period/jurisdiction limits, locators and reverse claim/node links.'),
  (22,'RETRIEVAL_GRAPH_LINEAGE_QA','At least 40 internal tests, boolean holdout and negative coverage ≥25%, eight classes, locked auditor tests and source authority ranking.'),
  (23,'ONE_SHOT_FINAL_ACCEPTANCE','Return only after external fresh-extraction Audit OS says MERGE_READY, score 100/100, P0=0 and P1=0.'),
  (25,'PREDELIVERY_AUDIT_OS_PROTOCOL','Run `scripts/run_predelivery_audit.py` against the final ZIP. Do not audit only the working directory.'),
  (26,'KNOWN_FAILURE_PREVENTION_MATRIX','All prior failure modes are blockers: meta-claims, all-support edges, template notes, zero recognized holdouts, primary-source rank failure, duplicate merge surface, stale identity and manifest drift.'),
  (27,'FINAL_SEAL_STATE_MACHINE','Receipts first, idempotency, manifest last, read-only verification, ZIP, fresh extraction audit, no later mutation.'),
  (28,'MANUAL_SEMANTIC_AUDIT_PROTOCOL','Manually sample high-risk support edges, primary claims, cases, source-note limitations and retrieval results. Record exact clauses and decisions.'),
  (29,'AUDITOR_HOLDOUT_CONTRACT','Dispatcher-authored queries and hashes are immutable. Expected ID migration requires documented node disposition.'),
  (30,'VERSION_IDENTITY_AND_MANIFEST_CONTRACT','All authoritative identity surfaces must match the final version and filename.'),
  (31,'SOURCE_IDENTITY_AND_TEMPORAL_METADATA_CONTRACT','Never infer publication year from access year. Record corporate renames, document versions and effective periods explicitly.'),
  (32,'SUPPORT_CALIBRATION_DECISION_TREE','Use support only for direct establishment; partial for incomplete coverage; contextual for background/transfer; challenge for contradiction or boundary stress.'),
  (33,'SOURCE_NOTE_ANTI_BOILERPLATE_STANDARD','Repeated disclaimer shells or semantically near-identical findings across many notes fail.'),
  (34,'NO_DUPLICATE_MERGE_SURFACE_CONTRACT','`knowledge/` is the only authoritative merge surface.'),
  (35,'CANDIDATE_LOCAL_CLOSURE_SCRIPTS','All scripts needed to reproduce retrieval, validation, idempotency and manifest verification must live inside the candidate.'),
  (36,'RETURN_RECEIPT_TEMPLATE','Return filename, SHA-256, Audit OS status/score, internal retrieval, auditor holdout, manual sample count, gaps and waivers.')]:
  w(root/f'{no:02d}_{title}.md',f'# {title.replace("_"," ").title()}\n\n{body}\n')
 w(root/'24_GATE0_RESPONSE_TEMPLATE.md',f'''# Gate 0 Response\n\n- Session ID: `{c['session_id']}`\n- Final output: `{c['final_output_name']}`\n- Modules: list all {len(modules)}\n- Ownership: list all\n- Exclusions: list all\n- Expected nodes: list all {len(nodes)}\n- Source routes: list all {len(routes)}\n- Semantic risks: list all {len(risks)}\n- Case floor: {c['case_minimum']}\n- Exact schemas confirmed: YES/NO\n- Eight retrieval classes confirmed: YES/NO\n- 10+ locked auditor tests confirmed: YES/NO\n- 2+ source-authority tests confirmed: YES/NO\n- Candidate self-check confirmed: YES/NO
- External independent semantic review contract confirmed: YES/NO\n- Final seal state machine confirmed: YES/NO\n- Gate result: PASS/STOP\n''')
def skeleton(root,domain,c):
 out=root/'OUTPUT_SKELETON'; qa=out/'qa'; research=out/'research'; hand=out/'handoff'; knowledge=out/'knowledge'; stage_review=out/'external_stage_review'
 for d in [qa,research,hand,stage_review,knowledge/'concepts',knowledge/'patterns',knowledge/'checklists',knowledge/'sources',out/'work']: d.mkdir(parents=True,exist_ok=True)
 for d in [knowledge/'concepts',knowledge/'patterns',knowledge/'checklists',knowledge/'sources']: w(d/'.gitkeep','')
 candidate_id=f"{c['session_id']}-{c['candidate_version']}"
 audit={'orchestration_os_version':'10.0.0','audit_os_version':'6.0.0','contract_generation':'v10','case_minimum':c['case_minimum'],'topic_title':f"{c['title']} / {c['title_en']}",'session_id':c['session_id'],'candidate_id':candidate_id,'candidate_version':c['candidate_version'],'final_output_name':c['final_output_name'],'expected_namespace_prefixes':c['namespace_prefixes'],'shared_namespace_prefixes':['shared/'],'lowercase_slugs':True,'allowed_claim_types':ALLOWED_CLAIM_TYPES,'allowed_support_levels':['support','partial-support','contextual-support','challenge'],'allowed_case_types':['evidence-backed','illustrative','counterexample','failure','comparative'],'minimum_evidence_backed_cases':c['case_minimum'],'minimum_retrieval_tests':40,'minimum_holdout_ratio':.25,'minimum_negative_test_ratio':.25,'required_retrieval_classes':REQ_CLASSES,'manifest_path':'handoff/file_manifest.json','release_stage':'child_candidate','reproducible_generated_at':'2000-01-01T00:00:00Z','production_release_output_name':c.get('production_release_output_name',c['final_output_name'].replace('PRODUCTION_CANDIDATE','PRODUCTION_RELEASE')),'paths':{'claim_ledger':'research/claim_ledger.csv','source_registry':'research/source_metadata_reconciliation.csv','source_identity':'research/source_identity_verification.csv','edge_entailment':'research/edge_entailment.csv','lineage':'research/lineage_cascade_register.csv','case_registry':'research/case_registry.csv','semantic_risks':'research/topic_semantic_risk_resolution.csv','retrieval_cases':'qa/retrieval_test_cases.json','seal_state':'qa/seal_state.json'}}
 w(out/'audit_config.json',json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
 w(qa/'retrieval_test_cases.json',json.dumps(internal_tests(c['expected_nodes']),ensure_ascii=False,indent=2)+'\n')
 w(qa/'AUDITOR_HOLDOUT_TESTS.json',json.dumps(auditor_tests(c['auditor_holdout_tests']),ensure_ascii=False,indent=2)+'\n')
 w(qa/'AUDITOR_SOURCE_PROVENANCE_TESTS.json',json.dumps(authority_tests(c['source_authority_tests']),ensure_ascii=False,indent=2)+'\n')
 w(qa/'reproduction_contract.json',json.dumps({'version':'1.0','root_resolution':'script-relative','source_date_epoch':0,'commands':[{'id':'retrieval','cwd':'.','argv':['{python}','qa/run_retrieval_benchmark.py','--root','{root}'],'outputs':['qa/corpus_manifest.json','qa/retrieval_results.json','qa/retrieval_results.md']}]},indent=2)+'\n')
 w(qa/'production_surface_manifest.json',json.dumps({'version':'1.0','release_stage':'child_candidate','surfaces':[{'surface_id':'knowledge','kind':'knowledge','root':'knowledge'}],'r2_object_plan':None,'audit_only_roots':['qa','research','handoff','work','AUDIT_OS']},indent=2)+'\n')
 # exact CSV headers
 headers={
 'source_snapshot_registry.csv':['source_id','snapshot_path','snapshot_sha256','source_identity_status','production_eligibility'],
 'material_clause_registry.csv':['clause_id','proposed_claim_id','clause_text','passage_ids','support_status','unsupported_remainder','external_pre_review_status'],
 'compiled_direct_support_claims.csv':['claim_id','claim_text','material_clause_ids','passage_ids','construction_method','candidate_reviewer_status'],
 'claim_ledger.csv':['claim_id','module_id','claim','claim_type','subtype','source_id','evidence_family_id','support_challenge','scope','confidence','candidate_node','notes'],
 'source_refresh_queue.csv':['finding_id','source_id','severity','gap_type','required_action','status','notes'],
 'source_metadata_reconciliation.csv':['source_id','current_title','verified_title','verified_authors','verified_year','effective_date_or_period_end','accessed_at','verified_source_type','verified_publisher','verified_doi_or_url','access_status','verification_status','action','evidence_family_id','entity_identity_notes','notes'],
 'case_registry.csv':['case_id','case_type','title','domain','jurisdiction_or_context','decision_or_problem','source_ids','mechanism','what_was_known_at_the_time','outcome','decision_quality_interpretation','transfer_limit','status'],
 'topic_semantic_risk_resolution.csv':['risk_id','risk','affected_nodes','claims','sources','resolution','residual_gap','status'],
 'accepted_sources.csv':['source_id','trust_tier','authority','method','directness','recency','independence','applicability','decision','notes'],
 'raw_source_registry.csv':['source_id','candidate_title','authors','year','source_type','publisher','doi_or_url','access_status','discovery_query','module_id','screening_status','notes'],
 'rejected_sources.csv':['source_id','title','url','rejection_reason','module_id','screened_at','notes'],
 'alias_map.csv':['alias','canonical_id','language','reason','source'],
 'canonical_concept_registry.csv':['id','title','kind','module_id','aliases','broader','contrasts','source_ids','maturity','confidence','status'],
 'confidence_assessment.csv':['canonical_id','confidence','maturity','evidence_basis','conflicts','notes'],
 'evidence_family_registry.csv':['evidence_family_id', 'canonical_name', 'description', 'source_ids', 'issuer_root', 'method_root', 'data_generation_root', 'publication_chain_root', 'derivative_of_family_id', 'independence_basis', 'modules', 'claims', 'status', 'notes'],
 'expected_node_disposition.csv':['candidate_id','final_disposition','final_id_or_ids','reason','evidence','claim_ids','source_ids','source_count','migration_required','status'],
 'source_identity_verification.csv':['source_id', 'declared_title', 'observed_title', 'title_match_status', 'declared_authors', 'observed_authors', 'author_match_status', 'identifier_type', 'declared_identifier', 'observed_identifier', 'identifier_match_status', 'canonical_url', 'publication_date', 'effective_or_period_date', 'accessed_at', 'date_basis', 'access_level', 'verification_method', 'exact_metadata_locator', 'metadata_excerpt', 'verified_proposition', 'abstract_support_allowed', 'identity_status', 'temporal_status', 'reviewer', 'notes', 'metadata_locator', 'identity_verdict', 'reviewer_status','responsible_entity','author_basis','production_eligibility'],
 'edge_entailment.csv':['edge_id','claim_id','source_id','candidate_node','support_label','claim_atomicity_status','passage_id','passage_type','evidence_boundary','exact_source_passage','exact_locator','coverage_ratio','supported_subset','unsupported_remainder','shared_contextual_concept','shared_concept_or_method','source_passage_function','claim_context_function','why_context_not_entailment','transfer_boundary','challenge_description','disposition','candidate_reviewer_status','notes','evidence_origin'],
 'claim_clause_matrix.csv':['claim_id','clause_id','clause_text','materiality','source_id','passage_id','support_status','unsupported_reason','candidate_reviewer_status'],
 'source_passage_registry.csv':['passage_id','source_id','passage_type','excerpt_text','locator_type','locator_value','locator_resolved','snapshot_path','snapshot_sha256','excerpt_sha256','observed_at','candidate_reviewer_status','capture_method','source_access_level','production_eligibility'],
 'source_claim_domain_compatibility.csv':['claim_id','source_id','source_domain','claim_domain','source_kind','transfer_type','compatibility_status','transfer_limit','independent_review_required','candidate_reviewer_status'],
 'lineage_cascade_register.csv':['node_id', 'active_claim_ids', 'active_source_ids', 'context_exception_source_ids', 'registry_source_ids', 'expected_disposition_source_ids', 'node_frontmatter_source_ids', 'source_note_reverse_source_ids', 'case_source_ids', 'source_count', 'status', 'notes'],
 'contextual_relevance_register.csv':['edge_id','claim_id','source_id','shared_concept_or_method','source_passage_function','claim_context_function','why_context_not_entailment','transfer_boundary','exact_locator','reviewer_status','notes'],
 'node_context_source_exceptions.csv':['node_id','source_id','reason','approved_by','status'],
 'source_coverage_matrix.csv':['module_id','question_id','source_id','coverage','directness','status','gap'],
 'source_family_map.csv':['module_id','research_question','source_family','priority','target_examples','status'],
 'provisional_concept_registry.csv':['provisional_id','title','kind','module_id','definition','aliases','source_ids','status','notes'],
 'framework_comparison_matrix.csv':['comparison_id','module_id','framework_a','framework_b','dimension','similarity','difference','non_interchangeability','source_ids','decision'],
 'claim_migration_log.csv':['old_claim_id','new_claim_id','action','reason','sources_changed','nodes_changed','confidence_change']}
 for n,h in headers.items(): csv_header(research/n,h)
 topic_tests=[{'risk_id':r['risk_id'],'failure_mode':r['risk'],'affected_nodes':r.get('affected_nodes',[]),'blocking_rule':r.get('preventive_control',''),'required_evidence':r.get('required_evidence',''),'counterexample_required':True,'independent_review_required':True,'candidate_status_required':'CANDIDATE_SELF_CHECK_PASS'} for r in c.get('semantic_risks',[])]
 w(qa/'TOPIC_SEMANTIC_RED_TEAM_TESTS.json',json.dumps(topic_tests,ensure_ascii=False,indent=2)+'\n')
 csv_header(qa/'TOPIC_SEMANTIC_RED_TEAM_RESULTS.csv',['risk_id','candidate_self_check_status','independent_review_status','counterexample_evidence','notes'])
 csv_header(stage_review/'PASSAGE_REVIEW.csv',['passage_id','row_sha256','verdict','reviewer_id','reviewer_session_id','reviewed_at','notes'])
 csv_header(stage_review/'CLAUSE_REVIEW.csv',['clause_id','row_sha256','verdict','reviewer_id','reviewer_session_id','reviewed_at','notes'])
 w(stage_review/'STAGE_REVIEW_IDENTITY.json',json.dumps({'status':'IN_PROGRESS','contract_generation':'v10','audit_os_version':'6.0.0','reviewer_id':'','reviewer_session_id':'','passage_registry_sha256':'','clause_registry_sha256':''},indent=2)+'\n')
 csv_header(qa/'auditor_test_migration_log.csv',['test_id','old_expected_id','new_expected_id','action','node_disposition_evidence','reason','status'])
 csv_header(qa/'manual_semantic_audit_samples.csv',['sample_id','sample_type','claim_id','source_id','node_id','case_id','locator','exact_supported_clause','unsupported_clause','support_label','review_result','notes'])
 csv_header(hand/'claim_migration_log.csv',headers['claim_migration_log.csv']); csv_header(hand/'source_metadata_reconciliation.csv',headers['source_metadata_reconciliation.csv'])
 for rel,title in [('phase01_scope.md','Phase 1 Scope'),('phase02_source_landscape.md','Phase 2 Source Landscape'),('research_questions.md','Research Questions'),('search_query_bank.md','Executed Search Query Bank'),('acquisition_log.md','Acquisition Log'),('inclusion_exclusion.md','Inclusion and Exclusion'),('paywall_and_access_gaps.md','Paywall and Access Gaps'),('source_quality_rubric.md','Source Quality Rubric'),('conflict_matrix.md','Conflict Matrix'),('deduplication_report.md','Deduplication Report'),('merge_split_decisions.md','Merge Split Decisions'),('ontology_map.md','Ontology Map'),('gap_register.md','Gap Register'),('open_questions.md','Open Questions'),('unresolved_claims.md','Unresolved Claims')]: w(research/rel,f'# {title}\n\n')
 for rel,title in [('REPRODUCE_RETRIEVAL.md','Reproduce Retrieval'),('adversarial_queries.md','Adversarial Queries'),('final_acceptance_checklist.md','Final Acceptance Checklist'),('link_validation.md','Link Validation'),('orphan_and_duplicate_report.md','Orphan and Duplicate Report'),('source_traceability_report.md','Source Traceability Report'),('validation_waivers.md','Validation Waivers')]: w(qa/rel,f'# {title}\n\nExpected final output: `{c["final_output_name"]}`\n')
 for rel,title in [('completion_report.md','Completion Report'),('cross_topic_overlap.md','Cross Topic Overlap'),('migration_log.md','Migration Log'),('open_gaps_and_update_triggers.md','Open Gaps and Update Triggers'),('production_build_summary.md','Production Build Summary'),('blog_article_candidates.md','Blog Article Candidates')]: w(hand/rel,f'# {title}\n\n')
 w(knowledge/'index.md',f'# {c["title"]}\n\nAuthoritative production knowledge lives only under `knowledge/`.\n'); w(knowledge/'log.md','# Knowledge Build Log\n\n')
 w(out/'00_COMPLETION_SUMMARY.md',f'# Completion Summary\n\nCandidate: `{candidate_id}`\nFinal output: `{c["final_output_name"]}`\n')
 w(out/'QUALITY_REPORT.md',f'# Quality Report\n\nFinal output: `{c["final_output_name"]}`\nInternal retrieval target: {len(internal_tests(c["expected_nodes"]))} tests, {sum(x["is_holdout"] for x in internal_tests(c["expected_nodes"]))} holdout.\n')
 w(out/'PHASE_RETURN_MANIFEST.json',json.dumps({'session_id':c['session_id'],'candidate_id':candidate_id,'candidate_version':c['candidate_version'],'final_output_name':c['final_output_name'],'status':'DRAFT'},indent=2)+'\n')
 w(hand/'merge_manifest.json',json.dumps({'candidate_id':candidate_id,'candidate_version':c['candidate_version'],'final_output_name':c['final_output_name'],'authoritative_surface':'knowledge/','status':'DRAFT'},indent=2)+'\n')
 w(hand/'contract_lineage.json',json.dumps({'status':'PENDING_BINDING','originating_handoff_id':f"{c['session_id']}:research:v10:{c['candidate_version']}",'originating_handoff_sha256':'REQUIRED_BEFORE_FINALISATION','orchestration_os_version':'10.0.0','audit_os_version':'6.0.0','contract_generation':'v10','expected_output_name':c['final_output_name'],'source_candidate_sha256':'','repair_contract_sha256':'','researcher_id':'REQUIRED_AT_GATE0','researcher_session_id':'REQUIRED_AT_GATE0'},indent=2)+'\n')
 for n,data in [('corpus_manifest.json',{}),('retrieval_results.json',{}),('package_validation.json',{}),('semantic_provenance_validation.json',{}),('candidate_self_check_receipt.json',{'status':'IN_PROGRESS','decision':'NOT_READY','researcher_id':'','completed_at':'','open_p0':999,'open_p1':999}),('independent_audit_required.json',{'required':True,'must_be_external_to_candidate':True,'audit_os_version':'6.0.0','promotion_required_for_production_release':True}),('seal_state.json',{'state':'CONTENT_IN_PROGRESS','post_manifest_mutations':999,'manifest_generated_after_all_receipts':False,'fresh_extraction_verified':False}),('file_manifest.json',{})]: w((qa if n!='file_manifest.json' else hand)/n,json.dumps(data,indent=2)+'\n')
 w(out/'work/PHASE_STATUS.md','# Phase Status\n\n')
 # candidate QA scripts
 copytree(RUNTIME/'candidate_qa_scripts',qa)
 copytree(PROOF/'scripts',root/'proof_carrying_scripts')
 copytree(PROOF/'schemas',root/'proof_carrying_schemas')
 # duplicate finalizer aliases expected by docs
 # child scripts outside candidate
 copytree(RUNTIME/'handoff_scripts',root/'scripts')
def package_one(domain,c,outdir):
 name=f"{c['session_id'].replace('/','-')}_PROOF_CARRYING_AUDIT_V6_RESEARCH_HANDOFF_v10"; root=outdir/name
 if root.exists(): shutil.rmtree(root)
 root.mkdir(parents=True)
 write_topic_docs(root,domain,c); skeleton(root,domain,c)
 copytree(RUNTIME/'contracts',root/'contracts'); copytree(RUNTIME/'canonical-templates',root/'canonical-templates'); copytree(RUNTIME/'templates',root/'templates'); copytree(RUNTIME/'registry-starters',root/'registry-starters'); copytree(AUDIT_CANONICAL,root/'AUDIT_OS/UNIVERSAL_RESEARCH_AUDIT_OS_v6_PROOF_CARRYING_RESEARCH_CONSTRUCTION')
 w(root/'PREDELIVERY_AUDIT_CONFIG.json',(root/'OUTPUT_SKELETON/audit_config.json').read_text())
 jident={'handoff_id':f"{c['session_id']}:research:v10:{c['candidate_version']}",'handoff_type':'INDEPENDENT_RESEARCH','status':'ACTIVE','orchestration_os_version':'10.0.0','audit_os_version':'6.0.0','contract_generation':'v10','expected_output_name':c['final_output_name'],'source_candidate_sha256':''};w(root/'HANDOFF_IDENTITY.json',json.dumps(jident,indent=2)+'\n');w(root/'HANDOFF_REGISTRATION_TEMPLATE.json',json.dumps({'handoff_id':jident['handoff_id'],'handoff_sha256':'COMPUTE_FROM_FINAL_ZIP','status':'ACTIVE','orchestration_os_version':'10.0.0','audit_os_version':'6.0.0','expected_output_name':c['final_output_name']},indent=2)+'\n')
 w(root/'SOURCE_INPUT_REGISTRY.json',json.dumps({'contract_generation':'v10','inputs':[{'role':'canonical_os','path':'EMBEDDED_RUNTIME_AND_AUDIT','sha256':'GOVERNED_BY_PACKAGE_MANIFEST'}]},indent=2)+'\n')
 w(root/'TARGET_IDENTITY.json',json.dumps({'target_type':'RESEARCH_CANDIDATE','candidate_id':c['session_id'],'expected_output_name':c['final_output_name'],'contract_generation':'v10','audit_os_version':'6.0.0'},indent=2)+'\n')
 w(root/'PROTECTED_SURFACE_BASELINE.json',json.dumps({'status':'GENERATED_AT_DISPATCH','protected_roots':['AUDIT_OS','RUNTIME','contracts','HANDOFF_IDENTITY.json'],'baseline_source':'manifest.json'},indent=2)+'\n')
 w(root/'ALLOWED_CHANGE_MATRIX.csv','path_pattern,action,allowed_columns,notes\nOUTPUT_SKELETON/**,ALLOW,,Candidate construction surface\nexternal_stage_review/**,EXTERNAL_AUDITOR_ONLY,,Research builder must not self-approve\nAUDIT_OS/**,DENY,,Immutable canonical Audit\nRUNTIME/**,DENY,,Immutable runtime\ncontracts/**,DENY,,Immutable contracts\n')
 w(root/'REQUIRED_OUTPUTS_AND_ACCEPTANCE.json',json.dumps({'required_outputs':[c['final_output_name'],'CONSTRUCTION_REPORT.md','RETURN_REPORT.md'],'acceptance':['Gate0 PASS','stage review PASS','candidate finalizer PASS','v10 admission PASS','external Audit OS v6 required']},indent=2)+'\n')
 w(root/'INDEPENDENCE_STATE_MACHINE.json',json.dumps({'states':['CONSTRUCT','STAGE_PRE_REVIEW','CANDIDATE_SEAL','RETURN_ADMISSION','EXTERNAL_CANDIDATE_AUDIT','PROMOTION'],'forbidden_role_collisions':['Research Builder != Stage Pre-review Auditor','Research Builder != Candidate Auditor','Global Builder != Global Auditor']},indent=2)+'\n')
 w(root/'PACKAGE_VALIDATION.json',json.dumps({'status':'PREDISPATCH_PENDING_FINAL_MANIFEST','contract_generation':'v10','audit_os_version':'6.0.0'},indent=2)+'\n')
 # package-level predispatch manifest
 files=[]
 for p in sorted(root.rglob('*')):
  if p.is_file() and p.relative_to(root).as_posix() not in {'manifest.json','SHA256SUMS.txt'}: files.append({'path':p.relative_to(root).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
 w(root/'manifest.json',json.dumps({'package_name':name,'session_id':c['session_id'],'final_output_name':c['final_output_name'],'files':files},ensure_ascii=False,indent=2)+'\n')
 w(root/'SHA256SUMS.txt',''.join(f"{x['sha256']}  {x['path']}\n" for x in files))
 zpath=outdir/(name+'.zip')
 if zpath.exists():zpath.unlink()
 epoch=(1980,1,1,0,0,0)
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(root.rglob('*')):
   if p.is_file():
    info=zipfile.ZipInfo((Path(root.name)/p.relative_to(root)).as_posix(),epoch);info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
    z.writestr(info,p.read_bytes())
 with zipfile.ZipFile(zpath) as z:
  if z.testzip(): raise SystemExit('ZIP integrity failure')
 return zpath
def main():
 ap=argparse.ArgumentParser();ap.add_argument('config');ap.add_argument('--output-dir',required=True);a=ap.parse_args();domain=json.loads(Path(a.config).read_text(encoding='utf-8'));out=Path(a.output_dir).resolve();out.mkdir(parents=True,exist_ok=True);zs=[]
 for c in domain['children']: zs.append(package_one(domain,c,out))
 print(json.dumps({'status':'PASS','packages':[str(x) for x in zs]},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
