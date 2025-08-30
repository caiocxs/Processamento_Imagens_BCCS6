import FreeSimpleGUI as sg
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import io
import webbrowser
import os
import requests

image_atual = None
image_path = None

def url_download(url):
    global image_atual
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            image_atual = Image.open(io.BytesIO(r.content))
            show_image()
        else:
            sg.popup("Falha ao baixar a imagem. Verifique a URL e tente novamente.")
    except Exception as e:
        sg.popup(f"Erro ao baixar a imagem: {str(e)}")

def show_image():
    global image_atual
    try:
        resized_img = resize_image(image_atual)
        img_bytes = io.BytesIO()
        resized_img.save(img_bytes, format='PNG')
        window['-IMAGE-'].update(data=img_bytes.getvalue())
    except Exception as e:
        sg.popup(f"Erro ao exibir a imagem: {str(e)}")

def open_image(filename):
    global image_atual
    global image_path
    try:
        image_path = filename
        image_atual = Image.open(filename)    
        show_image()
    except Exception as e:
        sg.popup(f"Erro ao abrir a imagem: {str(e)}")

def save_image(filename):
    global image_atual
    try:
        if image_atual:
            with open(filename, 'wb') as file:
                image_atual.save(file)
        else:
            sg.popup("Nenhuma imagem aberta.")
    except Exception as e:
        sg.popup(f"Erro ao salvar a imagem: {str(e)}")

def resize_img_proportional(path):
    img = Image.open(path)

    new_w, new_h = (800, 600)
    width, height = img.size

    if (width > height):
        x = 1
    
    proportion = width * new_h / width
    new_w = proportion

    img = img.resize((int(new_w), int(new_h)), Image.Resampling.LANCZOS)
    return img


def resize_img(size, image, difference):
    img = image
    
    x = (size[0] - difference[0], size[1] - difference[1])

    img = img.resize(x, Image.Resampling.LANCZOS)
    return img


def convert_to_degrees(value):
        d = float(value[0])
        m = float(value[1])
        s = float(value[2])
        return d + (m / 60.0) + (s / 3600.0)


def show_link_popup(latitude, longitude):
    layout = [
        [sg.Text("Click the link below:")],
        [sg.Text(f"See on the map these coordinates: ({latitude}, {longitude})", enable_events=True, key='-LINK-', tooltip=f"https://www.google.com/maps?q={latitude},{longitude}")],
        [sg.Button('Close')]
    ]

    window = sg.Window('Link Popup', layout, modal=True)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close':
            break
        elif event == '-LINK-':
            webbrowser.open(f"https://www.google.com/maps?q={latitude},{longitude}")

    window.close()

img = None
path = None

layout2 = [
    [sg.Menu([["File", ["Open", "About", "Quit"]], ["EXIF", ["Show image data", "Show GPS data"]], ["Help", ["Credits"]]])],
    [sg.Image(key = "-IMAGE-", size = (800,600))],
    [sg.Sizegrip()]
]

window2 = sg.Window("Hey, you came!!", layout2, resizable = True, finalize = True)
difference = (window2.size[0] - 800, window2.size[1] - 600)
window2.bind("<Configure>", "_RESIZE_")
while True:
    ev2, va2 = window2.Read()
    if ev2 == sg.WIN_CLOSED or ev2 == "Quit":
        break

    if ev2 == "Open":
        path = sg.popup_get_file("Select an image file", file_types = (("Images", "*.jpg *.png"),))
        if path:
            img = resize_img_proportional(path)

            img_bytes = io.BytesIO()
            img.save(img_bytes, format = "PNG")

            window2["-IMAGE-"].update(data = img_bytes.getvalue())
            
    elif ev2 == "Credits":
        sg.popup("Developed by Computer Science - BCCS6 🤑🤑🤑🔥🔥🔥.\n\n Caio Xavier ")
    
    elif ev2 == "_RESIZE_" and path:
        img = resize_img(window2.size, Image.open(path), difference)

        img_bytes = io.BytesIO()
        img.save(img_bytes, format = "PNG")

        window2['-IMAGE-'].update(data = img_bytes.getvalue())
    
    elif ev2 == "About":
        if path:
            bytes_img = os.path.getsize(path)
            img_size_mb = bytes_img / (1024 * 1024)

            img_size = Image.open(path).size

            img_format = Image.open(path).format
            popup = sg.popup("Information about the image.", f"Size in MB: {img_size_mb:.2f}MB", f"Dimensions: {img_size}",
                            f"Format: {img_format}")
        else:
            popup = sg.popup("Please select an image.")

    elif ev2 == "Show image data":
        if path:
            exif = Image.open(path)._getexif()

            if exif:
                data = []
                for tag_id, value in exif.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    data.append((tag_name, value))
                
                popup = sg.popup("Here it is the data:", '\n'.join(f"{t[0]}: {t[1]}" for t in data))
        else: 
            popup = sg.popup("Please select an image.")

    elif ev2 == "Show GPS data":
        if path:
            exif = Image.open(path)._getexif()
            
            if exif:
                gps_info = {}
                for tag_id, value in exif.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    if tag_name == "GPSInfo":
                        for gps_tag_id, gps_value in value.items():
                            gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
                            gps_info[gps_tag_name] = gps_value
                        break
                
                if sg.popup_yes_no("Here it is the data:", '\n'.join(f"{key}: {value}" for key, value in gps_info.items()),
                    "Do you want the coordinates?") == "Yes":
                    latitude = None
                    longitude = None

                    if "GPSLatitude" in gps_info and "GPSLatitudeRef" in gps_info:
                        latitude = convert_to_degrees(gps_info["GPSLatitude"])
                        if gps_info["GPSLatitudeRef"] == "S":
                            latitude *= -1

                    if "GPSLongitude" in gps_info and "GPSLongitudeRef" in gps_info:
                        longitude = convert_to_degrees(gps_info["GPSLongitude"])
                        if gps_info["GPSLongitudeRef"] == "W":
                            longitude *= -1

                    if latitude and longitude:
                        if sg.popup_yes_no("The coordinates are: ", latitude, longitude, "See in google!") == "Yes":
                            show_link_popup(latitude, longitude)

        else: 
            popup = sg.popup("Please select an image.")

window2.close()