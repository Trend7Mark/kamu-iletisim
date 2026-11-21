import streamlit as st
import google.generativeai as genai

from shorts_prompts import MODULES, build_prompt, ideas_batch_instructions

# Sayfa ayarları
st.set_page_config(page_title="Kamu İletişim Asistanı", page_icon="🏛️", layout="centered")

MODEL_OPTIONS = ["gemini-2.5-flash", "gemini-2.5-pro", "Diğer (elle gir)"]

# Sol Menü (Mod seçimi ve API Anahtarı girişi)
with st.sidebar:
    st.header("🧭 Mod")
    mode = st.radio(
        "Araç seçin:",
        ["🏛️ Kamu İletişim Asistanı", "🎬 YouTube Shorts Stüdyosu"],
        label_visibility="collapsed",
    )
    st.divider()
    st.header("⚙️ Ayarlar")
    st.markdown("Uygulamanın çalışması için bir Google Gemini API anahtarına ihtiyacınız var.")
    api_key = st.text_input("Gemini API Anahtarı:", type="password", help="API anahtarınız sadece bu ekranda kalır, hiçbir yere kaydedilmez.")
    st.markdown("[Ücretsiz API Anahtarı Almak İçin Tıklayın](https://aistudio.google.com/app/apikey)")
    model_choice = st.selectbox("Model", MODEL_OPTIONS, help="Uzun stratejiler için 'pro' daha kalitelidir, 'flash' daha hızlı ve ücretsiz kotası daha geniştir.")
    if model_choice == "Diğer (elle gir)":
        model_name = st.text_input("Model adı:", value="gemini-2.5-flash")
    else:
        model_name = model_choice
    st.divider()
    st.info("💡 İpucu: Bu araç metinleri üretirken uydurma bilgiler eklememesi ve kurumsal ciddiyeti koruması için özel olarak programlanmıştır.")


def generate(prompt_parts, max_tokens=16384):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(
        prompt_parts,
        generation_config={"max_output_tokens": max_tokens, "temperature": 0.8},
    )
    return response.text


# ---------------------------------------------------------------------------
# Mod 1: Kamu İletişim Asistanı
# ---------------------------------------------------------------------------
def kamu_iletisim():
    st.title("🏛️ Kamu İletişim Asistanı")
    st.markdown("Kamu kurumları için yapay zeka destekli sosyal medya ve haber metni yazım aracı.")
    st.divider()

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

    if st.button("🚀 Metni Üret", use_container_width=True):
        if not api_key:
            st.error("⚠️ Lütfen sol menüden Gemini API Anahtarınızı girin.")
        elif not brief:
            st.warning("⚠️ Lütfen haberin detaylarını boş bırakmayın.")
        else:
            try:
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
                    text = generate([system_prompt, user_prompt], max_tokens=4096)

                st.success("✅ Metin başarıyla üretildi!")
                st.markdown("### 📝 Üretilen İçerik:")
                st.code(text, language="markdown")

            except Exception as e:
                st.error(f"❌ Bir hata oluştu. Lütfen API anahtarınızı ve model adını kontrol edin. Hata detayı: {e}")


# ---------------------------------------------------------------------------
# Mod 2: YouTube Shorts Stüdyosu
# ---------------------------------------------------------------------------
LANG_OPTIONS = ["English", "Türkçe", "Español", "Deutsch", "Français", "Português", "العربية"]
PRIOR_CONTEXT_CHARS = 5000  # her önceki modül çıktısından bağlama eklenecek en fazla karakter


def run_module(key, profile, explain_lang, content_lang, use_context):
    """Bir modülü çalıştırır, sonucu session_state'e kaydeder ve döndürür."""
    outputs = st.session_state.setdefault("shorts_outputs", {})
    prior = ""
    if use_context:
        prior = "\n\n".join(
            f"## {MODULES[k]['title']}\n{v[:PRIOR_CONTEXT_CHARS]}"
            for k, v in outputs.items() if k != key and k != "ideas"
        )

    m = MODULES[key]
    if key == "ideas":
        parts, titles = [], []
        for i in range(m["batches"]):
            instructions = ideas_batch_instructions(i, m["batches"], m["batch_size"], "\n".join(titles))
            prompt = build_prompt(key, profile, explain_lang, content_lang, prior, instructions)
            with st.spinner(f"Fikirler üretiliyor: {i * m['batch_size'] + 1}–{(i + 1) * m['batch_size']} / 200 ..."):
                chunk = generate(prompt, max_tokens=16384)
            parts.append(chunk)
            # Sonraki partilerde tekrarı önlemek için tablo satırlarının başlık hücrelerini topla
            for line in chunk.splitlines():
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) > 2 and cells[0].isdigit():
                    titles.append(f"{cells[0]}. {cells[1]}")
        text = "\n\n".join(parts)
    else:
        prompt = build_prompt(key, profile, explain_lang, content_lang, prior)
        with st.spinner(f"{m['title']} hazırlanıyor..."):
            text = generate(prompt, max_tokens=16384)

    outputs[key] = text
    return text


def combined_markdown(profile):
    outputs = st.session_state.get("shorts_outputs", {})
    header = f"# YouTube Shorts Strategy — {profile.get('niche') or 'My Channel'}\n\n"
    return header + "\n\n---\n\n".join(
        f"# {MODULES[k]['title']}\n\n{outputs[k]}" for k in MODULES if k in outputs
    )


def shorts_studio():
    st.title("🎬 YouTube Shorts Stüdyosu")
    st.markdown(
        "Kanalınızı bir kez tanımlayın; 8 uzman modül size özel strateji, 200 viral fikir, "
        "hook kütüphanesi, üretim akışı, analiz paneli ve 12 aylık yol haritası üretsin. "
        "**Videolarda kullanılacak tüm metinler (hook, başlık, senaryo, altyazı, hashtag) varsayılan olarak İngilizce üretilir** "
        "— küresel erişim ve daha yüksek reklam gelirleri için."
    )
    st.divider()

    st.subheader("1) Kanal Profili")
    profile = {
        "niche": st.text_input("İçerik alanı (niş) *", placeholder="Örn: Turkish history & lesser-known Ottoman stories / productivity for students / AI tools for teachers"),
        "audience": st.text_area("Hedef kitle", height=80, placeholder="Örn: 18–34 yaş, ABD/İngiltere, tarih meraklıları, dizi izleyicileri; kısa ve şaşırtıcı bilgi seviyor"),
        "competitors": st.text_area("Rakipler / örnek kanallar", height=80, placeholder="Kanal adlarını ve beğendiğiniz/beğenmediğiniz yönlerini yazın"),
        "goals": st.text_area("Hedefler", height=80, placeholder="Örn: 6 ayda 10.000 abone, YPP'ye girmek, dijital ürün satmak"),
        "status": st.text_input("Mevcut durum", placeholder="Örn: 0 abone, yeni kanal / 1.200 abone, haftada 3 Short"),
        "resources": st.text_input("Kaynaklar", placeholder="Örn: haftada 6 saat, yüzsüz (faceless) kanal, ücretsiz araçlar, CapCut"),
        "notes": st.text_area("Ek notlar (isteğe bağlı)", height=68),
    }

    st.subheader("2) Dil Ayarları")
    c1, c2 = st.columns(2)
    with c1:
        content_lang = st.selectbox("Video içerik dili", LANG_OPTIONS, index=0,
                                    help="Hook, başlık, senaryo, altyazı, açıklama ve hashtag'ler bu dilde yazılır.")
    with c2:
        explain_lang = st.selectbox("Açıklama / strateji dili", ["Türkçe", "English"], index=0,
                                    help="Analiz ve stratejik açıklamalar bu dilde yazılır.")
    use_context = st.checkbox("Önceki modül çıktılarını bağlam olarak kullan (tutarlı strateji için önerilir)", value=True)

    st.subheader("3) Modül Seçimi")
    keys = list(MODULES.keys())
    key = st.selectbox("Modül", keys, format_func=lambda k: MODULES[k]["title"])
    st.caption(MODULES[key]["short"])
    if key == "ideas":
        st.caption("ℹ️ 200 fikir, tekrar olmaması için 4 parti hâlinde (4 API çağrısı) üretilir.")

    b1, b2 = st.columns(2)
    run_one = b1.button("🚀 Seçili Modülü Üret", use_container_width=True)
    run_all = b2.button("⚡ 8 Modülün Tümünü Üret", use_container_width=True,
                        help="Modüller sırayla çalışır ve her biri öncekileri bağlam olarak kullanır. Birkaç dakika sürebilir.")

    if run_one or run_all:
        if not api_key:
            st.error("⚠️ Lütfen sol menüden Gemini API Anahtarınızı girin.")
            return
        if not profile["niche"].strip():
            st.warning("⚠️ Lütfen en azından içerik alanınızı (niş) yazın.")
            return
        targets = keys if run_all else [key]
        progress = st.progress(0.0) if run_all else None
        for i, k in enumerate(targets):
            try:
                run_module(k, profile, explain_lang, content_lang, use_context)
            except Exception as e:
                st.error(f"❌ {MODULES[k]['title']} üretilirken hata oluştu: {e}")
                break
            if progress:
                progress.progress((i + 1) / len(targets))
        st.success("✅ Üretim tamamlandı!")

    outputs = st.session_state.get("shorts_outputs", {})
    if outputs:
        st.divider()
        st.subheader("📚 Üretilen Çıktılar")
        for k in MODULES:
            if k in outputs:
                with st.expander(MODULES[k]["title"], expanded=(k == key)):
                    st.markdown(outputs[k])
                    st.download_button("⬇️ Bu modülü indir (.md)", outputs[k],
                                       file_name=f"shorts_{k}.md", mime="text/markdown", key=f"dl_{k}")
        d1, d2 = st.columns(2)
        d1.download_button("⬇️ Tüm stratejiyi indir (.md)", combined_markdown(profile),
                           file_name="youtube_shorts_strategy.md", mime="text/markdown", use_container_width=True)
        if d2.button("🗑️ Çıktıları temizle", use_container_width=True):
            st.session_state["shorts_outputs"] = {}
            st.rerun()


if mode.startswith("🏛️"):
    kamu_iletisim()
else:
    shorts_studio()
