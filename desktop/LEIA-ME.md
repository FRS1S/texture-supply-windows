# Texture Supply by piraru*: app de computador

App Electron feito a partir de `../app.html` (a mesma página do Artifact).

## Comandos
- `npm start`: abre o app para testar
- `npm run dist`: gera o instalador em `dist/Texture-Supply-by-piraru-Instalador-<versão>.exe`
- `npm run dist:portable`: gera um `.exe` portátil, que roda sem instalar

Os dois comandos rodam antes `build-html.js`, que copia `../app.html` para `app/index.html`
trocando as fontes do Google e o JSZip por arquivos locais. Assim o app funciona sem internet.

## Fluxo para uma nova versão
1. Edite `../app.html`.
2. Aumente `"version"` no `package.json` (ex.: 1.0.1).
3. Rode `npm run dist` e distribua o novo instalador.

## Arquivos
- `main.js`: janela, menus (PT/EN/ES) e diálogo "Salvar como"
- `preload.js`: avisa o processo principal quando o idioma ou o tema muda nas Configurações
- Textos da interface: dicionário `I18N` em `../app.html` (chave em português, valores em inglês e espanhol)
- `splash/`: vídeo de abertura (`abertura.mp4`) e `intro.html`, que toca o vídeo por cima do app na mesma janela e some com um fade. Para trocar o vídeo, substitua o `.mp4` mantendo o nome; a pausa no logo e a duração do fade ficam no topo do script de `intro.html`
- `build-html.js`: monta a versão offline do HTML
- `make-icon.py`: gera `build/icon.png` (rode `python make-icon.py` para recriar o ícone)
