# Jira Task Is Updated?

Bu GitHub Action, Jira'da JQL sorgusu kullanarak arama yapar, bulduğu sonuçlar ile GitHub branch'lerini karşılaştırır. Bulduğu sonuçların release branch'lerle merge olup olmadığını kontrol eder ve Jira issue açar.

## Giriş

Bu GitHub Action, Jira'daki görevlerin durumunu GitHub branch'leriyle senkronize etmek için kullanılır. Belirli bir JQL sorgusuna göre Jira'da arama yapar, bulunan görevlerin release branch'lerle merge olup olmadığını kontrol eder ve gerekirse Jira'da otomatik olarak issue açar.

## Çalışma Prensibi

Bu action aşağıdaki adımları izler:

1.  **Jira'ya Bağlan:** Sağlanan Jira sunucu URL'si ve API token'ı ile Jira'ya bağlanır.
2.  **JQL Sorgusu Çalıştır:** Belirtilen JQL sorgusunu Jira'da çalıştırır ve sonuçları alır.
3.  **Branch'leri Karşılaştır:** Bulunan Jira görevleriyle ilişkili GitHub branch'lerini karşılaştırır.
4.  **Merge Kontrolü:** Branch'lerin release branch'lerle merge olup olmadığını kontrol eder.
5.  **Jira Issue Aç:** Eğer bir görev release branch'lerle merge olmadıysa, Jira'da otomatik olarak bir issue açar.

## Açıklama

Bu action, Jira sunucusuna bağlanır, belirtilen JQL sorgusunu çalıştırır ve sonuçları GitHub Actions iş akışınızda kullanmanıza olanak tanır.

## Kullanım

### Ön Koşullar

*   Bir Jira hesabınızın olması gerekir.
*   Bir Jira API token'ına sahip olmanız gerekir.
*   Bir GitHub Actions iş akışınızın olması gerekir.

### Kurulum

1.  Bu action'ı GitHub Actions iş akışınıza ekleyin.
2.  Aşağıdaki giriş parametrelerini yapılandırın:

    *   `jira_server`: Jira sunucu URL'si. Örneğin: `https://jira.example.com` (gerekli).
    *   `jira_api_token`: Jira API token'ı. Jira hesabınızdan oluşturabilirsiniz (gerekli).
    *   `jql_query`: Jira'da arama yapmak için kullanılacak JQL sorgusu. Örneğin: `'project = MYPROJECT AND status = "In Progress"'` (gerekli).
    *   `release_branch`: Sürüm branch'lerini tanımlayan regex. Örneğin: `'release/.*'` (gerekli).

### Jira Issue Açma

Bu action, eğer bir Jira görevi release branch'lerle merge olmadıysa, otomatik olarak bir Jira issue açabilir. Bu özellik, release süreçlerini takip etmek ve hataları hızlı bir şekilde bildirmek için kullanışlıdır. Açılan issue, ilgili görevin release branch'lerle merge edilmediğini belirtir ve geliştiricilerin dikkatini çekmeyi amaçlar. Bu sayede, release süreçlerindeki olası gecikmeler veya hatalar önceden tespit edilebilir.

### Örnek

```yaml
name: Jira Integration Workflow

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  jira-integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Jira Search Action
        uses: ./.github/actions
        with:
          jira_server: ${{ secrets.JIRA_SERVER }}
          jira_api_token: ${{ secrets.JIRA_API_TOKEN }}
          jql_query: 'project = MYPROJECT AND status = "In Progress"'
          release_branch: 'release/.*'
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## Katkıda Bulunma

Katkılarınız memnuniyetle karşılanır. Lütfen bir pull request göndermeden önce bir issue oluşturun.
