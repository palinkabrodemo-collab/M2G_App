import flet as ft

# --- VERSIONE 33.0: ARCHITETTURA VISIBILITÀ ---
# Torniamo alla logica della v30 (che partiva!) ma usiamo
# la proprietà 'visible' per nascondere le pagine invece di sovrapporle male.

# --- DATI ---
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
    "edit": "edit"
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
    # 1. SETUP BASE
    page.title = "M2G App"
    page.padding = 0
    page.spacing = 0
    page.safe_area = ft.SafeArea(content=None)
    page.bgcolor = "white"

    # 2. RECUPERO DATI SICURO (Con valori di default immediati)
    user_name = "Utente"
    user_notes = ""
    is_dark = False
    
    try:
        if page.client_storage.contains_key("user_name"):
            user_name = page.client_storage.get("user_name")
        if page.client_storage.contains_key("dark_mode"):
            is_dark = page.client_storage.get("dark_mode")
        if page.client_storage.contains_key("user_notes"):
            user_notes = page.client_storage.get("user_notes")
    except:
        pass # Se fallisce, usiamo i default e andiamo avanti

    def get_c(key):
        return COLORS["dark" if is_dark else "light"][key]

    # --- 3. CREAZIONE DELLE PAGINE (TUTTE SUBITO) ---

    # HEADER COMPONENT
    txt_welcome = ft.Text(f"Bentornato, {user_name}", size=24, weight="w400", color=get_c("text"))
    header_container = ft.Container(
        padding=ft.padding.only(top=40, bottom=20, left=20, right=20),
        bgcolor=get_c("bg"),
        content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15, controls=[
            ft.Container(
                width=65, height=65, border_radius=18, bgcolor=get_c("primary"),
                alignment=ft.Alignment(0, 0), 
                content=ft.Text("M2G", color="white", size=22, weight="w300")
            ), 
            txt_welcome
        ])
    )

    # PAGE 1: HOME
    cards_col = ft.Column(spacing=20, scroll="auto")
    items = [("Lodi Mattutine", "sunrise"), ("Libretto", "book-open"), ("Inno", "music"), ("Foto ricordo", "camera")]
    
    for title, icon_key in items:
        cards_col.controls.append(
            ft.Container(
                bgcolor=get_c("card"), border_radius=22, padding=15, height=80,
                shadow=ft.BoxShadow(blur_radius=10, color="#11000000", offset=ft.Offset(0,5)),
                on_click=lambda e, t=title: open_reader(t),
                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.Row(controls=[
                        ft.Container(width=50, height=50, bgcolor=get_c("icon_bg"), border_radius=14, alignment=ft.Alignment(0, 0), content=ft.Icon(ICON_MAP[icon_key], color=get_c("primary"))),
                        ft.Container(width=10),
                        ft.Text(title, size=16, weight="bold", color=get_c("text"))
                    ]),
                    ft.Icon(ICON_MAP["chevron-right"], color="#dddddd")
                ])
            )
        )

    home_view = ft.Container(
        padding=20, expand=True, visible=True, # HOME È VISIBILE ALL'AVVIO
        content=cards_col
    )

    # PAGE 2: USER
    name_input = ft.TextField(value=user_name, label="Nome", border_color=get_c("primary"))
    
    def save_name_change(e):
        txt_welcome.value = f"Bentornato, {e.control.value}"
        page.client_storage.set("user_name", e.control.value)
        page.update()

    name_input.on_change = save_name_change

    user_view = ft.Container(
        padding=20, expand=True, visible=False, # NASCOSTA ALL'AVVIO
        content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, controls=[
            ft.Icon("person", size=80, color=get_c("primary")),
            ft.Text("Profilo", size=20, weight="bold", color=get_c("text")),
            name_input,
            ft.Divider(),
            ft.Container(
                bgcolor=get_c("primary"), border_radius=10, padding=15, width=300,
                on_click=lambda e: open_notes(),
                content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Icon(ICON_MAP["edit"], color="white"), ft.Text("NOTE", color="white", weight="bold")])
            )
        ])
    )

    # PAGE 3: NOTES (Full Screen)
    notes_input = ft.TextField(value=user_notes, multiline=True, border=ft.InputBorder.NONE, color=get_c("text"))
    
    def save_notes_change(e):
        page.client_storage.set("user_notes", e.control.value)

    notes_input.on_change = save_notes_change

    notes_view = ft.Container(
        expand=True, visible=False, bgcolor=get_c("bg"), padding=20,
        content=ft.Column(controls=[
            ft.Row([
                ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: navigate("user")),
                ft.Text("Note", size=20, weight="bold", color=get_c("text")),
                ft.Icon(ICON_MAP["save"], color=get_c("primary"))
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(expand=True, bgcolor=get_c("input_bg"), padding=10, border_radius=10, content=notes_input)
        ])
    )

    # PAGE 4: READER (Full Screen)
    reader_title_txt = ft.Text("", size=20, weight="bold", color=get_c("text"))
    reader_content_txt = ft.Text("", color=get_c("text"))
    
    reader_view = ft.Container(
        expand=True, visible=False, bgcolor=get_c("bg"), padding=20,
        content=ft.Column(controls=[
            ft.Row([
                ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: navigate("home")),
                reader_title_txt,
                ft.Container(width=40)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.Container(expand=True, content=ft.Column(scroll="auto", controls=[reader_content_txt]))
        ])
    )

    # NAVBAR COMPONENT
    btn_nav_home = ft.Container(padding=10, border_radius=10, bgcolor=get_c("primary"), on_click=lambda e: navigate("home"), content=ft.Icon(ICON_MAP["home"], color="white"))
    btn_nav_user = ft.Container(padding=10, border_radius=10, bgcolor=get_c("nav_bg"), on_click=lambda e: navigate("user"), content=ft.Icon(ICON_MAP["user"], color=get_c("text")))
    
    navbar = ft.Container(
        padding=15, bgcolor=get_c("nav_bg"),
        border_radius=ft.border_radius.only(top_left=20, top_right=20),
        shadow=ft.BoxShadow(blur_radius=10, color="#11000000"),
        content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[btn_nav_home, btn_nav_user])
    )

    # --- 4. LOGICA DI NAVIGAZIONE ---
    def navigate(target):
        # 1. Gestione Visibilità Pagine
        home_view.visible = (target == "home")
        user_view.visible = (target == "user")
        notes_view.visible = False # Si apre solo con open_notes
        reader_view.visible = False # Si apre solo con open_reader
        
        # 2. Gestione Header e Navbar (Nascosti se siamo in note/reader)
        is_main_tab = target in ["home", "user"]
        header_container.visible = is_main_tab
        navbar.visible = is_main_tab
        
        # 3. Aggiorna colori bottoni navbar
        if target == "home":
            btn_nav_home.bgcolor = get_c("primary"); btn_nav_home.content.color = "white"
            btn_nav_user.bgcolor = get_c("nav_bg"); btn_nav_user.content.color = get_c("text")
        elif target == "user":
            btn_nav_home.bgcolor = get_c("nav_bg"); btn_nav_home.content.color = get_c("text")
            btn_nav_user.bgcolor = get_c("primary"); btn_nav_user.content.color = "white"
            
        page.update()

    def open_notes():
        notes_view.visible = True
        home_view.visible = False
        user_view.visible = False
        header_container.visible = False
        navbar.visible = False
        page.update()

    def open_reader(title):
        reader_title_txt.value = title
        reader_content_txt.value = f"Contenuto di {title}..."
        reader_view.visible = True
        home_view.visible = False
        user_view.visible = False
        header_container.visible = False
        navbar.visible = False
        page.update()

    # --- 5. ASSEMBLAGGIO FINALE ---
    # Invece di Stack, usiamo una colonna che si espande.
    # Le pagine invisibili occupano spazio 0.
    
    content_area = ft.Column(
        expand=True, 
        spacing=0,
        controls=[
            header_container,   # Visibile solo in Home/User
            home_view,          # Visibile in Home
            user_view,          # Visibile in User
            notes_view,         # Visibile solo in Note
            reader_view         # Visibile solo in Reader
        ]
    )

    layout = ft.Column(
        expand=True, 
        spacing=0, 
        controls=[
            content_area,
            navbar              # Visibile solo in Home/User
        ]
    )

    page.add(layout)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
