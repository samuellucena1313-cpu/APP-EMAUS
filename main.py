from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import json, os

base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=base_dir, static_folder=base_dir, static_url_path='/static')
app.secret_key = "emaus_secret_key"
CONFIG_FILE = os.path.join(base_dir, "config.json")
UPLOAD_FOLDER = os.path.join(base_dir, 'uploads')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {"username": "Usuario", "theme": "light", "font_size": 16, "profile_pic": ""}

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    config = load_config()
    return render_template('index.html', config=config)

@app.route('/login', methods=['GET', 'POST'])
def login():
    config = load_config()
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        if password == "EMAUS123":
            session['logged_in'] = True
            return redirect(url_for('index'))
        error = "Contraseña incorrecta"
    return render_template('login.html', config=config, error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/prayer')
def prayer():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    config = load_config()
    return render_template('prayer.html', config=config)

@app.route('/guide')
def guide():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    config = load_config()
    return render_template('guide.html', config=config)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    config = load_config()

    if request.method == 'POST':
        config['username'] = request.form.get('username')
        config['theme'] = request.form.get('theme')
        
        # Manejo de la imagen desde la galería
        file = request.files.get('profile_pic_file')
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            config['profile_pic'] = '/static/uploads/' + filename

        save_config(config)
        return redirect(url_for('index'))
    return render_template('settings.html', config=config)


@app.route('/ocr')
def ocr():
    rosario_data = {
        "introduccion": {
            "titulo": "ORACIÓN INTRODUCTORIA",
            "texto": "Padre Celestial, en nombre de Tu Hijo Jesucristo, te pido que envíes sobre mí a tu Espíritu Santo, a fin de que mi corazón pueda abrirse y prepararse a aceptar Tu presencia en Jesucristo. Tú nos enviaste a tu Hijo y Él es el Emmanuel, el Dios con nosotros. Jesús abre nuestros corazones, así como abriste los corazones de los discípulos de Emaús, Tú te uniste a ellos, caminaste a su lado como un extraño, pero también como alguien dispuesto a escuchar sus lamentaciones, para así poder abrir sus corazones y revelarte a ellos. Fue así como se derritió el hielo en sus corazones y ellos pudieron reconocerte. Jesús, aquí estoy yo delante de ti y te ruego, que hagas todo lo posible para que también mi corazón pueda reconocer tu Palabra en este momento y pueda abrirse a la oración y al encuentro contigo y con mis hermanos en el amor. Amén.\n\n(En silencio, presenta a Jesús tu propia situación y comienza a orar)",
            "imagen": "/static/Jesus.jpg"
        },
        "misterios": [
            {
                "titulo": "PRIMER MISTERIO",
                "subtitulo": "JESÚS SE ACERCÓ A ELLOS",
                "lectura": "Dice San Lucas: \"Aquel mismo día dos discípulos se dirigían a un pueblecito llamado Emaús, que está a unos doce kilómetros de Jerusalén, e iban conversando sobre todo lo que había ocurrido. Mientras conversaban y discutían, Jesús en persona se les acercó y se puso a caminar con ellos, pero algo impedía que sus ojos lo reconocieran.\" (Lc 24, 13-16)",
                "reflexion": "Gracias Jesús por no haber rechazado a los discípulos de Emaús. Aunque ellos habían abandonado Jerusalén para regresar a sus casas, Tú los guiaste, no los dejes solos. Tú eres el viajero con los viajeros, Tú los entiendes y es por eso que te unes a ellos. ¡Gracias Señor!<br><br>Jesús, en este momento cuestiono seriamente mi vida. Tú eres también mi compañero de viaje, aun cuando muchas veces no soy capaz de reconocerte. Pero eres al fin, un verdadero compañero de viaje. ¿Señor, podrías acercarte más a mí? ¿Dime, de qué debo conversar con los demás en mi camino?<br><br>He de admitir que pocas veces hablo con otros de lo que te ocurrió y muchas otras también, mi conversación se convierte en una discusión, en el juicio que condena los errores que cometen las demás personas. ¡Perdóname Jesús!<br><br>Ahora comprendo que en muchas ocasiones Tú me has guiado de lejos y que, al acercarte a mí, no has podido participar en mi conversación porque esta no era buena. ¡Oh Jesús dame la fortaleza que necesito para vencer este mal dentro de mí! Haz que, en todo momento, mi conversación esté acompañada por Ti, para que así Tú siempre puedas participar de ella. Haz que, de ahora en adelante, Tú seas el tema de mi conversación, mi camino y mi luz en el viaje.",
                "imagen": "/static/misterio1.jpg"
            },
            {
                "titulo": "SEGUNDO MISTERIO",
                "subtitulo": "SE DETUVIERON ENTRISTECIDOS",
                "lectura": "Dice San Lucas: \"Jesús les dijo: «¿De qué van discutiendo por el camino?» Se detuvieron, y parecían muy entristecidos. Uno de ellos, llamado Cleofás, le contestó: «¿Cómo? ¿Eres tú el único peregrino en Jerusalén que no está enterado de lo que ha pasado aquí estos días?» «¿Qué pasó?», les preguntó.\" (Lc 24, 17-19)",
                "reflexion": "Jesús, tu pregunta sorprendió a los dos viajeros. Es evidente que ellos te amaban, por eso se sintieron heridos ante el hecho de que Tú, como extraño, no supieras nada acerca de lo sucedido. Ni siquiera podían imaginar, que Tú mismo, con tu resurrección, habías ya anulado la razón de su tristeza. Gracias Jesús, porque Tú puedes y Tú quieres desaparecer la tristeza y la desilusión y desean convertirlas en nueva esperanza. Gracias Jesús, porque Tú haces que esto sea posible también para mí.<br><br>Abre mis ojos Señor, para que sea capaz de reconocer los momentos en que pueda y deba yo ayudar a otros en Tu nombre. Perdóname Jesús, porque muchas veces he huido de los que están tristes, muchas veces he tenido miedo de aceptar a aquellos que son despreciados por otros, muchas veces no me he acercado a quienes estaban decepcionados y no he reconciliado a aquellos que peleaban. Perdóname Jesús y derrama en mí Tu divino Espíritu para poder ser tu compañero de viaje y luz para los que están tristes y que tienen problemas. ¡Oh Jesús, quédate conmigo y así podré ser una persona nueva para mi prójimo en el camino de la vida!",
                "imagen": "/static/misterio2.jpg"
            },
            {
                "titulo": "TERCER MISTERIO",
                "subtitulo": "NOSOTROS ESPERÁBAMOS…",
                "lectura": "Dice San Lucas: \"Le contestaron: «¡Todo el asunto de Jesús Nazareno!» Era un profeta poderoso en obras y palabras, reconocido por Dios y por todo el pueblo. Pero nuestros sumos sacerdotes y nuestros jefes renegaron de él, lo hicieron condenar a muerte y clavar en la cruz. Nosotros pensábamos que él sería el que debía libertar a Israel.\" (Lc 24, 19b-21)",
                "reflexion": "Jesús, los discípulos permanecieron junto a tí por largo tiempo. Tú les hablaste acerca de la muerte y la resurrección. Pero ellos no comprendieron nada. Permanecieron ajenos, aún después de haber estado tan cerca de ti. Su fe se acabó con tu muerte. Ellos te reconocían como un gran profeta en obras y palabras y por eso tuvieron esperanza. Pero esa esperanza falló, porque su fe no fue suficiente para hacerles comprender el significado de la Cruz, de la muerte, del sepulcro y de la resurrección.<br><br>Jesús, Tú sabes que también mi fe es débil. Por eso mi esperanza no es firme. Despierta mi fe Señor, aumenta mi fe para que mi esperanza no siga siendo frágil. Así seré capaz de decir con san Pablo: \"...yo sé bien en quien tengo puesta mi fe...\" (2Tm 1, 12). ¡Dame el don de tu Espíritu Santo!<br><br>Te pido ahora Jesús, por todos los que están decepcionados de los demás. Transforma a aquellas familias, en las que los padres se han decepcionado de los hijos. Tú bien sabes Jesús las esperanzas no realizadas se convierten en causa de conflictos. ¡Cámbianos a todos Señor y dirige tú nuestra esperanza!",
                "imagen": "/static/misterio3.jpg"
            },
            {
                "titulo": "CUARTO MISTERIO",
                "subtitulo": "¿NO ERA NECESARIO QUE PADECIERA?",
                "lectura": "Dice San Lucas: \"Entonces él les dijo: «¡Qué poco entienden ustedes y qué lentos son sus corazones para creer todo lo que anunciaron los profetas! 26 ¿No tenía que ser así y que el Mesías padeciera para entrar en su gloria? 27 Y les interpretó lo que se decía de él en todas las Escrituras, comenzando por Moisés y siguiendo por los profetas.\" (Lc 24, 25-27)",
                "reflexion": "¡Oh Jesús, ni siquiera para ti fue fácil padecer! Sin embargo, Tú habías anunciado que tendrías que sufrir y como sufriste! Pero Señor, ¿quién puede hacer entender a un inocente que aún los inocentes tienen que sufrir? ¿Quién hará comprender a los que han sido privados de sus derechos por medio de sus sufrimientos? ¿Quién hará ver a los niños inocentes que han encontrado la muerte en el vientre de sus madres, que esto tenía que ser así? Jesús, tú no permaneces mudo ante las víctimas de la violencia, tú conviertes el destino de todos aquellos que sufren en la gloria de la resurrección.<br><br>Permite Señor, que la cruz de todos aquellos que sufren florezca con la esperanza y la alegría de la resurrección, para que así puedan ser revestidos con la paz y alimentados con la leche y la miel de la nueva justicia. Ayúdanos a todos a ser capaces de cargar con nuestra propia cruz como tú mismo lo hiciste: con amor, aun cuando no podamos entenderla. María, Madre de todos los que sufren, no nos dejes solos en medio de nuestros sufrimientos, así como tampoco dejaste solo a tu Hijo.",
                "imagen": "/static/misterio4.jpg"
            },
            {
                "titulo": "QUINTO MISTERIO",
                "subtitulo": "¿NO ARDÍAN NUESTROS CORAZONES?",
                "lectura": "Dice San Lucas: \"Al llegar cerca del pueblo al que iban, hizo como que quisiera seguir adelante, pero ellos le insistieron diciendo: «Quédate con nosotros, ya está cayendo la tarde y se termina el día.» Entró, pues, para quedarse con ellos. Y mientras estaba en la mesa con ellos, tomó el pan, pronunció la bendición, lo partió y se lo dio. En ese momento se les abrieron los ojos y lo reconocieron, pero él desapareció. Entonces se dijeron el uno al otro: «¿No sentíamos arder nuestro corazón cuando nos hablaba en el camino y nos explicaba las Escrituras?»\" (Lc 24, 28-32)",
                "reflexion": "Jesús, en este misterio te pido por todos aquellos que proclaman tu Palabra. Llénalos de tu Espíritu, inspira su palabra. Enciende el fuego que caliente los corazones de aquellos que los tienen fríos, que suavice los corazones de aquellos que los tienen duros. Haz que proclamen tu Palabra con poder para convertir a los corazones que maldicen en corazones que te alaben y te glorifiquen, los corazones desesperados en corazones llenos de esperanza y los corazones desolados en corazones llenos de alegría.<br><br>Te ruego especialmente por los mensajeros de tu Palabra que se sienten tristes y solos, por aquellos que se preguntan por qué han sido llamados y por aquellos que abandonan su vocación. Por favor Jesús, da a todos tus sacerdotes la gracia de celebrar la misa de tal manera, que siempre puedan reconocerte en la Hostia Sagrada. Señor, te pido particularmente por todos aquellos que reciben la Sagrada Comunión, para que puedan reconocerte y nunca olvidarte.",
                "imagen": "/static/misterio5.jpg"
            }
        ],
        "conclusion": {
            "titulo": "ORACIÓN CONCLUSIVA",
            "texto": "¡Gracias Jesús por este encuentro! Se Tú Señor el remedio a mi alma y la protección de mi vida. A partir de hoy, al igual que tus discípulos después de haberse encontrado contigo, yo quiero caminar decidido por la vida y no rehuir a mis obligaciones. Espero que tú y tu Madre Santísima sean siempre mis compañeros de viaje. Amén.",
            "imagen": "/static/Jesus.jpg"
        }
    }
    return jsonify(rosario_data)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
