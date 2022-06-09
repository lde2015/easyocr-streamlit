import streamlit as st
from PIL import Image
import easyocr
import cv2
import numpy as np
import sys

def load_image(image_file):
	img = Image.open(image_file)

	return img



list_lang = ['Abaza - abq',
'Adyghe - ady',
'Afrikaans - af',
'Angika - ang',
'Arabic - ar',
'Assamese - as',
'Avar - ava',
'Azerbaijani - az',
'Belarusian - be',
'Bulgarian - bg',
'Bihari - bh',
'Bhojpuri - bho',
'Bengali - bn',
'Bosnian - bs',
'Simplified Chinese - ch_sim',
'Traditional Chinese - ch_tra',
'Chechen - che',
'Czech - cs',
'Welsh - cy',
'Danish - da',
'Dargwa - dar',
'German - de',
'English - en',
'Spanish - es',
'Estonian - et',
'Persian (Farsi) - fa',
'French - fr',
'Irish - ga',
'Goan Konkani - gom',
'Hindi - hi',
'Croatian - hr',
'Hungarian - hu',
'Indonesian - id',
'Ingush - inh',
'Icelandic - is',
'Italian - it',
'Japanese - ja',
'Kabardian - kbd',
'Kannada - kn',
'Korean - ko',
'Kurdish - ku',
'Latin - la',
'Lak - lbe',
'Lezghian - lez',
'Lithuanian - lt',
'Latvian - lv',
'Magahi - mah',
'Maithili - mai',
'Maori - mi',
'Mongolian - mn',
'Marathi - mr',
'Malay - ms',
'Maltese - mt',
'Nepali - ne',
'Newari - new',
'Dutch - nl',
'Norwegian - no',
'Occitan - oc',
'Pali - pi',
'Polish - pl',
'Portuguese - pt',
'Romanian - ro',
'Russian - ru',
'Serbian (cyrillic) - rs_cyrillic',
'Serbian (latin) - rs_latin',
'Nagpuri - sck',
'Slovak - sk',
'Slovenian - sl',
'Albanian - sq',
'Swedish - sv',
'Swahili - sw',
'Tamil - ta',
'Tabassaran - tab',
'Telugu - te',
'Thai - th',
'Tajik - tjk',
'Tagalog - tl',
'Turkish - tr',
'Uyghur - ug',
'Ukranian - uk',
'Urdu - ur',
'Uzbek - uz',
'Vietnamese - vi',
]

st.set_page_config(page_title='EasyOCR', layout ="wide")

st.title("Détection de texte dans une image")

image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])

lang = st.multiselect("Language(s) :", list_lang, ['English - en', 'French - fr'])
code_lang = [x.split(" ")[-1] for x in lang]

if image_file is not None:

	# To See details
	#file_details = {"filename":image_file.name, "filetype":image_file.type,
    #                "filesize":image_file.size}
	#st.write(file_details)

    # To View Uploaded Image
    img = load_image(image_file)
    st.image(img,width=500)
   

    # OpenCv Read
    with open(image_file.name, 'wb') as f:
        f.write(image_file.read())
    img_res = cv2.imread(image_file.name)

    col1, col2 = st.columns(2)

    reader = easyocr.Reader(code_lang)

    result = reader.readtext("img.jpg", paragraph=False)
    text = "'''\n"
    for i in range(len(result)):
        text += result[i][1] + " (" + str(np.round(100*result[i][2], 2)) + " %)\n"
    text += "'''"

    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 0, 0)

    result = reader.readtext("img.jpg", paragraph=True)
    try:
        for i in range(len(result)):
            top_left = tuple(result[i][0][0])
            bottom_right = tuple(result[i][0][2])
            top_right = tuple(result[i][0][1])
            bottom_left = tuple(result[i][0][3])

            img_res = cv2.rectangle(img_res,top_left,bottom_right,color,7)
            #img = cv2.putText(img,text,bottom_left, font, 5.5,color,4,cv2.LINE_AA)
            RGB_img = cv2.cvtColor(img_res, cv2.COLOR_BGR2RGB)
        with col1:
            st.subheader("Détection")
            st.image(RGB_img,width=500)
    except:        
        print(sys.exc_info()[0])
        pass

    with col2:
        st.subheader("Texte")
        st.code(text)