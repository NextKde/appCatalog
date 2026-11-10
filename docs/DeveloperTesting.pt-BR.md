# Modo de teste para desenvolvedores

[English](DeveloperTesting.md) · [简体中文](DeveloperTesting.zh-CN.md)

Em Configurações → Aplicativos e serviços → **Entrar no modo de teste**, teste seu catálogo antes de enviar uma submissão. O modo mantém o ID original e a instalação Flatpak do usuário. Um pacote de teste pode substituir um aplicativo instalado e usar seus dados existentes. Faça backup de dados importantes e prefira uma VM de desenvolvimento.

## Publicar e selecionar

1. Gere o bundle com o ID original e a branch Flatpak `stable`. Publique o pacote e seu manifest schema 2 num repositório GitHub público. A versão do manifest deve corresponder à tag sem `v`, por exemplo `v1.2.0-rc.1` / `1.2.0-rc.1`. Pré-lançamentos publicados são aceitos quando selecionados explicitamente; rascunhos e autenticação de repositórios privados não são suportados.
2. Prepare um repositório de catálogo separado com o formato do appCatalog. Use seu próprio `sourceId`, uma sequência crescente e sua própria chave de assinatura. Publique `catalog.json` e `catalog.json.sig` num GitHub Release, por exemplo `catalog-test-1`, que pode ser marcado como pré-lançamento.
3. Entre no modo de teste e abra o gerenciamento de origens. Informe o ID, repositório GitHub, arquivo público binário `.gpg` e impressão digital completa, aceitando explicitamente a confiança. A lista de teste começa vazia e não herda a confiança oficial.
4. Em **Release do catálogo**, selecione a tag publicada. Aplicar atualiza e verifica o catálogo. Deixar em branco usa a versão estável mais recente. A seleção não ignora expiração ou proteção contra sequências antigas; para um histórico independente, use outro ID de origem e assine um documento com o mesmo `sourceId`.
5. Expanda os detalhes do aplicativo, selecione **Release do aplicativo** e verifique as atualizações. A lista mostra até 30 Releases publicados recentes; tags antigas podem ser digitadas. Revise o plano e o aviso de modo de teste antes de confirmar.
6. Publique uma versão mais nova e selecione-a para testar atualizações. Para testar downgrade ou substituição da mesma versão, desinstale primeiro. Instalações pertencentes a outra origem ou não verificáveis pela chave selecionada também precisam ser desinstaladas antes da instalação de teste.

Assinatura do catálogo e SHA-256 do pacote continuam obrigatórios. A assinatura do desenvolvedor é opcional, mas é exigida se uma chave estiver configurada. Os downloads continuam restritos aos anexos de GitHub Releases do repositório autorizado. Não são aceitos pacotes locais, URLs raw, servidores arbitrários nem scripts de instalação.

## Sair e restaurar

**Sair do modo de teste** restaura somente as origens normais. Não desinstala aplicativos, não restaura versões antigas, não apaga dados e não transfere origens de teste para a configuração normal. Instalações de teste continuam disponíveis para abrir/desinstalar, sem adoção automática pelo atualizador normal. Para restaurar uma versão normal, desinstale o teste manualmente e instale a versão normal; a desinstalação preserva os dados do aplicativo.

Verificações agendadas e notificações de atualização ficam pausadas durante o modo de teste. Atualização manual do catálogo, verificações individuais e verificação de todos os aplicativos continuam disponíveis. Consulte erros de origem, tags selecionadas, versões e logs para diagnosticar problemas.

## Estado e validação

A seleção é salva por usuário, persiste após reiniciar as Configurações e vale para o backend compartilhado de Settings, CLI, worker e updater. Resultados da CLI incluem `testMode`. Origens usam `app-sources-test.json`; caches e estado de atualização usam `app-catalog/test/`; planos usam `flatpak-plans-test/`. Instalações Flatpak, dados e registros de instalação são compartilhados, e os registros identificam implantações de teste.

Alterar o modo ou a seleção de Release invalida planos e descobertas anteriores. Um bloqueio compartilhado impede alterações durante verificações de catálogo/inventário e operações de aplicativos. Resultados de uma varredura de atualização são descartados se o contexto mudar. O agente de atualização nunca confirma instalações.

Contribuidores deste projeto devem compilar e validar somente em VM ou CI. Cubra separação de origens/histórico, IDs originais, planos antigos, assinaturas e hashes inválidos, tags divergentes, ordenação de pré-lançamentos, suspensão das verificações agendadas e saída sem desinstalação. Valide também instalação/atualização/desinstalação reais em uma VM isolada e a interface nos idiomas suportados.
