import flet as ft

# --- VERSIONE 64.0: DEBUG GEOMETRICO (NO ICONE) ---
# DIAGNOSI: L'app caricava lo sfondo (Beige) ma si bloccava sul contenuto.
# CAUSA PROBABILE: Il caricamento del font delle icone (ft.Icon) fallisce e blocca il disegno.
# SOLUZIONE: Sostituiamo TUTTE le icone con dei quadratini colorati.
# Se questa versione mostra i testi e i quadrati, sappiamo che il colpevole sono le Icone.

def main(page: ft.Page):
    # 1. SETUP
    page.title = "M2G App"
    page.bgcolor = "#f3f0e9" # Beige (Se lo vedi, il setup è ok)
    page.padding = 20
    
    # Niente scroll sulla pagina per ora, per sicurezza massima
    page.clean()

    # --- COLORI ---
    c_primary = "#6a8a73" # Verde
    c_text = "#1a1a1a"    # Nero

    # --- COSTRUZIONE ELEMENTI (SENZA USARE ft.Icon) ---

    # 1. HEADER
    # Invece del logo icona, usiamo testo puro
    header = ft.Row(controls=[
        ft.Container(
            width=60, height=60, bgcolor=c_primary, 
            border_radius=15, alignment=ft.alignment.center,
            content=ft.Text("M2G", color="white", size=20, weight="bold")
        ),
    ])
    
    welcome_text = ft.Text("Bentornato, Utente", size=22, weight="bold", color=c_text)

    # 2. CARD HELPER (Sostituzione Icone -> Quadrati)
    def simple_card(title):
        return ft.Container(
            bgcolor="white",
            height=80,
            border_radius=15,
            padding=15,
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(controls=[
                        # --- QUI C'ERA L'ICONA ---
                        # La sostituiamo con un Container (quadratino verde)
                        ft.Container(
                            width=50, height=50, bgcolor="#dbe4de", 
                            border_radius=12, alignment=ft.alignment.center,
                            content=ft.Container(width=20, height=20, bgcolor=c_primary) # IL QUADRATINO
                        ),
                        # -------------------------
                        ft.Container(width=10),
                        ft.Text(title, size=16, weight="bold", color=c_text)
                    ]),
                    # --- QUI C'ERA LA FRECCIA ---
                    # Sostituiamo con un piccolo cerchio grigio
                    ft.Container(width=10, height=10, bgcolor="#cccccc", border_radius=5)
                ]
            )
        )

    # --- AGGIUNTA DIRETTA ALLA PAGINA ---
    page.add(header)
    page.add(ft.Container(height=5))
    page.add(welcome_text)
    page.add(ft.Container(height=20))
    
    # Aggiungiamo le card
    page.add(simple_card("Lodi Mattutine"))
    page.add(ft.Container(height=10)) # Spazio manuale
    
    page.add(simple_card("Libretto"))
    page.add(ft.Container(height=10))
    
    page.add(simple_card("Inno"))
    page.add(ft.Container(height=10))
    
    page.add(simple_card("Foto ricordo"))
    
    # Bottone Test (Senza Icona)
    page.add(ft.Container(height=20))
    page.add(ft.ElevatedButton("TEST BOTTONE", bgcolor=c_primary, color="white"))

    page.update()

# Nessuna dipendenza esterna
if __name__ == "__main__":
    ft.app(target=main)
