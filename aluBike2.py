import streamlit as st


import hashlib
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()

def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data

def main():

	st.title("ALuBIke App")

	menu = ["Home","Login","Cadastrar"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Muito mais que um aluguel, uma transformação em nossa Comunidade!!")
		st.markdown("""
			Trazendo uma proposta ousada e desafiadora, propomos o exercício da
		 cidadania através de uma atitude nobre: Pessoas que como eu e você querem um mundo
		  melhor, estão disponibilizando suas bicicletas em prol de melhorar a mobilidade 
		  urbana, pois pessoas que possuem carros podem optar por usar uma bicicleta e ao 
		  mesmo tempo ajudar de forma real as pessoas que precisam de um transporte para seu
		   trabalho e até mesmo seu lazer!!!""")

	elif choice == "Login":
		st.subheader("Escolha aqui sua bicicleta")

		username = st.sidebar.text_input("Nome do Usuário")
		password = st.sidebar.text_input("Senha",type='password')
		if st.sidebar.checkbox("Login"):

			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success(f"Seja bem vindo {username}")
				st.subheader('Escolha o bairro mais próximo a você')

				task = st.selectbox("Bairro: ",["Urca","Copacabana","Leme"])
				if task == "Urca":
					st.markdown(f"Aqui serão mostradas as bicicletas disponíveis na {task}")

				elif task == "Copacabana":
					st.markdown(f"Aqui serão mostradas as bicicletas disponíveis em {task}")

				elif task == "Leme":
					st.markdown(f"Aqui serão mostradas as bicicletas disponíveis no {task}")

			else:
				st.warning("Incorrect Username/Password")





	elif choice == "Cadastrar":
		st.subheader("Criar um novo usuário")
		new_user = st.sidebar.text_input("Nome")
		new_password = st.sidebar.text_input("Senha",type='password')

		if st.sidebar.button("Cadastrar"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("Parabéns, você agora está cadastrado")
			st.info("Agora já pode fazer o seu Login")

if __name__ == '__main__':
	main()