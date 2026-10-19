# Regras do projeto

- **Não publicar no Netlify a cada edição.** Juntar as alterações (commit + push no git normalmente) e só publicar quando o dono pedir explicitamente.
- Editar sempre `src/index.html`; `python3 build.py` gera `index.html` (publicação) e `preview.html` (prévia).
- Para publicar: `./deploy-stage.sh` e enviar `/tmp/site.zip` ao Netlify (projeto `mundo-autista-atividades`).
