# Manutenção e publicação

[English](MAINTAINING.md) · [简体中文](MAINTAINING.zh-CN.md)

PRs executam verificações estruturais em uma VM do GitHub, sem executar os aplicativos, baixar instaladores ou acessar segredos de assinatura. Isso não substitui revisão de segurança. Antes de aceitar, confira propriedade do repositório, conflitos de ID, anexos do Release, permissões Flatpak, runtimes/extensões, SHA-256 e chave opcional do desenvolvedor. Teste instalação e atualização em VM descartável. Traduções não devem alterar identidade ou confiança.

## Publicação manual ou por workflow

A chave privada pode permanecer na máquina de assinatura. Gere e valide o catálogo na VM, envie apenas `catalog.json` à máquina de assinatura, assine com a chave autorizada e devolva JSON e assinatura à VM para verificação. Publique os dois anexos num Release estável `catalog-N`, apontando para o commit revisado. Confira todo o histórico: N deve ser maior que qualquer sequência anterior. Não transfira o diretório privado do GPG.

Para usar **Publish catalog**, configure o ambiente `catalog-release` com revisores e restrição ao ramo main. Armazene a chave ASCII-armored em `CATALOG_SIGNING_PRIVATE_KEY` e a senha, se necessária, em `CATALOG_SIGNING_PASSPHRASE`. A chave deve corresponder a `catalog-public.gpg`, `catalog-fingerprint.txt` e à chave fixada no cliente. Execute o workflow em main com sequência crescente; ele monta, assina, verifica e publica `catalog.json` e `catalog.json.sig`.

O prazo padrão é 30 dias. Renove antes do vencimento mesmo sem mudanças. Catálogos vencidos não autorizam instalação ou atualização. Nunca reutilize sequências, altere o JSON após assinar, substitua um Release publicado ou apague o histórico para reiniciar a contagem. Correções exigem nova sequência. Confira a atualização no cliente da VM antes de anunciar disponibilidade.

## Origens de terceiros

Use suas próprias chaves e um ID único. Altere `--source-id nextkde` no workflow para o ID informado pelos usuários. Não reutilize o ID oficial. Configure seus próprios segredos ou assine manualmente e publique os dois anexos com os nomes fixos num GitHub Release estável. Os usuários devem obter a impressão digital por um canal confiável independente e aceitar a origem explicitamente.

A rotação automática da chave raiz não está implementada. Uma chave substituta de terceiros requer novo ID e nova aceitação; mudanças na chave oficial exigem distribuição coordenada do cliente.

## Comandos na VM de desenvolvimento

```sh
python3 build_catalog.py --check
python3 -m unittest discover -s tests
python3 build_catalog.py --sequence 1
gpgv --keyring ./catalog-public.gpg dist/catalog.json.sig dist/catalog.json
```

A sequência 1 é apenas um exemplo para catálogos novos. Não execute código de aplicativos não confiáveis na máquina de assinatura.

O catálogo schema 2 incorpora manifests aprovados e ícones imutáveis; veja [aprovação de versões](docs/PinnedReleases.pt-BR.md).
