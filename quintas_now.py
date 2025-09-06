import FreeSimpleGUI as sg
from PIL import Image, ExifTags
import io
import os
import webbrowser
import requests

current_image = None
image_path = None
last_image = []


layout = [
    [sg.Menu([
        ['Files', ['Open', 'Open URL', 'Save', 'Close']],
        ['EXIF', ['Show image data', 'Show GPS data']],
        ['Image', ['Filters', ['B/W', 'Sepian', 'Negative', '4 bits',
                                'Blur', 'Borderline', 'Detail', 'Border highlight',
                                'Topography', 'Dectect borders', 'Sharpness', 'Smooth',
                                'Min Filter', 'Max Filter'],
                    'Rotate', ['Rotate 90 degrees clockwise', 'Rotate 90 degrees anti clockwise']]],
                    'Histogram RGB'
        ['Commands', ['Undo']],
        ['About the image', ['Information']]
        ['About', ['Developers']]
    ])],
    [sg.Image(key='-IMAGE-', size=(800, 600))]
]

window = sg.Window('Processamento de Imagens', layout, finalize=True)

while True:
    event, values = window.read()

    if event in (sg.WINDOW_CLOSED, 'Close'):
        break
    elif event == 'Open':
        arquivo = sg.popup_get_file('Selecionar image', file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
        if arquivo:
            open_image(arquivo)
    elif event == 'Open URL':
        url = sg.popup_get_text("Digite a url")
        if url:
            url_download(url)
    elif event == 'Save':
        if image_atual:
            arquivo = sg.popup_get_file('Salvar image como', save_as=True, file_types=(("Imagens", "*.png;*.jpg;*.jpeg;*.gif"),))
            if arquivo:
                save_image(arquivo)
    elif event == 'Negative':
        invert_img_colors()
    elif event == 'Sepian':
        sepia_img_colors()
    elif event == 'B/W':
        preto_branco_img_colors()
    elif event == 'Information':
        info_image()
    elif event == "Undo":
        undo()
    elif event == 'Show image data':
        exif_data()
    elif event == 'Show GPS data':
        gps_data()
    elif event == 'Developers':
        sg.popup('Desenvolvido por Caiozika 👌👌👌👌👌👌👌')