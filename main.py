import flet as ft

def main(page: ft.Page):
    # Setup essenziale
    page.bgcolor = "#f3f0e9"
    page.scroll = None # Niente scroll sulla root
    
    # Unica colonna semplice
    col = ft.Column(controls=[
        ft.Text("M2G APP", size=30, color="black", weight="bold"),
        ft.Container(height=20),
        ft.Container(
            bgcolor="white", padding=20, border_radius=10,
            content=ft.Row([
                ft.Container(width=20, height=20, bgcolor="green"),
                ft.Text("Lodi Mattutine", color="black")
            ])
        ),
        ft.Container(
            bgcolor="white", padding=20, border_radius=10, margin=ft.margin.only(top=10),
            content=ft.Text("Se vedi questo funziona", color="black")
        )
    ])

    page.add(col) # Aggiunta diretta

if __name__ == "__main__":
    ft.app(target=main)
