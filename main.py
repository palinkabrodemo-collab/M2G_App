import flet as ft

# --- VERSIONE 62.0: IL "TEST BLU" TRAVESTITO ---
# Questa versione usa ESATTAMENTE la struttura della v58 (quella che funzionava).
# Cambiamo solo i colori e il testo.
# NESSUN layout complesso (Column expand, Stack, Overlay) che possa bloccare Android.

def main(page: ft.Page):
    # 1. SETUP (Copia esatta del Test Blu, solo cambio colore)
    page.title = "M2G App"
    page.bgcolor = "#f3f0e9" # Beige (invece di Blue)
    page.padding = 20
    
    # IMPORTANTE: Nel test blu non c'era page.scroll="auto". 
    # Usiamo "adaptive" che è più sicuro su mobile, o niente.
    page.scroll = "adaptive"

    # Pulizia
    page.clean()

    # --- DEFINIZIONE ELEMENTI ---
    # Invece di fare layout complessi, creiamo oggetti semplici e li buttiamo dentro.

    # 1. LOGO M2G
    logo_box = ft.Container(
        width=60, height=60, bgcolor="#6a8a73", # Verde
        border_radius=15, alignment=ft.alignment.center,
        content=ft.Text("M2G", color="white", size=20, weight="bold")
    )

    # 2. TITOLO
    titolo = ft.Text("Bentornato, Utente", size=22, weight="bold", color="#1a1a1a")

    # 3. CARD DI TEST (Una sola per vedere se va)
    card_prova = ft.Container(
        bgcolor="white",
        height=80,
        border_radius=15,
        padding=15,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(controls=[
                    ft.Container(
                        width=50, height=50, bgcolor="#dbe4de", 
                        border_radius=12, alignment=ft.alignment.center,
                        # Icona nativa stringa (sicura)
                        content=ft.Icon("wb_sunny", color="#6a8a73", size=24)
                    ),
                    ft.Container(width=10),
                    ft.Text("Lodi Mattutine", size=16, weight="bold", color="#1a1a1a")
                ]),
                ft.Icon("chevron_right", color="#cccccc")
            ]
        )
    )

    # --- AGGIUNTA DIRETTA (STILE TEST BLU) ---
    # Niente colonne wrapper, niente expand. Dritto nella pagina.
    page.add(logo_box)
    page.add(ft.Container(height=10)) # Spazietto
    page.add(titolo)
    page.add(ft.Container(height=30)) # Spazio
    page.add(card_prova)
    
    # Aggiungo un testo di debug per essere sicuro
    page.add(ft.Container(height=20))
    page.add(ft.Text("Se vedi questo, la grafica è salva.", color="red"))

    page.update()

# Nessun assets_dir
if __name__ == "__main__":
    ft.app(target=main)
