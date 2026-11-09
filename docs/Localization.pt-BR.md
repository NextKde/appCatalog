# Localização do catálogo

[English](Localization.md) · [简体中文](Localization.zh-CN.md)

`name` e `description` são mapas por idioma. Ambos exigem `en` não vazio como alternativa. A interface atual oferece `en`, `zh-CN` e `pt-BR`; outros códigos válidos podem ser armazenados para clientes futuros. Traduções ausentes usam inglês. Idiomas da documentação não implicam suporte na interface.

Não traduza appId, key, format, repository, manifest, status ou impressões digitais. Use texto simples: nomes de até 120 caracteres e descrições de até 600, no máximo 32 idiomas por campo, sem valores vazios ou caracteres de controle. Traduções passam por PR e publicação assinada do catálogo; não exigem novo pacote do aplicativo.

As traduções da interface do aplicativo ficam no próprio pacote, separadas das descrições do catálogo. Recomendamos `separate-locales: false` inicialmente; uma extensão Locale própria não fica disponível automaticamente na origem aprovada. Veja [Runtime Qt](QtRuntime.pt-BR.md).
