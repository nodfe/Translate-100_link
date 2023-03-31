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

l1="Afrikaans"
class Language:
    def __init__(self, name, code):
        self.name = name
        self.code = code

lang_id = [
    Language("Afrikaans", "af"),
    Language("Albanian", "sq"),
    Language("Amharic", "am"),
    Language("Arabic", "ar"),
    Language("Armenian", "hy"),
    Language("Asturian", "ast"),
    Language("Azerbaijani", "az"),
    Language("Bashkir", "ba"),
    Language("Belarusian", "be"),
    Language("Bulgarian", "bg"),
    Language("Bengali", "bn"),
    Language("Breton", "br"),
    Language("Bosnian", "bs"),
    Language("Burmese", "my"),
    Language("Catalan", "ca"),
    Language("Cebuano", "ceb"),
    Language("Chinese","zh"),
    Language("Croatian","hr"),
    Language("Czech","cs"),
    Language("Danish","da"),
    Language("Dutch","nl"),
    Language("English","en"),
    Language("Estonian","et"),
    Language("Fulah","ff"),
    Language("Finnish","fi"),
    Language("French","fr"),
    Language("Western Frisian","fy"),
    Language("Gaelic","gd"),
    Language("Galician","gl"),
    Language("Georgian","ka"),
    Language("German","de"),
    Language("Greek","el"),
    Language("Gujarati","gu"),
    Language("Hausa","ha"),
    Language("Hebrew","he"),
    Language("Hindi","hi"),
    Language("Haitian","ht"),
    Language("Hungarian","hu"),
    Language("Irish","ga"),
    Language("Indonesian","id"),
    Language("Igbo","ig"),
    Language("Iloko","ilo"),
    Language("Icelandic","is"),
    Language("Italian","it"),
    Language("Japanese","ja"),
    Language("Javanese","jv"),
    Language("Kazakh","kk"),
    Language("Central Khmer","km"),
    Language("Kannada","kn"),
    Language("Korean","ko"),
    Language("Luxembourgish","lb"),
    Language("Ganda","lg"),
    Language("Lingala","ln"),
    Language("Lao","lo"),
    Language("Lithuanian","lt"),
    Language("Latvian","lv"),
    Language("Malagasy","mg"),
    Language("Macedonian","mk"),
    Language("Malayalam","ml"),
    Language("Mongolian","mn"),
    Language("Marathi","mr"),
    Language("Malay","ms"),
    Language("Nepali","ne"),
    Language("Norwegian","no"),
    Language("Northern Sotho","ns"),
    Language("Occitan","oc"),
    Language("Oriya","or"),
    Language("Panjabi","pa"),
    Language("Persian","fa"),
    Language("Polish","pl"),
    Language("Pushto","ps"),
    Language("Portuguese","pt"),
    Language("Romanian","ro"),
    Language("Russian","ru"),
    Language("Sindhi","sd"),
    Language("Sinhala","si"),
    Language("Slovak","sk"),
    Language("Slovenian","sl"),
    Language("Spanish","es"),
    Language("Somali","so"),
    Language("Serbian","sr"),
    Language("Serbian (cyrillic)","sr"),
    Language("Serbian (latin)","sr"),
    Language("Swati","ss"),
    Language("Sundanese","su"),
    Language("Swedish","sv"),
    Language("Swahili","sw"),
    Language("Tamil","ta"),
    Language("Thai","th"),
    Language("Tagalog","tl"),
    Language("Tswana","tn"),
    Language("Turkish","tr"),
    Language("Ukrainian","uk"),
    Language("Urdu","ur"),
    Language("Uzbek","uz"),
    Language("Vietnamese","vi"),
    Language("Welsh","cy"),
    Language("Wolof","wo"),
    Language("Xhosa","xh"),
    Language("Yiddish","yi"),
    Language("Yoruba","yo"),
    Language("Zulu","zu"),
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
                t_space = gr.Dropdown(label="Translate Space", choices=[l.name for l in lang_id], value="English")
                #t_space = gr.Dropdown(label="Translate Space", choices=list(lang_id.keys()),value="English")
                t_submit = gr.Button("Translate Space")
        gr.Column()
        
    with gr.Row():
        gr.Column()
        with gr.Column():
            md = gr.Markdown("""<h1><center>Translate - 100 Languages</center></h1><h4><center>Translation may not be accurate</center></h4>""")
            with gr.Row():

                lang_from = gr.Dropdown(label="From:", choices=[l.name for l in lang_id],value="English")
                lang_to = gr.Dropdown(label="To:", choices=[l.name for l in lang_id],value="Chinese")
                
                #lang_from = gr.Dropdown(label="From:", choices=list(lang_id.keys()),value="English")
                #lang_to = gr.Dropdown(label="To:", choices=list(lang_id.keys()),value="Chinese")
            submit = gr.Button("Go")
            with gr.Row():
                with gr.Column():
                    message = gr.Textbox(label="Prompt",placeholder="Enter Prompt",lines=4)
                    translated = gr.Textbox(label="Translated",lines=4,interactive=False)
        gr.Column()
    t_submit.click(trans_page,[md,t_space],[md])
    
    submit.click(trans_to, inputs=[message,lang_from,lang_to], outputs=[translated])
transbot.queue(concurrency_count=20)
transbot.launch()

