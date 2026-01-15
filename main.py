import flet as ft

# --- VERSIONE 31.0: ARCHITETTURA STABILE ---
# Nessuna sovrapposizione strana. Solo pulizia e ordine.

# --- DATI ---
BOOKS_DATA = {
    "Lodi Mattutine": [],
    "Libretto": [],
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

LYRICS_TEXT = """
Lo sai che ti amo
Ma a volte è difficile sai?
Io mi perdo, mi strappo
E arriviamo sempre allo stesso punto...
(Testo presente)
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
    # Setup di base pulito
    page.title = "M2G App"
    page.padding = 0
    page.spacing = 0
    page.safe_area = ft.SafeArea(content=None)
    page.bgcolor = "white"
    
    # Inizializza memoria
    page.client_storage.get("init")

    # --- STATO (Memoria dell'app) ---
    state = {
        "current_page": "home", # Può essere: home, user, notes, reader
        "dark": page.client_storage.get("dark_mode") or False,
        "font": float(page.client_storage.get("font_size") or 16.0),
        "user_name": page.client_storage.get("user_name") or "Utente",
        "notes": page.client_storage.get("user_notes") or "",
        "reader_title": ""
    }

    def get_c(key):
        return COLORS["dark" if state["dark"] else "light"][key]

    # --- FUNZIONI PER CREARE LE PAGINE ---

    def build_home():
        # Creiamo la lista delle card
        cards_content = ft.Column(spacing=20, scroll="auto")
        
        items = [
            ("Lodi Mattutine", "sunrise"), 
            ("Libretto", "book-open"), 
            ("Inno", "music"), 
            ("Foto ricordo", "camera")
        ]
        
        for title, icon_key in items:
            # Singola card
            card = ft.Container(
                bgcolor=get_c("card"), 
                border_radius=22, padding=15, height=80,
                on_click=lambda e, t=title: navigate_to("reader", t),
                shadow=ft.BoxShadow(blur_radius=10, color="#11000000", offset=ft.Offset(0,5)),
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN, 
                    controls=[
                        ft.Row(controls=[
                            ft.Container(
                                width=50, height=50, bgcolor=get_c("icon_bg"), 
                                border_radius=14, alignment=ft.Alignment(0, 0), 
                                content=ft.Icon(ICON_MAP[icon_key], size=24, color=get_c("primary"))
                            ),
                            ft.Container(width=10),
                            ft.Text(title, size=16, weight="bold", color=get_c("text"))
                        ]),
                        ft.Icon(ICON_MAP["chevron-right"], size=24, color="#dddddd")
                    ]
                )
            )
            cards_content.controls.append(card)
            
        # Contenitore Home con padding
        return ft.Container(padding=20, content=cards_content, expand=True)

    def build_user():
        def save_name(e):
            state["user_name"] = e.control.value
            page.client_storage.set("user_name", e.control.value)
            page.update() # Aggiorna solo per salvare, non ridisegna tutto

        def toggle_theme(e):
            state["dark"] = e.control.value
            page.client_storage.set("dark_mode", e.control.value)
            render() # Ridisegna tutto per cambiare colori

        return ft.Column(
            scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20,
            controls=[
                ft.Container(height=20),
                ft.Icon("person", size=80, color=get_c("primary")),
                ft.Text("Il tuo Profilo", size=20, weight="bold", color=get_c("text")),
                ft.Container(
                    width=280, 
                    content=ft.TextField(value=state["user_name"], label="Il tuo nome", on_change=save_name, border_color=get_c("primary"))
                ),
                ft.Divider(),
                ft.Container(
                    bgcolor=get_c("primary"), border_radius=10, padding=15, width=300,
                    on_click=lambda e: navigate_to("notes"),
                    content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
                        ft.Icon(ICON_MAP["edit"], size=20, color="white"),
                        ft.Text("APRI LE TUE NOTE", color="white", weight="bold")
                    ])
                ),
                ft.Divider(),
                ft.Container(
                    padding=20,
                    content=ft.Row([
                        ft.Text("Modalità Notte", color=get_c("text"), size=16), 
                        ft.Switch(value=state["dark"], on_change=toggle_theme, active_color=get_c("primary"))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            ]
        )

    def build_notes():
        return ft.Column(controls=[
            ft.Container(
                padding=10, bgcolor=get_c("bg"),
                content=ft.Row([
                    ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: navigate_to("user")),
                    ft.Text("Note Personali", size=20, weight="bold", color=get_c("text")),
                    ft.Icon(ICON_MAP["save"], color=get_c("primary"))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ),
            ft.Container(
                expand=True, bgcolor=get_c("input_bg"), padding=20,
                content=ft.TextField(
                    value=state["notes"], multiline=True, border=ft.InputBorder.NONE, 
                    text_size=state["font"], color=get_c("text"),
                    on_change=lambda e: page.client_storage.set("user_notes", e.control.value)
                )
            )
        ])

    def build_reader():
        title = state["reader_title"]
        content = ft.Column(scroll="auto", expand=True, controls=[
            ft.Container(padding=20, content=ft.Text(f"Qui leggerai: {title}", color=get_c("text"), size=18))
        ])
        
        if title == "Inno":
            content.controls.append(ft.Container(padding=20, content=ft.Text(LYRICS_TEXT, text_align="center", color=get_c("text"))))

        return ft.Column(controls=[
            ft.Container(
                padding=10, bgcolor=get_c("bg"),
                content=ft.Row([
                    ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: navigate_to("home")),
                    ft.Text(title, size=20, weight="bold", color=get_c("text")),
                    ft.Container(width=40) # Spazio vuoto per bilanciare
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            ),
            ft.Divider(height=1),
            ft.Container(expand=True, content=content)
        ])

    # --- NAVIGAZIONE ---
    def navigate_to(page_name, extra_data=""):
        state["current_page"] = page_name
        if extra_data: state["reader_title"] = extra_data
        render()

    # --- DISEGNO PRINCIPALE (RENDER) ---
    def render():
        # 1. Aggiorna colori sfondo
        page.bgcolor = get_c("bg")
        
        # 2. Prepara Navbar e Header
        navbar = ft.Container(
            padding=15, bgcolor=get_c("nav_bg"),
            border_radius=ft.border_radius.only(top_left=20, top_right=20),
            shadow=ft.BoxShadow(blur_radius=10, color="#11000000"),
            content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
                ft.Container(
                    padding=10, border_radius=10, 
                    bgcolor=get_c("primary") if state["current_page"]=="home" else get_c("nav_bg"),
                    on_click=lambda e: navigate_to("home"),
                    content=ft.Row([ft.Icon(ICON_MAP["home"], color="white" if state["current_page"]=="home" else get_c("text")), ft.Text("HOME", color="white" if state["current_page"]=="home" else get_c("text"), weight="bold")])
                ),
                ft.Container(
                    padding=10, border_radius=10,
                    bgcolor=get_c("primary") if state["current_page"] in ["user", "notes"] else get_c("nav_bg"),
                    on_click=lambda e: navigate_to("user"),
                    content=ft.Row([ft.Icon(ICON_MAP["user"], color="white" if state["current_page"] in ["user", "notes"] else get_c("text")), ft.Text("PROFILO", color="white" if state["current_page"] in ["user", "notes"] else get_c("text"), weight="bold")])
                )
            ])
        )

        header = ft.Container(
            padding=ft.padding.symmetric(horizontal=20, vertical=30),
            content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, controls=[
                ft.Container(
                    width=60, height=60, bgcolor=get_c("primary"), border_radius=15, 
                    alignment=ft.Alignment(0,0), content=ft.Text("M2G", color="white", size=20, weight="bold")
                ),
                ft.Text(f"Bentornato, {state['user_name']}", size=22, color=get_c("text"))
            ])
        )

        # 3. Scegli il contenuto centrale
        pg = state["current_page"]
        content = None
        show_ui = True # Mostrare Header e Navbar?

        if pg == "home":
            content = build_home()
        elif pg == "user":
            content = build_user()
        elif pg == "notes":
            content = build_notes()
            show_ui = False # Nascondi header/nav per dare spazio alle note
        elif pg == "reader":
            content = build_reader()
            show_ui = False # Nascondi header/nav per leggere meglio

        # 4. Pulisci e assembla
        page.clean()
        
        if show_ui:
            page.add(ft.Column(expand=True, spacing=0, controls=[
                header,
                ft.Container(expand=True, content=content), # Il contenuto riempie lo spazio centrale
                navbar
            ]))
        else:
            # Modalità Full Screen (Note/Reader)
            # Aggiungiamo SafeArea per non finire sotto la fotocamera
            page.add(ft.Container(expand=True, padding=ft.padding.only(top=30, bottom=10), content=content))

        page.update()

    # Avvio
    render()

if __name__ == "__main__":
    ft.app(target=main)
