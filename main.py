import flet as ft

# --- VERSIONE 35.0: CODICE COMPLETO (TESTI INTEGRALI) ---
# Nessun taglio al testo.
# Architettura "Swap" per risolvere i rettangoli grigi.
# Funzionalità Audio e Memoria attive.

# --- 1. DATI E COSTANTI ---

# Liste per le immagini (da riempire con i nomi dei file se li hai)
BOOKS_DATA = {
    "Lodi Mattutine": ["lodi1.jpg", "lodi2.jpg", "lodi3.jpg", "lodi4.jpg", "lodi5.jpg"],
    "Libretto": ["lib1.jpg", "lib2.jpg", "lib3.jpg", "lib4.jpg", "lib5.jpg"],
    "Foto ricordo": [] 
}

# Icone sicure (stringhe)
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

# TESTO COMPLETO (Senza tagli)
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

Sono l'eroe
Che ucciderà i mostri
Sotto al tuo letto
Mentre riposi
E non importa se non dormirò
Li distruggo tutti e poi ripartirò (oooh)
(Dammi il tuo cuore baby)

"Hey pronto amore mio perché non vieni qui a casa mia?
Sono da sola... c'è la mia coperta calda che ti piace tanto, 
i pop corn... e poi guardiamo un film... dai che ho il ciclo 
e non mi sento tanto bene... allora ciao, a dopo amore..."

Sono le nove e fuori piove
Anche stasera un segone
Te l'ho detto
Se hai le mestruazioni non mi cercare
Se poi arrivo
E non possiamo più nemmeno scopare
Eppure sai che c'è
Sperimentiamo
Analizziamo
Di orifizi tu ne hai tre
Quando sto con te mi diventa duro
Mi devi dare il culo
Non lo diciamo a nessuno
Sborro come Nettuno

Sono l'eroe
Che ucciderà i mostri
Sotto al tuo letto
Mentre riposi
E non importa se non me la dai
Ti distruggo il culo mentre dormirai

Sono l'eroe
Che ucciderà i mostri
Sotto al tuo letto
Mentre riposi
E non importa se non me la dai
Ti distruggo il culo mentre dormirai

Sono l'eroe
Che ucciderà i mostri
Sotto al tuo letto
Mentre riposi
E non importa se non me la dai
Ti distruggo il culo mentre dormirai
E non importa
"""

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
    # SETUP PAGINA
    page.title = "M2G App"
    page.padding = 0
    page.spacing = 0
    page.safe_area = ft.SafeArea(content=None)
    page.bgcolor = "white"

    # AUDIO
    audio_player = ft.Audio(src="inno.mp3", autoplay=False, release_mode="stop")
    page.overlay.append(audio_player)

    # --- 2. STATO DELL'APP (MEMORIA) ---
    state = {
        "page": "home",
        "name": "Utente",
        "notes": "",
        "dark": False,
        "reader_title": "",
        "audio_playing": False
    }

    # Caricamento sicuro dati
    try:
        if page.client_storage.contains_key("user_name"):
            state["name"] = page.client_storage.get("user_name")
        if page.client_storage.contains_key("user_notes"):
            state["notes"] = page.client_storage.get("user_notes")
        if page.client_storage.contains_key("dark_mode"):
            state["dark"] = page.client_storage.get("dark_mode")
    except:
        pass # Se fallisce, usa i default

    def get_c(key):
        return COLORS["dark" if state["dark"] else "light"][key]

    # --- 3. COSTRUTTORI PAGINE ---

    def build_home():
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
        col.controls.append(ft.Container(height=20))
        return col

    def build_user():
        def save_name(e):
            state["name"] = e.control.value
            page.client_storage.set("user_name", e.control.value)
            header_title.value = f"Bentornato, {state['name']}"
            header_title.update()
        
        def toggle_dark(e):
            state["dark"] = e.control.value
            page.client_storage.set("dark_mode", e.control.value)
            update_ui() 

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

    def build_notes():
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

    def build_reader():
        title = state["reader_title"]
        content_body = ft.Column(scroll="auto", expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        if title == "Inno":
            # LOGICA AUDIO E TESTO INNO
            def toggle_audio(e):
                state["audio_playing"] = not state["audio_playing"]
                if state["audio_playing"]: 
                    audio_player.play()
                    btn_play.icon = ICON_MAP["pause"]
                    btn_play.text = "PAUSA"
                    btn_play.bgcolor = "#d9534f"
                else: 
                    audio_player.pause()
                    btn_play.icon = ICON_MAP["play"]
                    btn_play.text = "PLAY"
                    btn_play.bgcolor = get_c("primary")
                page.update()

            btn_play = ft.ElevatedButton(text="PLAY", icon=ICON_MAP["play"], on_click=toggle_audio, bgcolor=get_c("primary"), color="white")
            
            content_body.controls.append(ft.Container(padding=20, content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                btn_play,
                ft.Container(height=20),
                ft.Text(LYRICS_TEXT, text_align="center", color=get_c("text"), size=16)
            ])))
        
        else:
            # LOGICA IMMAGINI (Lodi, Libretto, Foto)
            # Se ci sono immagini nella lista BOOKS_DATA, le mostriamo
            images_list = BOOKS_DATA.get(title, [])
            
            if not images_list and title == "Foto ricordo":
                 content_body.controls.append(ft.Container(padding=20, content=ft.Text("Galleria foto non ancora caricata.", color=get_c("text"))))
            elif not images_list:
                 content_body.controls.append(ft.Container(padding=20, content=ft.Text(f"Nessuna pagina trovata per {title}.", color=get_c("text"))))
            else:
                for img_name in images_list:
                    # Carichiamo l'immagine. Flet cercherà automaticamente in 'assets'
                    # Se non le trova, mostrerà un'icona di errore ma non crasherà l'app
                    content_body.controls.append(
                        ft.Image(src=img_name, width=400, fit=ft.ImageFit.CONTAIN, error_content=ft.Text("Immagine non trovata"))
                    )
                    content_body.controls.append(ft.Container(height=10))

        return ft.Column(expand=True, controls=[
            ft.Container(padding=10, content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: navigate("home")),
                ft.Text(title, size=20, weight="bold", color=get_c("text")),
                ft.Container(width=40)
            ])),
            ft.Divider(height=1),
            content_body
        ])

    # --- 4. GESTIONE NAVIGAZIONE E UI ---
    
    header_title = ft.Text("", size=22, weight="w400")
    header_container = ft.Container(padding=ft.padding.only(top=30, bottom=10, left=20, right=20))
    body_container = ft.Container(expand=True, padding=0) 
    navbar_container = ft.Container()

    def navigate(target, data=""):
        state["page"] = target
        if data: state["reader_title"] = data
        
        # Se usciamo dall'inno, fermiamo l'audio per sicurezza
        if target != "reader" and state["audio_playing"]:
             audio_player.pause()
             state["audio_playing"] = False

        update_ui()

    def update_ui():
        page.bgcolor = get_c("bg")
        header_title.color = get_c("text")
        header_title.value = f"Bentornato, {state['name']}"

        # 1. HEADER
        if state["page"] in ["home", "user"]:
            header_container.content = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, controls=[
                ft.Container(width=60, height=60, bgcolor=get_c("primary"), border_radius=15, alignment=ft.Alignment(0,0), content=ft.Text("M2G", color="white", size=20, weight="bold")),
                header_title
            ])
            header_container.visible = True
        else:
            header_container.visible = False

        # 2. BODY (SWAP)
        body_container.content = None 
        
        if state["page"] == "home":
            body_container.content = build_home()
            body_container.padding = 20
        elif state["page"] == "user":
            body_container.content = build_user()
            body_container.padding = 20
        elif state["page"] == "notes":
            body_container.content = build_notes()
            body_container.padding = 0
        elif state["page"] == "reader":
            body_container.content = build_reader()
            body_container.padding = 0

        # 3. NAVBAR
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

    page.add(ft.Column(expand=True, spacing=0, controls=[header_container, body_container, navbar_container]))
    update_ui()

if __name__ == "__main__":
    ft.app(target=main)
