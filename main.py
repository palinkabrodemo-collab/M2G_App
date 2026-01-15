import flet as ft

# --- VERSIONE 36.0: TEST GRAFICO PURO ---
# Abbiamo il TESTO COMPLETO.
# Abbiamo DISATTIVATO Audio e Memoria per capire se sono loro a bloccare l'avvio.

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

# --- TESTO COMPLETO ---
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
    "dark": { # (Non usato ora, ma pronto)
        "bg": "#1e1e1e", "primary": "#6a8a73", "text": "#ffffff", 
        "card": "#2c2c2c", "icon_bg": "#3a3a3a", "nav_bg": "#2c2c2c", "input_bg": "#333333"
    }
}

def main(page: ft.Page):
    # 1. SETUP BASE
    page.title = "M2G App"
    page.padding = 0
    page.spacing = 0
    page.safe_area = ft.SafeArea(content=None)
    page.bgcolor = "white"

    # --- DISATTIVATO TEMPORANEAMENTE PER EVITARE SCHERMO BIANCO ---
    # audio_player = ft.Audio(src="inno.mp3")
    # page.overlay.append(audio_player)

    # Dati Fissi (Niente caricamento memoria per ora)
    state = {
        "page": "home",
        "name": "Utente", 
        "notes": "",
        "dark": False,
        "reader_title": ""
    }

    def get_c(key):
        return COLORS["light"][key] # Forziamo Light per sicurezza

    # --- 2. CONTENUTI ---

    def get_home_content():
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

    def get_user_content():
        return ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, scroll="auto", controls=[
            ft.Container(height=10),
            ft.Icon("person", size=80, color=get_c("primary")),
            ft.Text("Il tuo Profilo", size=20, weight="bold", color=get_c("text")),
            ft.Container(width=280, content=ft.TextField(value=state["name"], label="Nome", border_color=get_c("primary"))),
            ft.Divider(),
            ft.Container(
                bgcolor=get_c("primary"), width=300, padding=15, border_radius=10,
                on_click=lambda e: navigate("notes"),
                content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Icon(ICON_MAP["edit"], color="white"), ft.Text("APRI NOTE", color="white", weight="bold")])
            )
        ])

    def get_reader_content():
        title = state["reader_title"]
        content_body = ft.Column(scroll="auto", expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        if title == "Inno":
            content_body.controls.append(ft.Container(padding=20, content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                ft.Icon(ICON_MAP["music"], size=50, color=get_c("primary")),
                ft.Text("Audio disattivato per Test", color="red"), # Avviso
                ft.Container(height=20),
                ft.Text(LYRICS_TEXT, text_align="center", color=get_c("text"), size=16)
            ])))
        else:
            content_body.controls.append(ft.Container(padding=20, content=ft.Text(f"Sezione: {title}", color=get_c("text"))))

        return ft.Column(expand=True, controls=[
            ft.Container(padding=10, content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: navigate("home")),
                ft.Text(title, size=20, weight="bold", color=get_c("text")),
                ft.Container(width=40)
            ])),
            ft.Divider(height=1),
            content_body
        ])

    def get_notes_content():
        return ft.Column(expand=True, controls=[
            ft.Container(padding=10, content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: navigate("user")),
                ft.Text("Note", size=20, weight="bold", color=get_c("text")),
                ft.Icon(ICON_MAP["save"], color=get_c("primary"))
            ])),
            ft.Container(expand=True, bgcolor=get_c("input_bg"), border_radius=10, padding=15, margin=10, content=ft.TextField(value=state["notes"], multiline=True, border=ft.InputBorder.NONE, color=get_c("text")))
        ])

    # --- 3. GESTIONE UI ---
    
    header_container = ft.Container(padding=ft.padding.only(top=30, bottom=10, left=20, right=20))
    body_container = ft.Container(expand=True, padding=0)
    navbar_container = ft.Container()

    def navigate(target, data=""):
        state["page"] = target
        if data: state["reader_title"] = data
        update_ui()

    def update_ui():
        page.bgcolor = get_c("bg")
        
        # Header
        if state["page"] in ["home", "user"]:
            header_container.content = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, controls=[
                ft.Container(width=60, height=60, bgcolor=get_c("primary"), border_radius=15, alignment=ft.Alignment(0,0), content=ft.Text("M2G", color="white", size=20, weight="bold")),
                ft.Text(f"Bentornato, {state['name']}", size=22, color=get_c("text"))
            ])
            header_container.visible = True
        else:
            header_container.visible = False

        # Body
        body_container.content = None
        if state["page"] == "home":
            body_container.content = get_home_content(); body_container.padding = 20
        elif state["page"] == "user":
            body_container.content = get_user_content(); body_container.padding = 20
        elif state["page"] == "notes":
            body_container.content = get_notes_content(); body_container.padding = 0
        elif state["page"] == "reader":
            body_container.content = get_reader_content(); body_container.padding = 0

        # Navbar
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
