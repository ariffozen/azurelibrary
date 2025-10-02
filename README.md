# Azure DevOps Variable Group Güncelleme Uygulaması

## Proje Hakkında
Bu uygulama, `appsettings.json` benzeri yapılandırma dosyalarındaki değerleri Azure DevOps variable group içerisine hızlı ve hatasız biçimde aktarmak için geliştirildi. Flask tabanlı bir arayüz üzerinden JSON verisini girerek ilgili projedeki variable group değerlerini oluşturabilir veya güncelleyebilirsiniz.

## Özellikler
- İç içe geçmiş JSON verilerini Azure DevOps variable group formatına otomatik olarak düzleştirir
- Kullanıcı dostu web arayüzü ile Azure organizasyonu, proje ve hedef variable group seçimleri yapılabilir
- Azure PAT bilgisi temel kimlik doğrulama başlığı olarak kullanılır ve isteğin dışında saklanmaz
- İstek sonuçları JSON olarak ekranda görüntülenir ve hata durumlarında anlamlı geri bildirim verilir

## Kullanılan Teknolojiler
- Python 3.9
- Flask, Flask-CORS ve Requests kütüphaneleri
- Bootstrap 5 tabanlı arayüz
- Azure DevOps REST API (Variable Groups endpoint)

## Gereksinimler
- Python 3.9 veya üzeri
- `pip` ve tercihen `venv`
- Alternatif olarak Docker 20.x+

## Kurulum ve Çalıştırma
### Python ile yerel ortam
```bash
python -m venv .venv
source .venv/bin/activate  # Windows için .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```
Uygulama varsayılan olarak `http://127.0.0.1:8081` adresinde çalışır.

## Kullanım
1. Tarayıcıda uygulamayı açın ve hedef Azure DevOps host adresini (`https://dev.azure.com` ya da özel sunucunuz) girin.
2. Azure organizasyon adını yazın.
3. Proje listesinden güncellemek istediğiniz Azure DevOps projesini seçin.
4. Azure PAT değerini ve hedef variable group adını belirtin.
5. Güncel `appsettings.json` içeriğini metin alanına yapıştırın ve **Gönder** düğmesine basın.
6. Sonuç bölmesinde dönen JSON yanıtını ve hata/başarı bildirimlerini izleyin.

### Azure Project Adı listesini özelleştirme
Varsayılan kurulumda `templates/index.html` dosyasında sık kullanılan projeler örnek olarak listelenir. Kendi Azure DevOps projelerinizi göstermek için aşağıdaki adımları izleyin:

1. `templates/index.html` dosyasını açın.
2. `id="projectName"` değerine sahip `<select>` bloğunu bulun.
3. Projelerinizi `<option value="MyProject">MyProject</option>` biçiminde ekleyin veya gerekirse var olan örnekleri güncelleyin/silin.

Örnek bir ekleme:

```html
<select class="form-select" id="projectName" required>
    <option value="" selected disabled>Proje seçin</option>
    <option value="Project1">Project1</option>
	<option value="Project2">Project2</option>
	<option value="Project3">Project3</option>
    </select>
```

Değişiklikleri kaydettikten sonra sayfayı yenilemeniz yeterlidir; ek bir derleme adımı gerekmez.

## API Bitiş Noktası
Arayüz, arka plandaki `/update-variable-group` uç noktasına POST isteği gönderir.
```http
POST /update-variable-group
Content-Type: application/json

{
  "azureHost": "https://dev.azure.com",
  "azureOrg": "your-org",
  "azurePat": "<PAT>",
  "projectName": "SampleProject",
  "variableGroupName": "AppSettings",
  "jsonData": { /* appsettings.json içeriği */ }
}
```
Başarılı istekte Azure DevOps tarafından dönen yanıt JSON olarak iletilir; hata durumunda `error` alanı doldurulur.

## JSON Düzleştirme Kuralları
- Her JSON anahtarı noktalarla bölünmüş tam yoluna dönüştürülür (`Logging.LogLevel.Default` gibi)
- Dizilerdeki elemanlar sıra numarasıyla (`ArrayKey.0`, `ArrayKey.1` vb.) isimlendirilir
- Her değer `{ "value": "...", "isSecret": false }` formatında Azure değişken tanımına çevrilir
- İç içe sözlükler özyinelemeli olarak gezilir ve komple yapı variable group içerisine yerleştirilir

## Yapılandırma Notları
- Azure DevOps host adresi arayüzden girilir, bu nedenle farklı sunuculara bağlantı kurmak için ek yapılandırma gerekmez.
- `flatten_json` fonksiyonu hassas verileri maskelemez; gizli değerler için Azure DevOps tarafında `isSecret` alanını uyarlamanız gerekir.

## Proje Yapısı
```
.
├── app.py              # Flask uygulaması ve API mantığı
├── dockerfile          # Konteyner yapılandırması
├── requirements.txt    # Python bağımlılıkları
└── templates/
    └── index.html      # Bootstrap tabanlı kullanıcı arayüzü
```

## Geliştirme ve Test
- Geliştirme sırasında debug modu açık gelir; üretim ortamı için uygun bir WSGI sunucusu tercih edin.
- PAT değerlerinin istemci tarafında saklanmaması için TLS (HTTPS) üzerinden hizmet verin.
- İhtiyaç halinde ek loglama veya hata yakalama mekanizmalarını `update_variable_group` içinde genişletebilirsiniz.

## Lisans
Bu depoda lisans bilgisi belirtilmemiştir. Paylaşım veya yeniden kullanım için depo sahibiyle iletişime geçin.
