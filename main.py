import flet as ft

# --- VERSIONE 58.0: HELLO WORLD (TEST DI VITA) ---
# Obiettivo: Capire se l'app è in grado di disegnare QUALCOSA.
# Se vedi lo sfondo BLU, siamo salvi.
# Se vedi BIANCO, il problema è strutturale (non nel codice Python).

def main(page: ft.Page):
    # Setup drastico per vedere se reagisce
    page.title = "Test M2G"
    page.bgcolor = "blue"  # Colore forte per capire subito se carica
    page.padding = 30
    
    # Puliamo tutto per sicurezza
    page.clean()

    # Aggiungiamo un testo enorme
    lbl = ft.Text(
        value="SE VEDI QUESTO\nL'APP FUNZIONA", 
        size=30, 
        color="white", 
        weight="bold",
        text_align="center"
    )
    
    # Aggiungiamo un contenitore bianco al centro
    container = ft.Container(
        bgcolor="white",
        padding=20,
        border_radius=10,
        content=ft.Text("Test Grafico Superato", color="black", size=20)
    )

    page.add(lbl)
    page.add(ft.Container(height=20))
    page.add(container)
    
    page.update()

# AVVIO MINIMALE
# IMPORTANTE: Nessun assets_dir, nessuna configurazione complessa.
if __name__ == "__main__":
    ft.app(target=main)
