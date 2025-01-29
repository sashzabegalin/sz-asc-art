from flask import Flask, render_template, request
from pyfiglet import Figlet  # For ASCII art generation
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Configuration defaults
DEFAULT_SETTINGS = {
    'name': 'S-yberpunk',
    'matrix_chars': 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
    'main_color': '#00ffff',
    'matrix_color': '#0066ff',
    'bg_color': '#000000',
    'hologram_color': '#0099ff'
}

LANGUAGE_CHARS = {
    "Japanese": "アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン",
    "Russian": "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя",
    "Arabic": "شغظذخثتسرقضطكمنتالبيسشضصثقفغعهخحجدطكمنتالب",
    "Greek": "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψω",
    "Korean": "ㅂㅈㄷㄱㅅㅛㅕㅑㅐㅔㅁㄴㅇㄹㅎㅗㅓㅏㅣㅋㅌㅊ퓨ㅜㅡ",
    "Code": "01{}[]()&%$#@!*-+=?",
    "Chinese": "的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件引北那处求各基月毛然问比展那着",
    "Hindi": "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहअआइईउऊऋएऐओऔंःँ",
    "Emoji": "🌌💫🌠🌃🌆🌇🎆🎇✨🌐🌀💠🔵🔷🔹🛸👾🤖💾💿📡🔭🌌🌠🌌",
    "Symbols": "♔♕♖♗♘♙♚♛♜♝♞♟⚡★☆☄☇☈☊☋☌☍☢☣☮☯☸☹☺♨♻♿⚒⚔⚖⚗⚙⚛⚜⚠⚡⚢⚣⚤⚥⚦⚧⚨⚩⚪⚫⚬⚭⚮⚯",
    "Math": "∀∁∂∃∄∅∆∇∈∉∊∋∌∍∎∏∐∑−∓∔∕∖∗∘∙√∛∜∝∞∟∠∡∢∣∤∥∦∧∨∩∪∫∬∭∮∯∰∱∲∳∴∵∶∷∸∹∺∻∼∽∾∿≀≁≂≃≄≅≆≇≈≉≊≋≌≍≎≏≐≑≒≓≔≕≖≗≘≙≚≛≜≝≞≟≠≡≢≣≤≥≦≧≨≩≪≫≬≭≮≯≰≱≲≳≴≵≶≷≸≹≺≻≼≽≾≿⊀⊁⊂⊃⊄⊅⊆⊇⊈⊉⊊⊋⊌⊍⊎⊏⊐⊑⊒⊓⊔⊕⊖⊗⊘⊙⊚⊛⊜⊝⊞⊟⊠⊡⊢⊣⊤⊥⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊱⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⋀⋁⋂⋃⋄⋅⋆⋇⋈⋉⋊⋋⋌⋍⋎⋏⋐⋑⋒⋓⋔⋕⋖⋗⋘⋙⋚⋛⋜⋝⋞⋟⋠⋡⋢⋣⋤⋥⋦⋧⋨⋩⋪⋫⋬⋭⋮⋯⋰⋱⋲⋳⋴⋵⋶⋷⋸⋹⋺⋻⋼⋽⋾⋿",
    "Thai": "กขฃคฅฆงจฉชซฌญฎฏฐฑฒณดตถทธนบปผฝพฟภมยรลวศษสหฬอฮฯะัาำิีึืุูเแโใไๅๆ็่้๊๋์ํ๎๏๐๑๒๓๔๕๖๗๘๙",
    "Turkish": "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZabcçdefgğhıijklmnoöprsştuüvyz",
    "Hebrew": "אבגדהוזחטיכךלמםנןסעפףצץקרשת",
    "Bengali": "অআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহড়ঢ়য়",
    "Tamil": "அஆஇஈஉஊஎஏஐஒஓஔகஙசஜஞடணதநனபமயரறலளழவஷஸஹ",
    "Armenian": "ԱԲԳԴԵԶԷԸԹԺԻԼԽԾԿՀՁՂՃՄՅՆՇՈՉՊՋՌՍՎՏՐՑՒՓՔՕՖաբգդեզէըթժիլխծկհձղճմյնշոչպջռսվտրցւփքօֆ",
    "Sinhala": "අආඇඈඉඊඋඌඍඎඏඐඑඒඓඔඕඖකඛගඝඞඟචඡජඣඤඥඦටඨඩඪණඬතථදධනඳපඵබභමඹයරලවශෂසහළෆ",
    "Khmer": "កខគឃងចឆជឈញដឋឌឍណតថទធនបផពភមយរលវឝឞសហឡអឣឤឥឦឧឨឩឪឫឬឭឮឯឰឱឲឳ",
    "Burmese": "ကခဂဃငစဆဇဈဉညဋဌဍဎဏတထဒဓနပဖဗဘမယရလဝသဟဠအဣဤဥဦဧဨဩဪါာိီုူေဲဳဴဵံ့း္်ျြွှဿ၀၁၂၃၄၅၆၇၈၉",
    "Tibetan": "ཀཁགགྷངཅཆཇ཈ཉཊཋཌཌྷཎཏཐདདྷནཔཕབབྷམཙཚཛཛྷཝཞཟའཡརལཤཥསཧཨཀྵཪཫཬ",
    "Spanish": "AÁBCDEÉFGHIÍJKLMNÑOÓPQRSTUÚÜVWXYZaábcdeéfghiíjklmnñoópqrstuúüvwxyz¿¡",
    "Vietnamese": "AĂÂBCDĐEÊGHIKLMNOÔƠPQRSTUƯVXYÁÀẢÃẠẮẰẲẴẶẤẦẨẪẬÉÈẺẼẸÍÌỈĨỊÓÒỎÕỌỐỒỔỖỘỚỜỞỠỢÚÙỦŨỤỨỪỬỮỰÝỲỶỸỴ",
    "Persian": "آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئؤأءۀةًٌٍَُِّ",
    "Urdu": "آابپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنںوہھیئےۓ",
    "Malayalam": "അആഇഈഉഊഋഌഎഏഐഒഓഔകഖഗഘങചഛജഝഞടഠഡഢണതഥദധനപഫബഭമയരറലളഴവശഷസഹാിീുൂൃെേൈൊോൌ്ൗ",
    "Gujarati": "અઆઇઈઉઊઋઍએઐઑઓઔકખગઘઙચછજઝઞટઠડઢણતથદધનપફબભમયરલળવશષસહ઼ઽાિીુૂૃૄૅેૈૉોૌ્",
    "Kannada": "ಅಆಇಈಉಊಋಌಎಏಐಒಓಔಕಖಗಘಙಚಛಜಝಞಟಠಡಢಣತಥದಧನಪಫಬಭಮಯರಱಲಳವಶಷಸಹ಼ಽಾಿೀುೂೃೄೆೇೈೊೋೌ್ೕೖ",
    "Telugu": "అఆఇఈఉఊఋఌఎఏఐఒఓఔకఖగఘఙచఛజఝఞటఠడఢణతథదధనపఫబభమయరఱలళవశషసహఽాిీుూృౄెేైొోౌ్ౕౖ",
    "Oriya": "ଅଆଇଈଉଊଋଌଏଐଓଔକଖଗଘଙଚଛଜଝଞଟଠଡଢଣତଥଦଧନପଫବଭମଯରଲଳଵଶଷସହ଼ଽାିୀୁୂୃୄେୈୋୌ୍ୖୗ",
    "Punjabi": "ਅਆਇਈਉਊਏਐਓਔਕਖਗਘਙਚਛਜਝਞਟਠਡਢਣਤਥਦਧਨਪਫਬਭਮਯਰਲਲ਼ਵਸ਼ਸਹਖ਼ਗ਼ਜ਼ੜਫ਼ੲੳ"
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get user settings from form
        settings = {
            'name': request.form.get('name', DEFAULT_SETTINGS['name']),
            'matrix_chars': request.form.get('matrix_chars', DEFAULT_SETTINGS['matrix_chars']),
            'main_color': request.form.get('main_color', DEFAULT_SETTINGS['main_color']),
            'matrix_color': request.form.get('matrix_color', DEFAULT_SETTINGS['matrix_color']),
            'bg_color': request.form.get('bg_color', DEFAULT_SETTINGS['bg_color']),
            'hologram_color': request.form.get('hologram_color', DEFAULT_SETTINGS['hologram_color'])
        }
        
        # Generate ASCII art
        f = Figlet(font='slant')
        ascii_art = f.renderText(settings['name'])
        settings['ascii_lines'] = ascii_art.split('\n')
        
        return render_template('display.html', settings=settings, site_title="Simulated Name Art Generator")
    
    return render_template('index.html', 
        defaults=DEFAULT_SETTINGS,
        site_title="Simulated Name Art Generator",
        languages=LANGUAGE_CHARS.items()
    )

if __name__ == '__main__':
    app.run(debug=True) 