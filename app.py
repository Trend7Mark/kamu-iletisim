import streamlit as st
import google.generativeai as genai

# Sayfa ayarları
st.set_page_config(page_title="Kamu İletişim Asistanı", page_icon="🏛️", layout="centered")

# Başlık ve Açıklama
st.title("🏛️ Kamu İletişim Asistanı")
st.markdown("Kamu kurumları için yapay zeka destekli sosyal medya ve haber metni yazım aracı.")
st.divider()

# Sol Menü (API Anahtarı girişi için)
with st.sidebar:
    st.header("⚙️ Ayarlar")
    st.markdown("Uygulamanın çalışması için bir Google Gemini API anahtarına ihtiyacınız var.")
    api_key = st.text_input("Gemini API Anahtarı:", type="password", help="API anahtarınız sadece bu ekranda kalır, hiçbir yere kaydedilmez.")
    st.markdown("[Ücretsiz API Anahtarı Almak İçin Tıklayın](https://aistudio.google.com/app/apikey)")
    st.divider()
    st.info("💡 İpucu: Bu araç metinleri üretirken uydurma bilgiler eklememesi ve kurumsal ciddiyeti koruması için özel olarak programlanmıştır.")

# Ana İçerik Alanı
st.subheader("Haber / Olay Detayları")
brief = st.text_area(
    "Yapay zekaya konuyu kısaca özetleyin (Ne oldu, kim katıldı, nerede oldu?):", 
    height=150, 
    placeholder="Örn: Kurum müdürümüz Sayın Ahmet Yılmaz, bugün bölge kütüphanesinin açılışını yaptı. Gençlerle sohbet etti ve 1000 adet kitap dağıtımı gerçekleştirdi."
)

col1, col2 = st.columns(2)
with col1:
    platform = st.selectbox("Hedef Platform", ["X (Twitter)", "Instagram", "Facebook", "Web Sitesi Haberi"])
with col2:
    tone = st.selectbox("İletişim Tonu", ["Resmi ve Ciddi", "Bilgilendirici", "Samimi ve Coşkulu"])

# Üretim Butonu
if st.button("🚀 Metni Üret", use_container_width=True):
    if not api_key:
        st.error("⚠️ Lütfen sol menüden Gemini API Anahtarınızı girin.")
    elif not brief:
        st.warning("⚠️ Lütfen haberin detaylarını boş bırakmayın.")
    else:
        try:
            # Gemini API Bağlantısı
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            
            # Yapay Zekaya Verilecek Özel Talimat (Prompt Engineering)
            system_prompt = f"""
            Sen bir devlet kurumunda çalışan kıdemli, dikkatli ve profesyonel bir Kurumsal İletişim Uzmanısın.
            Görevin, sana verilen taslak metinleri ve bilgileri kullanarak {platform} platformu için bir içerik üretmek.
            
            İletişim Tonu: {tone}.
            
            KESİN KURALLAR:
            1. Kurumsal devlet ciddiyetini, saygınlığını ve hiyerarşik nezaketi koru.
            2. ASLA HALÜSİNASYON YAPMA: Sadece verilen bilgilere sadık kal. Verilmeyen isimleri, makamları, rakamları veya mekanları kendi kendine uydurma.
            3. Hedef platformun formatına tam olarak uygun yaz:
               - X (Twitter) ise: Kısa, öz, vurucu ol. Gerekli hashtag'leri ekle. Karakter sınırını aşma. Metin sonuna kurum web sitesi linki için (Link: ...) yeri bırak.
               - Instagram/Facebook ise: Görsel betimlemeye açık, emoji kullanımı (uygunsa ve çok abartmadan) ve okunması kolay paragraflar kullan.
               - Web Sitesi Haberi ise: Mutlaka ilgi çekici resmi bir haber başlığı (Title), konuyu özetleyen bir giriş paragrafı (Lead) ve ardından detay paragrafları içeren uzun ve edebi bir bülten formatında yaz.
            """
            
            user_prompt = f"İşte olayın detayları (Sadece bu bilgilere dayanarak metni yaz):\n\n{brief}"
            
            with st.spinner("Yapay zeka metni hazırlıyor, lütfen bekleyin..."):
                # Yapay zekaya komutu gönderiyoruz
                response = model.generate_content([system_prompt, user_prompt])
                
            st.success("✅ Metin başarıyla üretildi!")
            
            # Çıktıyı Ekrana Yazdırma
            st.markdown("### 📝 Üretilen İçerik:")
            
            # Metni kopyalanabilir bir alanda göster
            st.code(response.text, language="markdown")
            
        except Exception as e:
            st.error(f"❌ Bir hata oluştu. Lütfen API anahtarınızı kontrol edin. Hata detayı: {e}")
