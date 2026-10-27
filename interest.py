import streamlit as st
import random
import collections

st.title("Simulatore Interesterificazione Enzimatica")

# 1. Sezione di Input
st.subheader("Imposta i Trigliceridi di partenza")
n_tags = st.number_input("Quanti trigliceridi diversi vuoi inserire?", min_value=1, max_value=10, value=3)

input_data = []
for i in range(n_tags):
    col1, col2 = st.columns(2)
    with col1:
        # L'utente può scrivere ABA, POP, OOO, ecc.
        tag = st.text_input(f"Molecola {i+1} (3 lettere)", value="AAA", key=f"tag_{i}").upper()
    with col2:
        quantita = st.number_input(f"Quantità {tag}", min_value=0, value=100, key=f"q_{i}")
    
    if len(tag) == 3:
        input_data.append((tag, quantita))

# 2. Pulsante di avvio
if st.button("Calcola Equilibrio"):
    listatag = []
    listaacidi = []
    
    # Costruiamo le liste dinamicamente in base agli input dell'utente
    for tag, quantita in input_data:
        # Aggiungiamo i centri 
        listatag.extend([["", tag[1], ""]] * quantita)
        # Aggiungiamo gli esterni (C1 e C3) al calderone
        listaacidi.extend(list(tag[0::2] * quantita))
        
    random.shuffle(listaacidi)
    
    # Riassemblaggio
    for i in range(len(listatag)):
        listatag[i] = listaacidi[2*i] + listatag[i][1] + listaacidi[2*i+1]
        
    # Accorpamento asimmetrici (CBA -> ABC)
    for i, element in enumerate(listatag):
        if element[0] > element[2]:
            listatag[i] = element[::-1]
            
    contatore = collections.Counter(listatag)
    
    # 3. Mostriamo i risultati
    st.subheader("Composizione Finale")
    for molecola, count in contatore.most_common():
        st.write(f"**{molecola}**: {count}")