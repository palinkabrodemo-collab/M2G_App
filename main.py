import flet as ft

# --- VERSIONE 50.0: PURE CODE (SENZA ASSETS ESTERNI) ---
# QUESTA VERSIONE NON CERCA FILE. NON PUÒ FALLIRE IL CARICAMENTO.
# Usiamo icone native colorate al posto delle immagini PNG per ora.
# Obiettivo: Vedere l'app accesa e funzionante.

# Mappa Icone Native (Sicure al 100%)
ICON_MAP = {
    "sunrise": ft.icons.WB_SUNNY,
    "book-open": ft.icons.MENU_BOOK,
    "music": ft.icons.MUSIC_NOTE,
    "camera": ft.icons.PHOTO_CAMERA,
    "chevron-right": ft.icons.CHEVRON_RIGHT,
    "home": ft.icons.HOME,
    "user": ft.icons.PERSON,
    "edit": ft.icons.EDIT,
    "play": ft.icons.PLAY_CIRCLE_FILLED,
    "pause": ft.icons.PAUSE_CIRCLE_FILLED,
    "save": ft.icons.SAVE,
    "arrow-left": ft.icons.ARROW_BACK
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
    # 1. SETUP MINIMALE (Anti-Crash)
    page.title = "M2G App"
    page.bgcolor = "#f3f0e9"
    page.padding = 0
    page.spacing = 0
    page.safe_area = ft.SafeArea(content=None)
    
    # 2. SCROLL NATIVO (Anti-Grigio)
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

    # --- MEMORIA (Lazy Load) ---
    def load_memory():
        try:
            updated = False
            if page.client_storage.contains_key("user_name"):
                state["name"] = page.client_storage.get("user_name"); updated = True
            if page.client_storage.contains_key("user_notes"):
                state["notes"] = page.client_storage.get("user_notes"); updated = True
            if updated: render()
        except: pass

    # --- AUDIO (Safe) ---
    def init_audio():
        nonlocal audio_player
        if audio_player is None:
            try:
                # Se il file non c'è, darà errore in console ma l'app resta accesa
                audio_player = ft.Audio(src="inno.mp3", autoplay=False, release_mode="stop")
                page.overlay.append(audio_player)
                page.update()
            except: pass

    # --- COSTRUTTORI ---

    def build_home():
        col = ft.Column(spacing=15)
        
        # Header
        col.controls.append(ft.Container(
            padding=ft.padding.only(top=20, bottom=20),
            content=ft.Column(spacing=10, controls=[
                ft.Container(width=60, height=60, bgcolor=get_c("primary"), border_radius=15, alignment=ft.Alignment(0,0), content=ft.Text("M2G", color="white", size=20, weight="bold")),
                ft.Text(f"Bentornato, {state['name']}", size=22, color=get_c("text"))
            ])
        ))

        # Cards con ICONE NATIVE (No png)
        items = [("Lodi Mattutine", "sunrise"), ("Libretto", "book-open"), ("Inno", "music"), ("Foto ricordo", "camera")]
        for title, icon_key in items:
            col.controls.append(
                ft.Container(
                    bgcolor=get_c("card"), height=80, border_radius=20, padding=15,
                    border=ft.border.all(1, "#eeeeee"),
                    on_click=lambda e, t=title: navigate("reader", t),
                    content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Row(controls=[
                            ft.Container(width=50, height=50, bgcolor=get_c("icon_bg"), border_radius=15, alignment=ft.Alignment(0,0), 
                                         content=ft.Icon(ICON_MAP[icon_key], size=28, color=get_c("primary"))),
                            ft.Container(width=10),
                            ft.Text(title, size=16, weight="bold", color=get_c("text"))
                        ]),
                        ft.Icon(ft.icons.CHEVRON_RIGHT, color="#cccccc")
                    ])
                )
            )
        
        col.controls.append(ft.Container(height=100))
        col.controls[0].on_click = lambda e: load_memory()
        return ft.Container(padding=20, content=col)

    def build_user():
        col = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        col.controls.append(ft.Container(height=40))
        col.controls.append(ft.Icon(ft.icons.PERSON, size=80, color=get_c("primary")))
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
                ft.Icon(ft.icons.EDIT, color="white"), 
                ft.Text("APRI NOTE", color="white", weight="bold")
            ])
        ))
        col.controls.append(ft.Container(height=100))
        return ft.Container(padding=20, content=col, alignment=ft.alignment.top_center)

    def build_reader(title):
        col = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
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
                icon = ft.icons.PAUSE if state["audio_playing"] else ft.icons.PLAY_ARROW
                color = "#d9534f" if state["audio_playing"] else get_c("primary")
                text = "PAUSA" if state["audio_playing"] else "RIPRODUCI"
                
                if state["audio_playing"]: audio_player.play()
                else: audio_player.pause()
                
                btn_play.content.controls[0].name = icon
                btn_play.content.controls[1].value = text
                btn_play.bgcolor = color
                btn_play.update()

            btn_play = ft.Container(
                bgcolor=get_c("primary"), padding=15, border_radius=30, width=160,
                on_click=toggle_audio,
                content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                    ft.Icon(ft.icons.PLAY_ARROW, color="white"),
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
            ft.IconButton(icon=ft.icons.ARROW_BACK, icon_color=get_c("text"), on_click=lambda e: navigate("user")),
            ft.Text("Note", size=20, weight="bold", color=get_c("text")),
            ft.Icon(ft.icons.SAVE, color=get_c("primary"))
        ])))
        col.controls.append(ft.TextField(
            value=state["notes"], multiline=True, min_lines=15,
            border=ft.InputBorder.NONE, color=get_c("text"), bgcolor="white",
            hint_text="Scrivi qui...", on_change=save_notes, content_padding=20
        ))
        return ft.Container(padding=10, content=col)

    # --- RENDERER ---
    
    def navigate(target, data=""):
        state["page"] = target
        if data: state["reader_title"] = data
        if target != "reader" and state["audio_playing"] and audio_player:
             audio_player.pause(); state["audio_playing"] = False
        render()

    def render():
        page.clean()
        
        # CONTENUTO
        if state["page"] == "home": page.add(build_home())
        elif state["page"] == "user": page.add(build_user())
        elif state["page"] == "notes": page.add(build_notes())
        elif state["page"] == "reader": page.add(build_reader(state["reader_title"]))

        # NAVBAR (Overlay)
        page.overlay.clear()
        if state["audio_playing"] and audio_player: page.overlay.append(audio_player)

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
                                 content=ft.Row([ft.Icon(ft.icons.HOME, color=btn_h_fg), ft.Text("HOME", color=btn_h_fg, weight="bold")])),
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_u_bg, on_click=lambda e: navigate("user"), 
                                 content=ft.Row([ft.Icon(ft.icons.PERSON, color=btn_u_fg), ft.Text("PROFILO", color=btn_u_fg, weight="bold")]))
                ])
            )
            page.overlay.append(ft.Container(content=navbar, alignment=ft.alignment.bottom_center))
        
        page.update()

    render()
    load_memory()

if __name__ == "__main__":
    ft.app(target=main)
