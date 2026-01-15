import flet as ft

# --- VERSIONE 44.0: ASSETS PERSONALIZZATI ---
# 1. Usa IMMAGINI dalla cartella 'assets' invece di icone standard.
# 2. Struttura grafica solida (v43).
# 3. Funzioni Audio/Memoria attive (Lazy Load).

# MAPPA DEI FILE IMMAGINE (Devono essere nella cartella 'assets')
# Se i tuoi file hanno nomi diversi, modificali qui sotto.
IMG_MAP = {
    "sunrise": "sunrise.png",
    "book-open": "book-open.png",
    "music": "music.png",
    "camera": "camera.png",
    "chevron-right": "chevron-right.png", # Se non hai questa, usa ft.icons.CHEVRON_RIGHT nel codice
    "home": "home.png",
    "user": "user.png",
    "edit": "edit.png",
    "play": "play.png",     # Immagine per il tasto Play
    "pause": "pause.png",   # Immagine per il tasto Pausa
    "save": "save.png",
    "arrow-left": "arrow-left.png"
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
    }
}

def main(page: ft.Page):
    # SETUP BASE
    page.title = "M2G App"
    page.padding = 0
    page.spacing = 0
    page.safe_area = ft.SafeArea(content=None)
    page.bgcolor = "#f3f0e9"

    # --- STATO GLOBALE ---
    state = {
        "page": "home",
        "name": "Utente",
        "notes": "",
        "audio_playing": False,
        "reader_title": ""
    }
    
    audio_player = None

    def get_c(key):
        return COLORS["light"][key]

    # --- CARICAMENTO MEMORIA ---
    def load_data_safe():
        try:
            updated = False
            if page.client_storage.contains_key("user_name"):
                state["name"] = page.client_storage.get("user_name")
                updated = True
            if page.client_storage.contains_key("user_notes"):
                state["notes"] = page.client_storage.get("user_notes")
                updated = True
            if updated: render()
        except: pass

    def init_audio():
        nonlocal audio_player
        if audio_player is None:
            try:
                # Carica il file audio (assicurati che inno.mp3 sia in assets o nella root)
                audio_player = ft.Audio(src="inno.mp3", autoplay=False, release_mode="stop")
                page.overlay.append(audio_player)
                page.update()
            except: pass

    # --- HELPERS GRAFICI ---
    
    # Funzione sicura per caricare immagini: se non trova il file, mette un'icona di errore
    def get_asset_image(img_key, width=30, height=30, color=None):
        src_path = IMG_MAP.get(img_key, "")
        return ft.Image(
            src=src_path,
            width=width,
            height=height,
            fit=ft.ImageFit.CONTAIN,
            # Se il colore è specificato (es. per icone monocromatiche), prova ad applicarlo.
            # Se le tue immagini sono colorate (es. png originali), togli 'color' qui sotto.
            color=color, 
            error_content=ft.Icon(ft.icons.BROKEN_IMAGE, color="red") # Se non trova il file
        )

    # --- COSTRUZIONE PAGINE ---

    def build_home():
        lv = ft.ListView(expand=True, spacing=15, padding=20)
        
        # Header
        lv.controls.append(ft.Container(
            padding=ft.padding.only(top=10, bottom=20),
            content=ft.Column(spacing=10, controls=[
                ft.Container(width=60, height=60, bgcolor=get_c("primary"), border_radius=15, alignment=ft.Alignment(0,0), content=ft.Text("M2G", color="white", size=20, weight="bold")),
                ft.Text(f"Bentornato, {state['name']}", size=22, color=get_c("text"))
            ])
        ))

        # Cards
        items = [("Lodi Mattutine", "sunrise"), ("Libretto", "book-open"), ("Inno", "music"), ("Foto ricordo", "camera")]
        for title, img_key in items:
            lv.controls.append(
                ft.Container(
                    bgcolor=get_c("card"), height=80, border_radius=20, padding=15,
                    border=ft.border.all(1, "#eeeeee"),
                    on_click=lambda e, t=title: navigate("reader", t),
                    content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Row(controls=[
                            # QUI CARICHIAMO L'IMMAGINE DAGLI ASSETS
                            ft.Container(
                                width=50, height=50, bgcolor=get_c("icon_bg"), border_radius=15, alignment=ft.Alignment(0,0), 
                                content=get_asset_image(img_key, 28, 28, color=get_c("primary")) # Togli color=... se le icone sono già colorate
                            ),
                            ft.Container(width=10),
                            ft.Text(title, size=16, weight="bold", color=get_c("text"))
                        ]),
                        # Freccia destra (usiamo standard o immagine se ce l'hai)
                        ft.Icon(ft.icons.CHEVRON_RIGHT, color="#cccccc") 
                    ])
                )
            )
        return lv

    def build_user():
        def save_name(e):
            state["name"] = e.control.value
            page.client_storage.set("user_name", e.control.value)

        col = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll="auto")
        col.controls.append(ft.Container(height=40))
        # Immagine profilo da assets
        col.controls.append(get_asset_image("user", 80, 80, color=get_c("primary")))
        col.controls.append(ft.Text("Profilo", size=20, weight="bold", color=get_c("text")))
        col.controls.append(ft.Container(width=280, content=ft.TextField(value=state["name"], label="Nome", border_color=get_c("primary"), on_change=save_name)))
        col.controls.append(ft.Divider())
        
        btn_content = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
            get_asset_image("edit", 20, 20, color="white"), 
            ft.Text("APRI NOTE", color="white", weight="bold")
        ])
        
        col.controls.append(ft.Container(
            bgcolor=get_c("primary"), width=300, padding=15, border_radius=10,
            on_click=lambda e: navigate("notes"),
            content=btn_content
        ))
        col.controls.append(ft.Container(height=50))
        return ft.Container(padding=20, content=col, alignment=ft.alignment.top_center)

    def build_reader(title):
        col = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll="auto")
        
        # Tasto Indietro (usiamo immagine se c'è, altrimenti standard per sicurezza)
        # Se hai arrow-left.png in assets, usa get_asset_image("arrow-left")
        back_btn = ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=get_c("text"), on_click=lambda e: navigate("home"))
        
        col.controls.append(ft.Container(padding=ft.padding.symmetric(horizontal=10, vertical=20), content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
            back_btn,
            ft.Text(title, size=20, weight="bold", color=get_c("text")),
            ft.Container(width=40)
        ])))
        col.controls.append(ft.Divider(height=1))

        if title == "Inno":
            init_audio()
            
            def toggle_audio(e):
                if not audio_player: return
                state["audio_playing"] = not state["audio_playing"]
                # Gestione icone Play/Pause
                icon_img = "pause" if state["audio_playing"] else "play"
                btn_color = "#d9534f" if state["audio_playing"] else get_c("primary")
                btn_text = "PAUSA" if state["audio_playing"] else "RIPRODUCI"
                
                if state["audio_playing"]: audio_player.play()
                else: audio_player.pause()
                
                # Aggiorniamo il bottone
                btn_play.content.controls[0] = get_asset_image(icon_img, 20, 20, color="white")
                btn_play.content.controls[1].value = btn_text
                btn_play.bgcolor = btn_color
                btn_play.update()

            # Bottone Play Custom
            btn_play = ft.Container(
                bgcolor=get_c("primary"), padding=15, border_radius=30, width=160,
                on_click=toggle_audio,
                content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                    get_asset_image("play", 20, 20, color="white"),
                    ft.Text("RIPRODUCI", color="white", weight="bold")
                ])
            )
            
            col.controls.append(btn_play)
            col.controls.append(ft.Text(LYRICS_TEXT, text_align="center", color=get_c("text"), size=16))
        else:
            col.controls.append(ft.Container(padding=20, content=ft.Text(f"Sezione: {title}", color=get_c("text"))))
        
        col.controls.append(ft.Container(height=50))
        return col

    def build_notes():
        def save_notes(e):
            state["notes"] = e.control.value
            page.client_storage.set("user_notes", e.control.value)

        col = ft.Column(spacing=10, expand=True)
        col.controls.append(ft.Container(padding=ft.padding.symmetric(horizontal=10, vertical=20), content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
            ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=get_c("text"), on_click=lambda e: navigate("user")),
            ft.Text("Note", size=20, weight="bold", color=get_c("text")),
            get_asset_image("save", 24, 24, color=get_c("primary"))
        ])))
        col.controls.append(ft.TextField(
            value=state["notes"], multiline=True, expand=True,
            border=ft.InputBorder.NONE, color=get_c("text"), bgcolor="white",
            hint_text="Scrivi qui...", on_change=save_notes, content_padding=20
        ))
        return col

    # --- RENDERER E NAVIGAZIONE ---
    
    body_container = ft.Container(expand=True)
    navbar_container = ft.Container()

    def navigate(target, data=""):
        state["page"] = target
        if data: state["reader_title"] = data
        if target != "reader" and state["audio_playing"] and audio_player:
             audio_player.pause(); state["audio_playing"] = False
        render()

    def render():
        body_container.content = None
        if state["page"] == "home": body_container.content = build_home()
        elif state["page"] == "user": body_container.content = build_user()
        elif state["page"] == "notes": body_container.content = build_notes()
        elif state["page"] == "reader": body_container.content = build_reader(state["reader_title"])

        if state["page"] in ["home", "user"]:
            btn_h_bg = get_c("primary") if state["page"] == "home" else "white"
            btn_h_fg = "white" if state["page"] == "home" else get_c("text")
            btn_u_bg = get_c("primary") if state["page"] == "user" else "white"
            btn_u_fg = "white" if state["page"] == "user" else get_c("text")

            # Navbar con icone assets
            navbar_container.content = ft.Container(
                bgcolor="white", padding=10, 
                border_radius=ft.border_radius.only(top_left=20, top_right=20),
                border=ft.border.only(top=ft.border.BorderSide(1, "#eeeeee")),
                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_h_bg, on_click=lambda e: navigate("home"), 
                                 content=ft.Row([get_asset_image("home", 24, 24, color=btn_h_fg), ft.Text("HOME", color=btn_h_fg, weight="bold")])),
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_u_bg, on_click=lambda e: navigate("user"), 
                                 content=ft.Row([get_asset_image("user", 24, 24, color=btn_u_fg), ft.Text("PROFILO", color=btn_u_fg, weight="bold")]))
                ])
            )
        else:
            navbar_container.content = None
        page.update()

    page.add(ft.Column(expand=True, spacing=0, controls=[body_container, navbar_container]))
    render()
    load_data_safe()

# NOTA FONDAMENTALE: assets_dir="assets" è obbligatorio
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
