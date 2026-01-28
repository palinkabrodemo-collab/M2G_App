import flet as ft

# --- VERSIONE 55.0: LA ROCCIA (STRUTTURA SEMPLICE) ---
# Obiettivo: Riaccendere lo schermo eliminando conflitti di layout.
# 1. Nessun "expand=True" (che causa lo schermo bianco).
# 2. Nessuna immagine esterna (che causa crash se manca il file).
# 3. Sintassi pulita (niente errori rossi).

# Mappa Icone Native (Solo stringhe sicure)
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
    # 1. SETUP PULITO
    page.title = "M2G App"
    page.bgcolor = "#f3f0e9"
    page.padding = 10 # Un po' di margine aiuta il rendering
    # Scroll "adaptive" è il più sicuro su mobile
    page.scroll = "adaptive" 

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

    # --- FUNZIONI (Protette) ---
    def load_memory():
        try:
            if page.client_storage.contains_key("user_name"):
                state["name"] = page.client_storage.get("user_name")
            if page.client_storage.contains_key("user_notes"):
                state["notes"] = page.client_storage.get("user_notes")
        except: pass

    def init_audio():
        nonlocal audio_player
        if audio_player is None:
            try:
                audio_player = ft.Audio(src="inno.mp3", autoplay=False, release_mode="stop")
                page.overlay.append(audio_player)
                page.update()
            except: pass

    # --- UI BUILDERS (Diretti, niente wrapper complessi) ---

    def build_view():
        # Puliamo la pagina PRIMA di aggiungere roba
        page.clean()

        # 1. COSTRUIAMO LA HOME
        if state["page"] == "home":
            # Header
            page.add(ft.Container(
                padding=20,
                content=ft.Column([
                    ft.Container(
                        width=60, height=60, bgcolor=get_c("primary"), 
                        border_radius=15, alignment=ft.alignment.center,
                        content=ft.Text("M2G", color="white", size=20, weight="bold")
                    ),
                    ft.Text(f"Bentornato, {state['name']}", size=22, color=get_c("text"))
                ])
            ))

            # Cards
            items = [("Lodi Mattutine", "sunrise"), ("Libretto", "book-open"), ("Inno", "music"), ("Foto ricordo", "camera")]
            for title, icon_key in items:
                page.add(ft.Container(
                    bgcolor=get_c("card"), height=80, border_radius=20, padding=15,
                    border=ft.border.all(1, "#eeeeee"),
                    on_click=lambda e, t=title: navigate("reader", t),
                    content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Row(controls=[
                            ft.Container(width=50, height=50, bgcolor=get_c("icon_bg"), 
                                       border_radius=15, alignment=ft.alignment.center, 
                                       content=ft.Icon(ICON_MAP[icon_key], size=28, color=get_c("primary"))),
                            ft.Container(width=10),
                            ft.Text(title, size=16, weight="bold", color=get_c("text"))
                        ]),
                        ft.Icon("chevron_right", color="#cccccc")
                    ])
                ))
            
            page.add(ft.Container(height=20)) # Spazio
            
            # Navbar Home
            page.add(ft.Container(height=20))
            page.add(ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
                ft.Container(padding=10, bgcolor=get_c("primary"), border_radius=10, 
                           content=ft.Row([ft.Icon("home", color="white"), ft.Text("HOME", color="white")])),
                ft.Container(padding=10, on_click=lambda e: navigate("user"),
                           content=ft.Row([ft.Icon("person", color=get_c("text")), ft.Text("PROFILO", color=get_c("text"))]))
            ]))
            page.add(ft.Container(height=20))


        # 2. COSTRUIAMO PROFILO
        elif state["page"] == "user":
            def save_name(e):
                state["name"] = e.control.value
                page.client_storage.set("user_name", e.control.value)

            page.add(ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                ft.Container(height=20),
                ft.Icon("person", size=80, color=get_c("primary")),
                ft.Text("Profilo", size=20, weight="bold", color=get_c("text")),
                ft.TextField(value=state["name"], label="Nome", on_change=save_name),
                ft.Divider(),
                ft.ElevatedButton("APRI NOTE", icon="edit", bgcolor=get_c("primary"), color="white", 
                                on_click=lambda e: navigate("notes")),
                ft.Container(height=20),
                # Navbar User
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
                    ft.Container(padding=10, on_click=lambda e: navigate("home"), 
                               content=ft.Row([ft.Icon("home", color=get_c("text")), ft.Text("HOME", color=get_c("text"))])),
                    ft.Container(padding=10, bgcolor=get_c("primary"), border_radius=10,
                               content=ft.Row([ft.Icon("person", color="white"), ft.Text("PROFILO", color="white")]))
                ])
            ]))

        # 3. COSTRUIAMO READER / INNO
        elif state["page"] == "reader":
            title = state["reader_title"]
            page.add(ft.Row([
                ft.IconButton(icon="arrow_back", on_click=lambda e: navigate("home")),
                ft.Text(title, size=20, weight="bold", color=get_c("text"))
            ]))
            page.add(ft.Divider())

            if title == "Inno":
                init_audio()
                def toggle_audio(e):
                    if not audio_player: return
                    state["audio_playing"] = not state["audio_playing"]
                    if state["audio_playing"]: audio_player.play()
                    else: audio_player.pause()
                    navigate("reader", title) # Ricarica icona

                icon = "pause" if state["audio_playing"] else "play_arrow"
                text = "PAUSA" if state["audio_playing"] else "RIPRODUCI"
                
                page.add(ft.Container(
                    bgcolor=get_c("primary"), padding=15, border_radius=30, alignment=ft.alignment.center,
                    on_click=toggle_audio,
                    content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                        ft.Icon(icon, color="white"), ft.Text(text, color="white", weight="bold")
                    ])
                ))
                page.add(ft.Text(LYRICS_TEXT, text_align="center"))
            else:
                page.add(ft.Text(f"Contenuto per {title}"))

        # 4. COSTRUIAMO NOTE
        elif state["page"] == "notes":
            def save_notes(e):
                state["notes"] = e.control.value
                page.client_storage.set("user_notes", e.control.value)
            
            page.add(ft.Row([
                ft.IconButton(icon="arrow_back", on_click=lambda e: navigate("user")),
                ft.Text("Note", size=20, weight="bold"),
                ft.Icon("save", color=get_c("primary"))
            ]))
            page.add(ft.TextField(value=state["notes"], multiline=True, min_lines=10, on_change=save_notes))

        page.update()

    def navigate(target, data=""):
        state["page"] = target
        if data: state["reader_title"] = data
        build_view()

    # AVVIO
    load_memory()
    build_view()

if __name__ == "__main__":
    ft.app(target=main)
