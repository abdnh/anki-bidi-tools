import anki.lang

strings = {
    'en': {
        'addon_name': 'Bidirectional Text Tools',
        'ltr_block_label': 'Left-To-Right',
        'rtl_block_label': 'Right-To-Left',
        'ltr_inline_label': 'LTR Selected',
        'rtl_inline_label': 'RTL Selected',
        'insert_chars': 'Insert Characters',
    },
    'ar': {
        'addon_name': 'أدوات النصوص ثنائية الاتجاه',
        'ltr_block_label': 'من اليسار إلى اليمين',
        'rtl_block_label': 'من اليمين إلى اليسار',
        'ltr_inline_label': 'من اليسار إلى اليمين للمحدد',
        'rtl_inline_label': 'من اليمين إلى اليسار للمحدد',
        'insert_chars': 'إدخال حروف',
    }
}

def get_current_lang() -> str:
    try:
        return anki.lang.current_lang
    except:
        return anki.lang.currentLang

def tr(label: str) -> str:
    langdict = strings.get(get_current_lang(), strings['en'])
    translation = langdict.get(label, strings['en'][label])
    return translation
