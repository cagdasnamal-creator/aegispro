import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import ta
import plotly.graph_objects as go
import time
import logging

# --- KONFİGÜRASYON ---
logging.getLogger('yfinance').setLevel(logging.CRITICAL)
st.set_page_config(page_title="AEGIS Pro", layout="wide")

# --- MEGA LİSTE ---
BIST_MEGA_TICKERS = [
    'AEFES.IS', 'AGHOL.IS', 'AHGAZ.IS', 'AKBNK.IS', 'AKCNS.IS', 'AKFGY.IS', 'AKFYE.IS', 'AKSA.IS', 'AKSEN.IS',
    'ALARK.IS', 'ALBRK.IS', 'ALFAS.IS', 'ARCLK.IS', 'ASELS.IS', 'ASGYO.IS', 'ASTOR.IS', 'BERA.IS', 'BIMAS.IS',
    'BIOEN.IS', 'BRSAN.IS', 'BRYAT.IS', 'BUCIM.IS', 'CANTE.IS', 'CCOLA.IS', 'CEMTS.IS', 'CIMSA.IS', 'CWENE.IS',
    'DOAS.IS', 'DOHOL.IS', 'ECILC.IS', 'ECZYT.IS', 'EGEEN.IS', 'EKGYO.IS', 'ENJSA.IS', 'ENKAI.IS', 'EREGL.IS',
    'EUPWR.IS', 'EUREN.IS', 'FROTO.IS', 'GARAN.IS', 'GENIL.IS', 'GESAN.IS', 'GLYHO.IS', 'GUBRF.IS', 'GWIND.IS',
    'HALKB.IS', 'HEKTS.IS', 'IMASM.IS', 'IPEKE.IS', 'ISCTR.IS', 'ISDMR.IS', 'ISGYO.IS', 'ISMEN.IS', 'IZMDC.IS',
    'KARSN.IS', 'KAYSE.IS', 'KCAER.IS', 'KCHOL.IS', 'KMPUR.IS', 'KONTR.IS', 'KONYA.IS', 'KORDS.IS', 'KOZAA.IS',
    'KOZAL.IS', 'KRDMD.IS', 'KZBGY.IS', 'MAVI.IS', 'MGROS.IS', 'MIATK.IS', 'ODAS.IS', 'OTKAR.IS', 'OYAKC.IS',
    'PENTA.IS', 'PETKM.IS', 'PGSUS.IS', 'PSGYO.IS', 'QUAGR.IS', 'SAHOL.IS', 'SASA.IS', 'SELEC.IS', 'SISE.IS',
    'SKBNK.IS', 'SMRTG.IS', 'SOKM.IS', 'TAVHL.IS', 'TCELL.IS', 'THYAO.IS', 'TKFEN.IS', 'TOASO.IS', 'TSKB.IS',
    'TTKOM.IS', 'TTRAK.IS', 'TUKAS.IS', 'TUPRS.IS', 'TURSG.IS', 'ULKER.IS', 'VAKBN.IS', 'VESBE.IS', 'VESTL.IS',
    'YEOTK.IS', 'YKBNK.IS', 'YYLGD.IS', 'ZOREN.IS', 'ADESE.IS', 'ANELE.IS', 'BAGFS.IS', 'CELHA.IS', 'DERIM.IS',
    'EDATA.IS', 'ESEN.IS', 'GOZDE.IS', 'HUBVC.IS', 'INVEO.IS', 'JANTS.IS', 'KFEIN.IS', 'LOGO.IS', 'NETAS.IS',
    'ORCAY.IS', 'PAPIL.IS', 'QNBFB.IS', 'RTALB.IS', 'SNGYO.IS', 'TKNSA.IS', 'VERTU.IS', 'ZEDUR.IS',
    'AATAC.IS', 'ABOT.IS', 'ACSEL.IS', 'ADEL.IS', 'AFYON.IS', 'AGESA.IS', 'AGROT.IS', 'AKENR.IS', 'AKGRT.IS', 'AKMGY.IS',
    'AKSGY.IS', 'AKSUE.IS', 'ALCAR.IS', 'ALCTL.IS', 'ALKA.IS', 'ALKIM.IS', 'ALMAD.IS', 'ALTNY.IS', 'ANGEN.IS',
    'ANKTM.IS', 'ANSGR.IS', 'ARASE.IS', 'ARDYZ.IS', 'ARENA.IS', 'ARSAN.IS', 'ARZUM.IS', 'ASUZU.IS', 'ATEKS.IS',
    'ATLAS.IS', 'ATSYH.IS', 'AVGYO.IS', 'AVHOL.IS', 'AVOD.IS', 'AVTUR.IS', 'AYCES.IS', 'AYDEM.IS', 'AYEN.IS',
    'AYES.IS', 'AYGAZ.IS', 'AZTEK.IS', 'BAKAB.IS', 'BALAT.IS', 'BANVT.IS', 'BARMA.IS', 'BASCM.IS', 'BASGZ.IS',
    'BAYRK.IS', 'BEGYO.IS', 'BELEN.IS', 'BEYAZ.IS', 'BFREN.IS', 'BIENP.IS', 'BIGCH.IS', 'BJKAS.IS', 'BLCYT.IS',
    'BMTKS.IS', 'BNASL.IS', 'BOBET.IS', 'BORSK.IS', 'BOSSA.IS', 'BRISA.IS', 'BRKO.IS', 'BRKSN.IS', 'BRMEN.IS',
    'BRKVY.IS', 'BRLS.IS', 'BTCIM.IS', 'BURCE.IS', 'BURVA.IS', 'BVSAN.IS', 'BYDNR.IS', 'CASA.IS', 'CATES.IS',
    'CEOEM.IS', 'CEWL.IS', 'CLEBI.IS', 'CONSE.IS', 'COSMO.IS', 'CRDFA.IS', 'CVKMD.IS', 'DAGHL.IS', 'DAGI.IS',
    'DAPGM.IS', 'DARDL.IS', 'DGATE.IS', 'DGGYO.IS', 'DGNMO.IS', 'DIRIT.IS', 'DITAS.IS', 'DMSAS.IS', 'DNISI.IS',
    'DOCO.IS', 'DOGUB.IS', 'DOKTA.IS', 'DURDO.IS', 'DYOBY.IS', 'DZGYO.IS', 'EBEBK.IS', 'EDIP.IS', 'EGEPO.IS',
    'EGGUB.IS', 'EGPRO.IS', 'EGSER.IS', 'EIBHK.IS', 'EKSUN.IS', 'ELITE.IS', 'EMKEL.IS', 'EMNIS.IS', 'ENERY.IS',
    'EPLAS.IS', 'ERCB.IS', 'ERSU.IS', 'ESCOM.IS', 'ESMT.IS', 'ETILR.IS', 'EUHOL.IS', 'EUKYO.IS', 'EYGYO.IS',
    'FADE.IS', 'FENER.IS', 'FLAP.IS', 'FMIZP.IS', 'FORMT.IS', 'FORTE.IS', 'FRIGO.IS', 'FUMX.IS', 'FZLGY.IS',
    'GARFA.IS', 'GEDIK.IS', 'GEDZA.IS', 'GENTS.IS', 'GEREL.IS', 'GIPTA.IS', 'GLBMD.IS', 'GLCVY.IS', 'GLRYH.IS',
    'GMTAS.IS', 'GOLTS.IS', 'GOODY.IS', 'GRNYO.IS', 'GSDDE.IS', 'GSDHO.IS', 'GSRAY.IS', 'GUBRF.IS', 'HLGYO.IS',
    'HTTBT.IS', 'HUNER.IS', 'ICBCT.IS', 'IDGYO.IS', 'IEYHO.IS', 'IHGZT.IS', 'IHLAS.IS', 'IHLGM.IS', 'INDES.IS',
    'INFO.IS', 'INGRM.IS', 'INTEM.IS', 'INVEO.IS', 'INVES.IS', 'ISATR.IS', 'ISBTR.IS', 'ISFIN.IS', 'ISGSY.IS',
    'ISKUR.IS', 'ITTFH.IS', 'IZENR.IS', 'IZFAS.IS', 'IZINV.IS', 'KAPLM.IS', 'KAREL.IS', 'KARTN.IS', 'KARYE.IS',
    'KATMR.IS', 'KBTIN.IS', 'KENT.IS', 'KERVN.IS', 'KERVT.IS', 'KGYO.IS', 'KIMMR.IS', 'KLGYO.IS', 'KLMSN.IS',
    'KLNMA.IS', 'KLRHO.IS', 'KLSYN.IS', 'KLYN.IS', 'KMEPU.IS', 'KNFRT.IS', 'KOCAER.IS', 'KONKA.IS', 'KOPOL.IS',
    'KRGYO.IS', 'KRONT.IS', 'KRPLS.IS', 'KRSTL.IS', 'KRTEK.IS', 'KRVGD.IS', 'KSTUR.IS', 'KUTPO.IS', 'KUVVA.IS',
    'KUYAS.IS', 'KZGYO.IS', 'LIDER.IS', 'LIDFA.IS', 'LINK.IS', 'LKMNH.IS', 'LUKSK.IS', 'MAALT.IS', 'MACKO.IS',
    'MAGEN.IS', 'MAKIM.IS', 'MAKTK.IS', 'MANAS.IS', 'MARKA.IS', 'MARTI.IS', 'MBELB.IS', 'MEDTR.IS', 'MEGAP.IS',
    'MEPET.IS', 'MERCN.IS', 'MERIT.IS', 'MERKO.IS', 'METRO.IS', 'MHRGY.IS', 'MIPAZ.IS', 'MMCAS.IS', 'MNDRS.IS',
    'MNDTR.IS', 'MOBTL.IS', 'MPARK.IS', 'MRGYO.IS', 'MRSHL.IS', 'MSGYO.IS', 'MTRKS.IS', 'MTRYO.IS', 'MZHLD.IS',
    'NIBAS.IS', 'NTGAZ.IS', 'NTHOL.IS', 'NUHCM.IS', 'OBASE.IS', 'OFSYM.IS', 'ONCSM.IS', 'ORGE.IS', 'ORMA.IS',
    'OSMEN.IS', 'OSTIM.IS', 'OYAYO.IS', 'OYLUM.IS', 'OYSAN.IS', 'OZGYO.IS', 'OZKGY.IS', 'OZRDN.IS', 'OZSUB.IS',
    'PAGYO.IS', 'PAMEL.IS', 'PANELS.IS', 'PARSN.IS', 'PASEU.IS', 'PCILT.IS', 'PEGYO.IS', 'PEKGY.IS', 'PENGD.IS',
    'PINSU.IS', 'PKART.IS', 'PKENT.IS', 'PNLSN.IS', 'PNSUT.IS', 'POLHO.IS', 'POLTK.IS', 'PRDGS.IS', 'PRKAB.IS',
    'PRKME.IS', 'PRZMA.IS', 'PSDTC.IS', 'QNBFL.IS', 'RALYH.IS', 'RAYSG.IS', 'REEDR.IS', 'RNPOL.IS', 'RODRG.IS',
    'ROYAL.IS', 'RUBNS.IS', 'RYGYO.IS', 'RYSAS.IS', 'SAFKR.IS', 'SAMAT.IS', 'SANEL.IS', 'SANFO.IS', 'SANKO.IS',
    'SARKY.IS', 'SARTN.IS', 'SAYAS.IS', 'SDTTR.IS', 'SEGYO.IS', 'SEKFK.IS', 'SEKUR.IS', 'SELGD.IS', 'SELVA.IS',
    'SEYKM.IS', 'SILVR.IS', 'SIMGW.IS', 'SNICA.IS', 'SNKPA.IS', 'SNPAM.IS', 'SODSN.IS', 'SONME.IS', 'SRVGY.IS',
    'SUMAS.IS', 'SUNTK.IS', 'SURGY.IS', 'SUWEN.IS', 'TABGD.IS', 'TARKM.IS', 'TATEN.IS', 'TATGD.IS', 'TDGYO.IS',
    'TEKTU.IS', 'TERA.IS', 'TETMT.IS', 'TEZOL.IS', 'TGSAS.IS', 'TIGRE.IS', 'TILLO.IS', 'TLMAN.IS', 'TMPOL.IS',
    'TMSN.IS', 'TNZTP.IS', 'TRILC.IS', 'TSPOR.IS', 'TUCLK.IS', 'TURGG.IS', 'TURSG.IS', 'UFUK.IS', 'ULAS.IS',
    'ULUSE.IS', 'ULUFA.IS', 'UNMAŞ.IS', 'USAK.IS', 'UYYO.IS', 'VAKFN.IS', 'VAKKO.IS', 'VANGD.IS', 'VBTYZ.IS', 'VERUS.IS',
    'VKFYO.IS', 'VKGYO.IS', 'VKING.IS', 'YAPRK.IS', 'YAYLA.IS', 'YBTAS.IS', 'YESIL.IS', 'YGGYO.IS', 'YGYO.IS',
    'YIGIT.IS', 'YLNMK.IS', 'YONGA.IS', 'YOTAS.IS', 'YUNSA.IS', 'YYAPI.IS'
]

# --- 1. OPTİMİZE VERİ MOTORU ---
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_stock_data(ticker, period='1y'):
    try:
        df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if df.empty:
            return pd.DataFrame()
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.droplevel(1)
        if len(df) < 50:
            return pd.DataFrame()
        return df
    except:
        return pd.DataFrame()

@st.cache_data(ttl=86400, show_spinner=False)
def get_fundamentals(ticker):
    try:
        info = yf.Ticker(ticker).info
        mcap = info.get('marketCap', 0)
        mcap_billion = round(mcap / 1e9, 2) if mcap else 0
        if mcap_billion > 50: tip = 'Büyük Ölçekli'
        elif mcap_billion >= 10: tip = 'Orta Ölçekli'
        else: tip = 'Yan Tahta/Küçük'

        return {
            'Sektör': info.get('sector', 'Bilinmiyor'),
            'ROE': info.get('returnOnEquity', 0),
            'Borç': info.get('debtToEquity', 0),
            'Piyasa_Degeri': mcap_billion,
            'Hisse_Tipi': tip,
            'FK': info.get('trailingPE', None),
            'PD_DD': info.get('priceToBook', None)
        }
    except:
        return {'Sektör': 'Bilinmiyor', 'ROE': 0, 'Borç': 0, 'Piyasa_Degeri': 0, 'Hisse_Tipi': 'Bilinmiyor', 'FK': None, 'PD_DD': None}

def get_volume_status(relative_volume_sma_3):
    if relative_volume_sma_3 > 1.5:
        return 'Güçlü Hacim'
    elif relative_volume_sma_3 > 1.2:
        return 'Artan Hacim'
    else:
        return 'Normal/Zayıf'

# --- 2. ANALİZ MOTORU ---
def add_indicators(df):
    try:
        df = df.copy()
        # Basic Indicators
        df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
        macd = ta.trend.MACD(df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_S'] = macd.macd_signal()
        
        # Trend
        df['SMA_50'] = ta.trend.SMAIndicator(df['Close'], 50).sma_indicator()
        df['SMA_200'] = ta.trend.SMAIndicator(df['Close'], 200).sma_indicator() # WAR MODE: SMA 200
        df['SMA_50_Lag_5'] = df['SMA_50'].shift(5) # WAR MODE: Slope Calculation
        
        # Volatility
        bb = ta.volatility.BollingerBands(df['Close'])
        df['BB_H'] = bb.bollinger_hband()
        df['BB_L'] = bb.bollinger_lband()
        
        # Momentum
        stoch = ta.momentum.StochasticOscillator(df['High'], df['Low'], df['Close'])
        df['Stoch'] = stoch.stoch()

        # --- Volume Indicators ---
        df['SMA_Volume_20'] = df['Volume'].rolling(window=20).mean()
        
        # Safe division for Relative Volume
        df['Relative_Volume'] = df['Volume'].div(df['SMA_Volume_20'].replace(0, np.nan)).fillna(0)
        
        # 3-Day SMA of Relative Volume with NaN fill
        df['Relative_Volume_SMA_3'] = df['Relative_Volume'].rolling(window=3).mean().fillna(0)

        df['OBV'] = ta.volume.OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()

        # [FIX 2] Safe dropna for stability
        return df.dropna(subset=[
            'RSI','MACD','MACD_S',
            'SMA_50','SMA_200',
            'BB_H','BB_L',
            'Stoch',
            'SMA_Volume_20',
            'Relative_Volume_SMA_3',
            'OBV'
        ])
    except:
        return pd.DataFrame()

def calculate_score(df, fund):
    last = df.iloc[-1]
    prev = df.iloc[-2]
    score = 0
    reasons = []

    # --- 1. TREND GÜCÜ (+3) ---
    # Fiyat > SMA50 VE SMA50 Eğimi Pozitif
    if (last['Close'] > last['SMA_50']) and (last['SMA_50'] > last['SMA_50_Lag_5']):
        score += 3
        reasons.append("Güçlü Trend (+3)")

    # --- 2. MOMENTUM (+2) ---
    # RSI 45-65 Aralığı (Sağlıklı Boğa)
    if 45 <= last['RSI'] <= 65:
        score += 2
        reasons.append("Sağlıklı Momentum (+2)")

    # --- 3. MACD GÜCÜ (+2) ---
    # MACD > Sinyal VE Histogram Artıyor
    hist_curr = last['MACD'] - last['MACD_S']
    hist_prev = prev['MACD'] - prev['MACD_S']
    if (last['MACD'] > last['MACD_S']) and (hist_curr > hist_prev):
        score += 2
        reasons.append("MACD Güçleniyor (+2)")

    # --- 4. TEMEL (+2) ---
    if fund['ROE'] > 0.20: score += 1
    if fund['Borç'] < 150: score += 1

    # --- 5. DİP SİNYALİ (+1) ---
    # Bollinger Altı veya Stoch < 20 (Anti-Overlap)
    if (last['Close'] < last['BB_L']) or (last['Stoch'] < 20):
        score += 1
        reasons.append("Dip Sinyali (+1)")

    # --- 6. DOWNTREND CAP (WAR MODE) ---
    # Fiyat < SMA200 VEYA Death Cross (SMA50 < SMA200)
    is_downtrend = (last['Close'] < last['SMA_200']) or (last['SMA_50'] < last['SMA_200'])
    
    final_score = score
    if is_downtrend:
        if score > 1:
            reasons.append("⚠️ DÜŞÜŞ KİLİDİ (Max 1 Puan)")
            final_score = 1
        else:
            final_score = score

    # Normalize 0-10
    return final_score, reasons

# --- 3. ARAYÜZ ---
st.title("🛡️ AEGIS Pro")
st.markdown("**0-10 Puanlama | Düşüş Trendi Koruması | Gelişmiş Filtreleme**")

# --- SIDEBAR RESTORATION ---
with st.sidebar:
    # --- YASAL UYARI & REHBER ---
    with st.expander("ℹ️ Yasal Uyarı & Rehber", expanded=False):
        st.markdown("""
        ⚠️ Yasal Uyarı

        Bu uygulama yatırım tavsiyesi niteliği taşımaz.
        Sunulan veriler, grafikler ve skorlar; geçmiş fiyat hareketleri ile halka açık finansal verilerin matematiksel ve teknik analiz yöntemleriyle değerlendirilmesi sonucunda oluşturulmuştur.

        AEGIS Pro, trend liderlerini ayıklayan ve para akışı teyidi sunan bir analiz motorudur.
        Herhangi bir AL / SAT / TUT önerisi, trade sinyali veya kişiye özel risk yönetimi hizmeti sunmaz.

        Finansal piyasalar risk içerir. Yatırım kararları, kullanıcıların kendi araştırmaları ve risk tercihleri doğrultusunda alınmalıdır.

        📘 Kullanım Rehberi

        1️⃣ Skorlama (0–10)
        AEGIS Skoru, teknik yapı, trend gücü ve momentum kalitesini ölçmeye yönelik bir değerlendirme puanıdır.
        Yüksek skor, güçlü teknik yapı olasılığına işaret eder; tek başına yatırım kararı için yeterli değildir.

        2️⃣ Düşüş Kilidi (Trend Filtresi)
        Fiyatın 200 günlük ortalamanın altında olması veya “Death Cross” (SMA50 < SMA200) yapısı görülmesi durumunda sistem, düşüş trendini işaret eder ve skoru sınırlandırır.

        3️⃣ Hacim Analizi (Para Akışı Teyidi)
        “Güçlü Hacim” veya “Artan Hacim” göstergeleri, fiyat hareketinin işlem hacmi ile desteklenip desteklenmediğini gösterir.
        Bu göstergeler trendin kalitesine dair ek teyit sunar.
        """)

if st.button("🚀 Taramayı Başlat"):
    results = []
    bar = st.progress(0)
    status = st.empty()
    total = len(BIST_MEGA_TICKERS)

    for i, t in enumerate(BIST_MEGA_TICKERS):
        status.text(f"Analiz: {t} ({i+1}/{total})")
        df = fetch_stock_data(t)
        if not df.empty:
            df = add_indicators(df)
            if not df.empty:
                fund = get_fundamentals(t)
                score, reasons = calculate_score(df, fund)
                last = df.iloc[-1]
                
                volume_status = get_volume_status(last['Relative_Volume_SMA_3'])
                
                # [FIX 1] Safer OBV Trend Calculation
                if len(df) >= 10:
                    obv_slope = df['OBV'].iloc[-1] - df['OBV'].iloc[-10]
                    obv_trend = "Yükseliş" if obv_slope > 0 else "Düşüş"
                else:
                    obv_trend = "Yetersiz Veri"

                # [FIX - TypeError] Safer Rounding
                try:
                    fk_val = round(float(fund['FK']), 2) if fund['FK'] is not None else None
                except: fk_val = None

                try:
                    pd_dd_val = round(float(fund['PD_DD']), 2) if fund['PD_DD'] is not None else None
                except: pd_dd_val = None

                results.append({
                    'Hisse': t, 
                    'Fiyat': round(last['Close'], 2), 
                    'Skor': score,
                    'Hacim_Artis': volume_status, 
                    'Sektör': fund['Sektör'],
                    'Piyasa_Degeri': fund['Piyasa_Degeri'], 
                    'Hisse_Tipi': fund['Hisse_Tipi'],
                    'FK': fk_val,
                    'PD_DD': pd_dd_val,
                    'OBV_Trend': obv_trend
                })
        bar.progress((i+1)/total)
    
    status.success("✅ Tarama Tamamlandı!")
    st.session_state['data'] = pd.DataFrame(results)

if 'data' in st.session_state:
    df = st.session_state['data']
    c1, c2, c3 = st.columns(3)
    # Updated slider range for 0-10 score
    min_skor = c1.slider("Min Skor", 0, 10, 3)
    tum_tipler = df['Hisse_Tipi'].unique().tolist()
    secilen_tipler = c2.multiselect("Hisse Büyüklüğü", options=tum_tipler, default=tum_tipler)
    sektor = c3.multiselect("Sektör", options=df['Sektör'].unique())

    # Filtering with masks
    mask = (df['Skor'] >= min_skor) & (df['Hisse_Tipi'].isin(secilen_tipler))
    if sektor:
        mask &= df['Sektör'].isin(sektor)
    
    filtered = df[mask]

    st.subheader("📊 Piyasa Raporu")
    st.dataframe(
        filtered.sort_values(['Skor', 'Piyasa_Degeri'], ascending=[False, False]),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Fiyat": st.column_config.NumberColumn(format="%.2f TL"),
            "Hacim_Artis": st.column_config.TextColumn("Hacim Durumu"),
            "Piyasa_Degeri": st.column_config.NumberColumn("PD (Milyar TL)", format="%.2f Mr"),
            "Skor": st.column_config.NumberColumn("Aegis Skoru"),
            "FK": st.column_config.NumberColumn("F/K Oranı", format="%.2f"),
            "PD_DD": st.column_config.NumberColumn("PD/DD", format="%.2f"),
            "OBV_Trend": st.column_config.TextColumn("OBV Trendi")
        }
    )

    st.divider()
    sel = st.selectbox("Detaylı Grafik Analizi İçin Hisse Seçin", options=filtered['Hisse'].unique())
    if sel:
        # Using cached data fetch here might save network time if already cached
        df_p = add_indicators(fetch_stock_data(sel))
        row = filtered[filtered['Hisse'] == sel].iloc[0]

        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Fiyat", f"{row['Fiyat']} TL")
        k2.metric("Skor", row['Skor'])
        k3.metric("F/K Oranı", row['FK'] if row['FK'] else "-")
        k4.metric("PD/DD", row['PD_DD'] if row['PD_DD'] else "-")
        k5.metric("Hacim Durumu", row['Hacim_Artis'])

        fig = go.Figure(data=[go.Candlestick(x=df_p.index, open=df_p['Open'], high=df_p['High'], low=df_p['Low'], close=df_p['Close'], name='Fiyat')])
        fig.add_trace(go.Scatter(x=df_p.index, y=df_p['BB_H'], line=dict(color='gray', width=1, dash='dot'), name='BB Üst'))
        fig.add_trace(go.Scatter(x=df_p.index, y=df_p['BB_L'], line=dict(color='gray', width=1, dash='dot'), name='BB Alt'))
        
        # Add SMA lines to chart
        fig.add_trace(go.Scatter(x=df_p.index, y=df_p['SMA_50'], line=dict(color='orange', width=1.5), name='SMA 50'))
        fig.add_trace(go.Scatter(x=df_p.index, y=df_p['SMA_200'], line=dict(color='blue', width=2), name='SMA 200'))

        fig.update_layout(title=f"{sel} Teknik Analiz ve Risk Seviyeleri", template="plotly_dark", height=500)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader(f"{sel} Hacim Analizi")
        fig_vol = go.Figure(data=[
            go.Bar(x=df_p.index, y=df_p['Volume'], name='Günlük Hacim', marker_color='rgba(102,153,204,0.6)'),
            go.Scatter(x=df_p.index, y=df_p['SMA_Volume_20'], mode='lines', name='20-Gün Hacim Ort.', line=dict(color='orange', width=2))
        ])
        fig_vol.update_layout(title='Günlük Hacim ve Ortalaması', template="plotly_dark", height=300)
        st.plotly_chart(fig_vol, use_container_width=True)

        st.markdown(f"**OBV (On-Balance Volume) Trendi:** Son 10 gün içinde **{row['OBV_Trend']}** yönünde.")
