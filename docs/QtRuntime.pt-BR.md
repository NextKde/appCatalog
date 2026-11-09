# Runtime Qt e empacotamento Flatpak

[English](QtRuntime.md) · [简体中文](QtRuntime.zh-CN.md)

Para aplicativos Qt 6 / Qt Quick, recomendamos `org.kde.Platform` para execução e `org.kde.Sdk` para compilação, com a mesma arquitetura e versão do ramo. O Qt do sistema não substitui as bibliotecas do sandbox. Não é necessário criar um pacote QtRuntime próprio do NextKde.

Os manifests atuais de `NextKde/kos-apps` usam o ramo **6.11**. É uma referência do projeto, não uma garantia de compatibilidade universal ou de versão mais recente. Escolha um ramo mantido que inclua seus módulos e valide em uma VM. Consulte a [documentação oficial](https://docs.flatpak.org/en/latest/available-runtimes.html) e o [modelo completo](QtRuntime.md#manifest-starting-point).

Use permissões mínimas e portais para escolher arquivos. Bibliotecas específicas ficam em `/app`; não misture o Qt do sistema com o runtime. Instale plugins, módulos QML, ícones e traduções no pacote. Recomendamos `separate-locales: false`: publicar um bundle não disponibiliza automaticamente uma extensão `.Locale` própria. Consulte [Localização](Localization.pt-BR.md).

Compile e teste apenas em VM ou CI com SDK/runtime correspondentes. Exporte o ref `stable` com `flatpak build-bundle`, sem `--repo-url` nem `--runtime-repo`. Gere o [manifest de lançamento](../RELEASE-CONTRACT.md) a partir do pacote final, incluindo SHA-256, commit, tamanhos e metadados exatos. Preserve a quebra de linha final dos metadados. Teste instalação, atualização, remoção com dados preservados e cada arquitetura anunciada antes de publicar o Release estável `vX.Y.Z` no GitHub.

O aplicativo vem sempre do GitHub Releases. Dependências ausentes vêm somente da origem Flathub de runtimes aprovada separadamente pelo cliente. O aplicativo não precisa estar no Flathub. A instalação explícita pode preparar essa origem; cancelar pode deixá-la configurada. Runtimes compatíveis são compartilhados por ID, arquitetura, ramo e origem confiável. Dependências indisponíveis bloqueiam a instalação, sem recorrer ao Qt do sistema.
