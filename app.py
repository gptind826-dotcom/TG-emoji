import telebot
from telebot import types
from telebot.types import MessageEntity, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import random
import emoji
import time
import os
import json
from datetime import datetime

# Bot Credentials
TOKEN = "8695295764:AAFepkw7-ffheky5umbgAxgSeRF-AQbBaJY"
ADMIN_IDS = [8379062893, 6907359862]  # Multiple Admin IDs
bot = telebot.TeleBot(TOKEN)

bot_active = True
user_db_file = "users.json"

def load_users():
    if os.path.exists(user_db_file):
        with open(user_db_file, "r") as f:
            return set(json.load(f))
    return set()

def save_users(users: set):
    with open(user_db_file, "w") as f:
        json.dump(list(users), f)

all_users: set = load_users()

# ALL EMOJI IDs FROM ALL YOUR JSON FILES (COMPLETE)
PREMIUM_EMOJIS = [
    "6246537187614005254", "6246610665914505571", "6244496562752331516",
    "6246782404476803545", "6247039939305808563", "6246774261218810895", "6246871001062185760",
    "5780840497958360623", "5780413823022273797", "5782940582347281850", "5783091623462180025",
    "5783151611270403662", "5783124312458270318", "5782741660936966676", "5782753386197685582",
    "5782746664573867142", "5783029694328738752", "5782671841948603573", "5780425243340313827",
    "5783170625090622777", "5782858359493366808", "5783016603268420398", "5782914709464289647",
    "5782897082918507949", "5783023329187206172", "5782731481864475831", "5782734256413349701",
    "5783133172975801184", "5783157259152397008", "5783175250770399822", "5782876166427775766",
    "5782804668107199927", "5783176625159935132", "5782829832320586664", "5782670102486848559",
    "5782901906166780625", "5782624593013379610", "5782993191401689635", "5782906235493816255",
    "5782634454258291475", "5782942227319756256", "5782894188110550192", "5782624902251025820",
    "5783154622042477033", "5782681033178617588", "5783067966782313540", "5782703143670256526",
    "5780793884678296697", "5780872727392949996", "5782853918497183319", "5780561810415424892",
    "5783028968479265911", "5782789524052513567", "5783140294031579063", "5782756916660802905",
    "5782705411412989810", "5782726546947052658", "5783024321324651865", "5782654387201512502",
    "5782644650510652590", "5783168829794293068", "5782902640606188584", "5780764734735259441",
    "5782968864706925844", "5782759549475754469", "5783034045130610245", "5780636053220103355",
    "5782720108791076012", "5782982204875347021", "5780690182692935276", "5782882973950940285",
    "5782800987320226758", "5782867877140895194", "5782827367009359233", "5783166815454630601",
    "5780387756865754165", "5782709955488388577", "5780490638512362573", "5783010354091005955",
    "5783000136363807783", "5783155498215806741", "5783093496067921133", "5780604781563221320",
    "5782697689061789959", "5782833521697494295", "5783036501851902672", "5782903074397885294",
    "5782791181909889905", "5783066686882059394", "5782850997919420883", "5782845371512263981",
    "5783157611339716764", "5783182264451995387", "5782975345812575635", "5783120180699731847",
    "5782960949082199720", "5783048836997977147", "5782956898928040265", "5782934895810580859",
    "5783182062588531009", "5782653493848315448", "5782678507737847165", "5783019966227813296",
    "5782938795640887007", "5782925773300044662", "5782961266909779599", "5783156301374690720",
    "5783066953170032069", "5785100057543972225", "5785114462864283016", "5782719769488659459",
    "5785087322965939455", "5782848150356104237", "5785056124323500928", "5784947758003656516",
    "5785381777333819001", "5785334107491800107", "5785181606088020813", "5785325680765965100",
    "6084695058894819673", "6086730718774300509", "6086664791026307819", "6089003761496232797",
    "6089028758205897441", "6086639764251873025", "6086690887247597839", "6089118557382121313",
    "6089140105233044310", "6089364701957853465", "6089079808187174973", "6086784182527202100",
    "6086954744268460848", "6087133294648890399", "6089206028686070348", "6086924086791902713",
    "6086672466132865380", "6089313931149448495", "6089196601232854885", "6086741365998227951",
    "6087162775304409688", "6089104607328342288", "6086730808968614780", "6086745394677551464",
    "6089423023318766264", "6089418114171147667", "6086642762139047154", "6086954160152908450",
    "6089079919856325971", "6087128656084210204", "6089130055009571008", "6087130726258446488",
    "6086615841284035037", "6086890285399282868", "6086747705369957045", "6088900055215902751",
    "6086933162057798581", "6086946867298439895", "6089302652565328018", "6087111093962937579",
    "6089091696656650615", "6086817820711064076", "6089217174126203362", "6089376431513539276",
    "6087012932485386636", "6086804742535647234", "6089094625824346130", "6089032941504041241",
    "6086778246882399112", "6089331793918434895", "6086715939791835654", "6089218471206327014",
    "6086909445248390037", "6089415747644168497", "6089415193593385928", "6089211642208326407",
    "6089111655369675615", "6087154735125630953", "6089273086010462949", "6086820878727778414",
    "6089205092383200572", "6088971806939550947", "6089124398537642497", "6087079590377820415",
    "6089024570612781324", "6086688769828721421", "6089349454823952869", "6088901236331910211",
    "6089016925570995663", "6088964329401487918", "6086784745167917713", "6086816966012573204",
    "6086827754970419634", "6087060924449953862", "6089005604037203306", "6088971480522035863",
    "6086990448331592466", "6086928089701421862", "6086657790229614985", "6086668836885500499",
    "6089019283508040459", "6086708148721160702", "6093377734715642495", "6093865234978574850",
    "6096160920768090742", "6095843123252957701", "6096180729157260119", "6095876155846431752",
    "6093636111358235216", "6093513636070822132", "6093852921307337895", "6093818260921258328",
    "6093852083788715042", "6093386410549581063", "6093786598422353987", "6093866381734842452",
    "6095957657145840116", "6093421221259514937", "6096140450953957819", "6093651105089065114",
    "6095865895169560113", "6093382540784046658", "6093583734232061379", "6095891759462617671",
    "6093596992796102377", "6093406373557571574", "6093890429256732821", "6093780439439249308",
    "6093875388281263010", "6093864814071780526", "6093425709500339144", "6093835694193512831",
    "6093376514944929700", "6095627640448750533", "6093710452947161299", "6093467039970629408",
    "6093461323369157449", "6093422342245979247", "6093922327978840798", "6093744967304352336",
    "6093379246544130083", "6093639774965338848", "6096056720566522801", "6095687735631155103",
    "6093706475807445989", "6093584842333622858", "6093772622598771321", "6093666528316625608",
    "6093576514392037256", "6093715675627393878", "6093399334106173535", "6093661404420641058",
    "6096157154081771397", "6093779241143374561", "6093434664507150188", "6093701420630938474",
    "6095742874421301875", "6093577759932552635", "6093464720688288321", "6093612746736145083",
    "6093899809465307155", "6093451264555750089", "6093778090092139204", "6093587384954262033",
    "6095795620914664179", "6095851644468072524", "6093786581242482660", "6093456762113888541",
    "6096002964755847104", "6093522689861882360", "6093650241800638523", "6093493892106162082",
    "6095888417978061469", "6093833452220585982", "6096026428162183499", "6093376261541859430",
    "6093725459562893833", "6093930033150170743", "6096153219891728680", "6093748819890018226",
    "6093869083269271739", "6111707285040403058", "6111865438621142779",
    "6298332994260175589", "6296140830067395531", "6298821774423361023", "6136464120779638846",
    "6298514001361897127", "6298570484476806736", "6219532735359223977", "6222247670086371092",
    "6219796119933683821", "6296501388276926215", "6104973532234516855", "6104780447684757396",
    "6104631352190043951", "6105062639921006899", "6298652161869874841", "6298804341151107148",
    "6296428614351062569", "6298747815086524010", "6298670698948724690", "6296577138615125756",
    "6298356878573307709", "6296303781126604562", "6255593645848660539", "6296218646284863141",
    "6298398604180588232", "6255963511252322252", "6219549292458150316", "6298728453373953912",
    "6298675732650395252", "6298295868562867971", "6298555228752971886", "6298299463450494630",
    "6298506420744619882", "6298335558355651118", "6298544959486167081", "6255548424138000488",
    "6255696037868996493", "6255933686999418808", "6255963721705719771", "6298480869984175913",
    "6298566954013689358", "6298289748234471193", "6298649503285118920", "6220029508456548253",
    "6220014823963363136", "6222091698349017452", "6219810752887262728", "6219882697884436514",
    "6219727185708582935", "6296514655430903710", "6298684666182371615", "6298526366572742762",
    "6298428643181856596", "6298565175897229863", "6296099808834750711", "6298389060763256330",
    "6298513503145691368", "6255685257501083955", "6255902733170116708", "6298505110779594363",
    "6296465761523206072", "6296400014163838663", "6298426688971736948", "6298292943690139437",
    "6298298582982199311", "6296367896398399651", "6298671811345254603", "6296341890371422476",
    "6296508771325707891", "6298691319086712919", "6296504553667823627", "6298486951657867390",
    "6233101473350158283", "6233326134499477163", "6231107453178611892", "6233534139765622291",
    "6298548743352355181", "6298608963088812117", "6298307679722932538", "6298597328022407025",
    "6298510088646690703", "6298650293559101195", "6255793039705377676", "6255512604110751681",
    "6296376065426196025", "6255572871091849620", "6255716507683129387", "6256032707470428424",
    "6231051773222586793", "6232982631605077725", "6255890170390775841", "6255738287462288807",
    "6298599647304746497", "6255600234328491647", "6255796213686208481", "6255693594032605539",
    "6298493673281685123", "6256052494384760637", "6298790803414189709", "6298471863437756136",
    "6298788673110410889", "6170120369274358018", "6298367066235734104", "6298678524379137990",
    "6323472378441501262", "6298591254938650495", "6298333093044422573", "6298540449770506365",
    "6298429115628259446", "6298711741656205491", "6298323188849838091", "6298585787445282748",
    "6298711604217251794", "6298452746538321740", "6298817866003122559", "6201834820104882435",
    "6138853050309150669", "6136551252781172945", "6307598797790775195", "6325465088648022080",
    "6104827683735078900", "6104981434974341363", "6105006251295377689", "6104762898448386278",
    "6105135237753210602", "6104710113300318347", "6104758079495079914", "6296492755392661339",
    "6298510092941657856", "6298369007560951386", "6298544740442834681", "6296106560523339437",
    "6298352377447581711", "6298836772449159126", "6298784038840698888", "6298309109947041834",
    "6296148681267611229", "6296098408675411733", "6296241860583097973", "6298470622192207446",
    "6296372573617784564", "6296488662288828276", "6296135547257620282", "6219488394116859803",
    "6219525412439984045", "6222029992553875665", "6219618059179526172", "6219826747345471627",
    "6219909202127620214", "6221746649266391336", "6220028211376425519", "6222219718439209089",
    "6222084349659973777", "6255625608995276407", "6298692242504681257", "6298454498884978957",
    "6298394017155516458", "6298428222275061774", "6255705323588290387", "6298717844804733009",
    "6296372968754776071", "6298644001432012664", "6298535785436022911", "6298772747371677910",
    "6298522513987078458", "6298440608960742886", "6298412927896520857", "6298321174510175872",
    "6255966826967074621", "6298666743283845636", "6244241334320762892", "6102848541330249485",
    "6102617459204822706", "6102796683895117675", "6102775780289287243", "6102511979102999895",
    "6102555792064386359"
]

MAIN_EMOJI_ID = PREMIUM_EMOJIS[0]
PLACEHOLDER = "🌟"

temp_data = {}

def _utf16_len(ch: str) -> int:
    return len(ch.encode("utf-16-le")) // 2

def _utf16_len_str(s: str) -> int:
    return len(s.encode("utf-16-le")) // 2

def _build_pe_entities(text: str, use_main: bool = True):
    entities = []
    utf16_offset = 0
    total_utf16 = _utf16_len_str(text)
    
    if total_utf16 > 0:
        entities.append(MessageEntity(type="bold", offset=0, length=total_utf16))
    
    for ch in text:
        ch_len = _utf16_len(ch)
        if ch == PLACEHOLDER:
            eid = MAIN_EMOJI_ID if use_main else random.choice(PREMIUM_EMOJIS)
            entities.append(MessageEntity(
                type="custom_emoji",
                offset=utf16_offset,
                length=ch_len,
                custom_emoji_id=eid
            ))
        utf16_offset += ch_len
    
    return entities

def _send_pe(chat_id, text: str, use_main: bool = True, reply_markup=None):
    entities = _build_pe_entities(text, use_main)
    return bot.send_message(chat_id, text, entities=entities, reply_markup=reply_markup, parse_mode=None)

def _send_pe_return(chat_id, text: str, use_main: bool = True, reply_markup=None):
    entities = _build_pe_entities(text, use_main)
    return bot.send_message(chat_id, text, entities=entities, reply_markup=reply_markup, parse_mode=None)

def process_text_and_entities(text: str, original_entities: list):
    final_text = ""
    new_entities = []
    offset_map = {}
    old_off = 0
    new_off = 0
    
    for char in text:
        offset_map[old_off] = new_off
        old_ch_len = _utf16_len(char)
        
        if emoji.is_emoji(char):
            rand_id = random.choice(PREMIUM_EMOJIS)
            ph_len = _utf16_len(PLACEHOLDER)
            new_entities.append(MessageEntity(
                type="custom_emoji",
                offset=new_off,
                length=ph_len,
                custom_emoji_id=rand_id
            ))
            final_text += PLACEHOLDER
            old_off += old_ch_len
            new_off += ph_len
        else:
            final_text += char
            old_off += old_ch_len
            new_off += old_ch_len
    
    offset_map[old_off] = new_off
    
    for ent in (original_entities or []):
        if ent.type == "custom_emoji":
            continue
        ns = offset_map.get(ent.offset)
        ne = offset_map.get(ent.offset + ent.length)
        if ns is not None and ne is not None and ne > ns:
            new_entities.append(MessageEntity(
                type=ent.type,
                offset=ns,
                length=ne - ns,
                url=ent.url,
                user=ent.user,
                language=ent.language,
                custom_emoji_id=ent.custom_emoji_id
            ))
    
    if final_text:
        total_len = _utf16_len_str(final_text)
        new_entities.append(MessageEntity(type="bold", offset=0, length=total_len))
    
    return final_text, new_entities

# Force join channels - You can add more here
REQUIRED_CHANNELS = [
    {"id": "-1003533135835", "name": "𝐙𝐄𝐑𝐈𝐍〆𝐂𝐎𝐃𝐄𝐗", "link": "https://t.me/+-3wP_B7TNEYwNGU1"},
    {"id": "-1003360548513", "name": "𝐄𝐗𝐔 𝐂𝐎𝐃𝐄𝐑 ⚡", "link": "https://t.me/exucoder1"},
    {"id": "-1003669933791", "name": "𝐄𝐗𝐔〆𝐏𝐑𝐈𝐌𝐄", "link": "https://t.me/exucodex"},
    {"id": "-1003645019104", "name": "ᴡᴇʙꜱɪᴛᴇ〆ꜰɪʟᴇ", "link": "https://t.me/webfileexu"},
    {"id": "-1003564583501", "name": "𝐕𝐀𝐍𝐙𝐎〆𝐂𝐈𝐙𝐘", "link": "https://t.me/vanzocizy"},
]

def is_admin(user_id):
    return user_id in ADMIN_IDS

def check_joined(uid: int) -> list:
    # Admins bypass join check
    if is_admin(uid):
        return []
    
    not_joined = []
    for ch in REQUIRED_CHANNELS:
        try:
            member = bot.get_chat_member(ch["id"], uid)
            if member.status in ("left", "kicked", "banned"):
                not_joined.append(ch)
        except Exception:
            not_joined.append(ch)
    return not_joined

def send_join_notice(chat_id: int, not_joined: list):
    joined_count = len(REQUIRED_CHANNELS) - len(not_joined)
    total_count = len(REQUIRED_CHANNELS)
    
    markup = InlineKeyboardMarkup()
    for ch in not_joined:
        markup.add(InlineKeyboardButton(f"📢 {ch['name']}", url=ch["link"]))
    markup.add(InlineKeyboardButton("✅ 𝐈 𝐇𝐀𝐕𝐄 𝐉𝐎𝐈𝐍𝐄𝐃", callback_data="check_join"))
    markup.add(InlineKeyboardButton("🔴 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐎𝐖𝐍𝐄𝐑", url="tg://user?id=8379062893"))
    
    if joined_count == 0:
        text = f"""
╔═══《 🔒 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃! 》═══╗

🚫 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃!

📊 𝐏𝐑𝐎𝐆𝐑𝐄𝐒𝐒: {joined_count}/{total_count} 𝐉𝐎𝐈𝐍𝐄𝐃

⚠️ 𝐓𝐎 𝐔𝐒𝐄 𝐓𝐇𝐈𝐒 𝐁𝐎𝐓, 𝐘𝐎𝐔 𝐌𝐔𝐒𝐓 𝐉𝐎𝐈𝐍 𝐀𝐋𝐋 𝐂𝐇𝐀𝐍𝐍𝐄𝐋𝐒 𝐅𝐈𝐑𝐒𝐓!

👇 𝐂𝐋𝐈𝐂𝐊 𝐓𝐇𝐄 𝐁𝐔𝐓𝐓𝐎𝐍𝐒 𝐁𝐄𝐋𝐎𝐖 𝐓𝐎 𝐉𝐎𝐈𝐍: 👇

╰══════════════════════════════╝
"""
    else:
        status_text = ""
        for ch in REQUIRED_CHANNELS:
            if ch in not_joined:
                status_text += f"📢  ❌ {ch['name']}\n"
            else:
                status_text += f"📢  ✅ {ch['name']}\n"
        
        text = f"""
╔═══《 🔒 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃! 》═══╗

🚫 𝐀𝐂𝐂𝐄𝐒𝐒 𝐃𝐄𝐍𝐈𝐄𝐃!

📊 𝐏𝐑𝐎𝐆𝐑𝐄𝐒𝐒: {joined_count}/{total_count} 𝐉𝐎𝐈𝐍𝐄𝐃

⚠️ 𝐓𝐎 𝐔𝐒𝐄 𝐓𝐇𝐈𝐒 𝐁𝐎𝐓, 𝐘𝐎𝐔 𝐌𝐔𝐒𝐓 𝐉𝐎𝐈𝐍 𝐀𝐋𝐋 𝐂𝐇𝐀𝐍𝐍𝐄𝐋𝐒 𝐅𝐈𝐑𝐒𝐓!

{status_text}
👇 𝐂𝐋𝐈𝐂𝐊 𝐓𝐇𝐄 𝐁𝐔𝐓𝐓𝐎𝐍𝐒 𝐁𝐄𝐋𝐎𝐖 𝐓𝐎 𝐉𝐎𝐈𝐍: 👇

╰══════════════════════════════╝
"""
    
    entities = _build_pe_entities(text, use_main=False)
    bot.send_message(chat_id, text, entities=entities, reply_markup=markup, parse_mode=None)

def register_user(uid: int):
    if uid not in all_users:
        all_users.add(uid)
        save_users(all_users)

def get_colorful_menu(user_id):
    is_admin_user = is_admin(user_id)
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=False)
    
    if is_admin_user:
        markup.row("🔴 𝐁𝐎𝐓 𝐎𝐅𝐅", "🟢 𝐁𝐎𝐓 𝐎𝐍")
        markup.row("✍️ 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓", "📢 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓")
        markup.row("👥 𝐔𝐒𝐄𝐑𝐒 𝐋𝐈𝐒𝐓", "📊 𝐁𝐎𝐓 𝐒𝐓𝐀𝐓𝐒")
        markup.row("❓ 𝐇𝐄𝐋𝐏", "🌟 𝐀𝐁𝐎𝐔𝐓 𝐁𝐎𝐓")
    else:
        markup.row("✍️ 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓")
        markup.row("❓ 𝐇𝐄𝐋𝐏", "🌟 𝐀𝐁𝐎𝐔𝐓 𝐁𝐎𝐓")
        markup.row("📊 𝐒𝐓𝐀𝐓𝐒")
    
    return markup

def send_welcome_message(chat_id: int, user_name: str, user_id: int):
    status = "𝐀𝐝𝐦𝐢𝐧𝐢𝐬𝐭𝐫𝐚𝐭𝐨𝐫" if is_admin(user_id) else "𝐔𝐬𝐞𝐫"
    
    text = f"""
╔═══《 🎉 𝐆𝐨𝐨𝐝 𝐀𝐟𝐭𝐞𝐫𝐧𝐨𝐨𝐧! 》═══╗

👤 𝐔𝐬𝐞𝐫: {user_name}
🆔 𝐔𝐬𝐞𝐫 𝐈𝐃: {user_id}
🌟 𝐒𝐭𝐚𝐭𝐮𝐬: {status}

╰═══════《 🤖 》═══════╝

𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐏𝐑𝐄𝐌𝐈𝐔𝐌 𝐄𝐌𝐎𝐉𝐈 𝐁𝐎𝐓

📌 𝐀𝐛𝐨𝐮𝐭 𝐓𝐡𝐢𝐬 𝐁𝐨𝐭:
• 🔥 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐀𝐧𝐢𝐦𝐚𝐭𝐞𝐝 𝐄𝐦𝐨𝐣𝐢 𝐂𝐨𝐧𝐯𝐞𝐫𝐭𝐞𝐫
• ✨ 𝐂𝐨𝐧𝐯𝐞𝐫𝐭 𝐚𝐧𝐲 𝐞𝐦𝐨𝐣𝐢 𝐭𝐨 𝐩𝐫𝐞𝐦𝐢𝐮𝐦
• 🎨 𝐏𝐫𝐞𝐬𝐞𝐫𝐯𝐞𝐬 𝐚𝐥𝐥 𝐟𝐨𝐫𝐦𝐚𝐭𝐭𝐢𝐧𝐠
• 📝 𝐒𝐮𝐩𝐩𝐨𝐫𝐭𝐬 𝐭𝐞𝐱𝐭, 𝐩𝐡𝐨𝐭𝐨, 𝐯𝐢𝐝𝐞𝐨, 𝐝𝐨𝐜𝐮𝐦𝐞𝐧𝐭
• 🔗 𝐀𝐝𝐝 𝐦𝐮𝐥𝐭𝐢𝐩𝐥𝐞 𝐢𝐧𝐥𝐢𝐧𝐞 𝐛𝐮𝐭𝐭𝐨𝐧𝐬

━━━━━━━━━━━━━━━━━━━━━━

✅ 𝐀𝐜𝐜𝐞𝐬𝐬 𝐆𝐫𝐚𝐧𝐭𝐞𝐝!
𝐘𝐨𝐮 𝐡𝐚𝐯𝐞 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲 𝐣𝐨𝐢𝐧𝐞𝐝 𝐚𝐥𝐥 𝐜𝐡𝐚𝐧𝐧𝐞𝐥𝐬.

📌 𝐐𝐮𝐢𝐜𝐤 𝐆𝐮𝐢𝐝𝐞:
• 𝐔𝐬𝐞 𝐦𝐞𝐧𝐮 𝐛𝐮𝐭𝐭𝐨𝐧𝐬 𝐭𝐨 𝐧𝐚𝐯𝐢𝐠𝐚𝐭𝐞
• /𝐡𝐞𝐥𝐩 𝐟𝐨𝐫 𝐦𝐨𝐫𝐞 𝐢𝐧𝐟𝐨𝐫𝐦𝐚𝐭𝐢𝐨𝐧
• ✍️ 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓 𝐭𝐨 𝐜𝐫𝐞𝐚𝐭𝐞

⚠️ 𝐍𝐨𝐭𝐞: 𝐈𝐟 𝐲𝐨𝐮 𝐥𝐞𝐚𝐯𝐞 𝐚𝐧𝐲 𝐜𝐡𝐚𝐧𝐧𝐞𝐥, 𝐲𝐨𝐮 𝐰𝐢𝐥𝐥 𝐥𝐨𝐬𝐞 𝐚𝐜𝐜𝐞𝐬𝐬!

━━━━━━━━━━━━━━━━━━━━━━
"""

    return text

@bot.message_handler(commands=["start"])
def welcome(message):
    uid = message.from_user.id
    
    # Admins bypass join check
    if not is_admin(uid):
        not_joined = check_joined(uid)
        if not_joined:
            send_join_notice(message.chat.id, not_joined)
            return
    
    register_user(uid)
    
    if not bot_active and not is_admin(uid):
        text = f"""
╔═══《 🔴 𝐁𝐎𝐓 𝐎𝐅𝐅𝐋𝐈𝐍𝐄 》═══╗

𝐓𝐡𝐞 𝐛𝐨𝐭 𝐢𝐬 𝐜𝐮𝐫𝐫𝐞𝐧𝐭𝐥𝐲 𝐨𝐟𝐟𝐥𝐢𝐧𝐞
𝐟𝐨𝐫 𝐦𝐚𝐢𝐧𝐭𝐞𝐧𝐚𝐧𝐜𝐞.

╰══════════════════════════════╝
"""
        _send_pe(message.chat.id, text, use_main=False)
        return
    
    name = message.from_user.first_name or "Friend"
    kb = get_colorful_menu(uid)
    text = send_welcome_message(message.chat.id, name, uid)
    _send_pe(message.chat.id, text, use_main=False, reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "❓ HELP")
def help_msg(message):
    uid = message.from_user.id
    
    if not bot_active and not is_admin(uid):
        return
    
    kb = get_colorful_menu(uid)
    
    text = f"""
╔═══《 ❓ 𝐇𝐎𝐖 𝐓𝐎 𝐔𝐒𝐄 》═══╗

𝐒𝐓𝐄𝐏 𝟏: 𝐓𝐚𝐩 ✍️ 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓

𝐒𝐓𝐄𝐏 𝟐: 𝐒𝐞𝐧𝐝 𝐲𝐨𝐮𝐫 𝐭𝐞𝐱𝐭 𝐦𝐞𝐬𝐬𝐚𝐠𝐞

𝐒𝐓𝐄𝐏 𝟑: 𝐂𝐡𝐨𝐨𝐬𝐞 𝐦𝐞𝐝𝐢𝐚 (𝐕𝐢𝐝𝐞𝐨/𝐈𝐦𝐚𝐠𝐞/𝐃𝐨𝐜𝐮𝐦𝐞𝐧𝐭/𝐒𝐤𝐢𝐩)

𝐒𝐓𝐄𝐏 𝟒: 𝐂𝐡𝐨𝐨𝐬𝐞 𝐡𝐨𝐰 𝐦𝐚𝐧𝐲 𝐛𝐮𝐭𝐭𝐨𝐧𝐬 (𝟏-𝟒)

𝐒𝐓𝐄𝐏 𝟓: 𝐄𝐧𝐭𝐞𝐫 𝐛𝐮𝐭𝐭𝐨𝐧 𝐧𝐚𝐦𝐞𝐬 𝐚𝐧𝐝 𝐥𝐢𝐧𝐤𝐬

𝐒𝐓𝐄𝐏 𝟔: 𝐘𝐨𝐮𝐫 𝐩𝐨𝐬𝐭 𝐰𝐢𝐥𝐥 𝐛𝐞 𝐜𝐫𝐞𝐚𝐭𝐞𝐝!

╰══════════════════════════════╝
"""
    
    _send_pe(message.chat.id, text, use_main=False, reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "🌟 𝐀𝐁𝐎𝐔𝐓 𝐁𝐎𝐓")
def about_bot(message):
    uid = message.from_user.id
    
    if not bot_active and not is_admin(uid):
        return
    
    kb = get_colorful_menu(uid)
    total = len(all_users)
    
    text = f"""
╔═══《 🔥 𝐀𝐁𝐎𝐔𝐓 𝐁𝐎𝐓 》═══╗

𝐓𝐡𝐢𝐬 𝐛𝐨𝐭 𝐜𝐨𝐧𝐯𝐞𝐫𝐭𝐬 𝐧𝐨𝐫𝐦𝐚𝐥 𝐞𝐦𝐨𝐣𝐢𝐬 𝐭𝐨
𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐏𝐫𝐞𝐦𝐢𝐮𝐦 𝐀𝐧𝐢𝐦𝐚𝐭𝐞𝐝 𝐄𝐦𝐨𝐣𝐢𝐬

📊 𝐒𝐭𝐚𝐭𝐢𝐬𝐭𝐢𝐜𝐬:
• 𝐓𝐨𝐭𝐚𝐥 𝐔𝐬𝐞𝐫𝐬: {total}
• 𝐄𝐦𝐨𝐣𝐢 𝐏𝐨𝐨𝐥: {len(PREMIUM_EMOJIS)}
• 𝐕𝐞𝐫𝐬𝐢𝐨𝐧: 4.0

╰══════════════════════════════╝
"""
    
    _send_pe(message.chat.id, text, use_main=False, reply_markup=kb)

@bot.message_handler(func=lambda m: m.text in ("📊 𝐒𝐓𝐀𝐓𝐒", "📊 𝐁𝐎𝐓 𝐒𝐓𝐀𝐓𝐒"))
def stats_msg(message):
    uid = message.from_user.id
    
    if not bot_active and not is_admin(uid):
        return
    
    kb = get_colorful_menu(uid)
    total = len(all_users)
    status = "🟢 𝐎𝐍𝐋𝐈𝐍𝐄" if bot_active else "🔴 𝐎𝐅𝐅𝐋𝐈𝐍𝐄"
    
    text = f"""
╔═══《 📊 𝐒𝐓𝐀𝐓𝐈𝐒𝐓𝐈𝐂𝐒 》═══╗

𝐁𝐨𝐭 𝐒𝐭𝐚𝐭𝐮𝐬: {status}
𝐓𝐨𝐭𝐚𝐥 𝐔𝐬𝐞𝐫𝐬: {total}
𝐄𝐦𝐨𝐣𝐢 𝐏𝐨𝐨𝐥: {len(PREMIUM_EMOJIS)}

╰══════════════════════════════╝
"""
    
    _send_pe(message.chat.id, text, use_main=False, reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "✍️ 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓")
def start_post(message):
    uid = message.from_user.id
    register_user(uid)
    
    if not bot_active and not is_admin(uid):
        text = "𝐁𝐨𝐭 𝐢𝐬 𝐨𝐟𝐟𝐥𝐢𝐧𝐞. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐭𝐫𝐲 𝐚𝐠𝐚𝐢𝐧 𝐥𝐚𝐭𝐞𝐫."
        _send_pe(message.chat.id, text, use_main=False)
        return
    
    temp_data[uid] = {
        "original_text": "",
        "original_entities": [],
        "media_type": None,
        "media_id": None,
        "media_name": None,
        "buttons": [],
        "button_count": 0,
        "current_button": 0,
        "processed_text": "",
        "processed_entities": [],
        "preview_msg_id": None,
        "action_msg_id": None,
    }
    
    text = f"""
╔═══《 ✍️ 𝐂𝐑𝐄𝐀𝐓𝐄 𝐏𝐎𝐒𝐓 》═══╗

𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝 𝐲𝐨𝐮𝐫 𝐭𝐞𝐱𝐭 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐧𝐨𝐰.

𝐒𝐮𝐩𝐩𝐨𝐫𝐭𝐬 𝐟𝐨𝐫𝐦𝐚𝐭𝐭𝐢𝐧𝐠: 𝐁𝐨𝐥𝐝, 𝐈𝐭𝐚𝐥𝐢𝐜, 𝐋𝐢𝐧𝐤𝐬

𝐀𝐥𝐥 𝐧𝐨𝐫𝐦𝐚𝐥 𝐞𝐦𝐨𝐣𝐢𝐬 𝐰𝐢𝐥𝐥 𝐛𝐞 𝐜𝐨𝐧𝐯𝐞𝐫𝐭𝐞𝐝!

╰══════════════════════════════╝
"""
    
    sent = _send_pe_return(message.chat.id, text, use_main=False)
    bot.register_next_step_handler(sent, process_post_text)

def process_post_text(message):
    uid = message.from_user.id
    
    if message.text and message.text.strip() == "/cancel":
        kb = get_colorful_menu(uid)
        _send_pe(message.chat.id, "𝐂𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝!", reply_markup=kb)
        temp_data.pop(uid, None)
        return
    
    if uid not in temp_data:
        _send_pe(message.chat.id, "𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐞𝐱𝐩𝐢𝐫𝐞𝐝! 𝐏𝐥𝐞𝐚𝐬𝐞 /𝐬𝐭𝐚𝐫𝐭 𝐚𝐠𝐚𝐢𝐧.")
        return
    
    temp_data[uid]["original_text"] = message.text or ""
    temp_data[uid]["original_entities"] = message.entities or []
    
    ask_media_type(message.chat.id, uid)

def ask_media_type(chat_id: int, uid: int):
    text = f"""
╔═══《 📎 𝐀𝐃𝐃 𝐌𝐄𝐃𝐈𝐀 》═══╗

𝐃𝐨 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐚𝐝𝐝 𝐦𝐞𝐝𝐢𝐚?

╰══════════════════════════════╝
"""

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🎬 𝐕𝐈𝐃𝐄𝐎", callback_data=f"media_video_{uid}"),
        InlineKeyboardButton("🖼️ 𝐈𝐌𝐀𝐆𝐄", callback_data=f"media_image_{uid}"),
        InlineKeyboardButton("📄 𝐃𝐎𝐂𝐔𝐌𝐄𝐍𝐓", callback_data=f"media_doc_{uid}"),
        InlineKeyboardButton("⏭️ 𝐒𝐊𝐈𝐏", callback_data=f"media_skip_{uid}"),
    )
    markup.add(InlineKeyboardButton("🔴 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐎𝐖𝐍𝐄𝐑", url="tg://user?id=8379062893"))
    
    entities = _build_pe_entities(text, use_main=False)
    bot.send_message(chat_id, text, entities=entities, reply_markup=markup, parse_mode=None)

@bot.callback_query_handler(func=lambda c: c.data.startswith("media_"))
def handle_media_selection(call):
    parts = call.data.split("_")
    action = parts[1]
    uid = int(parts[2]) if len(parts) > 2 else call.from_user.id
    chat_id = call.message.chat.id
    
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    if uid not in temp_data:
        bot.answer_callback_query(call.id, "Session expired!")
        return
    
    if action == "skip":
        temp_data[uid]["media_type"] = None
        ask_button_amount(chat_id, uid)
    
    elif action in ["video", "image", "doc"]:
        temp_data[uid]["media_type"] = action
        media_text = {"video": "𝐕𝐢𝐝𝐞𝐨", "image": "𝐈𝐦𝐚𝐠𝐞", "doc": "𝐃𝐨𝐜𝐮𝐦𝐞𝐧𝐭"}[action]
        
        text = f"""
╔═══《 📤 𝐒𝐄𝐍𝐃 {media_text} 》═══╗

𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝 𝐲𝐨𝐮𝐫 {media_text} 𝐧𝐨𝐰.

╰══════════════════════════════╝
"""
        
        sent = _send_pe_return(chat_id, text, use_main=False)
        bot.register_next_step_handler(sent, receive_media, action)
    
    bot.answer_callback_query(call.id)

def receive_media(message, media_type):
    uid = message.from_user.id
    
    if message.text and message.text.strip() == "/cancel":
        kb = get_colorful_menu(uid)
        _send_pe(message.chat.id, "𝐂𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝!", reply_markup=kb)
        temp_data.pop(uid, None)
        return
    
    if uid not in temp_data:
        _send_pe(message.chat.id, "𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐞𝐱𝐩𝐢𝐫𝐞𝐝!")
        return
    
    if media_type == "video" and message.video:
        temp_data[uid]["media_id"] = message.video.file_id
        if message.caption:
            temp_data[uid]["original_text"] = message.caption
            temp_data[uid]["original_entities"] = message.caption_entities or []
    elif media_type == "image" and message.photo:
        temp_data[uid]["media_id"] = message.photo[-1].file_id
        if message.caption:
            temp_data[uid]["original_text"] = message.caption
            temp_data[uid]["original_entities"] = message.caption_entities or []
    elif media_type == "doc" and message.document:
        temp_data[uid]["media_id"] = message.document.file_id
        if message.caption:
            temp_data[uid]["original_text"] = message.caption
            temp_data[uid]["original_entities"] = message.caption_entities or []
    else:
        text = f"𝐏𝐥𝐞𝐚𝐬𝐞 𝐬𝐞𝐧𝐝 𝐚 𝐯𝐚𝐥𝐢𝐝 {media_type.upper()}!"
        sent = _send_pe_return(message.chat.id, text, use_main=False)
        bot.register_next_step_handler(sent, receive_media, media_type)
        return
    
    ask_button_amount(message.chat.id, uid)

def ask_button_amount(chat_id: int, uid: int):
    text = f"""
╔═══《 🔘 𝐀𝐃𝐃 𝐁𝐔𝐓𝐓𝐎𝐍𝐒 》═══╗

𝐃𝐨 𝐲𝐨𝐮 𝐰𝐚𝐧𝐭 𝐭𝐨 𝐚𝐝𝐝 𝐢𝐧𝐥𝐢𝐧𝐞 𝐛𝐮𝐭𝐭𝐨𝐧𝐬?

𝐒𝐞𝐥𝐞𝐜𝐭 𝐡𝐨𝐰 𝐦𝐚𝐧𝐲:

╰══════════════════════════════╝
"""

    markup = InlineKeyboardMarkup(row_width=4)
    markup.add(
        InlineKeyboardButton("1", callback_data=f"btn_amt_1_{uid}"),
        InlineKeyboardButton("2", callback_data=f"btn_amt_2_{uid}"),
        InlineKeyboardButton("3", callback_data=f"btn_amt_3_{uid}"),
        InlineKeyboardButton("4", callback_data=f"btn_amt_4_{uid}"),
        InlineKeyboardButton("⏭️ 𝐍𝐎 𝐁𝐔𝐓𝐓𝐎𝐍𝐒", callback_data=f"btn_amt_0_{uid}"),
    )
    markup.add(InlineKeyboardButton("🔴 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐎𝐖𝐍𝐄𝐑", url="tg://user?id=8379062893"))
    
    entities = _build_pe_entities(text, use_main=False)
    bot.send_message(chat_id, text, entities=entities, reply_markup=markup, parse_mode=None)

@bot.callback_query_handler(func=lambda c: c.data.startswith("btn_amt_"))
def handle_button_amount(call):
    parts = call.data.split("_")
    amount = int(parts[2])
    uid = int(parts[3]) if len(parts) > 3 else call.from_user.id
    chat_id = call.message.chat.id
    
    try:
        bot.delete_message(chat_id, call.message.message_id)
    except:
        pass
    
    if uid not in temp_data:
        bot.answer_callback_query(call.id, "Session expired!")
        return
    
    if amount == 0:
        temp_data[uid]["button_count"] = 0
        temp_data[uid]["buttons"] = []
        create_preview(chat_id, uid)
    else:
        temp_data[uid]["button_count"] = amount
        temp_data[uid]["buttons"] = []
        temp_data[uid]["current_button"] = 1
        ask_button_name(chat_id, uid)
    
    bot.answer_callback_query(call.id)

def ask_button_name(chat_id, uid):
    current = temp_data[uid]["current_button"]
    total = temp_data[uid]["button_count"]
    
    text = f"""
╔═══《 🔘 𝐁𝐔𝐓𝐓𝐎𝐍 {current}/{total} 》═══╗

𝐄𝐧𝐭𝐞𝐫 𝐭𝐡𝐞 𝐛𝐮𝐭𝐭𝐨𝐧 𝐧𝐚𝐦𝐞/𝐥𝐚𝐛𝐞𝐥

╰══════════════════════════════╝
"""
    
    sent = _send_pe_return(chat_id, text, use_main=False)
    bot.register_next_step_handler(sent, save_button_name)

def save_button_name(message):
    uid = message.from_user.id
    chat_id = message.chat.id
    
    if message.text and message.text.strip() == "/cancel":
        kb = get_colorful_menu(uid)
        _send_pe(chat_id, "𝐂𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝!", reply_markup=kb)
        temp_data.pop(uid, None)
        return
    
    if uid not in temp_data:
        _send_pe(chat_id, "𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐞𝐱𝐩𝐢𝐫𝐞𝐝!")
        return
    
    button_name = (message.text or "").strip()[:30]
    if not button_name:
        text = "𝐁𝐮𝐭𝐭𝐨𝐧 𝐧𝐚𝐦𝐞 𝐜𝐚𝐧𝐧𝐨𝐭 𝐛𝐞 𝐞𝐦𝐩𝐭𝐲! 𝐓𝐫𝐲 𝐚𝐠𝐚𝐢𝐧:"
        sent = _send_pe_return(chat_id, text, use_main=False)
        bot.register_next_step_handler(sent, save_button_name)
        return
    
    temp_data[uid]["buttons"].append({"name": button_name, "url": ""})
    ask_button_url(chat_id, uid)

def ask_button_url(chat_id, uid):
    current = temp_data[uid]["current_button"]
    total = temp_data[uid]["button_count"]
    
    text = f"""
╔═══《 🔗 𝐁𝐔𝐓𝐓𝐎𝐍 {current}/{total} 》═══╗

𝐄𝐧𝐭𝐞𝐫 𝐭𝐡𝐞 𝐛𝐮𝐭𝐭𝐨𝐧 𝐔𝐑𝐋/𝐋𝐢𝐧𝐤
(𝐌𝐮𝐬𝐭 𝐬𝐭𝐚𝐫𝐭 𝐰𝐢𝐭𝐡 https://)

╰══════════════════════════════╝
"""
    
    sent = _send_pe_return(chat_id, text, use_main=False)
    bot.register_next_step_handler(sent, save_button_url)

def save_button_url(message):
    uid = message.from_user.id
    chat_id = message.chat.id
    
    if message.text and message.text.strip() == "/cancel":
        kb = get_colorful_menu(uid)
        _send_pe(chat_id, "𝐂𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝!", reply_markup=kb)
        temp_data.pop(uid, None)
        return
    
    if uid not in temp_data:
        _send_pe(chat_id, "𝐒𝐞𝐬𝐬𝐢𝐨𝐧 𝐞𝐱𝐩𝐢𝐫𝐞𝐝!")
        return
    
    url = (message.text or "").strip()
    valid_prefixes = ("http://", "https://", "tg://")
    if not any(url.startswith(p) for p in valid_prefixes):
        text = "𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐔𝐑𝐋! 𝐓𝐫𝐲 𝐚𝐠𝐚𝐢𝐧:"
        sent = _send_pe_return(chat_id, text, use_main=False)
        bot.register_next_step_handler(sent, save_button_url)
        return
    
    idx = temp_data[uid]["current_button"] - 1
    temp_data[uid]["buttons"][idx]["url"] = url
    
    if temp_data[uid]["current_button"] < temp_data[uid]["button_count"]:
        temp_data[uid]["current_button"] += 1
        ask_button_name(chat_id, uid)
    else:
        create_preview(chat_id, uid)

def create_preview(chat_id, uid):
    data = temp_data.get(uid)
    if not data:
        return
    
    processed_text, processed_entities = process_text_and_entities(
        data["original_text"],
        data["original_entities"]
    )
    data["processed_text"] = processed_text
    data["processed_entities"] = processed_entities
    
    reply_markup = None
    if data["buttons"]:
        keyboard = []
        for btn in data["buttons"]:
            keyboard.append([InlineKeyboardButton(btn["name"], url=btn["url"])])
        reply_markup = InlineKeyboardMarkup(keyboard)
        reply_markup.add(InlineKeyboardButton("🔴 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐎𝐖𝐍𝐄𝐑", url="tg://user?id=8379062893"))
    
    try:
        if data["media_type"] == "image" and data.get("media_id"):
            preview = bot.send_photo(chat_id, data["media_id"], caption=processed_text or None, caption_entities=processed_entities or None, reply_markup=reply_markup)
        elif data["media_type"] == "video" and data.get("media_id"):
            preview = bot.send_video(chat_id, data["media_id"], caption=processed_text or None, caption_entities=processed_entities or None, reply_markup=reply_markup)
        elif data["media_type"] == "doc" and data.get("media_id"):
            preview = bot.send_document(chat_id, data["media_id"], caption=processed_text or None, caption_entities=processed_entities or None, reply_markup=reply_markup)
        else:
            preview = bot.send_message(chat_id, processed_text if processed_text else "📝 𝐘𝐨𝐮𝐫 𝐩𝐨𝐬𝐭", entities=processed_entities or None, reply_markup=reply_markup)
        
        data["preview_msg_id"] = preview.message_id
        
    except Exception as e:
        _send_pe(chat_id, f"❌ 𝐄𝐫𝐫𝐨𝐫: {e}", use_main=False)
        return
    
    action_markup = InlineKeyboardMarkup(row_width=2)
    action_markup.add(
        InlineKeyboardButton("🔄 𝐑𝐄𝐅𝐑𝐄𝐒𝐇", callback_data=f"refresh_{uid}"),
        InlineKeyboardButton("🗑 𝐃𝐄𝐋𝐄𝐓𝐄", callback_data=f"delete_{uid}"),
        InlineKeyboardButton("✅ 𝐃𝐎𝐍𝐄", callback_data=f"done_{uid}"),
    )
    action_markup.add(InlineKeyboardButton("🔴 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐎𝐖𝐍𝐄𝐑", url="tg://user?id=8379062893"))
    
    action_text = f"""
╔═══《 ✨ 𝐏𝐑𝐄𝐕𝐈𝐄𝐖 𝐑𝐄𝐀𝐃𝐘 》═══╗

𝐘𝐨𝐮𝐫 𝐩𝐨𝐬𝐭 𝐢𝐬 𝐫𝐞𝐚𝐝𝐲!

🔄 𝐑𝐄𝐅𝐑𝐄𝐒𝐇 - 𝐍𝐞𝐰 𝐞𝐦𝐨𝐣𝐢𝐬
🗑 𝐃𝐄𝐋𝐄𝐓𝐄 - 𝐑𝐞𝐦𝐨𝐯𝐞 𝐩𝐫𝐞𝐯𝐢𝐞𝐰
✅ 𝐃𝐎𝐍𝐄 - 𝐅𝐢𝐧𝐢𝐬𝐡

╰══════════════════════════════╝
"""
    
    entities = _build_pe_entities(action_text, use_main=False)
    action_msg = bot.send_message(chat_id, action_text, entities=entities, reply_markup=action_markup, parse_mode=None)
    data["action_msg_id"] = action_msg.message_id
    temp_data[uid] = data

@bot.callback_query_handler(func=lambda c: c.data.startswith(("refresh_", "delete_", "done_")))
def handle_preview_actions(call):
    parts = call.data.split("_")
    action = parts[0]
    uid = int(parts[1]) if len(parts) > 1 else call.from_user.id
    chat_id = call.message.chat.id
    
    if uid not in temp_data:
        bot.answer_callback_query(call.id, "Session expired!")
        return
    
    data = temp_data[uid]
    
    if action == "refresh":
        bot.answer_callback_query(call.id, "Refreshing emojis...")
        if data.get("preview_msg_id"):
            try: bot.delete_message(chat_id, data["preview_msg_id"])
            except: pass
        if data.get("action_msg_id"):
            try: bot.delete_message(chat_id, data["action_msg_id"])
            except: pass
        processed_text, processed_entities = process_text_and_entities(data["original_text"], data["original_entities"])
        data["processed_text"] = processed_text
        data["processed_entities"] = processed_entities
        create_preview(chat_id, uid)
        
    elif action == "delete":
        bot.answer_callback_query(call.id, "Deleted!")
        if data.get("preview_msg_id"):
            try: bot.delete_message(chat_id, data["preview_msg_id"])
            except: pass
        if data.get("action_msg_id"):
            try: bot.delete_message(chat_id, data["action_msg_id"])
            except: pass
        temp_data.pop(uid, None)
        
    elif action == "done":
        bot.answer_callback_query(call.id, "Post created!")
        if data.get("action_msg_id"):
            try: bot.delete_message(chat_id, data["action_msg_id"])
            except: pass
        temp_data.pop(uid, None)
        kb = get_colorful_menu(uid)
        text = f"""
╔═══《 ✅ 𝐏𝐎𝐒𝐓 𝐂𝐑𝐄𝐀𝐓𝐄𝐃! 》═══╗

𝐘𝐨𝐮𝐫 𝐩𝐫𝐞𝐦𝐢𝐮𝐦 𝐞𝐦𝐨𝐣𝐢 𝐩𝐨𝐬𝐭 𝐢𝐬 𝐫𝐞𝐚𝐝𝐲!

𝐓𝐚𝐩 ✍️ 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓 𝐭𝐨 𝐜𝐫𝐞𝐚𝐭𝐞 𝐚𝐧𝐨𝐭𝐡𝐞𝐫

╰══════════════════════════════╝
"""
        _send_pe(chat_id, text, use_main=False, reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data == "check_join")
def handle_check_join(call):
    uid = call.from_user.id
    chat_id = call.message.chat.id
    
    not_joined = check_joined(uid)
    
    if not_joined:
        try: bot.delete_message(chat_id, call.message.message_id)
        except: pass
        send_join_notice(chat_id, not_joined)
    else:
        try: bot.delete_message(chat_id, call.message.message_id)
        except: pass
        register_user(uid)
        name = call.from_user.first_name or "Friend"
        kb = get_colorful_menu(uid)
        text = send_welcome_message(chat_id, name, uid)
        _send_pe(chat_id, text, use_main=False, reply_markup=kb)
    
    bot.answer_callback_query(call.id)

# Admin Commands
@bot.message_handler(func=lambda m: m.text == "🔴 𝐁𝐎𝐓 𝐎𝐅𝐅" and is_admin(m.from_user.id))
def bot_off(message):
    global bot_active
    bot_active = False
    text = f"""
╔═══《 🔴 𝐁𝐎𝐓 𝐎𝐅𝐅𝐋𝐈𝐍𝐄 》═══╗

𝐁𝐨𝐭 𝐢𝐬 𝐧𝐨𝐰 𝐎𝐅𝐅𝐋𝐈𝐍𝐄.

╰══════════════════════════════╝
"""
    _send_pe(message.chat.id, text, use_main=False, reply_markup=get_colorful_menu(message.from_user.id))

@bot.message_handler(func=lambda m: m.text == "🟢 𝐁𝐎𝐓 𝐎𝐍" and is_admin(m.from_user.id))
def bot_on(message):
    global bot_active
    bot_active = True
    text = f"""
╔═══《 🟢 𝐁𝐎𝐓 𝐎𝐍𝐋𝐈𝐍𝐄 》═══╗

𝐁𝐨𝐭 𝐢𝐬 𝐧𝐨𝐰 𝐎𝐍𝐋𝐈𝐍𝐄!

╰══════════════════════════════╝
"""
    _send_pe(message.chat.id, text, use_main=False, reply_markup=get_colorful_menu(message.from_user.id))

@bot.message_handler(func=lambda m: m.text == "👥 𝐔𝐒𝐄𝐑𝐒 𝐋𝐈𝐒𝐓" and is_admin(m.from_user.id))
def users_list(message):
    total = len(all_users)
    user_list = list(all_users)
    
    text = f"""
╔═══《 👥 𝐑𝐄𝐆𝐈𝐒𝐓𝐄𝐑𝐄𝐃 𝐔𝐒𝐄𝐑𝐒 》═══╗

𝐓𝐨𝐭𝐚𝐥: {total} 𝐮𝐬𝐞𝐫𝐬

╰══════════════════════════════╝
"""
    _send_pe(message.chat.id, text, use_main=False, reply_markup=get_colorful_menu(message.from_user.id))
    
    if user_list:
        for i in range(0, len(user_list), 50):
            batch = user_list[i:i+50]
            batch_text = "\n".join([f"• {uid}" for uid in batch])
            bot.send_message(message.chat.id, batch_text)

@bot.message_handler(func=lambda m: m.text == "📢 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓" and is_admin(m.from_user.id))
def broadcast_start(message):
    text = f"""
╔═══《 📢 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓 》═══╗

𝐒𝐞𝐧𝐝 𝐲𝐨𝐮𝐫 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐧𝐨𝐰.

╰══════════════════════════════╝
"""
    sent = _send_pe_return(message.chat.id, text, use_main=False)
    bot.register_next_step_handler(sent, do_broadcast)

def do_broadcast(message):
    if message.text and message.text.strip() == "/cancel":
        _send_pe(message.chat.id, "𝐂𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝!", reply_markup=get_colorful_menu(message.from_user.id))
        return
    
    success = 0
    failed = 0
    total = len(all_users)
    status_msg = bot.send_message(message.chat.id, f"📢 𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭𝐢𝐧𝐠 𝐭𝐨 {total} 𝐮𝐬𝐞𝐫𝐬...")
    
    for uid in list(all_users):
        try:
            bot.copy_message(uid, message.chat.id, message.message_id)
            success += 1
            time.sleep(0.05)
        except Exception:
            failed += 1
    
    try:
        bot.delete_message(message.chat.id, status_msg.message_id)
    except:
        pass
    
    text = f"""
╔═══《 ✅ 𝐁𝐑𝐎𝐀𝐃𝐂𝐀𝐒𝐓 𝐃𝐎𝐍𝐄! 》═══╗

𝐒𝐮𝐜𝐜𝐞𝐬𝐬: {success} ✅
𝐅𝐚𝐢𝐥𝐞𝐝: {failed} ❌

╰══════════════════════════════╝
"""
    _send_pe(message.chat.id, text, use_main=False, reply_markup=get_colorful_menu(message.from_user.id))

@bot.message_handler(func=lambda m: True)
def fallback(message):
    uid = message.from_user.id
    
    if not is_admin(uid):
        not_joined = check_joined(uid)
        if not_joined:
            send_join_notice(message.chat.id, not_joined)
            return
    
    register_user(uid)
    
    if not bot_active and not is_admin(uid):
        text = "𝐁𝐨𝐭 𝐢𝐬 𝐨𝐟𝐟𝐥𝐢𝐧𝐞."
        _send_pe(message.chat.id, text, use_main=False)
        return
    
    kb = get_colorful_menu(uid)
    text = f"""
╔═══《 📌 𝐌𝐄𝐍𝐔 》═══╗

𝐏𝐥𝐞𝐚𝐬𝐞 𝐜𝐡𝐨𝐨𝐬𝐞 𝐟𝐫𝐨𝐦 𝐭𝐡𝐞 𝐦𝐞𝐧𝐮:

✍️ 𝐌𝐀𝐊𝐄 𝐏𝐎𝐒𝐓
❓ 𝐇𝐄𝐋𝐏
🌟 𝐀𝐁𝐎𝐔𝐓 𝐁𝐎𝐓
📊 𝐒𝐓𝐀𝐓𝐒

╰══════════════════════════════╝
"""
    _send_pe(message.chat.id, text, use_main=False, reply_markup=kb)

@bot.message_handler(commands=["cancel"])
def cancel_step(message):
    uid = message.from_user.id
    temp_data.pop(uid, None)
    kb = get_colorful_menu(uid)
    _send_pe(message.chat.id, "𝐂𝐚𝐧𝐜𝐞𝐥𝐥𝐞𝐝!", reply_markup=kb)

if __name__ == "__main__":
    print("Bot Started - Premium Emoji Bot")
    print(f"Admins: {ADMIN_IDS}")
    print(f"Placeholder: {PLACEHOLDER}")
    print("Status: RUNNING")
    bot.infinity_polling(timeout=30, long_polling_timeout=15)