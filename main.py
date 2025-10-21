import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    testo_marca = ft.TextField('Marca')
    testo_modello = ft.TextField('Modello')
    testo_anno = ft.TextField('Anno')
    testo_contatore = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    def bottone_minus(e):
        testo_contatore.value = str(int(testo_contatore.value) - 1)
        page.update()

    def bottone_plus(e):
        testo_contatore.value = str(int(testo_contatore.value) + 1)
        page.update()

    # TODO


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    def clicca_bottone(e):
        marca = testo_marca.value
        modello = testo_modello.value
        try:
            anno = int(testo_anno.value)
            num_posti = int(testo_contatore.value)
            if testo_marca.value.isdigit() or testo_modello.value.isdigit():
                alert.show_alert("Marca e modello devono contenere testo, non numeri.")
                return
            autonoleggio.aggiungi_automobile(marca, modello, anno, num_posti)
            aggiorna_lista_auto()
            testo_marca.value = ""
            testo_modello.value = ""
            testo_anno.value = ""
            testo_contatore.value = "0"
            page.update()
        except ValueError:
            alert.show_alert("Anno e numero di posti devono essere numerici.")

        autonoleggio.aggiungi_automobile(marca, modello, anno, num_posti)
        aggiorna_lista_auto()

        testo_marca.value = ''
        testo_modello.value = ''
        testo_anno.value = ''

        page.update()

    # TODO

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    btnPress = ft.ElevatedButton("Aggiungi automobile", on_click=clicca_bottone)
    btnPress.color= 'blue'
    # TODO

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi automobile", size=20),
        ft.Row(spacing=20,
               controls=[testo_marca, testo_modello, testo_anno,
                        ft.IconButton(ft.Icons.REMOVE, on_click=bottone_minus, icon_color='red'), testo_contatore,
                        ft.IconButton(ft.Icons.ADD, on_click=bottone_plus, icon_color='green'),],
               alignment=ft.MainAxisAlignment.CENTER),
        ft.Row(btnPress, alignment=ft.MainAxisAlignment.CENTER),

        # TODO

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
