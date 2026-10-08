# Gatti per la sfida "Tocca a voi" (slide GAN)

Nella slide GAN, il passo 5 mostra una griglia 3×3: **una sola foto è vera**, le altre 8 sono create da un'AI. La classe vota dal telefono quale è quella vera.

In questa cartella servono 9 file:

| File | Cosa contiene |
|---|---|
| `vero.jpg` | La foto vera: un gattino tigrato sdraiato su un divano grigio. Già presente. È una foto CC0 (pubblico dominio) presa da Wikimedia Commons ("Cat resting on a couch", Unsplash). |
| `ai-1.jpg` … `ai-8.jpg` | 8 gatti generati con un'AI. Da creare. |

Se un file manca, nella griglia compare la scritta "manca il file".

## Come creare gli 8 gatti AI

1. Usate un generatore di immagini gratuito, per esempio ChatGPT, Gemini o Bing Image Creator.
2. Generate un'immagine per ogni prompt qui sotto, in formato **quadrato (1:1)**.
3. Salvatele qui con i nomi `ai-1.jpg`, `ai-2.jpg`, … `ai-8.jpg`.

Perché il gioco sia difficile, le immagini devono sembrare **foto normali fatte col telefono**, non illustrazioni. Scartate quelle che sembrano disegni o troppo perfette.

1. `Close-up smartphone photo of a young tabby kitten lying on a grey fabric sofa, looking at the camera, soft window light, shallow depth of field, natural colors, square format`
2. `Casual phone photo of an orange tabby cat sitting on a wooden kitchen floor, looking up, indoor evening light, slightly grainy, square format`
3. `Close-up photo of a grey British Shorthair cat with copper eyes resting on a knitted blanket, natural daylight, realistic, square format`
4. `Photo of a black cat with green eyes sitting on a windowsill, soft backlight from the window, realistic smartphone photo, square format`
5. `Close-up of a tabby kitten sleeping curled up on a dark couch cushion, whiskers in focus, natural light, realistic photo, square format`
6. `Photo of a white and grey cat lying in the sun on a terracotta floor, eyes half closed, realistic, slightly overexposed like a phone picture, square format`
7. `Close-up portrait of a calico cat looking slightly to the side, outdoor garden background blurred, natural light, realistic photo, square format`
8. `Photo of a fluffy brown tabby Maine Coon kitten lying on a grey carpet, looking at the camera, indoor light, realistic smartphone photo, square format`

Controllate i termini del servizio che usate per generarle.

Dopo averle salvate, pubblicate la cartella (commit e push) insieme alla presentazione: i telefoni degli studenti caricano le foto dal sito online.
