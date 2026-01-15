import flet as ft

# --- VERSIONE 39.0: RITORNO ALLE ORIGINI (FIXED) ---
# Basata sulla v30 (l'unica che partiva), ma corretta graficamente.
# - NIENTE MEMORIA (client_storage disattivato)
# - NIENTE AUDIO (ft.Audio disattivato)
# - NIENTE STACK (Niente rettangoli grigi)

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
    }
}

def main(page: ft.Page):
    # --- SETUP SICURISSIMO ---
    page.title = "M2G App"
    page.padding = 0
    page.spacing = 0
    page.safe_area = ft.SafeArea(content=None)
    page.bgcolor = "#f3f0e9" # Colore fisso background

    # Variabili semplici (Niente client_storage)
    current_page = "home"
    reader_title = ""
    user_name = "Utente"
    user_notes = ""

    def get_c(key):
        return COLORS["light"][key]

    # --- COSTRUZIONE PAGINE (Semplice) ---

    def build_home():
        col = ft.Column(spacing=15, scroll="auto")
        items = [("Lodi Mattutine", "sunrise"), ("Libretto", "book-open"), ("Inno", "music"), ("Foto ricordo", "camera")]
        
        for title, icon in items:
            col.controls.append(
                ft.Container(
                    bgcolor=get_c("card"), height=80, border_radius=20, padding=15,
                    shadow=ft.BoxShadow(blur_radius=5, color="#11000000", offset=ft.Offset(0,4)),
                    on_click=lambda e, t=title: go_to_reader(t),
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
        col.controls.append(ft.Container(height=50))
        return ft.Container(padding=20, content=col)

    def build_user():
        return ft.Container(padding=20, content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20, scroll="auto", controls=[
            ft.Container(height=10),
            ft.Icon("person", size=80, color=get_c("primary")),
            ft.Text("Profilo", size=20, weight="bold", color=get_c("text")),
            ft.TextField(value=user_name, label="Nome", border_color=get_c("primary")),
            ft.Divider(),
            ft.Container(
                bgcolor=get_c("primary"), width=300, padding=15, border_radius=10,
                on_click=lambda e: go_to_notes(),
                content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Icon(ICON_MAP["edit"], color="white"), ft.Text("APRI NOTE", color="white", weight="bold")])
            )
        ]))

    def build_notes():
        return ft.Column(expand=True, controls=[
            ft.Container(padding=10, content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: go_to_user()),
                ft.Text("Note", size=20, weight="bold", color=get_c("text")),
                ft.Icon(ICON_MAP["save"], color=get_c("primary"))
            ])),
            ft.Container(expand=True, bgcolor=get_c("input_bg"), border_radius=10, padding=15, margin=10, content=ft.TextField(value=user_notes, multiline=True, border=ft.InputBorder.NONE, color=get_c("text")))
        ])

    def build_reader(title):
        content_body = ft.Column(scroll="auto", expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        if title == "Inno":
            content_body.controls.append(ft.Container(padding=20, content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                ft.Icon(ICON_MAP["music"], size=50, color=get_c("primary")),
                ft.Container(height=20),
                ft.Text(LYRICS_TEXT, text_align="center", color=get_c("text"), size=16)
            ])))
        else:
             content_body.controls.append(ft.Container(padding=20, content=ft.Text(f"Sezione: {title}", color=get_c("text"))))

        return ft.Column(expand=True, controls=[
            ft.Container(padding=10, content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: go_to_home()),
                ft.Text(title, size=20, weight="bold", color=get_c("text")),
                ft.Container(width=40)
            ])),
            ft.Divider(height=1),
            content_body
        ])

    # --- NAVIGAZIONE SEMPLICE ---
    # Niente Stack, niente nascondere. Ricostruiamo la pagina principale.
    
    def render():
        page.controls.clear()
        
        # 1. HEADER (Solo Home/User)
        if current_page in ["home", "user"]:
            header = ft.Container(
                padding=ft.padding.only(top=30, bottom=10, left=20, right=20),
                content=ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10, controls=[
                    ft.Container(width=60, height=60, bgcolor=get_c("primary"), border_radius=15, alignment=ft.Alignment(0,0), content=ft.Text("M2G", color="white", size=20, weight="bold")),
                    ft.Text(f"Bentornato, {user_name}", size=22, color=get_c("text"))
                ])
            )
            page.add(header)

        # 2. BODY (Contenuto variabile)
        body = ft.Container(expand=True)
        if current_page == "home":
            body.content = build_home()
        elif current_page == "user":
            body.content = build_user()
        elif current_page == "notes":
            body.content = build_notes()
        elif current_page == "reader":
            body.content = build_reader(reader_title)
        
        page.add(body)

        # 3. NAVBAR (Solo Home/User)
        if current_page in ["home", "user"]:
            btn_h_bg = get_c("primary") if current_page == "home" else "white"
            btn_h_fg = "white" if current_page == "home" else get_c("text")
            btn_u_bg = get_c("primary") if current_page == "user" else "white"
            btn_u_fg = "white" if current_page == "user" else get_c("text")

            navbar = ft.Container(
                padding=15, bgcolor="white",
                border_radius=ft.border_radius.only(top_left=20, top_right=20),
                shadow=ft.BoxShadow(blur_radius=10, color="#11000000"),
                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_h_bg, on_click=lambda e: go_to_home(), content=ft.Row([ft.Icon(ICON_MAP["home"], color=btn_h_fg), ft.Text("HOME", color=btn_h_fg, weight="bold")])),
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_u_bg, on_click=lambda e: go_to_user(), content=ft.Row([ft.Icon(ICON_MAP["user"], color=btn_u_fg), ft.Text("PROFILO", color=btn_u_fg, weight="bold")]))
                ])
            )
            page.add(navbar)

        page.update()

    # Funzioni di cambio pagina
    def go_to_home(e=None):
        nonlocal current_page
        current_page = "home"
        render()

    def go_to_user(e=None):
        nonlocal current_page
        current_page = "user"
        render()

    def go_to_notes(e=None):
        nonlocal current_page
        current_page = "notes"
        render()

    def go_to_reader(title):
        nonlocal current_page, reader_title
        current_page = "reader"
        reader_title = title
        render()

    # AVVIO
    render()

if __name__ == "__main__":
    ft.app(target=main)
