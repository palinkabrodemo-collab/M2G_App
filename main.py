import flet as ft
import traceback

# --- VERSIONE 32.0: SAFE MODE & ERROR CATCHING ---
# 1. Mostra subito "Caricamento..."
# 2. Gestisce gli errori di memoria senza bloccare (schermo bianco)
# 3. Se crasha, scrive l'errore a video invece di morire

BOOKS_DATA = {
    "Lodi Mattutine": [],
    "Libretto": [],
    "Foto ricordo": [] 
}

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
    # --- 1. SETUP SICURO ---
    page.title = "M2G App"
    page.padding = 0
    page.spacing = 0
    page.safe_area = ft.SafeArea(content=None)
    page.bgcolor = "white"
    
    # Mostriamo SUBITO qualcosa per evitare lo schermo bianco
    loading_text = ft.Text("Avvio dell'app...", color="black", size=20)
    page.add(ft.Container(alignment=ft.alignment.center, content=loading_text, expand=True))
    page.update()

    # --- 2. GESTIONE STATO PROTETTA ---
    # Usiamo valori default, poi proviamo a caricare dalla memoria
    state = {
        "current_page": "home",
        "dark": False,
        "font": 16.0,
        "user_name": "Utente",
        "notes": "",
        "reader_title": ""
    }

    def load_data_safely():
        try:
            state["dark"] = page.client_storage.get("dark_mode") or False
            state["font"] = float(page.client_storage.get("font_size") or 16.0)
            state["user_name"] = page.client_storage.get("user_name") or "Utente"
            state["notes"] = page.client_storage.get("user_notes") or ""
            print("Dati caricati con successo")
        except Exception as e:
            print(f"Errore caricamento dati (usiamo default): {e}")

    def get_c(key):
        return COLORS["dark" if state["dark"] else "light"][key]

    # --- 3. DEFINIZIONE UI (Tutto dentro try-except globale) ---
    try:
        # Carichiamo i dati ora che la pagina è visibile
        load_data_safely()

        # -- COMPONENTI UI --
        def build_home():
            cards_content = ft.Column(spacing=20, scroll="auto")
            items = [("Lodi Mattutine", "sunrise"), ("Libretto", "book-open"), ("Inno", "music"), ("Foto ricordo", "camera")]
            
            for title, icon_key in items:
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
            return ft.Container(padding=20, content=cards_content, expand=True)

        def build_user():
            def save_name(e):
                state["user_name"] = e.control.value
                page.client_storage.set("user_name", e.control.value)

            def toggle_theme(e):
                state["dark"] = e.control.value
                page.client_storage.set("dark_mode", e.control.value)
                render()

            return ft.Column(
                scroll="auto", horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20,
                controls=[
                    ft.Container(height=20),
                    ft.Icon("person", size=80, color=get_c("primary")),
                    ft.Text("Profilo", size=20, weight="bold", color=get_c("text")),
                    ft.Container(width=280, content=ft.TextField(value=state["user_name"], label="Il tuo nome", on_change=save_name, border_color=get_c("primary"))),
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
                    ft.Container(padding=20, content=ft.Row([ft.Text("Modalità Notte", color=get_c("text")), ft.Switch(value=state["dark"], on_change=toggle_theme, active_color=get_c("primary"))], alignment=ft.MainAxisAlignment.SPACE_BETWEEN))
                ]
            )

        def build_notes():
            return ft.Column(controls=[
                ft.Container(
                    padding=10, bgcolor=get_c("bg"),
                    content=ft.Row([
                        ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: navigate_to("user")),
                        ft.Text("Note", size=20, weight="bold", color=get_c("text")),
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
            return ft.Column(controls=[
                ft.Container(
                    padding=10, bgcolor=get_c("bg"),
                    content=ft.Row([
                        ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: navigate_to("home")),
                        ft.Text(title, size=20, weight="bold", color=get_c("text")),
                        ft.Container(width=40)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ),
                ft.Divider(height=1),
                ft.Container(expand=True, content=ft.Column(scroll="auto", controls=[
                    ft.Container(padding=20, content=ft.Text(f"Contenuto di {title}...", color=get_c("text")))
                ]))
            ])

        def navigate_to(page_name, extra=""):
            state["current_page"] = page_name
            if extra: state["reader_title"] = extra
            render()

        def render():
            page.bgcolor = get_c("bg")
            
            # Navbar
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

            # Header
            header = ft.Container(
                padding=ft.padding.symmetric(horizontal=20, vertical=30),
                content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, controls=[
                    ft.Container(width=60, height=60, bgcolor=get_c("primary"), border_radius=15, alignment=ft.Alignment(0,0), content=ft.Text("M2G", color="white", size=20, weight="bold")),
                    ft.Text(f"Bentornato, {state['user_name']}", size=22, color=get_c("text"))
                ])
            )

            pg = state["current_page"]
            content = None
            show_ui = True

            if pg == "home": content = build_home()
            elif pg == "user": content = build_user()
            elif pg == "notes": content = build_notes(); show_ui = False
            elif pg == "reader": content = build_reader(); show_ui = False

            page.clean()
            if show_ui:
                page.add(ft.Column(expand=True, spacing=0, controls=[header, ft.Container(expand=True, content=content), navbar]))
            else:
                page.add(ft.Container(expand=True, padding=ft.padding.only(top=30, bottom=10), content=content))
            page.update()

        # AVVIO
        render()

    except Exception as e:
        # --- CATTURA ERRORI GLOBALE ---
        # Se qualcosa fallisce, mostriamo l'errore invece dello schermo bianco
        page.clean()
        page.bgcolor = "red"
        page.add(
            ft.Column(scroll="auto", controls=[
                ft.Icon("error", color="white", size=50),
                ft.Text("ERRORE AVVIO:", color="white", weight="bold", size=20),
                ft.Text(str(e), color="white"),
                ft.Text(traceback.format_exc(), color="white", font_family="monospace")
            ])
        )
        page.update()

if __name__ == "__main__":
    ft.app(target=main)
