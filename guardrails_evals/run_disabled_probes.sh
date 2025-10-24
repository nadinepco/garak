uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes ansiescape.AnsiEscaped --parallel_requests 10 --generations 3 --report_prefix "disabled_ansiescape_AnsiEscaped" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes atkgen.Tox --parallel_requests 10 --generations 3 --report_prefix "disabled_atkgen_Tox" &
wait
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes continuation.ContinueSlursReclaimedSlurs --parallel_requests 10 --generations 3 --report_prefix "disabled_continuation_ContinueSlursReclaimedSlurs"
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes dan.Ablation_Dan_11_0 --parallel_requests 10 --generations 3 --report_prefix "disabled_dan_Ablation_Dan_11_0" &
wait
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes divergence.Repeat --parallel_requests 10 --generations 3 --report_prefix "disabled_divergence_Repeat" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes dra.DRA --parallel_attempts 10 --generations 3 --report_prefix "disabled_dra_DRA" &
wait
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectAscii85 --parallel_requests 10 --generations 3 --report_prefix "disabled_encoding_InjectAscii85" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes exploitation.JinjaTemplatePythonInjection --parallel_requests 10 --generations 3 --report_prefix "disabled_exploitation_JinjaTemplatePythonInjection" &
wait
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes goodside.Tag --parallel_requests 10 --generations 3 --report_prefix "disabled_goodside_Tag" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes grandma.Slurs --parallel_requests 10 --generations 3 --report_prefix "disabled_grandma_Slurs" &
wait
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes latentinjection.LatentInjectionFactSnippetEiffel --parallel_attempts 10 --generations 3 --report_prefix "disabled_latentinjection_LatentInjectionFactSnippetEiffel" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes leakreplay.GuardianCloze --parallel_requests 10 --generations 3 --report_prefix "disabled_leakreplay_GuardianCloze" &
wait
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes lmrc.Bullying --parallel_requests 10 --generations 3 --report_prefix "disabled_lmrc_Bullying" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes malwaregen.Evasion --parallel_requests 10 --generations 3 --report_prefix "disabled_malwaregen_Evasion" &
wait
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes misleading.FalseAssertion --parallel_requests 10 --generations 3 --report_prefix "disabled_misleading_FalseAssertion" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes packagehallucination.Dart --parallel_requests 10 --generations 3 --report_prefix "disabled_packagehallucination_Dart" &
wait
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes phrasing.FutureTense --parallel_requests 10 --generations 3 --report_prefix "disabled_phrasing_FutureTense" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes promptinject.HijackHateHumans --parallel_requests 10 --generations 3 --report_prefix "disabled_promptinject_HijackHateHumans" &
wait
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes realtoxicityprompts.RTPBlank --parallel_requests 10 --generations 3 --report_prefix "disabled_realtoxicityprompts_RTPBlank" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes snowball.GraphConnectivity --parallel_requests 10 --generations 3 --report_prefix "disabled_snowball_GraphConnectivity" &
wait
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes suffix.GCGCached --parallel_requests 10 --generations 3 --report_prefix "disabled_suffix_GCGCached" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes tap.TAPCached --parallel_requests 10 --generations 3 --report_prefix "disabled_tap_TAPCached" &
wait
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes topic.WordnetControversial --parallel_requests 10 --generations 3 --report_prefix "disabled_topic_WordnetControversial" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes web_injection.ColabAIDataLeakage --parallel_requests 10 --generations 3 --report_prefix "disabled_web_injection_ColabAIDataLeakage" &

