import flet as ft
import time

# --- VERSIONE 41.0: FIX ICONE E FUNZIONI ATTIVE ---
# 1. ICONE CORRETTE: Usiamo i nomi ufficiali Android (es. 'wb_sunny' invece di 'sunrise').
# 2. AUDIO SICURO: Caricato solo quando serve, non all'avvio.
# 3. MEMORIA SICURA: Caricata in background dopo l'avvio grafico.

# Mappa con nomi icone UFFICIALI Android (Google Fonts)
ICON_MAP = {
    "sunrise": "wb_sunny",       # Sole
    "book-open": "menu_book",    # Libro aperto
    "music": "music_note",       # Nota musicale
    "camera": "photo_camera",    # Macchina fotografica
    "chevron-right": "chevron_right",
    "home": "home", 
    "user": "person",
    "arrow-left": "arrow_back",  # Freccia indietro standard
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
    page.theme_mode = ft.ThemeMode.LIGHT

    # --- STATO GLOBALE ---
    state = {
        "page": "home",
        "name": "Utente",
        "notes": "",
        "audio_playing": False,
        "reader_title": ""
    }

    # Audio Player (Inizialmente None per non bloccare l'avvio)
    audio_player = None 

    def get_c(key):
        return COLORS["light"][key]

    # --- FUNZIONI DI CARICAMENTO SICURO ---
    def load_memory_safe():
        """Carica i dati dopo che l'app è partita"""
        try:
            if page.client_storage.contains_key("user_name"):
                state["name"] = page.client_storage.get("user_name")
            if page.client_storage.contains_key("user_notes"):
                state["notes"] = page.client_storage.get("user_notes")
            render() # Ridisegna con i dati veri
        except:
            print("Errore memoria (non critico)")

    def init_audio():
        """Inizializza l'audio solo quando serve"""
        nonlocal audio_player
        if audio_player is None:
            try:
                audio_player = ft.Audio(src="inno.mp3", autoplay=False, release_mode="stop")
                page.overlay.append(audio_player)
                page.update()
            except:
                print("Errore Audio")

    # --- COSTRUZIONE PAGINE ---

    def build_home():
        col = ft.Column(spacing=15)
        
        # Header Home
        col.controls.append(ft.Container(
            padding=ft.padding.only(top=30, bottom=20, left=20, right=20),
            content=ft.Column(spacing=10, controls=[
                ft.Container(width=60, height=60, bgcolor=get_c("primary"), border_radius=15, alignment=ft.Alignment(0,0), content=ft.Text("M2G", color="white", size=20, weight="bold")),
                ft.Text(f"Bentornato, {state['name']}", size=22, color=get_c("text"))
            ])
        ))

        # Cards
        items = [("Lodi Mattutine", "sunrise"), ("Libretto", "book-open"), ("Inno", "music"), ("Foto ricordo", "camera")]
        for title, icon in items:
            # FIX ICONE: Rimosso Container superfluo attorno all'icona che creava il grigio
            icon_control = ft.Icon(name=ICON_MAP[icon], color=get_c("primary"), size=30)
            
            col.controls.append(
                ft.Container(
                    bgcolor=get_c("card"), height=80, border_radius=20, padding=15,
                    border=ft.border.all(1, "#eeeeee"), 
                    on_click=lambda e, t=title: go_to_reader(t),
                    content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                        ft.Row(controls=[
                            ft.Container(width=50, height=50, bgcolor=get_c("icon_bg"), border_radius=15, alignment=ft.Alignment(0,0), content=icon_control),
                            ft.Container(width=10),
                            ft.Text(title, size=16, weight="bold", color=get_c("text"))
                        ]),
                        ft.Icon(name=ICON_MAP["chevron-right"], color="#cccccc")
                    ])
                )
            )
        
        col.controls.append(ft.Container(height=100))
        return ft.Container(padding=20, content=col)

    def build_user():
        def save_name(e):
            state["name"] = e.control.value
            page.client_storage.set("user_name", e.control.value)
            # Non ricarichiamo tutto per velocità, salviamo e basta

        col = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        col.controls.append(ft.Container(height=40))
        col.controls.append(ft.Icon(name="person", size=80, color=get_c("primary")))
        col.controls.append(ft.Text("Profilo", size=20, weight="bold", color=get_c("text")))
        col.controls.append(ft.TextField(value=state["name"], label="Nome", border_color=get_c("primary"), on_change=save_name))
        col.controls.append(ft.Divider())
        col.controls.append(ft.Container(
            bgcolor=get_c("primary"), width=300, padding=15, border_radius=10,
            on_click=lambda e: go_to_notes(),
            content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Icon(name=ICON_MAP["edit"], color="white"), ft.Text("APRI NOTE", color="white", weight="bold")])
        ))
        col.controls.append(ft.Container(height=100))
        return ft.Container(padding=20, content=col)

    def build_reader(title):
        col = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # FIX ERROR ROSSO: IconButton ora ha l'icona esplicita "arrow_back"
        back_btn = ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: go_to_home())
        
        col.controls.append(ft.Container(padding=10, content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
            back_btn,
            ft.Text(title, size=20, weight="bold", color=get_c("text")),
            ft.Container(width=40)
        ])))
        col.controls.append(ft.Divider(height=1))

        if title == "Inno":
            # Inizializza audio solo qui
            init_audio()
            
            def toggle_audio(e):
                if not audio_player: return
                state["audio_playing"] = not state["audio_playing"]
                if state["audio_playing"]: 
                    audio_player.play()
                    btn_play.text = "PAUSA"
                    btn_play.icon = ICON_MAP["pause"]
                    btn_play.bgcolor = "#d9534f"
                else: 
                    audio_player.pause()
                    btn_play.text = "RIPRODUCI"
                    btn_play.icon = ICON_MAP["play"]
                    btn_play.bgcolor = get_c("primary")
                btn_play.update()

            btn_play = ft.ElevatedButton("RIPRODUCI", icon=ICON_MAP["play"], on_click=toggle_audio, bgcolor=get_c("primary"), color="white")
            col.controls.append(btn_play)
            col.controls.append(ft.Text(LYRICS_TEXT, text_align="center", color=get_c("text"), size=16))
        else:
            col.controls.append(ft.Text(f"Contenuto di: {title}", color=get_c("text")))
        
        col.controls.append(ft.Container(height=50))
        return ft.Container(padding=10, content=col)

    def build_notes():
        def save_notes_storage(e):
            state["notes"] = e.control.value
            page.client_storage.set("user_notes", e.control.value)

        col = ft.Column(spacing=10)
        col.controls.append(ft.Container(padding=10, content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
            ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: go_to_user()),
            ft.Text("Note", size=20, weight="bold", color=get_c("text")),
            ft.Icon(name=ICON_MAP["save"], color=get_c("primary"))
        ])))
        col.controls.append(ft.TextField(
            value=state["notes"], multiline=True, min_lines=15, 
            border=ft.InputBorder.NONE, color=get_c("text"), bgcolor="white",
            hint_text="Scrivi qui le tue note...", on_change=save_notes_storage
        ))
        return ft.Container(padding=10, content=col)

    # --- RENDERER ---
    
    def render():
        page.controls.clear()
        
        main_content = None
        if state["page"] == "home": main_content = build_home()
        elif state["page"] == "user": main_content = build_user()
        elif state["page"] == "notes": main_content = build_notes()
        elif state["page"] == "reader": main_content = build_reader(state["reader_title"])

        # ListView unica = stabilità
        lv = ft.ListView(expand=True, controls=[main_content])
        page.add(lv)

        # Navbar
        if state["page"] in ["home", "user"]:
            btn_h_bg = get_c("primary") if state["page"] == "home" else "white"
            btn_h_fg = "white" if state["page"] == "home" else get_c("text")
            btn_u_bg = get_c("primary") if state["page"] == "user" else "white"
            btn_u_fg = "white" if state["page"] == "user" else get_c("text")

            navbar = ft.Container(
                bgcolor="white", padding=15, 
                border_radius=ft.border_radius.only(top_left=20, top_right=20),
                border=ft.border.only(top=ft.border.BorderSide(1, "#eeeeee")),
                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_h_bg, on_click=lambda e: go_to_home(), content=ft.Row([ft.Icon(name=ICON_MAP["home"], color=btn_h_fg), ft.Text("HOME", color=btn_h_fg, weight="bold")])),
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_u_bg, on_click=lambda e: go_to_user(), content=ft.Row([ft.Icon(name=ICON_MAP["user"], color=btn_u_fg), ft.Text("PROFILO", color=btn_u_fg, weight="bold")]))
                ])
            )
            page.overlay.append(ft.Container(content=navbar, alignment=ft.alignment.bottom_center))

        page.update()

    # --- NAVIGAZIONE ---
    def go_to_home(e=None): page.overlay.clear(); state["page"] = "home"; render()
    def go_to_user(e=None): page.overlay.clear(); state["page"] = "user"; render()
    def go_to_notes(e=None): page.overlay.clear(); state["page"] = "notes"; render()
    def go_to_reader(t): 
        # Se stiamo uscendo dall'inno e l'audio va, fermiamolo
        if state["audio_playing"] and audio_player:
            audio_player.pause()
            state["audio_playing"] = False
        page.overlay.clear(); state["page"] = "reader"; state["reader_title"] = t; render()

    # AVVIO
    render()
    
    # TRUCCO CARICAMENTO SICURO:
    # Non carichiamo la memoria subito. Aspettiamo che la grafica sia pronta.
    # Questo evita lo "Schermo Bianco della Morte".
    load_memory_safe()

if __name__ == "__main__":
    ft.app(target=main)
