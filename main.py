import flet as ft

# --- VERSIONE 40.0: FIX GRAFICO "NO OMBRE" ---
# 1. Abbiamo rimosso tutte le BoxShadow (che causavano i rettangoli grigi).
# 2. Abbiamo rimosso "expand=True" (che causava problemi di dimensione).
# 3. Usiamo una ListView unica per evitare sovrapposizioni.

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
    # SETUP BASE
    page.title = "M2G App"
    page.padding = 0
    page.spacing = 0
    page.safe_area = ft.SafeArea(content=None)
    page.bgcolor = "#f3f0e9" 

    # Variabili Stato (Senza memoria per ora)
    current_page = "home"
    reader_title = ""
    user_name = "Utente"
    user_notes = ""

    def get_c(key):
        return COLORS["light"][key]

    # --- FUNZIONI CONTENUTO ---

    def build_home():
        # Lista verticale semplice
        col = ft.Column(spacing=15)
        
        # Header Home
        col.controls.append(ft.Container(
            padding=ft.padding.only(top=30, bottom=20, left=20, right=20),
            content=ft.Column(spacing=10, controls=[
                ft.Container(width=60, height=60, bgcolor=get_c("primary"), border_radius=15, alignment=ft.Alignment(0,0), content=ft.Text("M2G", color="white", size=20, weight="bold")),
                ft.Text(f"Bentornato, {user_name}", size=22, color=get_c("text"))
            ])
        ))

        # Cards
        items = [("Lodi Mattutine", "sunrise"), ("Libretto", "book-open"), ("Inno", "music"), ("Foto ricordo", "camera")]
        for title, icon in items:
            col.controls.append(
                ft.Container(
                    bgcolor=get_c("card"), height=80, border_radius=20, padding=15,
                    # NIENTE OMBRA QUI -> Risolve il rettangolo grigio
                    border=ft.border.all(1, "#eeeeee"), 
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
        
        # Spazio per la navbar
        col.controls.append(ft.Container(height=100))
        
        return ft.Container(padding=20, content=col)

    def build_user():
        col = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        col.controls.append(ft.Container(height=40))
        col.controls.append(ft.Icon("person", size=80, color=get_c("primary")))
        col.controls.append(ft.Text("Profilo", size=20, weight="bold", color=get_c("text")))
        col.controls.append(ft.TextField(value=user_name, label="Nome", border_color=get_c("primary")))
        col.controls.append(ft.Divider())
        col.controls.append(ft.Container(
            bgcolor=get_c("primary"), width=300, padding=15, border_radius=10,
            on_click=lambda e: go_to_notes(),
            content=ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[ft.Icon(ICON_MAP["edit"], color="white"), ft.Text("APRI NOTE", color="white", weight="bold")])
        ))
        col.controls.append(ft.Container(height=100))

        return ft.Container(padding=20, content=col)

    def build_reader(title):
        col = ft.Column(spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Header Reader
        col.controls.append(ft.Container(padding=10, content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
            ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: go_to_home()),
            ft.Text(title, size=20, weight="bold", color=get_c("text")),
            ft.Container(width=40)
        ])))
        col.controls.append(ft.Divider(height=1))

        if title == "Inno":
            col.controls.append(ft.Icon(ICON_MAP["music"], size=50, color=get_c("primary")))
            col.controls.append(ft.Text(LYRICS_TEXT, text_align="center", color=get_c("text"), size=16))
        else:
            col.controls.append(ft.Text(f"Sezione: {title}", color=get_c("text")))
        
        col.controls.append(ft.Container(height=50))
        return ft.Container(padding=10, content=col)

    def build_notes():
        col = ft.Column(spacing=10)
        col.controls.append(ft.Container(padding=10, content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
            ft.IconButton(icon=ICON_MAP["arrow-left"], icon_color=get_c("text"), on_click=lambda e: go_to_user()),
            ft.Text("Note", size=20, weight="bold", color=get_c("text")),
            ft.Icon(ICON_MAP["save"], color=get_c("primary"))
        ])))
        col.controls.append(ft.TextField(value=user_notes, multiline=True, min_lines=10, border=ft.InputBorder.NONE, color=get_c("text"), bgcolor="white"))
        return ft.Container(padding=10, content=col)

    # --- RENDERER ---
    
    def render():
        page.controls.clear()
        
        # CONTENUTO PRINCIPALE (Scrollabile)
        main_content = None
        if current_page == "home": main_content = build_home()
        elif current_page == "user": main_content = build_user()
        elif current_page == "notes": main_content = build_notes()
        elif current_page == "reader": main_content = build_reader(reader_title)

        # Usiamo ListView per permettere lo scroll di tutto
        lv = ft.ListView(expand=True, controls=[main_content])
        page.add(lv)

        # NAVBAR FLOTTANTE (Solo Home/User)
        if current_page in ["home", "user"]:
            btn_h_bg = get_c("primary") if current_page == "home" else "white"
            btn_h_fg = "white" if current_page == "home" else get_c("text")
            btn_u_bg = get_c("primary") if current_page == "user" else "white"
            btn_u_fg = "white" if current_page == "user" else get_c("text")

            # Posizioniamo la navbar in basso usando un Stack fittizio o overlay
            # Ma per semplicità ora la mettiamo fissa in basso
            navbar = ft.Container(
                bgcolor="white", padding=15, 
                border_radius=ft.border_radius.only(top_left=20, top_right=20),
                border=ft.border.only(top=ft.border.BorderSide(1, "#eeeeee")),
                content=ft.Row(alignment=ft.MainAxisAlignment.SPACE_AROUND, controls=[
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_h_bg, on_click=lambda e: go_to_home(), content=ft.Row([ft.Icon(ICON_MAP["home"], color=btn_h_fg), ft.Text("HOME", color=btn_h_fg, weight="bold")])),
                    ft.Container(padding=10, border_radius=10, bgcolor=btn_u_bg, on_click=lambda e: go_to_user(), content=ft.Row([ft.Icon(ICON_MAP["user"], color=btn_u_fg), ft.Text("PROFILO", color=btn_u_fg, weight="bold")]))
                ])
            )
            # Aggiungiamo la navbar sopra la lista (in un layout fisso)
            page.overlay.append(ft.Container(
                content=navbar,
                alignment=ft.alignment.bottom_center,
                padding=0,
                margin=0
            ))

        page.update()

    # Funzioni Navigazione
    def go_to_home(e=None): nonlocal current_page; page.overlay.clear(); current_page = "home"; render()
    def go_to_user(e=None): nonlocal current_page; page.overlay.clear(); current_page = "user"; render()
    def go_to_notes(e=None): nonlocal current_page; page.overlay.clear(); current_page = "notes"; render()
    def go_to_reader(t): nonlocal current_page, reader_title; page.overlay.clear(); current_page = "reader"; reader_title = t; render()

    render()

if __name__ == "__main__":
    ft.app(target=main)
