#!/bin/bash
# Auto-generated script to run all active probes from starred modules
# Each probe runs with parallel_requests=10 (single test per prompt, 10 concurrent requests)

# Batch 1
echo "=== Batch 1/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes ansiescape.AnsiEscaped --parallel_requests 10 --generations 3 --report_prefix "lenient_ansiescape_AnsiEscaped" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes ansiescape.AnsiRaw --parallel_requests 10 --generations 3 --report_prefix "lenient_ansiescape_AnsiRaw" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes atkgen.Tox --parallel_requests 10 --generations 3 --report_prefix "lenient_atkgen_Tox" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes continuation.ContinueSlursReclaimedSlurs --parallel_requests 10 --generations 3 --report_prefix "lenient_continuation_ContinueSlursReclaimedSlurs" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes dan.Ablation_Dan_11_0 --parallel_requests 10 --generations 3 --report_prefix "lenient_dan_Ablation_Dan_11_0" &
wait
echo "Batch 1 complete"
echo ""

# Batch 2
echo "=== Batch 2/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes dan.AutoDANCached --parallel_requests 10 --generations 3 --report_prefix "lenient_dan_AutoDANCached" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes dan.DanInTheWild --parallel_requests 10 --generations 3 --report_prefix "lenient_dan_DanInTheWild" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes divergence.Repeat --parallel_requests 10 --generations 3 --report_prefix "lenient_divergence_Repeat" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes divergence.RepeatedToken --parallel_requests 10 --generations 3 --report_prefix "lenient_divergence_RepeatedToken" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes dra.DRA --parallel_attempts 10 --generations 3 --report_prefix "lenient_dra_DRA" &
wait
echo "Batch 2 complete"
echo ""

# Batch 3
echo "=== Batch 3/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectAscii85 --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectAscii85" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectAtbash --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectAtbash" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectBase16 --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectBase16" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectBase2048 --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectBase2048" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectBase32 --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectBase32" &
wait
echo "Batch 3 complete"
echo ""

# Batch 4
echo "=== Batch 4/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectBase64 --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectBase64" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectBraille --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectBraille" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectEcoji --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectEcoji" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectHex --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectHex" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectMorse --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectMorse" &
wait
echo "Batch 4 complete"
echo ""

# Batch 5
echo "=== Batch 5/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectNato --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectNato" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectROT13 --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectROT13" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectUU --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectUU" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectUnicodeTagChars --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectUnicodeTagChars" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes encoding.InjectZalgo --parallel_requests 10 --generations 3 --report_prefix "lenient_encoding_InjectZalgo" &
wait
echo "Batch 5 complete"
echo ""

# Batch 6
echo "=== Batch 6/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes exploitation.JinjaTemplatePythonInjection --parallel_requests 10 --generations 3 --report_prefix "lenient_exploitation_JinjaTemplatePythonInjection" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes exploitation.SQLInjectionEcho --parallel_requests 10 --generations 3 --report_prefix "lenient_exploitation_SQLInjectionEcho" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes goodside.Tag --parallel_requests 10 --generations 3 --report_prefix "lenient_goodside_Tag" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes goodside.ThreatenJSON --parallel_requests 10 --generations 3 --report_prefix "lenient_goodside_ThreatenJSON" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes goodside.WhoIsRiley --parallel_requests 10 --generations 3 --report_prefix "lenient_goodside_WhoIsRiley" &
wait
echo "Batch 6 complete"
echo ""

# Batch 7
echo "=== Batch 7/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes grandma.Slurs --parallel_requests 10 --generations 3 --report_prefix "lenient_grandma_Slurs" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes grandma.Substances --parallel_requests 10 --generations 3 --report_prefix "lenient_grandma_Substances" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes grandma.Win10 --parallel_requests 10 --generations 3 --report_prefix "lenient_grandma_Win10" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes grandma.Win11 --parallel_requests 10 --generations 3 --report_prefix "lenient_grandma_Win11" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes latentinjection.LatentInjectionFactSnippetEiffel --parallel_attempts 10 --generations 3 --report_prefix "lenient_latentinjection_LatentInjectionFactSnippetEiffel" &
wait
echo "Batch 7 complete"
echo ""

# Batch 8
echo "=== Batch 8/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes latentinjection.LatentInjectionFactSnippetLegal --parallel_requests 10 --generations 3 --report_prefix "lenient_latentinjection_LatentInjectionFactSnippetLegal" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes latentinjection.LatentInjectionReport --parallel_requests 10 --generations 3 --report_prefix "lenient_latentinjection_LatentInjectionReport" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes latentinjection.LatentInjectionResume --parallel_requests 10 --generations 3 --report_prefix "lenient_latentinjection_LatentInjectionResume" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes latentinjection.LatentInjectionTranslationEnFr --parallel_requests 10 --generations 3 --report_prefix "lenient_latentinjection_LatentInjectionTranslationEnFr" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes latentinjection.LatentInjectionTranslationEnZh --parallel_requests 10 --generations 3 --report_prefix "lenient_latentinjection_LatentInjectionTranslationEnZh" &
wait
echo "Batch 8 complete"
echo ""

# Batch 9
echo "=== Batch 9/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes latentinjection.LatentJailbreak --parallel_requests 10 --generations 3 --report_prefix "lenient_latentinjection_LatentJailbreak" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes latentinjection.LatentWhois --parallel_requests 10 --generations 3 --report_prefix "lenient_latentinjection_LatentWhois" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes latentinjection.LatentWhoisSnippet --parallel_requests 10 --generations 3 --report_prefix "lenient_latentinjection_LatentWhoisSnippet" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes leakreplay.GuardianCloze --parallel_requests 10 --generations 3 --report_prefix "lenient_leakreplay_GuardianCloze" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes leakreplay.GuardianComplete --parallel_requests 10 --generations 3 --report_prefix "lenient_leakreplay_GuardianComplete" &
wait
echo "Batch 9 complete"
echo ""

# Batch 10
echo "=== Batch 10/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes leakreplay.LiteratureCloze --parallel_requests 10 --generations 3 --report_prefix "lenient_leakreplay_LiteratureCloze" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes leakreplay.LiteratureComplete --parallel_requests 10 --generations 3 --report_prefix "lenient_leakreplay_LiteratureComplete" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes leakreplay.NYTCloze --parallel_requests 10 --generations 3 --report_prefix "lenient_leakreplay_NYTCloze" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes leakreplay.NYTComplete --parallel_requests 10 --generations 3 --report_prefix "lenient_leakreplay_NYTComplete" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes leakreplay.PotterCloze --parallel_requests 10 --generations 3 --report_prefix "lenient_leakreplay_PotterCloze" &
wait
echo "Batch 10 complete"
echo ""

# Batch 11
echo "=== Batch 11/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes leakreplay.PotterComplete --parallel_requests 10 --generations 3 --report_prefix "lenient_leakreplay_PotterComplete" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes lmrc.Bullying --parallel_requests 10 --generations 3 --report_prefix "lenient_lmrc_Bullying" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes lmrc.Deadnaming --parallel_requests 10 --generations 3 --report_prefix "lenient_lmrc_Deadnaming" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes lmrc.QuackMedicine --parallel_requests 10 --generations 3 --report_prefix "lenient_lmrc_QuackMedicine" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes lmrc.SexualContent --parallel_requests 10 --generations 3 --report_prefix "lenient_lmrc_SexualContent" &
wait
echo "Batch 11 complete"
echo ""

# Batch 12
echo "=== Batch 12/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes lmrc.Sexualisation --parallel_requests 10 --generations 3 --report_prefix "lenient_lmrc_Sexualisation" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes lmrc.SlurUsage --parallel_requests 10 --generations 3 --report_prefix "lenient_lmrc_SlurUsage" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes malwaregen.Evasion --parallel_requests 10 --generations 3 --report_prefix "lenient_malwaregen_Evasion" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes malwaregen.Payload --parallel_requests 10 --generations 3 --report_prefix "lenient_malwaregen_Payload" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes malwaregen.SubFunctions --parallel_requests 10 --generations 3 --report_prefix "lenient_malwaregen_SubFunctions" &
wait
echo "Batch 12 complete"
echo ""

# Batch 13
echo "=== Batch 13/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes malwaregen.TopLevel --parallel_requests 10 --generations 3 --report_prefix "lenient_malwaregen_TopLevel" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes misleading.FalseAssertion --parallel_requests 10 --generations 3 --report_prefix "lenient_misleading_FalseAssertion" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes packagehallucination.Dart --parallel_requests 10 --generations 3 --report_prefix "lenient_packagehallucination_Dart" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes packagehallucination.JavaScript --parallel_requests 10 --generations 3 --report_prefix "lenient_packagehallucination_JavaScript" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes packagehallucination.Perl --parallel_requests 10 --generations 3 --report_prefix "lenient_packagehallucination_Perl" &
wait
echo "Batch 13 complete"
echo ""

# Batch 14
echo "=== Batch 14/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes packagehallucination.Python --parallel_requests 10 --generations 3 --report_prefix "lenient_packagehallucination_Python" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes packagehallucination.RakuLand --parallel_requests 10 --generations 3 --report_prefix "lenient_packagehallucination_RakuLand" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes packagehallucination.Ruby --parallel_requests 10 --generations 3 --report_prefix "lenient_packagehallucination_Ruby" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes packagehallucination.Rust --parallel_requests 10 --generations 3 --report_prefix "lenient_packagehallucination_Rust" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes phrasing.FutureTense --parallel_requests 10 --generations 3 --report_prefix "lenient_phrasing_FutureTense" &
wait
echo "Batch 14 complete"
echo ""

# Batch 15
echo "=== Batch 15/16 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes phrasing.PastTense --parallel_requests 10 --generations 3 --report_prefix "lenient_phrasing_PastTense" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes promptinject.HijackHateHumans --parallel_requests 10 --generations 3 --report_prefix "lenient_promptinject_HijackHateHumans" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes promptinject.HijackKillHumans --parallel_requests 10 --generations 3 --report_prefix "lenient_promptinject_HijackKillHumans" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes promptinject.HijackLongPrompt --parallel_requests 10 --generations 3 --report_prefix "lenient_promptinject_HijackLongPrompt" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes realtoxicityprompts.RTPBlank --parallel_requests 10 --generations 3 --report_prefix "lenient_realtoxicityprompts_RTPBlank" &
wait
echo "Batch 15 complete"
echo ""

# Batch 16 (final batch - 4 probes)
echo "=== Batch 16/16 (final) ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes snowball.GraphConnectivity --parallel_requests 10 --generations 3 --report_prefix "lenient_snowball_GraphConnectivity" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes suffix.GCGCached --parallel_requests 10 --generations 3 --report_prefix "lenient_suffix_GCGCached" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes tap.TAPCached --parallel_requests 10 --generations 3 --report_prefix "lenient_tap_TAPCached" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes topic.WordnetControversial --parallel_requests 10 --generations 3 --report_prefix "lenient_topic_WordnetControversial" &
wait
echo "Batch 16 complete"
echo ""

# Batch 17 (web_injection - 8 probes, split into 2 sub-batches)
echo "=== Batch 17a/17 ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes web_injection.ColabAIDataLeakage --parallel_requests 10 --generations 3 --report_prefix "lenient_web_injection_ColabAIDataLeakage" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes web_injection.MarkdownImageExfil --parallel_attempts 10 --generations 3 --report_prefix "lenient_web_injection_MarkdownImageExfil" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes web_injection.MarkdownURIImageExfilExtended --parallel_requests 10 --generations 3 --report_prefix "lenient_web_injection_MarkdownURIImageExfilExtended" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes web_injection.MarkdownURINonImageExfilExtended --parallel_requests 10 --generations 3 --report_prefix "lenient_web_injection_MarkdownURINonImageExfilExtended" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes web_injection.MarkdownXSS --parallel_requests 10 --generations 3 --report_prefix "lenient_web_injection_MarkdownXSS" &
wait
echo "Batch 17a complete"
echo ""

echo "=== Batch 17b/17 (final) ==="
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes web_injection.PlaygroundMarkdownExfil --parallel_requests 10 --generations 3 --report_prefix "lenient_web_injection_PlaygroundMarkdownExfil" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes web_injection.StringAssemblyDataExfil --parallel_attempts 10 --generations 3 --report_prefix "lenient_web_injection_StringAssemblyDataExfil" &
uv run python -m garak --target_type rest -G tools/rest/streaming_config.json --probes web_injection.TaskXSS --parallel_requests 10 --generations 3 --report_prefix "lenient_web_injection_TaskXSS" &
wait
echo "Batch 17b complete"
echo ""

echo "✅ All probes completed!"
echo "Check the garak_runs directory for reports with 'lenient_' prefix"
