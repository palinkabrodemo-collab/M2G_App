import flet as ft

# --- VERSIONE 59.0: RICOSTRUZIONE GRAFICA SICURA ---
# OBIETTIVO: Ripristinare la grafica Beige/Verde (M2G) mantenendo la stabilità del Test Blu.
# STRATEGIA:
# 1. Nessun caricamento file esterno (Niente Assets -> Niente Schermo Bianco).
# 2. Sintassi icone corretta (Niente "name=" -> Niente Errore Rosso).
# 3. Layout ListView (Niente "expand" complessi -> Niente Schermo Grigio).

def main(page: ft.Page):
    # 1. SETUP VISIVO (Identico al design M2G)
    page.title = "M2G App"
    page.bgcolor = "#f3f0e9"  # Il tuo colore Beige
    page.padding = 0
    page.spacing = 0
    page.safe_area = ft.SafeArea(content=None) # Rispetta il notch del telefono

    # --- COLORI ---
    c_primary = "#6a8a73" # Verde
    c_text = "#1a1a1a"    # Nero scuro
    c_card = "white"
    c_icon_bg = "#dbe4de" # Verdino chiaro

    # --- DATI FITTIZI (Per non bloccare la memoria) ---
    user_name = "Utente"

    # --- COSTRUZIONE HOME ---
    # Usiamo una ListView: è il modo più sicuro per disegnare liste su Android
    lv = ft.ListView(expand=True, spacing=15, padding=20)

    # HEADER
    lv.controls.append(ft.Container(height=20)) # Spazio sopra
    lv.controls.append(ft.Column(spacing=5, controls=[
        ft.Container(
            width=60, height=60, bgcolor=c_primary, 
            border_radius=15, alignment=ft.alignment.center,
            content=ft.Text("M2G", color="white", size=20, weight="bold")
        ),
        ft.Text(f"Bentornato, {user_name}", size=22, weight="bold", color=c_text)
    ]))
    
    # SPAZIO
    lv.controls.append(ft.Container(height=10))

    # FUNZIONE PER CREARE LE CARD (Senza errori di sintassi)
    def add_card(title, icon_native_name):
        lv.controls.append(ft.Container(
            bgcolor=c_card, height=80, border_radius=20, padding=15,
            border=ft.border.all(1, "#eeeeee"),
            content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.Row(controls=[
                    ft.Container(
                        width=50, height=50, bgcolor=c_icon_bg, 
                        border_radius=15, alignment=ft.alignment.center, 
                        # NOTA BENE: ft.Icon(nome_stringa) SENZA "name="
                        content=ft.Icon(icon_native_name, size=28, color=c_primary)
                    ),
                    ft.Container(width=10),
                    ft.Text(title, size=16, weight="bold", color=c_text)
                ]),
                # Freccia destra
                ft.Icon("chevron_right", color="#cccccc")
            ])
        ))

    # AGGIUNTA CARDS (Uso nomi nativi sicuri)
    add_card("Lodi Mattutine", "wb_sunny")
    add_card("Libretto", "menu_book")
    add_card("Inno", "music_note")
    add_card("Foto ricordo", "photo_camera")

    # NAVBAR (Semplice, in fondo alla lista per ora)
    lv.controls.append(ft.Container(height=30))
    lv.controls.append(ft.Container(
        bgcolor="white", padding=15, border_radius=20,
        content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
            ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0, controls=[
                ft.Icon("home", color=c_primary), 
                ft.Text("HOME", size=10, color=c_primary, weight="bold")
            ]),
            ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0, controls=[
                ft.Icon("person", color=c_text), 
                ft.Text("PROFILO", size=10, color=c_text, weight="bold")
            ])
        ])
    ))
    
    # SPAZIO FONDO
    lv.controls.append(ft.Container(height=50))

    # AGGIUNGIAMO TUTTO ALLA PAGINA
    page.add(lv)

# IMPORTANTE: NON rimettere assets_dir="assets" qui sotto, 
# altrimenti torna lo schermo bianco se la cartella non viene trovata.
if __name__ == "__main__":
    ft.app(target=main)
