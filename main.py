import flet as ft

# --- VERSIONE 46.0: FIX ATTRIBUTO ICONE ---
# 1. ICONE: Usiamo stringhe esplicite (es. "home") invece di costanti (es. ft.icons.HOME).
#    Questo risolve l'AttributeError che hai appena visto.
# 2. SINTASSI: Usiamo ft.Icon("nome") senza "name=" per evitare il vecchio TypeError.
# 3. FUNZIONI: Audio e Memoria attive con caricamento sicuro.

# Mappa icone usando STRINGHE SEMPLICI (Universali)
ICON_MAP = {
    "sunrise": "wb_sunny",
    "book-open": "menu_book",
    "music": "music_note",
    "camera": "photo_camera",
    "chevron-right": "chevron_right",
    "home": "home",
    "user": "person",
    "edit": "edit",
    "play": "play_circle_filled",
    "pause": "pause_circle_filled",
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

    # --- CARICAMENTO MEMORIA (SAFE) ---
    def load_data_safe():
        try:
            updated = False
            if page.client_storage.contains_key("user_name"):
                state["name"] = page.client_storage.get("user_name"); updated = True
            if page.client_storage.contains_key("user_notes"):
                state["notes"] = page.client_storage.get("user_notes"); updated = True
            if updated: render()
        except: pass

    # --- AUDIO (Lazy Load) ---
    def init_audio():
        nonlocal audio_player
        if audio_player is None:
            try:
                # Caricamento audio
                audio_player = ft.Audio(src="inno.mp3", autoplay=False, release_mode="stop")
                page.overlay.append(audio_player)
                page.update()
            except: pass

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
        for title, icon_key in items:
            lv.controls.append(
                ft.Container(
                    bgcolor=get_c("card"), height=80, border_radius=20, padding=15,
                    border=ft.border.all(1, "#eeeeee"),
                    on_click=lambda e, t=title: navigate("reader", t),
                    content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Row(controls=[
                            ft.Container(width=50, height=50, bgcolor=get_c("icon_bg"), border_radius=15, alignment=ft.Alignment(0,0), 
                                         # FIX ICONA: Stringa diretta, no costante, no "name="
                                         content=ft.Icon(ICON_MAP[icon_key], color=get_c("primary"), size=28)),
                            ft.Container(width=10),
                            ft.Text(title, size=16, weight="bold", color=get_c("text"))
                        ]),
                        ft.Icon(ICON_MAP["chevron-right"], color="#cccccc")
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
        # FIX ICONA
        col.controls.append(ft.Icon(ICON_MAP["user"], size=80, color=get_c("primary")))
        col.controls.append(ft.Text("Profilo", size=20, weight="bold", color=get_c("text")))
        col.controls.append(ft.Container(width=280, content=ft.TextField(value=state["name"], label="Nome", border_color=get_c("primary"), on_change=save_name)))
        col.controls.append(ft.Divider())
        
        col.controls.append(ft.Container(
            bgcolor=get_c("primary"), width=300, padding=15, border_radius=10,
            on_click=lambda e: navigate("notes"),
            content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                # FIX ICONA
                ft.Icon(ICON_MAP["edit"], color="white"), 
                ft.Text("APRI NOTE", color="white", weight="bold")
            ])
        ))
        col.controls.append(ft.Container(height=50))
        return ft.Container(padding=20, content=col, alignment=ft.alignment.top_center)

    def build_reader(title):
        col = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll="auto")
        
        # FIX ICONA
        back_btn = ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: navigate("home"))
        
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
                # Gestione icone Play/Pause (stringhe)
                icon_str = ICON_MAP["pause"] if state["audio_playing"] else ICON_MAP["play"]
                color = "#d9534f" if state["audio_playing"] else get_c("primary")
                text = "PAUSA" if state["audio_playing"] else "RIPRODUCI"
                
                if state["audio_playing"]: audio_player.play()
                else: audio_player.pause()
                
                # Aggiornamento UI
                btn_play.content.controls[0].name = icon_str
                btn_play.content.controls[1].value = text
                btn_play.bgcolor = color
                btn_play.update()

            btn_play = ft.Container(
                bgcolor=get_c("primary"), padding=15, border_radius=30, width=160,
                on_click=toggle_audio,
                content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                    # FIX ICONA
                    ft.Icon(ICON_MAP["play"], color="white"),
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
            # FIX ICONA
            ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: navigate("user")),
            ft.Text("Note", size=20, weight="bold", color=get_c("text")),
            # FIX ICONA
            ft.Icon(ICON_MAP["save"], color=get_c("primary"))
        ])))
        col.controls.append(ft.TextField(
            value=state["notes"], multiline=True, expand=True,
            border=ft.InputBorder.NONE, color=get_c("text"), bgcolor="white",
            hint_text="Scrivi qui...", on_change=save_notes, content_padding=20
        ))
        return col

    # --- UI & NAVIGATION ---
    
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

            # Navbar
            navbar_container.content = ft.Container(
                bgcolor="white", padding=10, 
                border_radius=ft.border_radius.only(top_left=20, top_right=20),
                border=ft.border.only(top=ft.border.BorderSide(1, "#eeeeee")),
                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_h_bg, on_click=lambda e: navigate("home"), 
                                 # FIX ICONA
                                 content=ft.Row([ft.Icon(ICON_MAP["home"], color=btn_h_fg), ft.Text("HOME", color=btn_h_fg, weight="bold")])),
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_u_bg, on_click=lambda e: navigate("user"), 
                                 # FIX ICONA
                                 content=ft.Row([ft.Icon(ICON_MAP["user"], color=btn_u_fg), ft.Text("PROFILO", color=btn_u_fg, weight="bold")]))
                ])
            )
        else:
            navbar_container.content = None
        page.update()

    page.add(ft.Column(expand=True, spacing=0, controls=[body_container, navbar_container]))
    render()
    load_data_safe()

if __name__ == "__main__":
    ft.app(target=main)
