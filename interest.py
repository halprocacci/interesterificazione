import streamlit as st
import random
import collections
import pandas as pd

st.title("Simulatore Interesterificazione Enzimatica")

st.subheader("Imposta i Trigliceridi di partenza (Totale: 100%)")
n_tags = st.number_input("Quanti trigliceridi diversi vuoi inserire?", min_value=1, max_value=10, value=3)

input_data = []
somma_perc = 0.0

for i in range(n_tags):
    col1, col2 = st.columns(2)
    with col1:
        default_tag = ["AAA", "BBB", "CCC"][i] if i < 3 else "AAA"
        tag = st.text_input(f"Molecola {i+1} (3 lettere)", value=default_tag, key=f"tag_{i}").upper()
    with col2:
        default_q = [20, 40, 40][i] if i < 3 else 0
        # Permettiamo anche i decimali
        quantita = st.number_input(f"Percentuale {tag} (%)", min_value=0.0, max_value=100.0, value=float(default_q), step=1.0, key=f"q_{i}")
        somma_perc += quantita
    
    if len(tag) == 3 and quantita > 0:
        input_data.append((tag, quantita))

if round(somma_perc, 2) != 100.00:
    st.error(f"La somma attuale è {somma_perc}%. Aggiusta i valori per arrivare esattamente a 100%.")
else:
    st.success("Composizione iniziale valida (100%).")
    
    if st.button("Calcola Equilibrio"):
        # Impostazioni della Monte Carlo
        moltiplicatore = 100  # 100% * 100 = 10.000 molecole totali nel calderone
        n_run = 10            # Ripetiamo il processo 10 volte per fare la media
        
        risultati_cumulati = collections.Counter()
        progress_bar = st.progress(0, text="Esecuzione simulazioni Monte Carlo in corso...")
        
        for run in range(n_run):
            listatag = []
            listaacidi = []
            
            for tag, quantita in input_data:
                q_simulata = int(quantita * moltiplicatore)
                listatag.extend([["", tag[1], ""]] * q_simulata)
                listaacidi.extend(list(tag[0::2] * q_simulata))
                
            random.shuffle(listaacidi)
            
            for i in range(len(listatag)):
                listatag[i] = listaacidi[2*i] + listatag[i][1] + listaacidi[2*i+1]
                
            for i, element in enumerate(listatag):
                if element[0] > element[2]:
                    listatag[i] = element[::-1]
                    
            contatore = collections.Counter(listatag)
            totale_molecole = sum(contatore.values())
            
            # Sommiamo le percentuali di ogni run
            for molecola, count in contatore.items():
                percentuale = (count / totale_molecole) * 100
                risultati_cumulati[molecola] += percentuale
                
            progress_bar.progress((run + 1) / n_run, text=f"Run {run+1}/10 completato...")
            
        progress_bar.empty() # Nasconde la barra a fine calcolo
        
        # Calcolo della media finale
        risultati_finali = []
        for molecola, somma_perc_run in risultati_cumulati.most_common():
            media_perc = somma_perc_run / n_run
            if media_perc > 0.1: # Esclude le tracce microscopiche
                risultati_finali.append({
                    "Trigliceride": molecola,
                    "Composizione Finale (%)": round(media_perc, 2)
                })
            
        df = pd.DataFrame(risultati_finali)
        
        st.write("---")
        st.subheader("📊 Risultati all'Equilibrio")
        st.caption("I dati sono la media di 10 simulazioni indipendenti da 10.000 molecole ciascuna.")
        
        # Grafico a barre grande in primo piano
        st.bar_chart(df.set_index("Trigliceride")["Composizione Finale (%)"])
        
        # Tabella dettagliata sotto
        st.dataframe(df, use_container_width=True, hide_index=True)
