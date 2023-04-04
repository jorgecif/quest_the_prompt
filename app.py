import streamlit as st
import PIL.Image




# Parámetros
menu = ["Seleccione", "Opción 1", "Opción 2","Opción 3","Créditos"]

st.set_page_config(
	page_title="Título de la aplicación",
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




# ------------
# Convertir a excel
def to_excel(df):
	output = BytesIO()
	writer = pd.ExcelWriter(output, engine='xlsxwriter', options = {'remove_timezone': True})
	df.to_excel(writer, sheet_name='Sheet1')
	writer.save()
	processed_data = output.getvalue()
	return processed_data

def get_table_download_link(df):
	"""Generates a link allowing the data in a given panda dataframe to be downloaded
	in:  dataframe
	out: href string
	"""
	val = to_excel(df)
	b64 = base64.b64encode(val).decode() # val looks like b'...'
	href=f'<a href="data:application/octet-stream;base64,{b64}" download="captura.xlsx" target="_blank">Descargar: Haga clic derecho y guardar enlace como...</a>' # decode b'abc' => abc	
	return href



def main():
	st.title("Título de la aplicación")

	image =  PIL.Image.open('logo.png')

	st.sidebar.image(image, use_column_width=False)
	choice = st.sidebar.selectbox("Seleccione la opción en el menú",menu)

	
	if choice == "Seleccione":
		st.subheader("Seleccione una de las opciones en el menú lateral")

	elif choice == "Opción 1":
		st.subheader("Seleccionó la opción 1")



	elif choice == 'Opción 2':
		st.subheader("Seleccionó la opción 2")

		# ------ Input término principal
		st.subheader("Término principal")

		# -----------------------------------
	elif choice == 'Opción 3':
		st.subheader("Seleccionó la opción 3")

		# ------ Input coordenadas y radio
		st.subheader("Localización")



	elif choice == 'Créditos':
		st.subheader("Jorge O. Cifuentes")
		body='<a href="https://www.quidlab.co">https://www.quidlab.co</a>'
		st.markdown(body, unsafe_allow_html=True)
		st.write('Email: *jorge@quidlab.co* :heart:')
		st.write("Version 1.0")
		st.write("Nombre de la aplicación")
		st.text("")

if __name__ == "__main__":
	main()