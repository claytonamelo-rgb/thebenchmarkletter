# ICIS Press Releases → RSS

Gera um feed RSS a partir dos press releases da ICIS (que o Inoreader/FetchRSS não conseguem detectar sozinhos) usando a API REST pública do WordPress do site, e publica automaticamente via GitHub Pages.

## Passo a passo (tudo pelo navegador, sem terminal)

1. **Criar o repositório**
   - Entre em github.com (crie uma conta grátis se ainda não tiver).
   - Clique em **New repository**. Nome sugerido: `icis-rss-feed`. Pode ser público ou privado — ambos funcionam com Pages (repositório privado exige plano Pro/Team para Pages público; se for privado no plano free, use público mesmo, já que não há dado sensível aqui).
   - Crie vazio, sem README inicial.

2. **Subir os arquivos**
   - Na página do repositório recém-criado, clique em **Add file → Upload files**.
   - Arraste esta pasta inteira (`generate_feed.py`, `README.md`, a pasta `docs/` com o XML placeholder, e a pasta `.github/workflows/` com o `update-feed.yml`) — o GitHub preserva a estrutura de pastas no upload.
   - Commit direto na branch `main`.

3. **Ativar o GitHub Pages**
   - Vá em **Settings → Pages** (menu lateral).
   - Em "Build and deployment" → Source, selecione **Deploy from a branch**.
   - Branch: `main`, pasta: `/docs`. Salve.
   - O GitHub mostra a URL pública (algo como `https://SEU-USUARIO.github.io/icis-rss-feed/icis_press_releases.xml`). Pode levar 1–2 minutos para ficar no ar.

4. **Rodar a primeira atualização**
   - Vá na aba **Actions** do repositório.
   - Você verá o workflow "Update ICIS press release feed". Clique nele → **Run workflow** (botão à direita) para rodar manualmente agora, sem esperar a próxima hora cheia.
   - Depois disso ele roda sozinho a cada hora (cron `0 * * * *`).

5. **Apontar o Inoreader/FetchRSS**
   - Use a URL do passo 3 (`.../icis_press_releases.xml`) como fonte do feed.

## Arquivos

- `generate_feed.py` — busca os press releases via `wp-json/wp/v2/press-releases` e monta o RSS.
- `.github/workflows/update-feed.yml` — roda o script a cada hora e commita o XML atualizado.
- `docs/icis_press_releases.xml` — o feed publicado (começa como placeholder, é sobrescrito automaticamente).

## Repetindo para outras empresas

Este mesmo padrão (achar a API/estrutura por trás da página de press releases → gerar RSS → publicar via Actions) pode ser replicado para outros sites. Quando tivermos a lista de URLs, cada empresa vira um novo script + entrada no workflow (ou um workflow único que gera vários arquivos XML, um por empresa).
