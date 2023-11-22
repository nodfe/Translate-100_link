import torch
import gradio as gr
from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration
from openxlab.model import download

class Language:
    def __init__(self, name, code):
        self.name = name
        self.code = code

lang_id = [
    Language("Afrikaans", "af"),
    Language("Shqip", "sq"),  # Albanian
    Language("አማርኛ", "am"),  # Amharic
    Language("العربية", "ar"),  # Arabic
    Language("Հայերեն", "hy"),  # Armenian
    Language("Asturianu", "ast"),  # Asturian
    Language("Azərbaycanca", "az"),  # Azerbaijani
    Language("Башҡортса", "ba"),  # Bashkir
    Language("Беларуская", "be"),  # Belarusian
    Language("Български", "bg"),  # Bulgarian
    Language("বাংলা", "bn"),  # Bengali
    Language("Brezhoneg", "br"),  # Breton
    Language("Bosanski", "bs"),  # Bosnian
    Language("မြန်မာစာ", "my"),  # Burmese
    Language("Català", "ca"),  # Catalan
    Language("Cebuano", "ceb"),  # Cebuano
    Language("中文", "zh"),  # Chinese
    Language("Hrvatski", "hr"),  # Croatian
    Language("Čeština", "cs"),  # Czech
    Language("Dansk", "da"),  # Danish
    Language("Nederlands", "nl"),  # Dutch
    Language("English", "en"),  # English
    Language("Eesti", "et"),  # Estonian
    Language("Fulfulde", "ff"),  # Fulah
    Language("Suomi", "fi"),  # Finnish
    Language("Français", "fr"),  # French
    Language("Frysk", "fy"),  # Western Frisian
    Language("Gàidhlig", "gd"),  # Gaelic
    Language("Galego", "gl"),  # Galician
    Language("ქართული", "ka"),  # Georgian
    Language("Deutsch", "de"),  # German
    Language("Ελληνικά", "el"),  # Greek
    Language("ગુજરાતી", "gu"),  # Gujarati
    Language("هَوُسَ", "ha"),  # Hausa
    Language("עברית", "he"),  # Hebrew
    Language("हिन्दी", "hi"),  # Hindi
    Language("Kreyòl ayisyen", "ht"),  # Haitian
    Language("Magyar", "hu"),  # Hungarian
    Language("Gaeilge", "ga"),  # Irish
    Language("Bahasa Indonesia", "id"),  # Indonesian
    Language("Igbo", "ig"),  # Igbo
    Language("Ilokano", "ilo"),  # Iloko
    Language("Íslenska", "is"),  # Icelandic
    Language("Italiano", "it"),  # Italian
    Language("日本語", "ja"),  # Japanese
    Language("Basa Jawa", "jv"),  # Javanese
    Language("Қазақша", "kk"),  # Kazakh
    Language("ភាសាខ្មែរ", "km"),  # Central Khmer
    Language("ಕನ್ನಡ", "kn"),  # Kannada
    Language("한국어", "ko"),  # Korean
    Language("Lëtzebuergesch", "lb"),  # Luxembourgish
    Language("Luganda", "lg"),  # Ganda
    Language("Lingála", "ln"),  # Lingala
    Language("ລາວ", "lo"),  # Lao
    Language("Lietuvių", "lt"),  # Lithuanian
    Language("Latviešu", "lv"),  # Latvian
    Language("Malagasy", "mg"),  # Malagasy
    Language("Македонски", "mk"),  # Macedonian
    Language("മലയാളം", "ml"),  # Malayalam
    Language("Монгол", "mn"),  # Mongolian
    Language("मराठी", "mr"),  # Marathi
    Language("Bahasa Melayu", "ms"),  # Malay
    Language("नेपाली", "ne"),  # Nepali
    Language("Norsk", "no"),  # Norwegian
    Language("Sesotho sa Leboa", "ns"),  # Northern Sotho
    Language("Occitan", "oc"),  # Occitan
    Language("ଓଡ଼ିଆ", "or"),  # Oriya
    Language("ਪੰਜਾਬੀ", "pa"),  # Panjabi
    Language("فارسی", "fa"),  # Persian
    Language("Polski", "pl"),  # Polish
    Language("پښتو", "ps"),  # Pushto
    Language("Português", "pt"),  # Portuguese
    Language("Română", "ro"),  # Romanian
    Language("Русский", "ru"),  # Russian
    Language("سنڌي", "sd"),  # Sindhi
    Language("සිංහල", "si"),  # Sinhala
    Language("Slovenčina", "sk"),  # Slovak
    Language("Slovenščina", "sl"),  # Slovenian
    Language("Español", "es"),  # Spanish
    Language("Soomaali", "so"),  # Somali
    Language("Српски / Srpski", "sr"),  # Serbian (both Cyrillic and Latin)
    Language("SiSwati", "ss"),  # Swati
    Language("Basa Sunda", "su"),  # Sundanese
    Language("Svenska", "sv"),  # Swedish
    Language("Kiswahili", "sw"),  # Swahili
    Language("தமிழ்", "ta"),  # Tamil
    Language("ไทย", "th"),  # Thai
    Language("Tagalog", "tl"),  # Tagalog
    Language("Setswana", "tn"),  # Tswana
    Language("Türkçe", "tr"),  # Turkish
    Language("Українська", "uk"),  # Ukrainian
    Language("اردو", "ur"),  # Urdu
    Language("Oʻzbekcha", "uz"),  # Uzbek
    Language("Tiếng Việt", "vi"),  # Vietnamese
    Language("Cymraeg", "cy"),  # Welsh
    Language("Wolof", "wo"),  # Wolof
    Language("isiXhosa", "xh"),  # Xhosa
    Language("ייִדיש", "yi"),  # Yiddish
    Language("Èdè Yorùbá", "yo"),  # Yoruba
    Language("isiZulu", "zu"),  # Zulu
]
d_lang = lang_id[21]
#d_lang_code = d_lang.code

def trans_page(input,trg):
    src_lang = d_lang.code
    for lang in lang_id:
            if lang.name == trg:
                trg_lang = lang.code
    if trg_lang != src_lang:
        tokenizer.src_lang = src_lang
        with torch.no_grad():
            encoded_input = tokenizer(input, return_tensors="pt").to(device)
            generated_tokens = model.generate(**encoded_input, forced_bos_token_id=tokenizer.get_lang_id(trg_lang))
            translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    else:
        translated_text=input
        pass
    """    
    if trg_lang != src_lang:
        
        tokenizer.src_lang = src_lang
        with torch.no_grad():
            #lang_tr = lang_id
            encoded_input = tokenizer(lang_id, return_tensors="pt").to(device)
            generated_tokens = model.generate(**encoded_input, forced_bos_token_id=tokenizer.get_lang_id(trg_lang))
            translated_text1 = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    else:
        translated_text1=input1
        pass
    #return translated_text,gr.Dropdown.update(choices=list(translated_text1.keys()))
    """
    return translated_text

def trans_to(input,src,trg):
    print(f"input={input}, src={src}, target={trg}")
    for lang in lang_id:
        if lang.name == trg:
            trg_lang = lang.code
    for lang in lang_id:
        if lang.name == src:
            src_lang = lang.code
    if trg_lang != src_lang:
        tokenizer.src_lang = src_lang
        with torch.no_grad():
            encoded_input = tokenizer(input, return_tensors="pt").to(device)
            # print(f"encoded_input = {encoded_input}")
            generated_tokens = model.generate(**encoded_input, forced_bos_token_id=tokenizer.get_lang_id(trg_lang))
            # print(f"generated_tokens = {generated_tokens}")
            translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
            # print(f"translated_text = {translated_text}")
    else:
        translated_text=input
        pass
    return translated_text


def download_models(models_path: str):
    # download models from openxlab-models by openxlab sdk
    print("start to download models from xlab-models")
    download(model_repo='xj/facebook_100-Translate_1.2billion', model_name='config', output=models_path)
    download(model_repo='xj/facebook_100-Translate_1.2billion', model_name='generation_config', output=models_path)
    download(model_repo='xj/facebook_100-Translate_1.2billion', model_name='pytorch_model', output=models_path)
    download(model_repo='xj/facebook_100-Translate_1.2billion', model_name='sentencepiece.bpe.model', output=models_path)
    download(model_repo='xj/facebook_100-Translate_1.2billion', model_name='special_tokens_map', output=models_path)
    download(model_repo='xj/facebook_100-Translate_1.2billion', model_name='tokenizer_config', output=models_path)
    download(model_repo='xj/facebook_100-Translate_1.2billion', model_name='vocab', output=models_path)
    print("end to download models from xlab-models")


md1 = "Translate - 100 Languages"

if torch.cuda.is_available():
    device = torch.device("cuda:0")
    # device = torch.device("cpu")
else:
    device = torch.device("cpu")

# models_path = "/data/huggingface/facebook-100translate/1.2b"
models_path = "/home/xlab-app-center/.cache/model/xj_facebook_100-Translate_1.2billion"
# download_models(models_path)


tokenizer = M2M100Tokenizer.from_pretrained(models_path)
model = M2M100ForConditionalGeneration.from_pretrained(models_path).to(device)
model.eval()

l1="Afrikaans"


with gr.Blocks(title="百语翻译-应用中心-OpenXLab", theme="soft") as transbot:
    #this=gr.State()
    # with gr.Row():
    #     gr.Column()
    #     with gr.Column():
    #         with gr.Row():
    #             t_space = gr.Dropdown(label="Translate Space", choices=[l.name for l in lang_id], value="Chinese")
    #             #t_space = gr.Dropdown(label="Translate Space", choices=list(lang_id.keys()),value="English")
    #             t_submit = gr.Button("Translate Space")
    #     gr.Column()
    md = gr.Markdown("""<h1><center>百语翻译</center></h1><h4><center>基于Facebook开源模型: m2m100_1.2B</center></h4>""")
    with gr.Row():
        with gr.Column():
            lang_from = gr.Dropdown(show_label=False, choices=[l.name for l in lang_id],value="English")
            message = gr.Textbox(label="原文", placeholder="请输入原文", lines=4)
        with gr.Column():
            lang_to = gr.Dropdown(show_label=False, choices=[l.name for l in lang_id],value="中文")
            translated = gr.Textbox(label="翻译", lines=4, interactive=False)
    with gr.Column():
        submit = gr.Button(value="翻译", variant="primary")
    submit.click(trans_to, inputs=[message,lang_from,lang_to], outputs=[translated])

def launch_app():
    transbot.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    launch_app()
