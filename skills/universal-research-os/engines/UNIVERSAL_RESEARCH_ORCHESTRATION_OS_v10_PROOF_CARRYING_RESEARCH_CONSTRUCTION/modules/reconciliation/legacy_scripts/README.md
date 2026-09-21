# Scripts

這些腳本是 universal scaffold validators，不會替代人工語義裁決。

建議順序：

```bash
python scripts/initialize_workspace.py --root work --project EXAMPLE
python scripts/verify_zip_and_manifest.py input.zip --receipt audit/input.json
python scripts/generate_semantic_candidate_queues.py ...
python scripts/validate_csv_headers.py ...
python scripts/validate_graph.py ...
python scripts/validate_retrieval_results.py ...
python scripts/build_manifest_and_checksums.py --root <package>
python scripts/build_deterministic_zip.py --root <package> --output <package>.zip
python scripts/validate_package_fresh_extract.py <package>.zip --receipt audit/fresh_extract.json
```

若 child packages 結構差異很大，先建立 adapter；不得直接修改 validator 讓錯誤消失。
