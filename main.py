import flet as ft

# --- VERSIONE 37.0: COMPONENTI NATIVI (SOLUZIONE DEFINITIVA) ---
# Abbandoniamo i Container manuali che causano il blocco grigio.
# Usiamo page.appbar (sopra) e page.navigation_bar (sotto).
# Il contenuto centrale (body) sarà libero da interferenze grafiche.

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

# TESTO COMPLETO
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
    # 1. SETUP BASE
    page.title = "M2G App"
    page.theme_mode = ft.ThemeMode.LIGHT # Forziamo Light all'inizio per sicurezza
    page.padding = 10 # Un po' di margine per non attaccare ai bordi
    page.spacing = 10

    # AUDIO (Definito ma parte in stop)
    audio_player = ft.Audio(src="inno.mp3", autoplay=False, release_mode="stop")
    page.overlay.append(audio_player)

    # 2. STATO (Memoria)
    state = {
        "name": "Utente",
        "notes": "",
        "dark": False,
        "audio_playing": False
    }

    # Caricamento sicuro (dentro Try-Except per evitare blocchi)
    try:
        if page.client_storage.contains_key("user_name"):
            state["name"] = page.client_storage.get("user_name")
        if page.client_storage.contains_key("user_notes"):
            state["notes"] = page.client_storage.get("user_notes")
        if page.client_storage.contains_key("dark_mode"):
            state["dark"] = page.client_storage.get("dark_mode")
            page.theme_mode = ft.ThemeMode.DARK if state["dark"] else ft.ThemeMode.LIGHT
    except:
        pass

    def get_c(key):
        return COLORS["dark" if state["dark"] else "light"][key]

    # --- 3. DEFINIZIONE DELLE VISTE (CONTENUTO) ---

    def view_home():
        # Usiamo ListView invece di Column: è più sicuro contro i glitch grafici su Android
        lv = ft.ListView(expand=True, spacing=15)
        
        items = [("Lodi Mattutine", "sunrise"), ("Libretto", "book-open"), ("Inno", "music"), ("Foto ricordo", "camera")]
        
        for title, icon in items:
            lv.controls.append(
                ft.Container(
                    bgcolor=get_c("card"), height=80, border_radius=20, padding=15,
                    shadow=ft.BoxShadow(blur_radius=5, color="#11000000", offset=ft.Offset(0,4)),
                    on_click=lambda e, t=title: navigate_to_reader(t),
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
        return lv

    def view_user():
        def save_name(e):
            state["name"] = e.control.value
            page.client_storage.set("user_name", e.control.value)
            page.appbar.title.value = f"Bentornato, {state['name']}" # Aggiorna titolo
            page.update()

        def toggle_dark(e):
            state["dark"] = e.control.value
            page.client_storage.set("dark_mode", e.control.value)
            page.theme_mode = ft.ThemeMode.DARK if state["dark"] else ft.ThemeMode.LIGHT
            navigate_to_tab(1) # Ricarica pagina profilo

        return ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, scroll="auto", controls=[
            ft.Container(height=10),
            ft.Icon("person", size=80, color=get_c("primary")),
            ft.Text("Il tuo Profilo", size=20, weight="bold", color=get_c("text")),
            ft.TextField(value=state["name"], label="Nome", on_change=save_name, border_color=get_c("primary")),
            ft.Divider(),
            ft.ElevatedButton("APRI NOTE", icon=ICON_MAP["edit"], bgcolor=get_c("primary"), color="white", on_click=lambda e: navigate_to_notes()),
            ft.Divider(),
            ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.Text("Tema Scuro", color=get_c("text"), size=16),
                ft.Switch(value=state["dark"], on_change=toggle_dark, active_color=get_c("primary"))
            ])
        ])

    def view_notes():
        def save_notes(e):
            state["notes"] = e.control.value
            page.client_storage.set("user_notes", e.control.value)

        # TextField che occupa tutto lo spazio disponibile
        return ft.TextField(
            value=state["notes"], 
            multiline=True, 
            expand=True, 
            border=ft.InputBorder.NONE, 
            bgcolor=get_c("input_bg"),
            color=get_c("text"), 
            on_change=save_notes,
            hint_text="Scrivi qui le tue note..."
        )

    def view_reader(title):
        content = ft.Column(scroll="auto", expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        if title == "Inno":
            def toggle_audio(e):
                state["audio_playing"] = not state["audio_playing"]
                if state["audio_playing"]: 
                    audio_player.play()
                    btn_play.text = "PAUSA"
                    btn_play.icon = ICON_MAP["pause"]
                    btn_play.bgcolor = "red"
                else: 
                    audio_player.pause()
                    btn_play.text = "PLAY"
                    btn_play.icon = ICON_MAP["play"]
                    btn_play.bgcolor = get_c("primary")
                btn_play.update()

            btn_play = ft.ElevatedButton("PLAY", icon=ICON_MAP["play"], on_click=toggle_audio, bgcolor=get_c("primary"), color="white")
            content.controls.append(ft.Container(padding=20, content=btn_play))
            content.controls.append(ft.Text(LYRICS_TEXT, text_align="center", color=get_c("text"), size=16))
        else:
            content.controls.append(ft.Container(padding=20, content=ft.Text(f"Sezione: {title}", color=get_c("text"), size=18)))

        return content

    # --- 4. NAVIGAZIONE (Logica "Swap" Pura) ---

    def navigate_to_tab(index):
        # Ripulisce la pagina e imposta la nuova vista
        page.controls.clear()
        
        # Reimposta AppBar e NavBar (sono spariti con clear)
        setup_bars(index)
        
        # Sceglie il contenuto
        if index == 0: # Home
            page.add(view_home())
        elif index == 1: # Profilo
            page.add(view_user())
            
        page.update()

    def navigate_to_notes():
        page.controls.clear()
        # Per le note usiamo una AppBar specifica con tasto indietro
        page.appbar = ft.AppBar(
            leading=ft.IconButton(ICON_MAP["arrow-left"], on_click=lambda e: navigate_to_tab(1), icon_color="white"),
            title=ft.Text("Note", color="white"),
            bgcolor=get_c("primary")
        )
        page.navigation_bar = None # Niente menu sotto nelle note
        page.add(view_notes())
        page.update()

    def navigate_to_reader(title):
        page.controls.clear()
        # AppBar specifica per il lettore
        page.appbar = ft.AppBar(
            leading=ft.IconButton(ICON_MAP["arrow-left"], on_click=lambda e: navigate_to_tab(0), icon_color="white"),
            title=ft.Text(title, color="white"),
            bgcolor=get_c("primary")
        )
        page.navigation_bar = None # Niente menu sotto nel lettore
        page.add(view_reader(title))
        page.update()

    def setup_bars(current_index):
        # Configura la barra superiore (AppBar)
        page.appbar = ft.AppBar(
            leading=ft.Container(padding=5, content=ft.Icon("star", color="white")), # Logo finto
            leading_width=40,
            title=ft.Text(f"Bentornato, {state['name']}", color="white"),
            center_title=False,
            bgcolor=get_c("primary")
        )
        
        # Configura la barra inferiore (NavigationBar)
        page.navigation_bar = ft.NavigationBar(
            selected_index=current_index,
            on_change=lambda e: navigate_to_tab(e.control.selected_index),
            destinations=[
                ft.NavigationDestination(icon=ICON_MAP["home"], label="Home"),
                ft.NavigationDestination(icon=ICON_MAP["user"], label="Profilo"),
            ],
            bgcolor=get_c("nav_bg")
        )

    # AVVIO
    page.bgcolor = get_c("bg")
    navigate_to_tab(0) # Parte dalla Home

if __name__ == "__main__":
    ft.app(target=main)
