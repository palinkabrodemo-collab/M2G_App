import flet as ft

# --- VERSIONE 49.0: NATIVE SCROLL (FIX DEFINITIVO) ---
# 1. Rimosso lo Stack (causa schermo bianco).
# 2. Attivato page.scroll = "auto" (risolve lo schermo grigio).
# 3. Assets con fallback automatico (se manca l'immagine, usa l'icona).

# Mappa Immagini (File in assets)
IMG_MAP = {
    "sunrise": "sunrise.png",
    "book-open": "book-open.png",
    "music": "music.png",
    "camera": "camera.png",
    "chevron-right": "chevron-right.png",
    "home": "home.png",
    "user": "user.png",
    "edit": "edit.png",
    "play": "play.png",
    "pause": "pause.png",
    "save": "save.png",
    "arrow-left": "arrow-left.png"
}

# Icone di riserva (Se l'immagine fallisce, usa queste)
FALLBACK_ICONS = {
    "sunrise": "wb_sunny",
    "book-open": "menu_book",
    "music": "music_note",
    "camera": "photo_camera",
    "chevron-right": "chevron_right",
    "home": "home",
    "user": "person",
    "edit": "edit",
    "play": "play_arrow",
    "pause": "pause",
    "save": "save",
    "arrow-left": "arrow_back"
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
    # 1. SETUP
    page.title = "M2G App"
    page.bgcolor = "#f3f0e9"
    page.padding = 0
    page.spacing = 0
    page.safe_area = ft.SafeArea(content=None)
    
    # --- IL SEGRETO DEL LAYOUT ---
    # Questo abilita lo scroll nativo del telefono.
    # Risolve il problema "schermo grigio" senza usare Stack complessi.
    page.scroll = "auto"

    # --- STATO ---
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
    def load_memory():
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

    # --- AUDIO ---
    def init_audio():
        nonlocal audio_player
        if audio_player is None:
            try:
                audio_player = ft.Audio(src="inno.mp3", autoplay=False, release_mode="stop")
                page.overlay.append(audio_player)
                page.update()
            except: pass

    # --- CARICATORE ICONE IBRIDO ---
    def get_icon(key, size=30, color=None):
        """
        Tenta di caricare l'immagine PNG.
        Se fallisce, carica l'icona standard.
        """
        img_src = IMG_MAP.get(key, "")
        fallback = FALLBACK_ICONS.get(key, "error")
        
        return ft.Image(
            src=img_src,
            width=size,
            height=size,
            fit=ft.ImageFit.CONTAIN,
            color=color,
            # Se l'immagine non c'è, mostra l'icona invece del crash
            error_content=ft.Icon(name=fallback, size=size, color=color)
        )

    # --- COSTRUTTORI ---

    def build_home():
        # Colonna semplice, lo scroll è gestito dalla Pagina (page.scroll)
        col = ft.Column(spacing=15)
        
        # Header
        col.controls.append(ft.Container(
            padding=ft.padding.only(top=20, bottom=20),
            content=ft.Column(spacing=10, controls=[
                ft.Container(width=60, height=60, bgcolor=get_c("primary"), border_radius=15, alignment=ft.Alignment(0,0), content=ft.Text("M2G", color="white", size=20, weight="bold")),
                ft.Text(f"Bentornato, {state['name']}", size=22, color=get_c("text"))
            ])
        ))

        # Cards
        items = [("Lodi Mattutine", "sunrise"), ("Libretto", "book-open"), ("Inno", "music"), ("Foto ricordo", "camera")]
        for title, key in items:
            col.controls.append(
                ft.Container(
                    bgcolor=get_c("card"), height=80, border_radius=20, padding=15,
                    border=ft.border.all(1, "#eeeeee"),
                    on_click=lambda e, t=title: navigate("reader", t),
                    content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Row(controls=[
                            ft.Container(width=50, height=50, bgcolor=get_c("icon_bg"), border_radius=15, alignment=ft.Alignment(0,0), 
                                         content=get_icon(key, 28, get_c("primary"))),
                            ft.Container(width=10),
                            ft.Text(title, size=16, weight="bold", color=get_c("text"))
                        ]),
                        ft.Icon(name="chevron_right", color="#cccccc")
                    ])
                )
            )
        
        # Spazio per la navbar
        col.controls.append(ft.Container(height=100))
        
        # Trigger memoria al click sul titolo (Debug sicuro)
        col.controls[0].on_click = lambda e: load_memory()

        return ft.Container(padding=20, content=col)

    def build_user():
        col = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        col.controls.append(ft.Container(height=40))
        col.controls.append(get_icon("user", 80, get_c("primary")))
        col.controls.append(ft.Text("Profilo", size=20, weight="bold", color=get_c("text")))
        
        def save_name(e):
            state["name"] = e.control.value
            page.client_storage.set("user_name", e.control.value)

        col.controls.append(ft.Container(width=280, content=ft.TextField(value=state["name"], label="Nome", border_color=get_c("primary"), on_change=save_name)))
        col.controls.append(ft.Divider())
        
        col.controls.append(ft.Container(
            bgcolor=get_c("primary"), width=300, padding=15, border_radius=10,
            on_click=lambda e: navigate("notes"),
            content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                get_icon("edit", 20, "white"), 
                ft.Text("APRI NOTE", color="white", weight="bold")
            ])
        ))
        col.controls.append(ft.Container(height=100))
        return ft.Container(padding=20, content=col, alignment=ft.alignment.top_center)

    def build_reader(title):
        col = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        back_btn = ft.IconButton(icon="arrow_back", icon_color=get_c("text"), on_click=lambda e: navigate("home"))
        
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
                
                key = "pause" if state["audio_playing"] else "play"
                color = "#d9534f" if state["audio_playing"] else get_c("primary")
                text = "PAUSA" if state["audio_playing"] else "RIPRODUCI"
                
                if state["audio_playing"]: audio_player.play()
                else: audio_player.pause()
                
                btn_play.content.controls[0] = get_icon(key, 20, "white")
                btn_play.content.controls[1].value = text
                btn_play.bgcolor = color
                btn_play.update()

            btn_play = ft.Container(
                bgcolor=get_c("primary"), padding=15, border_radius=30, width=160,
                on_click=toggle_audio,
                content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                    get_icon("play", 20, "white"),
                    ft.Text("RIPRODUCI", color="white", weight="bold")
                ])
            )
            col.controls.append(btn_play)
            col.controls.append(ft.Text(LYRICS_TEXT, text_align="center", color=get_c("text"), size=16))
        else:
            col.controls.append(ft.Container(padding=20, content=ft.Text(f"Sezione: {title}", color=get_c("text"))))
        
        col.controls.append(ft.Container(height=50))
        return ft.Container(content=col)

    def build_notes():
        def save_notes(e):
            state["notes"] = e.control.value
            page.client_storage.set("user_notes", e.control.value)

        col = ft.Column(spacing=10)
        col.controls.append(ft.Container(padding=ft.padding.symmetric(horizontal=10, vertical=20), content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
            ft.IconButton(icon="arrow_back", icon_color=get_c("text"), on_click=lambda e: navigate("user")),
            ft.Text("Note", size=20, weight="bold", color=get_c("text")),
            get_icon("save", 24, get_c("primary"))
        ])))
        col.controls.append(ft.TextField(
            value=state["notes"], multiline=True, min_lines=15,
            border=ft.InputBorder.NONE, color=get_c("text"), bgcolor="white",
            hint_text="Scrivi qui...", on_change=save_notes, content_padding=20
        ))
        return ft.Container(padding=10, content=col)

    # --- RENDERER ---
    
    # Overlay per la Navbar (resta fissa in basso sopra lo scroll)
    page.overlay.clear()

    def navigate(target, data=""):
        state["page"] = target
        if data: state["reader_title"] = data
        if target != "reader" and state["audio_playing"] and audio_player:
             audio_player.pause(); state["audio_playing"] = False
        render()

    def render():
        page.clean() # Pulisce tutto il contenuto precedente

        # 1. Contenuto Principale
        if state["page"] == "home": page.add(build_home())
        elif state["page"] == "user": page.add(build_user())
        elif state["page"] == "notes": page.add(build_notes())
        elif state["page"] == "reader": page.add(build_reader(state["reader_title"]))

        # 2. Navbar (Gestita tramite Overlay per stare sempre sopra)
        # Nota: L'overlay non si cancella con page.clean(), quindi lo gestiamo qui.
        page.overlay.clear()
        if state["audio_playing"] and audio_player: page.overlay.append(audio_player) # Mantiene audio

        if state["page"] in ["home", "user"]:
            btn_h_bg = get_c("primary") if state["page"] == "home" else "white"
            btn_h_fg = "white" if state["page"] == "home" else get_c("text")
            btn_u_bg = get_c("primary") if state["page"] == "user" else "white"
            btn_u_fg = "white" if state["page"] == "user" else get_c("text")

            navbar = ft.Container(
                bgcolor="white", padding=10, 
                border_radius=ft.border_radius.only(top_left=20, top_right=20),
                border=ft.border.only(top=ft.border.BorderSide(1, "#eeeeee")),
                shadow=ft.BoxShadow(blur_radius=10, color=ft.colors.with_opacity(0.1, "black")),
                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_h_bg, on_click=lambda e: navigate("home"), 
                                 content=ft.Row([get_icon("home", 24, btn_h_fg), ft.Text("HOME", color=btn_h_fg, weight="bold")])),
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_u_bg, on_click=lambda e: navigate("user"), 
                                 content=ft.Row([get_icon("user", 24, btn_u_fg), ft.Text("PROFILO", color=btn_u_fg, weight="bold")]))
                ])
            )
            # Posizioniamo la navbar fissa in basso
            page.overlay.append(ft.Container(content=navbar, alignment=ft.alignment.bottom_center))

        page.update()

    # Avvio
    render()
    load_memory()

if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
