# NextKde appCatalog

[English](README.md) · [简体中文](README.zh-CN.md) · **Português (Brasil)**

Repositório de submissões para Configurações → **Aplicativos e serviços**. Os pacotes ficam nos **GitHub Releases** dos desenvolvedores. Aqui publicamos um catálogo assinado de identidades e locais de lançamento, sem scripts de instalação.

A integração do cliente já foi incorporada à branch `main` do NextKde; isso não significa que versões já distribuídas a suportam. As publicações do catálogo e do cliente são independentes. A implementação e a validação em VM/CI estão no [PR #340 do cliente](https://github.com/NextKde/NextKde/pull/340). O [primeiro catálogo assinado](https://github.com/NextKde/appCatalog/releases/tag/catalog-1) já foi publicado.

## Publicar um aplicativo

1. Prepare um bundle Flatpak com ID estável seguindo o [guia de runtime Qt](docs/QtRuntime.pt-BR.md).
2. Publique um GitHub Release estável `vX.Y.Z`, sem rascunho ou pré-lançamento, com pacote e [manifest JSON](RELEASE-CONTRACT.pt-BR.md). SHA-256 é obrigatório; assinatura do desenvolvedor é opcional.
3. Envie um PR com `apps/<appId>.json`, usando o [exemplo completo](README.md#submit-an-application) e as [regras de localização](docs/Localization.pt-BR.md).
4. Após revisão e publicação do catálogo assinado, o cliente encontra o aplicativo sem recompilar Settings.

Cada nova versão exige um PR com a versão aprovada e seu manifest exato; o cliente compara o catálogo com as versões locais sem consultar cada repositório. Remover uma entrada ou marcar `withdrawn` bloqueia instalações/atualizações; `revoked` revoga a confiança. Isso não apaga aplicativos instalados nem dados pessoais. Use o nome canônico do repositório GitHub. Somente o adaptador Flatpak está implementado; outros formatos exigem suporte no cliente.

## Segurança e manutenção

A assinatura do catálogo e o SHA-256 do pacote são obrigatórios. O campo opcional `publisher` contém a impressão digital completa da chave principal e a chave pública binária em Base64. Quando configurado, o cliente exige a assinatura do manifest e do commit Flatpak, sem alternativa sem assinatura se falharem.

A assinatura do catálogo protege o hash aprovado; substituir pacote e manifest no repositório do aplicativo não altera esse hash. A confiança depende da revisão e da chave do mantenedor do catálogo. Assinaturas e hashes não garantem que o aplicativo seja inofensivo.

A assinatura manual pode manter a chave fora do GitHub. Para usar o workflow, os mantenedores configuram o ambiente `catalog-release`, o secret `CATALOG_SIGNING_PRIVATE_KEY` e, se necessário, `CATALOG_SIGNING_PASSPHRASE`. A chave deve corresponder à chave pública fixada pelo cliente. Execute **Publish catalog** com sequência maior que todas as anteriores, antes do vencimento padrão de 30 dias. Nunca publique chaves privadas ou reutilize sequências. Veja [Manutenção](MAINTAINING.pt-BR.md).

## Catálogos de terceiros

Use seu próprio repositório GitHub, chave e `sourceId`; adapte o workflow e publique `catalog.json` e `catalog.json.sig` num Release estável. Nas configurações de origens, o usuário informa ID, `owner/repository`, arquivo público binário `.gpg` e impressão digital completa, aceitando explicitamente a confiança. Obtenha a impressão digital por um canal confiável independente. IDs de apps em conflito não podem ser sobrescritos silenciosamente. Remover uma origem preserva o gerenciamento dos apps instalados.

O agente verifica atualizações e avisa, mas não instala automaticamente. Consulte a [arquitetura no NextKde](https://github.com/NextKde/NextKde/blob/main/docs/app-store/SignedCatalog.md).

Antes da submissão, use o [modo de teste e a seleção de Releases](docs/DeveloperTesting.pt-BR.md). O ID original é mantido; para restaurar a versão normal, desinstale e reinstale manualmente.

Veja [versões aprovadas e ícones](docs/PinnedReleases.pt-BR.md). Schema 2 exige Settings compatível.
