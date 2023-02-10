import gradio as gr
import os
import torch
import gradio as gr
from transformers import M2M100Tokenizer, M2M100ForConditionalGeneration

if torch.cuda.is_available():
    device = torch.device("cuda:0")
else:
    device = torch.device("cpu")

tokenizer = M2M100Tokenizer.from_pretrained("facebook/m2m100_1.2B")
model = M2M100ForConditionalGeneration.from_pretrained("facebook/m2m100_1.2B").to(device)
model.eval()

lang_id = {
    "":"",
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Asturian": "ast",
    "Azerbaijani": "az",
    "Bashkir": "ba",
    "Belarusian": "be",
    "Bulgarian": "bg",
    "Bengali": "bn",
    "Breton": "br",
    "Bosnian": "bs",
    "Burmese": "my",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chinese": "zh",
    "Chinese (simplified)": "zh",
    "Chinese (traditional)": "zh",    
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Estonian": "et",
    "Fulah": "ff",
    "Finnish": "fi",
    "French": "fr",
    "Western Frisian": "fy",
    "Gaelic": "gd",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Hausa": "ha",
    "Hebrew": "he",
    "Hindi": "hi",
    "Haitian": "ht",
    "Hungarian": "hu",
    "Irish": "ga",
    "Indonesian": "id",
    "Igbo": "ig",
    "Iloko": "ilo",
    "Icelandic": "is",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jv",
    "Kazakh": "kk",
    "Central Khmer": "km",
    "Kannada": "kn",
    "Korean": "ko",
    "Luxembourgish": "lb",
    "Ganda": "lg",
    "Lingala": "ln",
    "Lao": "lo",
    "Lithuanian": "lt",
    "Latvian": "lv",
    "Malagasy": "mg",
    "Macedonian": "mk",
    "Malayalam": "ml",
    "Mongolian": "mn",
    "Marathi": "mr",
    "Malay": "ms",
    "Nepali": "ne",
    "Norwegian": "no",
    "Northern Sotho": "ns",
    "Occitan": "oc",
    "Oriya": "or",
    "Panjabi": "pa",
    "Persian": "fa",
    "Polish": "pl",
    "Pushto": "ps",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Spanish": "es",
    "Somali": "so",
    "Serbian": "sr",
    "Serbian (cyrillic)": "sr",
    "Serbian (latin)": "sr",    
    "Swati": "ss",
    "Sundanese": "su",
    "Swedish": "sv",
    "Swahili": "sw",
    "Tamil": "ta",
    "Thai": "th",
    "Tagalog": "tl",
    "Tswana": "tn",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Wolof": "wo",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",
}

def trans_page(input,input1,trg):
    src_lang = lang_id["English"]
    trg_lang = lang_id[trg]
    if trg_lang != src_lang:
        
        tokenizer.src_lang = src_lang
        with torch.no_grad():
            encoded_input = tokenizer(input, return_tensors="pt").to(device)
            generated_tokens = model.generate(**encoded_input, forced_bos_token_id=tokenizer.get_lang_id(trg_lang))
            translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    else:
        translated_text=input
        pass
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
    return translated_text,gr.Dropdown.update(choices=list(translated_text1.keys()))


def trans_to(input,src,trg):
    src_lang = lang_id[src]
    trg_lang = lang_id[trg]
    if trg_lang != src_lang:
        tokenizer.src_lang = src_lang
        with torch.no_grad():
            encoded_input = tokenizer(input, return_tensors="pt").to(device)
            generated_tokens = model.generate(**encoded_input, forced_bos_token_id=tokenizer.get_lang_id(trg_lang))
            translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    else:
        translated_text=input
        pass
    return translated_text

md1 = "Translate - 100 Languages"



with gr.Blocks() as transbot:
    #this=gr.State()
    with gr.Row():
        gr.Column()
        with gr.Column():
            with gr.Row():
                t_space = gr.Dropdown(label="Translate Space", choices=list(lang_id.keys()),value="English")
                t_submit = gr.Button("Translate Space")
        gr.Column()
        
    with gr.Row():
        gr.Column()
        with gr.Column():
            md = gr.Markdown("""<h1><center>Translate - 100 Languages</center></h1><h4><center>Translation may not be accurate</center></h4>""")
            with gr.Row():
                lang_from = gr.Dropdown(label="From:", choices=list(lang_id.keys()),value="English")
                lang_to = gr.Dropdown(label="To:", choices=list(lang_id.keys()),value="Chinese")
            submit = gr.Button("Go")
            with gr.Row():
                with gr.Column():
                    message = gr.Textbox(label="Prompt",placeholder="Enter Prompt",lines=4)
                    translated = gr.Textbox(label="Translated",lines=4,interactive=False)
        gr.Column()
    t_submit.click(trans_page,[md,lang_from,t_space],[md,lang_from])
    
    submit.click(trans_to, inputs=[message,lang_from,lang_to], outputs=[translated])
transbot.queue(concurrency_count=20)
transbot.launch()