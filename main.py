import flet as ft

# --- VERSIONE 34.0: ARCHITETTURA "CAMBIO SECCO" ---
# Questa versione NON nasconde le pagine (che causava i rettangoli grigi).
# Invece, svuota il contenitore centrale e ci mette dentro la nuova pagina.
# Nessun "fantasma" grafico possibile.

# --- DATI E COSTANTI ---
ICON_MAP = {
    "sunrise": "wb_sunny",
    "book-open": "menu_book",
    "music": "music_note", 
    "camera": "camera_alt",
    "chevron-right": "chevron_right",
    "home": "home", 
    "user": "person",
    "arrow-left": "arrow_back",
    "save": "save", 
    "edit": "edit",
    "play": "play_circle",
    "pause": "pause_circle", 
    "stop": "stop_circle"
}

LYRICS_TEXT = """
Lo sai che ti amo
Ma a volte è difficile sai?
Io mi perdo, mi strappo
E arriviamo sempre allo stesso punto

Sono le nove e fuori piove
Il cielo è pieno di te
I tuoi capelli scintillano sotto la Luna
E la tua bianca pelle mi ricorda la radura

Il mio amore per te
È lapalissiano
Io so chi siamo
Solo quando sto con te
Ti respiro cosi forte
Da rimanerne asfissiato
E solo se ti metti di lato
Posso mostrarti con le mani
Quanto ti amo perché
"""

# Colori definiti
COLORS = {
    "light": {
        "bg": "#f3f0e9", "primary": "#6a8a73", "text": "#1a1a1a", 
        "card": "white", "icon_bg": "#dbe4de", "nav_bg": "white", "input_bg": "white"
    },
    "dark": {
        "bg": "#1e1e1e", "primary": "#6a8a73", "text": "#ffffff", 
        "card": "#2c2c2c", "icon_bg": "#3a3a3a", "nav_bg": "#2c2c2c", "input_bg": "#333333"
    }
}

def main(page: ft.Page):
    # 1. SETUP INIZIALE
    page.title = "M2G App"
    page.padding = 0
    page.spacing = 0
    page.safe_area = ft.SafeArea(content=None)
    page.bgcolor = "white" # Importante per evitare sfondi grigi default

    # 2. AUDIO PLAYER (Sicuro)
    audio_player = ft.Audio(src="inno.mp3", autoplay=False, release_mode="stop")
    page.overlay.append(audio_player)

    # 3. GESTIONE STATO (Memoria)
    state = {
        "page": "home",
        "dark": False,
        "name": "Utente",
        "notes": "",
        "reader_title": "",
        "audio_playing": False
    }

    # Caricamento sicuro dati
    try:
        state["name"] = page.client_storage.get("user_name") or "Utente"
        state["notes"] = page.client_storage.get("user_notes") or ""
        state["dark"] = page.client_storage.get("dark_mode") or False
    except:
        pass

    def get_c(key):
        return COLORS["dark" if state["dark"] else "light"][key]

    # --- 4. FUNZIONI COSTRUZIONE PAGINE (Creano la grafica al momento) ---

    def get_home_content():
        # Lista Card
        col = ft.Column(spacing=15, scroll="auto")
        items = [("Lodi Mattutine", "sunrise"), ("Libretto", "book-open"), ("Inno", "music"), ("Foto ricordo", "camera")]
        
        for title, icon in items:
            col.controls.append(
                ft.Container(
                    bgcolor=get_c("card"), height=80, border_radius=20, padding=15,
                    shadow=ft.BoxShadow(blur_radius=5, color="#11000000", offset=ft.Offset(0,4)),
                    on_click=lambda e, t=title: navigate("reader", t),
                    content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Row(controls=[
                            ft.Container(width=50, height=50, bgcolor=get_c("icon_bg"), border_radius=15, alignment=ft.Alignment(0,0), content=ft.Icon(ICON_MAP[icon], color=get_c("primary"))),
                            ft.Container(width=10),
                            ft.Text(title, size=16, weight="bold", color=get_c("text"))
                        ]),
                        ft.Icon(ICON_MAP["chevron-right"], color="#cccccc")
                    ])
                )
            )
        # Aggiungiamo spazio in fondo per lo scroll
        col.controls.append(ft.Container(height=20))
        return col

    def get_user_content():
        def save_name(e):
            state["name"] = e.control.value
            page.client_storage.set("user_name", e.control.value)
            update_ui() # Aggiorna header
        
        def toggle_dark(e):
            state["dark"] = e.control.value
            page.client_storage.set("dark_mode", e.control.value)
            update_ui() # Ridisegna tutto coi nuovi colori

        return ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, scroll="auto", controls=[
            ft.Container(height=10),
            ft.Icon("person", size=80, color=get_c("primary")),
            ft.Text("Il tuo Profilo", size=20, weight="bold", color=get_c("text")),
            ft.Container(width=280, content=ft.TextField(value=state["name"], label="Nome", on_change=save_name, border_color=get_c("primary"))),
            ft.Divider(),
            ft.Container(
                bgcolor=get_c("primary"), width=300, padding=15, border_radius=10,
                on_click=lambda e: navigate("notes"),
                content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Icon(ICON_MAP["edit"], color="white"), ft.Text("APRI NOTE", color="white", weight="bold")])
            ),
            ft.Divider(),
            ft.Container(padding=10, content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.Text("Tema Scuro", color=get_c("text"), size=16),
                ft.Switch(value=state["dark"], on_change=toggle_dark, active_color=get_c("primary"))
            ]))
        ])

    def get_notes_content():
        def save_notes(e):
            state["notes"] = e.control.value
            page.client_storage.set("user_notes", e.control.value)

        return ft.Column(expand=True, controls=[
            ft.Container(padding=10, content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: navigate("user")),
                ft.Text("Note", size=20, weight="bold", color=get_c("text")),
                ft.Icon(ICON_MAP["save"], color=get_c("primary"))
            ])),
            ft.Container(
                expand=True, bgcolor=get_c("input_bg"), border_radius=10, padding=15, margin=10,
                content=ft.TextField(value=state["notes"], multiline=True, border=ft.InputBorder.NONE, color=get_c("text"), on_change=save_notes)
            )
        ])

    def get_reader_content():
        title = state["reader_title"]
        content_body = ft.Column(scroll="auto", expand=True)

        if title == "Inno":
            # LOGICA AUDIO
            def toggle_audio(e):
                state["audio_playing"] = not state["audio_playing"]
                if state["audio_playing"]: 
                    audio_player.play()
                    btn_play.icon = ICON_MAP["pause"]
                    btn_play.text = "PAUSA"
                else: 
                    audio_player.pause()
                    btn_play.icon = ICON_MAP["play"]
                    btn_play.text = "PLAY"
                page.update()

            btn_play = ft.ElevatedButton(text="PLAY", icon=ICON_MAP["play"], on_click=toggle_audio, bgcolor=get_c("primary"), color="white")
            content_body.controls.append(ft.Container(padding=20, content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                btn_play,
                ft.Container(height=20),
                ft.Text(LYRICS_TEXT, text_align="center", color=get_c("text"), size=16)
            ])))
        else:
            content_body.controls.append(ft.Container(padding=20, content=ft.Text(f"Qui andrà il contenuto di: {title}", color=get_c("text"))))

        return ft.Column(expand=True, controls=[
            ft.Container(padding=10, content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: navigate("home")),
                ft.Text(title, size=20, weight="bold", color=get_c("text")),
                ft.Container(width=40)
            ])),
            ft.Divider(height=1),
            content_body
        ])

    # --- 5. COMPONENTI STRUTTURALI ---
    
    # Contenitore Centrale (BODY) - Qui avviene la magia del cambio pagina
    body_container = ft.Container(expand=True, padding=0)

    # Header (Solo per Home/User)
    header_container = ft.Container(padding=ft.padding.only(top=30, bottom=10, left=20, right=20))
    
    # Navbar (Solo per Home/User)
    navbar_container = ft.Container()

    # --- 6. NAVIGAZIONE ---
    def navigate(target, data=""):
        state["page"] = target
        if data: state["reader_title"] = data
        update_ui()

    def update_ui():
        # Aggiorna Colori Generali
        page.bgcolor = get_c("bg")
        
        # 1. Costruisci Header (Se serve)
        if state["page"] in ["home", "user"]:
            header_container.content = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, controls=[
                ft.Container(width=60, height=60, bgcolor=get_c("primary"), border_radius=15, alignment=ft.Alignment(0,0), content=ft.Text("M2G", color="white", size=20, weight="bold")),
                ft.Text(f"Bentornato, {state['name']}", size=22, color=get_c("text"))
            ])
            header_container.visible = True
        else:
            header_container.visible = False

        # 2. Costruisci Body (Contenuto centrale)
        body_container.content = None # Svuota il vecchio contenuto
        if state["page"] == "home":
            body_container.content = get_home_content()
            body_container.padding = 20
        elif state["page"] == "user":
            body_container.content = get_user_content()
            body_container.padding = 20
        elif state["page"] == "notes":
            body_container.content = get_notes_content()
            body_container.padding = 0
        elif state["page"] == "reader":
            body_container.content = get_reader_content()
            body_container.padding = 0

        # 3. Costruisci Navbar (Se serve)
        if state["page"] in ["home", "user"]:
            btn_h_bg = get_c("primary") if state["page"] == "home" else get_c("nav_bg")
            btn_h_fg = "white" if state["page"] == "home" else get_c("text")
            btn_u_bg = get_c("primary") if state["page"] == "user" else get_c("nav_bg")
            btn_u_fg = "white" if state["page"] == "user" else get_c("text")

            navbar_container.content = ft.Container(
                padding=15, bgcolor=get_c("nav_bg"),
                border_radius=ft.border_radius.only(top_left=20, top_right=20),
                shadow=ft.BoxShadow(blur_radius=10, color="#11000000"),
                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_h_bg, on_click=lambda e: navigate("home"), content=ft.Row([ft.Icon(ICON_MAP["home"], color=btn_h_fg), ft.Text("HOME", color=btn_h_fg, weight="bold")])),
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_u_bg, on_click=lambda e: navigate("user"), content=ft.Row([ft.Icon(ICON_MAP["user"], color=btn_u_fg), ft.Text("PROFILO", color=btn_u_fg, weight="bold")]))
                ])
            )
            navbar_container.visible = True
        else:
            navbar_container.visible = False

        page.update()

    # LAYOUT PRINCIPALE
    # Usiamo una colonna semplice che si espande. Niente Stack.
    page.add(ft.Column(
        expand=True, 
        spacing=0,
        controls=[
            header_container, # In alto
            body_container,   # Al centro (si espande)
            navbar_container  # In basso
        ]
    ))

    # Primo avvio
    update_ui()

if __name__ == "__main__":
    ft.app(target=main)
