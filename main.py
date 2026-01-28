import flet as ft

# --- VERSIONE 57.0: DIAGNOSTICA PURA ---
# OBIETTIVO: Capire perché l'app si blocca sul bianco.
# AZIONE: Abbiamo DISATTIVATO Memoria e Audio.
# Se questa versione si vede, il colpevole era il caricamento dati.

def main(page: ft.Page):
    # 1. SETUP SUPER BASE
    page.title = "M2G App"
    page.bgcolor = "#f3f0e9"
    page.padding = 20
    page.spacing = 0
    # Scroll adattivo per evitare blocchi grafici
    page.scroll = "adaptive" 
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- NIENTE CARICAMENTO DATI ---
    # Sto forzando i valori di default per evitare che l'app si blocchi leggendo la memoria
    user_name = "Utente (Test)"
    
    # --- UI SEMPLIFICATA AL MASSIMO ---
    # Costruiamo l'interfaccia direttamente, senza funzioni complesse
    
    # HEADER
    header = ft.Column(spacing=5, controls=[
        ft.Container(
            width=60, height=60, bgcolor="#6a8a73", 
            border_radius=15, alignment=ft.alignment.center,
            content=ft.Text("M2G", color="white", size=20, weight="bold")
        ),
        ft.Text(f"Bentornato, {user_name}", size=22, weight="bold", color="#1a1a1a"),
        ft.Text("Modalità Test: Memoria Disattivata", size=12, color="red")
    ])

    # DEFINIZIONE CARD (Semplice)
    def make_card(title, icon_name):
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
                            width=50, height=50, 
                            bgcolor="#dbe4de", 
                            border_radius=12, 
                            alignment=ft.alignment.center,
                            # Usiamo icone native stringa (sicurissime)
                            content=ft.Icon(name=icon_name, color="#6a8a73", size=24)
                        ),
                        ft.Container(width=10),
                        ft.Text(title, size=16, weight="bold", color="#1a1a1a")
                    ]),
                    ft.Icon(name="chevron_right", color="#cccccc")
                ]
            )
        )

    # CORPO DELL'APP
    # Aggiungiamo direttamente alla pagina, niente funzioni render() complicate
    page.add(header)
    page.add(ft.Container(height=20))
    
    page.add(make_card("Lodi Mattutine", "wb_sunny"))
    page.add(ft.Container(height=10))
    page.add(make_card("Libretto", "menu_book"))
    page.add(ft.Container(height=10))
    page.add(make_card("Inno", "music_note"))
    page.add(ft.Container(height=10))
    page.add(make_card("Foto ricordo", "photo_camera"))
    
    page.add(ft.Container(height=30))
    page.add(ft.ElevatedButton("TEST BOTTONE", bgcolor="#6a8a73", color="white"))

    # Aggiorniamo la pagina per forzare il disegno
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
