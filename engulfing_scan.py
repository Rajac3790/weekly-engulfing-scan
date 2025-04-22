import yfinance as yf
import pandas as pd
import requests
import os
from time import sleep

# ====== Stock List ======
nse_stocks = [
  "3MINDIA.NS", "AARTIDRUGS.NS", "AARTIIND.NS", "AAVAS.NS", "ACCELYA.NS", "ACE.NS", "ADFFOODS.NS", "ADVENZYMES.NS", "AIAENG.NS", "AJANTPHARM.NS", "AKZOINDIA.NS", "ALEMBICLTD.NS", "ALKEM.NS", "ALKYLAMINE.NS", "ALLCARGO.NS", "ALOKINDS.NS", "AMBER.NS", "AMRUTANJAN.NS", "ANANTRAJ.NS", "ANDHRSUGAR.NS", "ANGELONE.NS", "ANURAS.NS", "APARINDS.NS", "APCOTEXIND.NS", "APLLTD.NS", "APLAPOLLO.NS", "APOLLOTYRE.NS", "ASTRAL.NS", "ASTEC.NS", "ASTRAZEN.NS", "ASTRAMICRO.NS", "ATGL.NS", "ATUL.NS", "AUBANK.NS", "AUTOAXLES.NS", "AUTOIND.NS", "AVANTIFEED.NS", "AXISBANK.NS", "BALAMINES.NS", "BALMLAWRIE.NS", "BALRAMCHIN.NS", "BANCOINDIA.NS", "BASF.NS", "BAJAJCON.NS", "BAJAJELEC.NS", "BAJAJHCARE.NS", "BAJAJHLDNG.NS", "BANKBARODA.NS", "BATAINDIA.NS", "BAYERCROP.NS", "BBTC.NS", "BEPL.NS", "BEL.NS", "BEML.NS", "BERGEPAINT.NS", "BFINVEST.NS", "BHARATFORG.NS", "BHARATRAS.NS", "BHEL.NS", "BHARTIARTL.NS", "BIRLACORPN.NS", "BLISSGVS.NS", "BLUESTARCO.NS", "BODALCHEM.NS", "BOMDYEING.NS", "BOROLTD.NS", "BORORENEW.NS", "BRIGADE.NS", "BSE.NS", "BSOFT.NS", "CAPLIPOINT.NS", "CARBORUNIV.NS", "CASTROLIND.NS", "CCL.NS", "CEATLTD.NS", "CERA.NS", "CESC.NS", "CHALET.NS", "CHAMBLFERT.NS", "CHENNPETRO.NS", "CHOLAFIN.NS", "CHOLAHLDNG.NS", "CIGNITITEC.NS", "CIPLA.NS", "COCHINSHIP.NS", "COFORGE.NS", "COLPAL.NS", "CONFIPET.NS", "CONCOR.NS", "COROMANDEL.NS", "CRAFTSMAN.NS", "CRISIL.NS", "CROMPTON.NS", "CUB.NS", "CUMMINSIND.NS", "CYIENT.NS", "DABUR.NS",  "DCAL.NS", "DCBBANK.NS", "DCMSHRIRAM.NS", "DEEPAKFERT.NS", "DEEPAKNTR.NS", "DELTACORP.NS", "DHAMPURSUG.NS", "DHANUKA.NS", "DHANI.NS", "DICIND.NS", "DIAMONDYD.NS", "DIXON.NS", "DOLLAR.NS", "DBCORP.NS", "DBL.NS", "DISHTV.NS", "DIVISLAB.NS", "DRREDDY.NS", "DREDGECORP.NS", "EASEMYTRIP.NS", "ECLERX.NS", "EDELWEISS.NS", "EICHERMOT.NS", "EIDPARRY.NS", "EIHOTEL.NS", "ELGIEQUIP.NS", "EMAMILTD.NS", "ENDURANCE.NS", "ENGINERSIN.NS", "ESCORTS.NS", "EVEREADY.NS", "EXCELINDUS.NS", "EXIDEIND.NS", "FDC.NS", "FEDERALBNK.NS", "FIEMIND.NS", "FILATEX.NS", "FINCABLES.NS", "FINPIPE.NS", "FINEORG.NS", "FORTIS.NS", "FSL.NS", "GABRIEL.NS", "GAEL.NS", "GALAXYSURF.NS", "GARFIBRES.NS", "GATECH.NS", "GESHIP.NS", "GHCL.NS", "GICRE.NS", "GILLETTE.NS", "GIPCL.NS", "GLAXO.NS", "GLENMARK.NS", "GMMPFAUDLR.NS", "GMBREW.NS", "GNFC.NS", "GODFRYPHLP.NS", "GODREJAGRO.NS", "GODREJCP.NS", "GODREJIND.NS", "GODREJPROP.NS", "GPIL.NS", "GPPL.NS", "GRANULES.NS", "GRAPHITE.NS", "GRASIM.NS", "GREAVESCOT.NS", "GREENPANEL.NS", "GREENPLY.NS", "GRINDWELL.NS", "GRSE.NS", "GUJALKALI.NS", "GUJGASLTD.NS", "GUFICBIO.NS", "HAPPSTMNDS.NS", "HATSUN.NS", "HAVELLS.NS", "HCC.NS", "HCG.NS", "HDFCBANK.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEG.NS", "HEIDELBERG.NS", "HEMIPROP.NS", "HERITGFOOD.NS", "HEROMOTOCO.NS", "HESTERBIO.NS", "HFCL.NS", "HGS.NS", "HIGREEN.NS", "HIKAL.NS", "HIL.NS", "HIMATSEIDE.NS", "HINDALCO.NS", "HINDCOPPER.NS", "HINDOILEXP.NS", "HINDPETRO.NS", "HINDUNILVR.NS", "HINDZINC.NS", "HONAUT.NS", "HSCL.NS", "HUDCO.NS", "HUHTAMAKI.NS", "IEX.NS", "IFBIND.NS", "IGARASHI.NS", "IGL.NS", "IGPL.NS", "IIFL.NS", "INDHOTEL.NS", "INDIACEM.NS", "INDIAGLYCO.NS", "INDIAMART.NS", "INDIANB.NS", "INDIANHUME.NS", "INDOSTAR.NS", "INDUSINDBK.NS", "INDUSTOWER.NS", "INFIBEAM.NS", "INFOBEAN.NS", "INFY.NS", "INGERRAND.NS", "INOXWIND.NS", "INTELLECT.NS", "IOB.NS", "IOLCP.NS", "IPCALAB.NS", "IRB.NS", "IRCON.NS", "IRCTC.NS", "IRFC.NS", "ISGEC.NS", "ITC.NS", "ITDC.NS", "ITDCEM.NS", "ITI.NS", "JAGRAN.NS", "JAICORPLTD.NS", "JAMNAAUTO.NS", "JBCHEPHARM.NS", "JBMA.NS", "JCHAC.NS", "JINDALPOLY.NS", "JINDALSAW.NS", "JINDALSTEL.NS", "JINDWORLD.NS", "JKCEMENT.NS", "JKIL.NS", "JKLAKSHMI.NS", "JKPAPER.NS", "JKTYRE.NS", "JMFINANCIL.NS", "JSL.NS", "JTEKTINDIA.NS", "JUSTDIAL.NS", "JUBLFOOD.NS", "JUBLPHARMA.NS", "JUBLINGREA.NS", "KALYANKJIL.NS", "KANSAINER.NS", "KARURVYSYA.NS", "KCP.NS", "KEC.NS", "KEI.NS", "KIRLOSBROS.NS", "KIRIINDUS.NS", "KIRLOSENG.NS", "KNRCON.NS", "KOLTEPATIL.NS", "KPRMILL.NS", "KPIL.NS", "KPITTECH.NS", "KRBL.NS", "KSCL.NS", "KSB.NS", "KSL.NS", "LAOPALA.NS", "LALPATHLAB.NS", "LXCHEM.NS", "LEMONTREE.NS", "LGBBROSLTD.NS", "LICHSGFIN.NS", "LINDEINDIA.NS", "LTF.NS", "LTFOODS.NS", "LTTS.NS", "LUMAXTECH.NS", "LUPIN.NS", "LUXIND.NS", "LXCHEM.NS", "MAHABANK.NS", "MAHICKRA.NS", "MAHLIFE.NS", "MAHLOG.NS", "MAHSCOOTER.NS", "MAHSEAMLES.NS", "MANAPPURAM.NS", "MANINFRA.NS", "MARKSANS.NS", "MASFIN.NS", "MASTEK.NS", "MAXHEALTH.NS", "MAYURUNIQ.NS", "MCX.NS", "MFSL.NS", "MGL.NS", "MHRIL.NS", "MIDHANI.NS", "UNOMINDA.NS", "MINDACORP.NS", "MOIL.NS", "MOLDTKPAC.NS", "MOREPENLAB.NS", "MOTHERSON.NS", "MOTILALOFS.NS", "MPHASIS.NS", "MRPL.NS", "MSTCLTD.NS", "MTARTECH.NS", "MTNL.NS", "MUTHOOTFIN.NS", "NAM_INDIA.NS", "NATCOPHARM.NS", "NATIONALUM.NS", "NAVINFLUOR.NS", "NAVNETEDUL.NS", "NCC.NS", "NEOGEN.NS", "NEULANDLAB.NS", "NETWORK18.NS", "NEWGEN.NS", "NIACL.NS", "NIITLTD.NS", "NILKAMAL.NS", "NLCINDIA.NS", "NOCIL.NS", "NRBBEARING.NS", "NTPC.NS", "NUCLEUS.NS", "OAL.NS", "OBEROIRLTY.NS", "OCCL.NS", "OFSS.NS", "OIL.NS", "OLECTRA.NS", "ORIENTCEM.NS", "ORIENTELEC.NS", "ORISSAMINE.NS", "PAGEIND.NS", "PAISALO.NS", "PANACEABIO.NS", "PANAMAPET.NS", "JKPAPER.NS", "PCJEWELLER.NS", "PERSISTENT.NS", "PFC.NS", "PFIZER.NS", "PHOENIXLTD.NS", "PILANIINVS.NS", "PITTIENG.NS", "PNB.NS", "PNBGILTS.NS", "PNBHOUSING.NS", "POONAWALLA.NS", "POWERINDIA.NS", "PRESTIGE.NS", "PRINCEPIPE.NS", "PRIVISCL.NS", "PRSMJOHNSN.NS", "PSPPROJECT.NS", "PURVA.NS", "PVRINOX.NS", "QUESS.NS", "QUICKHEAL.NS", "RADICO.NS", "RAIN.NS", "RAJESHEXPO.NS", "RAMCOCEM.NS", "RAMCOIND.NS", "RAMCOSYS.NS", "RANEHOLDIN.NS", "RATNAMANI.NS", "RBLBANK.NS", "RAYMOND.NS", "RCF.NS", "RECLTD.NS", "RELIANCE.NS", "RELAXO.NS", "RENUKA.NS", "RITES.NS", "ROUTE.NS", "RPSGVENT.NS", "RSYSTEMS.NS", "RUPA.NS", "RUSHIL.NS", "RVNL.NS", "SAGCEM.NS", "SANOFI.NS", "SANGHIIND.NS", "SAREGAMA.NS", "SASKEN.NS", "SATIA.NS", "SCHAEFFLER.NS", "SCHNEIDER.NS", "SCHNEIDER.NS", "SDBL.NS", "SEAMECLTD.NS", "SEQUENT.NS", "SESHAPAPER.NS", "SHALBY.NS", "SHANKARA.NS", "SHARDACROP.NS", "SHARDAMOTR.NS", "SHILPAMED.NS", "SHOPERSTOP.NS", "SHREECEM.NS", "SHREEPUSHK.NS", "SHRIRAMFIN.NS", "SIEMENS.NS", "SIYSIL.NS", "SJS.NS", "SJVN.NS", "SKFINDIA.NS", "SOLARA.NS", "SOLARINDS.NS", "SONACOMS.NS", "SONATSOFTW.NS", "SOTL.NS", "SPANDANA.NS", "SPARC.NS", "STAR.NS", "STARCEMENT.NS", "STERTOOLS.NS", "STLTECH.NS", "STOVEKRAFT.NS", "SUBEXLTD.NS", "SUBROS.NS", "SUMICHEM.NS", "SUNDARMFIN.NS", "SUNDRMFAST.NS", "SUNFLAG.NS", "SUNTECK.NS", "SUNTV.NS", "SUPRAJIT.NS", "SUPREMEIND.NS", "SURANASOL.NS", "SURYAROSNI.NS", "SUTLEJTEX.NS", "SWSOLAR.NS", "SYNGENE.NS", "TANLA.NS", "TASTYBITE.NS", "TATACHEM.NS", "TATACOMM.NS", "TATAELXSI.NS", "TATAINVEST.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TCI.NS", "TCIEXP.NS", "TCL.NS", "TEAMLEASE.NS", "TECHNOE.NS", "TECHM.NS", "TEGA.NS", "TEJASNET.NS", "TEXRAIL.NS", "THERMAX.NS", "THOMASCOOK.NS", "THYROCARE.NS", "TIINDIA.NS", "TIMETECHNO.NS", "TIMKEN.NS", "TIRUMALCHM.NS", "TITAN.NS", "TMB.NS", "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS", "TRIDENT.NS", "TRITURBINE.NS", "TRIVENI.NS", "TVSMOTOR.NS", "TVSSRICHAK.NS", "TVTODAY.NS", "UBL.NS", "UFLEX.NS", "UJJIVANSFB.NS", "ULTRACEMCO.NS", "UNIONBANK.NS", "UNICHEMLAB.NS", "UNIPARTS.NS", "UPL.NS", "USHAMART.NS", "UTIAMC.NS", "VAIBHAVGBL.NS", "VARROC.NS", "VEDL.NS", "VENKEYS.NS", "VESUVIUS.NS", "VGUARD.NS", "VINATIORGA.NS", "VIPIND.NS", "VISAKAIND.NS", "VOLTAMP.NS", "VOLTAS.NS", "VRLLOG.NS", "VSTIND.NS", "VSTTILLERS.NS", "WABAG.NS", "WELCORP.NS", "WELENT.NS", "WESTLIFE.NS", "WHIRLPOOL.NS", "WHEELS.NS", "WIPRO.NS", "WOCKPHARMA.NS", "WONDERLA.NS", "WSTCSTPAPR.NS", "ZEEL.NS", "ZENSARTECH.NS", "ZYDUSWELL.NS",  "ABB.NS", "ACC.NS", "APLAPOLLO.NS", "AUBANK.NS", "AARTIIND.NS", "ADANIENSOL.NS", "ADANIENT.NS",
    "ADANIGREEN.NS", "ADANIPORTS.NS", "ATGL.NS", "ABCAPITAL.NS", "ABFRL.NS", "ALKEM.NS", "AMBUJACEM.NS",
    "ANGELONE.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS", "ASIANPAINT.NS", "ASTRAL.NS", 
    "AUROPHARMA.NS", "DMART.NS", "AXISBANK.NS", "BSOFT.NS", "BSE.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", 
    "BAJAJFINSV.NS", "BALKRISIND.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", "BERGEPAINT.NS", 
    "BEL.NS", "BHARATFORG.NS", "BHEL.NS", "BPCL.NS", "BHARTIARTL.NS", "BIOCON.NS", "BOSCHLTD.NS", 
    "BRITANNIA.NS", "CESC.NS", "CGPOWER.NS", "CANBK.NS", "CDSL.NS", "CHAMBLFERT.NS", "CHOLAFIN.NS", 
    "CIPLA.NS", "COALINDIA.NS", "COFORGE.NS", "COLPAL.NS", "CAMS.NS", "CONCOR.NS", "CROMPTON.NS", 
    "CUMMINSIND.NS", "CYIENT.NS", "DLF.NS", "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", "DELHIVERY.NS", 
    "DIVISLAB.NS", "DIXON.NS", "DRREDDY.NS", "EICHERMOT.NS", "ESCORTS.NS", "EXIDEIND.NS", "NYKAA.NS", 
    "GAIL.NS", "GMRAIRPORT.NS", "GLENMARK.NS", "GODREJCP.NS", "GODREJPROP.NS", "GRANULES.NS", "GRASIM.NS", 
    "HCLTECH.NS", "HDFCAMC.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HFCL.NS", "HAVELLS.NS", "HEROMOTOCO.NS", 
    "HINDALCO.NS", "HAL.NS", "HINDCOPPER.NS", "HINDPETRO.NS", "HINDUNILVR.NS", "HINDZINC.NS", "HUDCO.NS", 
    "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IDFCFIRSTB.NS", "IIFL.NS", "IRB.NS", "ITC.NS", 
    "INDIANB.NS", "IEX.NS", "IOC.NS", "IRCTC.NS", "IRFC.NS", "IREDA.NS", "IGL.NS", "INDUSTOWER.NS", 
    "INDUSINDBK.NS", "NAUKRI.NS", "INFY.NS", "INOXWIND.NS", "INDIGO.NS", "JSWENERGY.NS", "JSWSTEEL.NS", 
    "JSL.NS", "JINDALSTEL.NS", "JIOFIN.NS", "JUBLFOOD.NS", "KEI.NS", "KPITTECH.NS", "KALYANKJIL.NS", 
    "KOTAKBANK.NS", "LTF.NS", "LICHSGFIN.NS", "LTIM.NS", "LT.NS", "LAURUSLABS.NS", "LICI.NS", "LUPIN.NS", 
    "MRF.NS", "LODHA.NS", "MGL.NS", "M&MFIN.NS", "M&M.NS", "MANAPPURAM.NS", "MARICO.NS", "MARUTI.NS", 
    "MFSL.NS", "MAXHEALTH.NS", "MPHASIS.NS", "MCX.NS", "MUTHOOTFIN.NS", "NBCC.NS", "NCC.NS", "NHPC.NS", 
    "NMDC.NS", "NTPC.NS", "NATIONALUM.NS", "NESTLEIND.NS", "OBEROIRLTY.NS", "ONGC.NS", "OIL.NS", "PAYTM.NS", 
    "OFSS.NS", "POLICYBZR.NS", "PIIND.NS", "PNBHOUSING.NS", "PAGEIND.NS", "PATANJALI.NS", "PERSISTENT.NS", 
    "PETRONET.NS", "PIDILITIND.NS", "PEL.NS", "POLYCAB.NS", "POONAWALLA.NS", "PFC.NS", "POWERGRID.NS", 
    "PRESTIGE.NS", "PNB.NS", "RBLBANK.NS", "RECLTD.NS", "RELIANCE.NS", "SBICARD.NS", "SBILIFE.NS", 
    "SHREECEM.NS", "SJVN.NS", "SRF.NS", "MOTHERSON.NS", "SHRIRAMFIN.NS", "SIEMENS.NS", "SOLARINDS.NS", 
    "SONACOMS.NS", "SBIN.NS", "SAIL.NS", "SUNPHARMA.NS", "SUPREMEIND.NS", "SYNGENE.NS", "TATACONSUM.NS", 
    "TITAGARH.NS", "TVSMOTOR.NS", "TATACHEM.NS", "TATACOMM.NS", "TCS.NS", "TATAELXSI.NS", "TATAMOTORS.NS", 
    "TATAPOWER.NS", "TATASTEEL.NS", "TATATECH.NS", "TECHM.NS", "FEDERALBNK.NS", "INDHOTEL.NS", 
    "PHOENIXLTD.NS", "RAMCOCEM.NS", "TITAN.NS", "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS", "TIINDIA.NS", 
    "UPL.NS", "ULTRACEMCO.NS", "UNIONBANK.NS", "UNITDSPR.NS", "VBL.NS", "VEDL.NS", "IDEA.NS", "VOLTAS.NS", 
    "WIPRO.NS", "YESBANK.NS"
]

# ====== Pattern Checker ======
def is_engulfing(df):
    if len(df) < 2:
        return False, False

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    def valid_candle(candle):
        body = abs(candle.Close - candle.Open)
        upper_wick = candle.High - max(candle.Open, candle.Close)
        lower_wick = min(candle.Open, candle.Close) - candle.Low
        # Relax wick rule
        return upper_wick <= body * 1.5 and lower_wick <= body * 1.5

    if not valid_candle(prev) or not valid_candle(curr):
        return False, False

    bullish = (
        (curr.Close > curr.Open) and
        (prev.Close < prev.Open) and
        (curr.Close > prev.Open) and
        (curr.Open < prev.Close)
    )

    bearish = (
        (curr.Close < curr.Open) and
        (prev.Close > prev.Open) and
        (curr.Close < prev.Open) and
        (curr.Open > prev.Close)
    )

    return bullish, bearish

# ====== Weekly Engulfing Scan ======
def weekly_scan():
    print("📥 Downloading weekly data...")
    data = yf.download(
        tickers=nse_stocks,
        period="35d",
        interval="1wk",
        threads=True,
        progress=False
    )

    results = []

    for stock in nse_stocks:
        try:
            df = data[stock].copy() if len(nse_stocks) > 1 else data.copy()
            df.dropna(inplace=True)
            if df.shape[0] < 2:
                continue

            bullish, bearish = is_engulfing(df.tail(2))
            if bullish or bearish:
                pattern = "Weekly Bullish Engulfing" if bullish else "Weekly Bearish Engulfing"
                date = df.index[-1].date()
                results.append(f"{stock}: {pattern} ({date})")
        except Exception as e:
            print(f"Error processing {stock}: {e}")

    return results

# ====== Daily Engulfing Scan ======
def daily_scan():
    print("📥 Downloading daily data...")
    results = []
    batch_size = 100

    for i in range(0, len(nse_stocks), batch_size):
        batch = nse_stocks[i:i + batch_size]
        try:
            data = yf.download(
                tickers=batch,
                period="5d",
                interval="1d",
                threads=True,
                progress=False
            )
        except Exception as e:
            print(f"Download error for batch: {e}")
            continue

        for stock in batch:
            try:
                df = data[stock].copy() if len(batch) > 1 else data.copy()
                df.dropna(inplace=True)
                if len(df) < 2:
                    continue

                bullish, bearish = is_engulfing(df.tail(2))
                if bullish or bearish:
                    pattern = "Daily Bullish Engulfing" if bullish else "Daily Bearish Engulfing"
                    date = df.index[-1].date()
                    results.append(f"{stock}: {pattern} ({date})")
            except Exception as e:
                print(f"Error processing {stock}: {e}")
        sleep(2)

    return results

# ====== Telegram Sender (optional) ======
def send_telegram_message(message):
    bot_token = os.getenv("BOT_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    if not bot_token or not chat_id:
        print("Telegram skipped: missing BOT_TOKEN or CHAT_ID.")
        return

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': message}
    try:
        response = requests.post(url, data=payload)
        print("Telegram sent:", response.json())
    except Exception as e:
        print("Telegram error:", e)

# ====== Main Logic ======
if __name__ == "__main__":
    weekly_results = weekly_scan()
    daily_results = daily_scan()

    full_message = "📊 Engulfing Pattern Scan Results\n\n"

    if weekly_results:
        full_message += "🗓️ Weekly Patterns:\n" + "\n".join(weekly_results) + "\n\n"
    else:
        full_message += "🗓️ Weekly: No patterns found.\n\n"

    if daily_results:
        full_message += "📆 Daily Patterns:\n" + "\n".join(daily_results)
    else:
        full_message += "📆 Daily: No patterns found."

    # Print to Jupyter/console
    print(full_message)

    # Telegram sending optional: set SEND_TELEGRAM=true in environment to enable
    if os.getenv("SEND_TELEGRAM", "false").lower() == "true":
        send_telegram_message(full_message)
