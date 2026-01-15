import flet as ft
import sys
import traceback

def main(page: ft.Page):
    # 1. IMPOSTAZIONI DI SICUREZZA ASSOLUTA
    page.title = "Test Diagnostico"
    page.bgcolor = "blue"  # Sfondo BLU per capire subito se carica
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 2. SISTEMA DI CATTURA ERRORI GLOBALE
    # Se qualcosa esplode, lo scriviamo sullo schermo
    try:
        # Troviamo la versione di Python per capire se l'ambiente è sano
        py_version = sys.version
        
        # Creiamo un testo semplice
        txt_status = ft.Text(
            f"SE LEGGI QUESTO, L'APP FUNZIONA!\n\nPython: {py_version}", 
            size=20, 
            color="white", 
            text_align="center"
        )
        
        # Aggiungiamo alla pagina
        page.add(
            ft.Icon(name="check_circle", color="white", size=50), # Icona nativa sicurissima
            ft.Container(height=20),
            txt_status
        )
        
        # Forziamo l'aggiornamento
        page.update()

    except Exception as e:
        # Se c'è un errore, lo mostriamo in ROSSO
        page.bgcolor = "red"
        error_msg = traceback.format_exc()
        page.add(ft.Text(f"ERRORE CRITICO:\n{error_msg}", color="white", size=15))
        page.update()

# 3. AVVIO SENZA ASSETS
# Rimuoviamo 'assets_dir' per isolare il problema. 
# Se l'app parte, il colpevole era la cartella assets.
if __name__ == "__main__":
    ft.app(target=main)
