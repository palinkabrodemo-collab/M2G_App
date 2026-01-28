import flet as ft

# --- VERSIONE 63.0: LOGICA "TEST BLU" (NO SCROLL) ---
# DIAGNOSI DEFINITIVA: L'attivazione di page.scroll sulle versioni precedenti causava lo schermo bianco.
# SOLUZIONE: Rimosso page.scroll. Usiamo l'addizione diretta (page.add) come nella v58 (Blue) che funzionava.

def main(page: ft.Page):
    # 1. SETUP IDENTICO AL TEST BLU (v58)
    page.title = "M2G App"
    page.bgcolor = "#f3f0e9" # Beige
    page.padding = 20
    page.spacing = 10        # Spazio tra gli elementi
    
    # CRUCIALE: NESSUN SCROLL IMPOSTATO.
    # Questo è ciò che rendeva stabile la versione 58.
    
    # Pulizia
    page.clean()

    # --- DEFINIZIONE COLORI ---
    c_primary = "#6a8a73" # Verde
    c_text = "#1a1a1a"    # Nero

    # --- COSTRUZIONE ELEMENTI (Semplici Container statici) ---
    
    # 1. HEADER
    header = ft.Column(spacing=5, controls=[
        ft.Container(height=20), # Spazio tetto
        ft.Row(controls=[
            ft.Container(
                width=60, height=60, bgcolor=c_primary, 
                border_radius=15, alignment=ft.alignment.center,
                content=ft.Text("M2G", color="white", size=20, weight="bold")
            ),
        ]),
        ft.Text("Bentornato, Utente", size=22, weight="bold", color=c_text)
    ])

    # 2. CARD HELPER (Senza logiche complesse)
    def simple_card(title, icon_name):
        return ft.Container(
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
                            # Icona stringa semplice
                            content=ft.Icon(icon_name, color=c_primary, size=24)
                        ),
                        ft.Container(width=10),
                        ft.Text(title, size=16, weight="bold", color=c_text)
                    ]),
                    ft.Icon("chevron_right", color="#cccccc")
                ]
            )
        )

    # --- AGGIUNTA DIRETTA (Stile v58) ---
    page.add(header)
    page.add(ft.Container(height=10))
    
    page.add(simple_card("Lodi Mattutine", "wb_sunny"))
    page.add(simple_card("Libretto", "menu_book"))
    page.add(simple_card("Inno", "music_note"))
    page.add(simple_card("Foto ricordo", "photo_camera"))
    
    # Test di verifica
    page.add(ft.Container(height=20))
    page.add(ft.Text("Grafica caricata con successo.", color="green", size=12))

    page.update()

# NESSUNA CARTELLA ASSETS CONFIGURATA
if __name__ == "__main__":
    ft.app(target=main)
