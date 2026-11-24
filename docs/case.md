# Case & evidence methodology

## Public references
- [FNE, acquisition of Klap by Itaú](https://www.fne.gob.cl/fne-aprueba-adquisicion-de-control-de-klap-por-parte-del-banco-itau/): mitigation measures intended to prevent the transfer of commercially sensitive information between competitors. Public context only, no inference of an incident or link to LemonTech.
- [Harvey, building ethical wall enforcement](https://www.harvey.ai/blog/building-ethical-wall-enforcement-into-harvey): legal matter access and rechecking authorization before sending retrieved content to a model.
- [LemonTech security policy](https://www.lemontech.com/legal/politica-de-seguridad-de-la-informacion): references ISO 27001, 27701 and 42001; not a statement that every certification is held.
- [OWASP AISVS v1.0 C5](https://github.com/OWASP/AISVS/blob/main/1.0/en/0x10-C05-Access-Control-and-Identity.md): C5.2.2 is a reference for end-user authorization at retrieval.
- [OWASP RAG Security](https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html): cross-tenant checks, stale permissions and tracing.

## Evidence method
Each check creates an independent fixture, executes a query or summary operation, compares observed behavior against an explicit expectation and records a result. No document body enters exported evidence. Source IDs and hashes identify the observed synthetic outcome; they do not establish independent authenticity. ISO Annex A references are illustrative mappings, not evidence of full control implementation. Block on high/critical failure; otherwise require human review. Severity is a proposed qualitative classification for this case, not a calibrated organizational risk methodology.

## Next iteration
The ContractNLI supervised evidence ranker is now evaluated separately from authorization. Future work could integrate this ranker into an authorization-aware retrieval pipeline and evaluate an optional generative model. Do not claim model resistance to prompt injection without tests against that model. All private tests stay synthetic.
