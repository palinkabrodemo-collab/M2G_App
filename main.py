import flet as ft

# --- VERSIONE 60.0: STRUTTURA "TEST BLU" RICOLORATA ---
# Se il Test Blu (v58) si vedeva, questo DEVE vedersi.
# Usiamo la stessa struttura semplice: page.add() diretti.
# Niente ListView, niente SafeArea complessa, niente expand.

def main(page: ft.Page):
    # 1. SETUP IDENTICO AL TEST BLU (Ma con i colori M2G)
    page.title = "M2G App"
    page.bgcolor = "#f3f0e9" # Beige
    page.padding = 20        # Padding semplice invece di SafeArea
    page.scroll = "auto"     # Scroll nativo (fondamentale)
    
    # Pulizia iniziale
    page.clean()

    # --- DEFINIZIONE COLORI ---
    c_primary = "#6a8a73" # Verde
    c_text = "#1a1a1a"    # Nero

    # --- 1. HEADER (Costruito come blocco semplice) ---
    header = ft.Column(spacing=5, controls=[
        ft.Container(height=20), # Spazio per la barra di stato
        ft.Row(controls=[
            ft.Container(
                width=60, height=60, bgcolor=c_primary, 
                border_radius=15, alignment=ft.alignment.center,
                content=ft.Text("M2G", color="white", size=20, weight="bold")
            ),
        ]),
        ft.Text("Bentornato, Utente", size=22, weight="bold", color=c_text)
    ])

    # --- 2. FUNZIONE CARD (Semplice container statico) ---
    def make_card(title, icon_code):
        return ft.Container(
            bgcolor="white",
            height=80,
            border_radius=15,
            padding=15,
            # Niente click per ora, solo grafica
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(controls=[
                        ft.Container(
                            width=50, height=50, bgcolor="#dbe4de", 
                            border_radius=12, alignment=ft.alignment.center,
                            # Icona nativa stringa
                            content=ft.Icon(icon_code, color=c_primary, size=24)
                        ),
                        ft.Container(width=10),
                        ft.Text(title, size=16, weight="bold", color=c_text)
                    ]),
                    ft.Icon("chevron_right", color="#cccccc")
                ]
            )
        )

    # --- 3. AGGIUNTA DIRETTA ALLA PAGINA (Come v58) ---
    # Non usiamo liste o colonne wrapper, buttiamo tutto dentro la pagina.
    page.add(header)
    page.add(ft.Container(height=20))
    
    page.add(make_card("Lodi Mattutine", "wb_sunny"))
    page.add(ft.Container(height=10))
    
    page.add(make_card("Libretto", "menu_book"))
    page.add(ft.Container(height=10))
    
    page.add(make_card("Inno", "music_note"))
    page.add(ft.Container(height=10))
    
    page.add(make_card("Foto ricordo", "photo_camera"))
    
    # Aggiornamento finale
    page.update()

# Nessun assets_dir
if __name__ == "__main__":
    ft.app(target=main)
