# Versões aprovadas e ícones

[English](PinnedReleases.md) · [简体中文](PinnedReleases.zh-CN.md)

No modo normal, o cliente baixa um catálogo assinado por origem e compara as versões aprovadas com as instalações locais. Não consulta cada repositório de aplicativo. Cada nova versão precisa de um PR e da publicação de um novo catálogo assinado.

No mesmo PR, envie `apps/<appId>.json`, `icons/<appId>.png` e o manifest original do Release em `releases/<appId>.flatpak-release.json`. Quando há `publisher`, inclua também a assinatura `.json.sig`, sem reformatar o manifest. Os instaladores continuam nos anexos de GitHub Releases.

Adicione `icon: "icons/<appId>.png"` e `release` com `version`, `tag` (`v` seguido da versão), `manifestFile` e, quando necessário, `signatureFile`. Use `release: null` explicitamente quando não houver pacote compatível aprovado. Não invente versões nem use latest como alternativa automática. O manifest contém os pacotes por arquitetura, SHA-256, tamanhos, commits, metadados e dependências. Revise os anexos e a tag publicados.

Ícones devem ser PNG de até 1024 × 1024 e 512 KiB; recomendamos 256 × 256. Preserve atribuições/licenças em `icons/`. O publicador calcula SHA-256 e fixa a URL raw do próprio repositório do catálogo num commit completo. O cliente valida origem, tamanho, dimensões e hash, mantém cache e usa um ícone padrão se necessário. Downloads têm tempo limitado e podem ser repetidos na próxima atualização.

Em VM/CI, execute `python3 build_catalog.py --check` e `python3 build_catalog.py --sequence N --repository OWNER/REPO --revision FULL_COMMIT`. Esse commit deve conter exatamente os ícones revisados. O workflow usa seu próprio commit; origens externas devem configurar repositório e source ID próprios.

O catálogo **schema 2** incorpora em Base64 os bytes originais do manifest e sua assinatura opcional, com `release.version` e `release.tag` legíveis. A assinatura do catálogo protege os hashes dos pacotes mesmo sem assinatura do desenvolvedor. Substituir pacote e manifest no repositório do aplicativo não altera o hash aprovado. Isso depende da revisão/chave do mantenedor e não garante comportamento seguro do aplicativo.

Atualize Settings ao migrar: clientes antigos rejeitam schema 2 e mantêm o snapshot anterior até expirar. Clientes novos preservam o histórico schema 1, mas não procuram versões para entradas antigas sem versão aprovada. Instalações existentes continuam gerenciáveis. O modo de teste mantém a descoberta direta de Releases selecionados/Latest para depuração antes da aprovação.
