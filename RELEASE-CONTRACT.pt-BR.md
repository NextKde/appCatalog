# Contrato de lançamento GitHub / Flatpak

[English e exemplo JSON completo](RELEASE-CONTRACT.md) · [简体中文](RELEASE-CONTRACT.zh-CN.md)

O cliente consulta `https://api.github.com/repos/OWNER/REPOSITORY/releases/latest` do repositório registrado. Aceita apenas Releases publicados e estáveis com tag `vX.Y.Z`, sem rascunho ou pré-lançamento. Os anexos exigidos devem ter nomes únicos. Downloads ficam restritos ao repositório registrado e aos redirecionamentos para o CDN de Releases do GitHub.

O campo `manifest` do catálogo indica o nome do anexo JSON. O `schemaVersion` é 2, `appId` corresponde à entrada, `version` corresponde à tag sem v e `revision` é o commit de origem de 40 caracteres hexadecimais. `bundles` contém uma entrada por arquitetura:

| Campo | Conteúdo |
| --- | --- |
| asset | Nome do anexo `.flatpak` neste Release |
| ref / commit | `app/<appId>/<arch>/stable` e commit OSTree real de 64 caracteres |
| sha256 / size | SHA-256 dos bytes do bundle final e tamanho em bytes |
| metadata | Metadados exatos do aplicativo em Base64, incluindo a quebra de linha final |
| metadataSha256 | SHA-256 dos bytes decodificados dos metadados |
| installedSize | Tamanho instalado declarado pelo bundle, não a diferença em disco após deduplicação |
| runtime | Objeto com o ref completo do runtime necessário |
| requiredExtensions | Lista de objetos ref das extensões necessárias, ou lista vazia |

Extraia os valores do pacote final. Não copie os marcadores do exemplo nem use o hash do arquivo de código-fonte. O pacote não pode incluir URLs de origem online ou runtime-repo. O cliente verifica as dependências e a origem de runtime aprovada separadamente.

Se houver `publisher`, publique também `<manifest>.sig`, assinado sobre os bytes exatos do JSON, e assine o commit OSTree com a chave autorizada. Sem `publisher`, a assinatura do desenvolvedor é opcional; SHA-256, identidade, metadados, versão e recibos de instalação continuam obrigatórios. GitHub Releases é obrigatório para todos os formatos. Apenas Flatpak está implementado atualmente.
