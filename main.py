import flet as ft

# --- VERSIONE 61.0: IL METODO "TEST BLU" EVOLUTO ---
# DIAGNOSI: Il colpevole dello schermo bianco era "page.scroll = 'auto'".
# SOLUZIONE: Togliamo lo scroll dalla pagina e lo mettiamo in una Colonna controllata.

def main(page: ft.Page):
    # 1. SETUP (Stesso del Test Blu che funzionava)
    page.title = "M2G App"
    page.bgcolor = "#f3f0e9" # Beige
    page.padding = 0
    page.spacing = 0
    
    # CRUCIALE: DISATTIVIAMO LO SCROLL DELLA PAGINA
    # Se attivato sulla root, su Android causa il collasso (schermo bianco)
    page.scroll = None 

    # --- DEFINIZIONE COLORI ---
    c_primary = "#6a8a73" # Verde
    c_text = "#1a1a1a"    # Nero

    # --- 2. CREIAMO IL CONTENUTO ---
    # Invece di aggiungere pezzi sparsi, creiamo una colonna unica.
    # Questo è il contenitore sicuro.
    
    main_column = ft.Column(
        spacing=0,
        scroll="auto", # LO SCROLL VA QUI, NON NELLA PAGINA
        expand=True,   # Occupa tutto lo spazio disponibile
        controls=[
            # --- HEADER ---
            ft.Container(
                padding=20,
                content=ft.Column(spacing=5, controls=[
                    ft.Container(height=20), # Spazio per la barra in alto
                    ft.Row(controls=[
                        ft.Container(
                            width=60, height=60, bgcolor=c_primary, 
                            border_radius=15, alignment=ft.alignment.center,
                            content=ft.Text("M2G", color="white", size=20, weight="bold")
                        ),
                    ]),
                    ft.Text("Bentornato, Utente", size=22, weight="bold", color=c_text)
                ])
            ),
            
            # --- CARDS ---
            # Inseriamo le card direttamente qui
        ]
    )

    # Funzione helper per creare le card in modo pulito
    def add_card_to_list(title, icon_name):
        card = ft.Container(
            bgcolor="white",
            height=80,
            border_radius=15,
            padding=15,
            margin=ft.margin.symmetric(horizontal=20, vertical=5), # Margine esterno
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(controls=[
                        ft.Container(
                            width=50, height=50, bgcolor="#dbe4de", 
                            border_radius=12, alignment=ft.alignment.center,
                            content=ft.Icon(icon_name, color=c_primary, size=24)
                        ),
                        ft.Container(width=10),
                        ft.Text(title, size=16, weight="bold", color=c_text)
                    ]),
                    ft.Icon("chevron_right", color="#cccccc")
                ]
            )
        )
        main_column.controls.append(card)

    # Aggiungiamo le card alla colonna
    add_card_to_list("Lodi Mattutine", "wb_sunny")
    add_card_to_list("Libretto", "menu_book")
    add_card_to_list("Inno", "music_note")
    add_card_to_list("Foto ricordo", "photo_camera")

    # Spazio finale per non tagliare l'ultimo elemento
    main_column.controls.append(ft.Container(height=50))

    # --- 3. AGGIUNTA ALLA PAGINA ---
    # Aggiungiamo SOLO la colonna principale.
    # Puliamo prima per essere sicuri (come nel test blu)
    page.clean()
    page.add(main_column)
    page.update()

# Nessun assets_dir, codice minimale
if __name__ == "__main__":
    ft.app(target=main)
