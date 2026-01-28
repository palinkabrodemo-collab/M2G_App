import flet as ft

# --- VERSIONE 56.0: RIPRISTINO TOTALE ---
# Obiettivo: Vedere l'app, centrata e funzionante.
# 1. NO IMMAGINI (Solo icone native per ora, per evitare crash).
# 2. SafeArea (Per inquadrare tutto bene nello schermo).
# 3. ListView (Per evitare schermo grigio e permettere lo scroll).

# Icone Native (Sicure al 100%)
ICON_MAP = {
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
...
(Testo presente)
"""

COLORS = {
    "bg": "#f3f0e9", 
    "primary": "#6a8a73", 
    "text": "#1a1a1a", 
    "card": "white", 
    "icon_bg": "#dbe4de"
}

def main(page: ft.Page):
    # --- SETUP FONDAMENTALE ---
    page.title = "M2G App"
    page.bgcolor = COLORS["bg"]
    page.padding = 0
    # SafeArea: Questo risolve il problema che le cose non erano "inquadrate"
    page.safe_area = ft.SafeArea(content=None) 
    # Theme: Forziamo colori chiari per evitare problemi di lettura
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- STATO ---
    state = {
        "page": "home",
        "name": "Utente",
        "notes": "",
        "audio_playing": False,
        "reader_title": ""
    }
    
    audio_player = None

    # --- MEMORIA (Semplificata) ---
    def load_memory():
        try:
            if page.client_storage.contains_key("user_name"):
                state["name"] = page.client_storage.get("user_name")
            if page.client_storage.contains_key("user_notes"):
                state["notes"] = page.client_storage.get("user_notes")
        except: pass

    # --- AUDIO (Protetto) ---
    def init_audio():
        nonlocal audio_player
        if audio_player is None:
            try:
                audio_player = ft.Audio(src="inno.mp3", autoplay=False, release_mode="stop")
                page.overlay.append(audio_player)
                page.update()
            except: pass

    # --- NAVIGAZIONE ---
    def navigate(target, data=""):
        state["page"] = target
        if data: state["reader_title"] = data
        if target != "reader" and state["audio_playing"] and audio_player:
             audio_player.pause(); state["audio_playing"] = False
        render()

    # --- COSTRUTTORI ---
    
    def build_card(title, icon_key):
        # Card semplice e robusta
        return ft.Container(
            bgcolor=COLORS["card"],
            height=80,
            border_radius=15,
            padding=15,
            on_click=lambda e: navigate("reader", title),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(controls=[
                        ft.Container(
                            width=50, height=50, 
                            bgcolor=COLORS["icon_bg"], 
                            border_radius=12, 
                            alignment=ft.alignment.center,
                            content=ft.Icon(ICON_MAP[icon_key], color=COLORS["primary"], size=24)
                        ),
                        ft.Container(width=10),
                        ft.Text(title, size=16, weight="bold", color=COLORS["text"])
                    ]),
                    ft.Icon("chevron_right", color="#cccccc")
                ]
            )
        )

    def get_view_controls():
        controls = []
        
        # 1. HOME
        if state["page"] == "home":
            # Header
            controls.append(ft.Container(height=20))
            controls.append(ft.Column(spacing=5, controls=[
                ft.Container(
                    width=60, height=60, bgcolor=COLORS["primary"], 
                    border_radius=15, alignment=ft.alignment.center,
                    content=ft.Text("M2G", color="white", size=20, weight="bold")
                ),
                ft.Text(f"Bentornato, {state['name']}", size=22, weight="bold", color=COLORS["text"])
            ]))
            controls.append(ft.Container(height=20))
            
            # Cards
            controls.append(build_card("Lodi Mattutine", "sunrise"))
            controls.append(ft.Container(height=10))
            controls.append(build_card("Libretto", "book-open"))
            controls.append(ft.Container(height=10))
            controls.append(build_card("Inno", "music"))
            controls.append(ft.Container(height=10))
            controls.append(build_card("Foto ricordo", "camera"))
            
            controls.append(ft.Container(height=30))
            
            # Navbar simulata (Bottoni semplici)
            controls.append(ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                 ft.ElevatedButton("PROFILO", icon="person", on_click=lambda e: navigate("user"), bgcolor=COLORS["primary"], color="white")
            ]))

        # 2. USER
        elif state["page"] == "user":
            def save_name(e):
                state["name"] = e.control.value
                page.client_storage.set("user_name", e.control.value)

            controls.append(ft.Container(height=20))
            controls.append(ft.Icon("person", size=80, color=COLORS["primary"]))
            controls.append(ft.Text("Profilo", size=20, weight="bold", color=COLORS["text"]))
            controls.append(ft.Container(height=20))
            controls.append(ft.TextField(value=state["name"], label="Nome", on_change=save_name))
            controls.append(ft.Container(height=20))
            controls.append(ft.ElevatedButton("APRI NOTE", icon="edit", bgcolor=COLORS["primary"], color="white", on_click=lambda e: navigate("notes")))
            controls.append(ft.Container(height=20))
            controls.append(ft.ElevatedButton("TORNA ALLA HOME", icon="home", on_click=lambda e: navigate("home")))

        # 3. READER
        elif state["page"] == "reader":
            title = state["reader_title"]
            controls.append(ft.Row(controls=[
                ft.IconButton(icon="arrow_back", on_click=lambda e: navigate("home")),
                ft.Text(title, size=20, weight="bold")
            ]))
            controls.append(ft.Divider())
            
            if title == "Inno":
                init_audio()
                def toggle(e):
                    if not audio_player: return
                    state["audio_playing"] = not state["audio_playing"]
                    if state["audio_playing"]: audio_player.play()
                    else: audio_player.pause()
                    render()

                icon = "pause" if state["audio_playing"] else "play_arrow"
                text = "PAUSA" if state["audio_playing"] else "RIPRODUCI"
                
                controls.append(ft.Container(height=20))
                controls.append(ft.ElevatedButton(text, icon=icon, bgcolor=COLORS["primary"], color="white", on_click=toggle))
                controls.append(ft.Container(height=20))
                controls.append(ft.Text(LYRICS_TEXT, text_align="center"))
            else:
                controls.append(ft.Text(f"Contenuto di {title}"))

        # 4. NOTES
        elif state["page"] == "notes":
            def save_notes(e):
                state["notes"] = e.control.value
                page.client_storage.set("user_notes", e.control.value)
            
            controls.append(ft.Row(controls=[
                ft.IconButton(icon="arrow_back", on_click=lambda e: navigate("user")),
                ft.Text("Note", size=20, weight="bold"),
                ft.Icon("save", color=COLORS["primary"])
            ]))
            controls.append(ft.TextField(value=state["notes"], multiline=True, min_lines=10, on_change=save_notes))

        return controls

    def render():
        page.clean()
        
        # STRUTTURA INDISTRUTTIBILE
        # SafeArea -> Container (Padding) -> ListView (Scroll) -> Column (Contenuto)
        # Questo garantisce che tutto sia visibile e scrollabile.
        
        page.add(
            ft.SafeArea(
                ft.Container(
                    padding=20,
                    expand=True,
                    content=ft.ListView(
                        expand=True,
                        spacing=10,
                        controls=get_view_controls()
                    )
                )
            )
        )
        page.update()

    # START
    load_memory()
    render()

if __name__ == "__main__":
    ft.app(target=main)
