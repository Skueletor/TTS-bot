from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import time, tempfile, azure.cognitiveservices.speech as speechsdk

#Todo sobre Pyrogram, el registro
api_id = "14055159"
api_hash = "bb6ef9e05341d820145de3f4d2bdbe1b"
bot_token = "6543848254:AAGyuHPSJky6MkOCdyKTvRN_rKSpY7QVknI"
app = Client("mi_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

#Todo el registro de Azure con su API
speech_key = "d846d186c5da419a8b4fd413d43b105a"
service_region = "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
speech_config.speech_synthesis_voice_name = "es-CR-JuanNeural"

#Uso de vectores y diccionarios
owners = [1426532395, 2059862037, 1216717141]
voces = {
        'es-CR-JuanNeural': "Juan - Costa Rica 🇨🇷",
        'es-GT-AndresNeural': "Andrés - Guatemala 🇬🇹",
        'es-MX-JorgeNeural': "Jorge - México 🇲🇽",
        'es-PA-MargaritaNeural': "Margarita - Panamá 🇵🇦",
        'es-DO-EmilioNeural': "Emilio - República Dominicana 🇩🇴",
        'es-VE-PaolaNeural': "Paola - Venezuela 🇻🇪"}

#Mensajes colocados en variables, básicamente para mantener más limpio el código
START_MSG_OWNER = "Hola {}, usted es parte de la lista de administradores del bot :)\nBienvenido al bot."
START_MSG = "Hola {}, bienvenido al bot :)\nEnvía /hablar seguido del texto que deseas convertir en voz, si necesitas más ayuda prueba el comando /help."
HELP_MSG = """Hola {}, para usar el bot debes escribir /hablar seguido del texto, el bot procesará el texto y lo convertirá en voz, además puedes seleccionar un cuento con los botones y modificarlo a tu gusto [😊](https://graph.org/file/930d1a2dcbc4fdf28c754.jpg)"""
ABOUT_MSG = """Este bot fue hecho por:
- [Juan Luis Menacho](https://t.me/DKzippO).
- [Delsy Noelia Cuellar](https://t.me/noeliacuellar_19).
- [José María Ayala](https://t.me/josemaria002).
"""

#Botones que aparecen en los mensajes
START_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('Source 🧑‍💻', url='https://github.com'),
        InlineKeyboardButton('Devs 😎', callback_data='about')
    ],[
        InlineKeyboardButton('Ayuda 🆘', callback_data='help'),
        InlineKeyboardButton('Info ℹ️', callback_data='about'),
        InlineKeyboardButton('Cerrar ❌', callback_data='close')
    ],[
        InlineKeyboardButton('Voces 🗣', callback_data='voice')
    ]]
)
HELP_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('Source 🧑‍💻', url='https://github.com'),
        InlineKeyboardButton('Devs 😎', callback_data='about')
    ],[
        InlineKeyboardButton('Inicio 🏡', callback_data='home'),
        InlineKeyboardButton('Info ℹ️', callback_data='about'),
        InlineKeyboardButton('Cerrar ❌', callback_data='close')
    ],[
        InlineKeyboardButton('Voces 🗣', callback_data='voice')
    ]]
)
ABOUT_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('Source 🧑‍💻', url='https://github.com'),
        InlineKeyboardButton('Devs 😎', callback_data='about')
    ],[
        InlineKeyboardButton('Ayuda 🆘', callback_data='help'),
        InlineKeyboardButton('Inicio 🏡', callback_data='home'),
        InlineKeyboardButton('Cerrar ❌', callback_data='close')
    ],[
        InlineKeyboardButton('Voces 🗣', callback_data='voice')
    ]]
)
VOICES_BUTTONS = InlineKeyboardMarkup(
    [[
        InlineKeyboardButton('Juan - Costa Rica 🇨🇷', callback_data='es-CR-JuanNeural')
    ],[
        InlineKeyboardButton('Andrés - Guatemala 🇬🇹', callback_data='es-GT-AndresNeural')
    ],[
        InlineKeyboardButton('Jorge - México 🇲🇽', callback_data='es-MX-JorgeNeural')
    ],[
        InlineKeyboardButton('Margarita - Panamá 🇵🇦', callback_data='es-PA-MargaritaNeural')
    ],[
        InlineKeyboardButton('Emilio - República Dominicana 🇩🇴', callback_data='es-DO-EmilioNeural')
    ],[
        InlineKeyboardButton('Paola - Venezuela 🇻🇪', callback_data='es-VE-PaolaNeural')
    ],]
)

#Comandos de telegram con funciones
@app.on_message(filters.private & filters.command("start"))
async def start(Client, message):
    if message.from_user.id in owners:
        await message.reply_text(
            text = START_MSG_OWNER.format(message.from_user.mention),
            disable_web_page_preview=True,
            )
    else:
        await message.reply_text(
            text = START_MSG.format(message.from_user.mention),
            reply_markup = START_BUTTONS)
@app.on_message(filters.private & filters.command(["help"]))
async def start(bot, message):
    await message.reply_text(
        text=HELP_MSG.format(message.from_user.mention),
        reply_markup=HELP_BUTTONS
    )
@app.on_message(filters.private & filters.command(["about"]))
async def start(bot, message):
    await message.reply_text(
        text=ABOUT_MSG.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=ABOUT_BUTTONS
    )
@app.on_message(filters.private & filters.command(["voces"]))
async def start(bot, message):
    await message.reply_text(
        text="Selecciona la voz de tu preferencia:",
        reply_markup=VOICES_BUTTONS
    )

#Al presionar los botones se ejecuta lo siguiente:
@app.on_callback_query()
async def cb_handler(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_MSG.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS,
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_MSG.format(update.from_user.mention),
            reply_markup=HELP_BUTTONS,
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_MSG.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS,
        )
    elif update.data == "voice":
        await update.message.edit_text(
            text="Seleccione la voz de su preferencia.",
            reply_markup=VOICES_BUTTONS
        )
    elif update.data in voces:  # Verifica si el valor está en el diccionario
        voz_elegida = update.data
        voz = voces[voz_elegida]  # Accede al valor correspondiente
        if voz:
            await update.message.edit_text(
                text=f"Voz seleccionada: {voz}\nEjecute /hablar y pruebe la nueva voz"
            )
        speech_config.speech_synthesis_voice_name = update.data
    else:
        await update.message.delete()

#Comando principal, /hablar
@app.on_message(filters.command("hablar"))
def hablar(_, message):
    texto = " ".join(message.command[1:])
    if texto:
        mensaje_grabando = message.reply("🎙 Grabando audio...")
        audio_data = sintetizar_voz(texto)
        time.sleep(3)
        mensaje_grabando.edit("✅ Audio grabado")

        if audio_data:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
                temp_audio_file.write(audio_data)

            message.reply_voice(temp_audio_file.name, caption="Mensaje de voz convertido y enviado: {}".format(texto))
        else:
            message.reply("Lo siento, no pude convertir el texto en voz.")
    else:
        message.reply("Por favor, proporciona el texto que deseas convertir en voz.")

#Función que sintetiza la voz, trabaja directamente con la API de azure
def sintetizar_voz(texto):
    audio_config = speechsdk.audio.AudioOutputConfig(filename="test.mp3")
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = speech_synthesizer.speak_text_async(texto).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    else:
        return None

app.run()
