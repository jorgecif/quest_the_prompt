import streamlit as st
import PIL.Image
import requests
import random
import spacy

# Variables de sesión 

if 'puntaje_guardado' not in st.session_state:
	st.session_state.puntaje_guardado = 0

if 'puntaje_actual' not in st.session_state:
	st.session_state.puntaje_actual = 0

if 'prompt_consultado' not in st.session_state:
	st.session_state.prompt_consultado = "Prompt"



# Parámetros

numero_rand = random.randint(0, 49) # Para seleccionar aleatoreamente entre las 50 respuestas del json del servicio de Lexica

menu = ["Seleccione", "Modo temática texto", "Modo temática imagen","Modo aleatorio","Créditos"]

puntaje_mayor = 0


st.set_page_config(
	page_title="Adivina el prompt",
	page_icon="random",
	layout="centered",
	initial_sidebar_state="expanded",
	)

# Parametros NLP
nlp = spacy.load("en_core_web_lg")




# Oculto botones de Streamlit
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


#Funciones
def fetch(session, url):
    try:
        result = session.get(url)
        return result.json()
    except Exception:
        return {}


def consultar_imagen(tematica):
	session = requests.Session()
	datos = fetch(session, f"https://lexica.art/api/v1/search?q={tematica}")
	datos_rand = datos["images"][numero_rand]
	prompt_consultado = datos_rand['prompt']
	URL_consultado = datos_rand['src']
	return URL_consultado, prompt_consultado
	 

def adivinar_prompt(prompt_adivinado, prompt_real):
	frase1=prompt_adivinado
	frase2=prompt_real
	fra1=nlp(frase1)
	fra2=nlp(frase2)
	similitud_frases=fra1.similarity(fra2)
	puntaje_actual = similitud_frases
	return puntaje_actual

	
def escribir(palabra):
	return palabra + " not good."



def main():
	st.title("Quest-the-prompt")

	image =  PIL.Image.open('logo.png')

	st.sidebar.image(image, use_column_width=False)
	choice = st.sidebar.selectbox("Seleccione la opción en el menú",menu)

	
	if choice == "Seleccione":
		st.subheader("Aplicación para entrenarse en el 'arte' de la redacción de prompts para la generación de imágenes con IA")

	elif choice == "Modo temática texto":
		st.subheader("Modo temática texto")
		
		#tematica = st.text_input('Temática', "earth")
		#boton_consultado= st.button("Generar imagen para adivinar", on_click=consultar_imagen, args=[tematica])

		with st.form(key='form_tematica'):
			tematica = st.text_input('Temática', "City")
			boton_consultado= st.form_submit_button(label="Generar imagen para adivinar", on_click=consultar_imagen, args=[tematica])
			if boton_consultado:
				URL_resultado = consultar_imagen(tematica)[0]
				prompt_resultado = consultar_imagen(tematica)[1]
				st.session_state.URL_consultado = URL_resultado
				st.session_state.prompt_consultado =prompt_resultado

				st.image(URL_resultado, caption = 'Imagen a adivinar')


		with st.form(key='form_adivinar'):
			prompt_real = st.session_state.prompt_consultado
			prompt_adivinado = st.text_input('Prompt: ', " ")
			boton_adivinar=st.form_submit_button("Adivinar", on_click=adivinar_prompt, args=[prompt_adivinado, prompt_real])

			if boton_adivinar:
				puntaje_actual = adivinar_prompt(prompt_adivinado, prompt_real)	
				st.session_state.puntaje_actual = puntaje_actual
				puntaje_guardado=st.session_state.puntaje_guardado
				diferencia = puntaje_actual - puntaje_guardado
				if puntaje_actual > puntaje_guardado:
					st.session_state.puntaje_guardado = puntaje_actual
				col1, col2 = st.columns(2)
				col1.metric(
								label="Puntaje más alto: ⏳",
								value=(st.session_state.puntaje_guardado),
								delta=diferencia,
							)
				col2.metric(
								label="Puntaje actual: ⏳",
								value=(st.session_state.puntaje_actual),
								delta=diferencia,
							)
				
				prompt_real = st.session_state.puntaje_actual
				col1.write("**Prompt real**")
				col1.write(st.session_state.prompt_consultado)
				col2.write("**Prompt propuesto**")
				col2.write(prompt_adivinado)
				st.image(st.session_state.URL_consultado)
				


	elif choice == 'Modo temática imagen':
		st.subheader("Modo temática imagen")




	elif choice == 'Modo aleatorio':
		st.subheader("Modo aleatorio")
		with st.form(key='form_palabra'):
			palabra = st.text_input('Palabra', " ")
			boton_palabra= st.form_submit_button(label="Escribir", on_click=consultar_imagen, args=[palabra])
			if boton_palabra:
				tttt = escribir(palabra)
				st.write(tttt)

	elif choice == 'Créditos':
		st.subheader("Jorge O. Cifuentes")
		body='<a href="https://www.quidlab.co">https://www.quidlab.co</a>'
		st.markdown(body, unsafe_allow_html=True)
		st.write('Email: *jorge@quidlab.co* :heart: :fleur_de_lis:')
		st.write("Quest-the-prompt")
		st.write("Version 1.0")
		st.text("")

if __name__ == "__main__":
	main()