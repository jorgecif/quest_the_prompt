import streamlit as st
import PIL.Image
import requests
import random



def consultar():

    session = requests.Session()
    with st.form("my_form"):
        index = st.text_input("Palabra clave", key="index")

        submitted = st.form_submit_button("Buscar")

        if submitted:
            st.write("Result")
            data = fetch(session, f"https://lexica.art/api/v1/search?q={index}")

            data2 = data["images"][numero]
            st.json = data2
            st.json
            if data2:
                st.image(data2['src'], caption=f"Author: {data2['prompt']}")
            else:
                st.error("Error")


# Parámetros

numero_rand = random.randint(0, 49) # Para seleccionar aleatoreamente entre las 50 respuestas del json del servicio de Lexica

menu = ["Seleccione", "Modo temática texto", "Modo temática imagen","Modo aleatorio","Créditos"]

st.set_page_config(
	page_title="Adivina el prompt",
	page_icon="random",
	layout="centered",
	initial_sidebar_state="expanded",
	)

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


def main():
	st.title("Quest-the-prompt")

	image =  PIL.Image.open('logo.png')

	st.sidebar.image(image, use_column_width=False)
	choice = st.sidebar.selectbox("Seleccione la opción en el menú",menu)

	
	if choice == "Seleccione":
		st.subheader("Aplicación para entrenarse en el 'arte' de la redacción de prompts para la generación de imágenes con IA")

	elif choice == "Modo temática texto":
		st.subheader("Modo temática texto")
		form = st.form("form1")
		tematica_texto=form.text_input("Tema a buscar: ", key="tematica_texto")
		texto_enviado = form.form_submit_button("Buscar")
		
		if texto_enviado:
			session = requests.Session()
			st.write("Resultado")
			datos = fetch(session, f"https://lexica.art/api/v1/search?q={tematica_texto}")
			datos_rand = datos["images"][numero_rand]
			prompt_real=datos_rand['prompt']
			URL_real=datos_rand['src']
			#st.json = datos_rand
			#st.json
			if datos_rand:
				#st.image(URL_real, caption=f"Prompt: {prompt_real}")
				st.image(URL_real)
			else:
				st.error("Se ha producido un error. Espera 1 minuto para volver a intentar")
			prompt_adivinado=form.text_input("Prompt adivinado: ", key="prompt_adivinado")
			prompt_enviado = form.form_submit_button("Enviar")
			if prompt_enviado:
				st.write("Resultado")

				#st.json = datos_rand
				#st.json




	elif choice == 'Modo temática imagen':
		st.subheader("Modo temática imagen")


	elif choice == 'Modo aleatorio':
		st.subheader("Modo aleatorio")




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