import os
import sqlite3
import random
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'chave_secreta_projeto_estudos'

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- 1. CLASSES E HERANÇA BÁSICA (FLASK-LOGIN) ---
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('database.db')
    data = conn.cursor().execute("SELECT id, username FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if data: return User(id=data[0], username=data[1])
    return None

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, meta_minutos INTEGER DEFAULT 0, total_segundos INTEGER DEFAULT 0)')
    cursor.execute('CREATE TABLE IF NOT EXISTS jardim (id INTEGER PRIMARY KEY AUTOINCREMENT, tipo_planta TEXT, usuario_id INTEGER, posicao INTEGER DEFAULT 0)')
    cursor.execute('CREATE TABLE IF NOT EXISTS repositorio (id INTEGER PRIMARY KEY AUTOINCREMENT, tipo TEXT, titulo TEXT, conteudo TEXT, resposta TEXT, usuario_id INTEGER)')
    conn.commit()
    conn.close()

init_db()


# =====================================================================
# 2. APLICAÇÃO DE OOP: CLASSES, HERANÇA E POLIMORFISMO (O CORAÇÃO DO PROJETO)
# =====================================================================

class ItemRepositorio:
    """Classe Base (Superclasse)"""
    def __init__(self, titulo, usuario_id):
        self.titulo = titulo
        self.usuario_id = usuario_id
        self.tipo = "indefinido"

    def preparar_dados(self):
        """Método que será sobrescrito (Polimorfismo)"""
        pass

    def salvar(self):
        """Método comum herdado por todos os filhos"""
        # Aqui o Polimorfismo age: ele chama o preparar_dados() específico de cada classe filha
        dados = self.preparar_dados() 
        
        conn = sqlite3.connect('database.db')
        conn.cursor().execute(
            "INSERT INTO repositorio (tipo, titulo, conteudo, resposta, usuario_id) VALUES (?, ?, ?, ?, ?)", 
            dados
        )
        conn.commit()
        conn.close()

class Resumo(ItemRepositorio):
    """Herança: Resumo é um ItemRepositorio"""
    def __init__(self, titulo, usuario_id, conteudo):
        super().__init__(titulo, usuario_id) # Chama o construtor da classe pai
        self.tipo = "resumo"
        self.conteudo = conteudo

    def preparar_dados(self):
        """Polimorfismo: Resumo salva seu texto na coluna conteúdo"""
        return (self.tipo, self.titulo, self.conteudo, "", self.usuario_id)

class Questao(ItemRepositorio):
    """Herança: Questao é um ItemRepositorio"""
    def __init__(self, titulo, usuario_id, pergunta, resposta):
        super().__init__(titulo, usuario_id)
        self.tipo = "questao"
        self.pergunta = pergunta
        self.resposta = resposta

    def preparar_dados(self):
        """Polimorfismo: Questão salva pergunta E resposta"""
        return (self.tipo, self.titulo, self.pergunta, self.resposta, self.usuario_id)

class ArquivoDigital(ItemRepositorio):
    """Herança: ArquivoDigital lida tanto com PDFs quanto com Músicas"""
    def __init__(self, titulo, usuario_id, arquivo_obj, tipo_arquivo):
        super().__init__(titulo, usuario_id)
        self.tipo = tipo_arquivo
        self.arquivo_obj = arquivo_obj

    def preparar_dados(self):
        """Polimorfismo: Lida com o salvamento físico no HD antes de ir pro Banco"""
        nome_arquivo = ""
        if self.arquivo_obj and self.arquivo_obj.filename:
            nome_arquivo = secure_filename(self.arquivo_obj.filename)
            self.arquivo_obj.save(os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo))
        return (self.tipo, self.titulo, nome_arquivo, "", self.usuario_id)

# =====================================================================


@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        user, pwd = request.form.get('username'), request.form.get('password')
        try:
            conn = sqlite3.connect('database.db')
            conn.cursor().execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (user, pwd))
            conn.commit()
            conn.close()
            flash('Conta criada! Faça login.')
            return redirect(url_for('login'))
        except: flash('Usuário já existe.')
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user, pwd = request.form.get('username'), request.form.get('password')
        conn = sqlite3.connect('database.db')
        data = conn.cursor().execute("SELECT id, username, password FROM usuarios WHERE username = ?", (user,)).fetchone()
        conn.close()
        if data and data[2] == pwd:
            login_user(User(data[0], data[1]))
            return redirect(url_for('index'))
        flash('Usuário ou senha incorretos.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index(): return render_template('index.html')

@app.route('/timer', methods=['GET', 'POST'])
@login_required
def timer():
    if request.method == 'POST':
        duracao = int(request.form.get('duracao', 0))
        planta = random.choice(["Carvalho", "Cerejeira", "Cacto"])
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        max_pos = cursor.execute("SELECT MAX(posicao) FROM jardim WHERE usuario_id = ?", (current_user.id,)).fetchone()[0]
        nova_posicao = (max_pos or 0) + 1
        
        cursor.execute("INSERT INTO jardim (tipo_planta, usuario_id, posicao) VALUES (?, ?, ?)", (planta, current_user.id, nova_posicao))
        cursor.execute("UPDATE usuarios SET total_segundos = total_segundos + ? WHERE id = ?", (duracao, current_user.id))
        conn.commit()
        conn.close()
        flash(f"Sessão finalizada! {duracao // 60} minutos contabilizados.")
        return redirect(url_for('jardim'))
    return render_template('timer.html')

@app.route('/metas', methods=['GET', 'POST'])
@login_required
def metas():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        nova_meta = request.form.get('nova_meta')
        if nova_meta:
            cursor.execute("UPDATE usuarios SET meta_minutos = ? WHERE id = ?", (nova_meta, current_user.id))
            flash(f"Meta de {nova_meta} minutos definida!")
        if 'resgatar' in request.form:
            plantas = ["Carvalho", "Cerejeira", "Cacto"]
            max_pos = cursor.execute("SELECT MAX(posicao) FROM jardim WHERE usuario_id = ?", (current_user.id,)).fetchone()[0]
            nova_posicao = (max_pos or 0) + 1
            for i in range(5):
                cursor.execute("INSERT INTO jardim (tipo_planta, usuario_id, posicao) VALUES (?, ?, ?)", (random.choice(plantas), current_user.id, nova_posicao + i))
            cursor.execute("UPDATE usuarios SET meta_minutos = 0 WHERE id = ?", (current_user.id,))
            flash("Parabéns! 5 árvores bônus foram adicionadas ao seu jardim!")
            conn.commit()
            conn.close()
            return redirect(url_for('jardim'))
        conn.commit()

    user_data = cursor.execute("SELECT meta_minutos, total_segundos FROM usuarios WHERE id = ?", (current_user.id,)).fetchone()
    conn.close()
    meta, total_minutos = user_data[0], user_data[1] // 60
    pode_resgatar = meta > 0 and total_minutos >= meta
    return render_template('metas.html', meta=meta, total_minutos=total_minutos, pode_resgatar=pode_resgatar)

@app.route('/jardim')
@login_required
def jardim():
    conn = sqlite3.connect('database.db')
    plantas = conn.cursor().execute("SELECT id, tipo_planta FROM jardim WHERE usuario_id = ? ORDER BY posicao ASC", (current_user.id,)).fetchall()
    conn.close()
    return render_template('jardim.html', plantas=plantas)

@app.route('/reordenar', methods=['POST'])
@login_required
def reordenar():
    ordem_ids = request.get_json()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    for index, planta_id in enumerate(ordem_ids):
        cursor.execute("UPDATE jardim SET posicao = ? WHERE id = ? AND usuario_id = ?", (index, planta_id, current_user.id))
    conn.commit()
    conn.close()
    return jsonify({"status": "sucesso"})

@app.route('/repositorio/<tipo>')
@login_required
def ver_repositorio(tipo):
    conn = sqlite3.connect('database.db')
    itens = conn.cursor().execute("SELECT id, titulo, conteudo, resposta FROM repositorio WHERE tipo=? AND usuario_id=?", (tipo, current_user.id)).fetchall()
    conn.close()
    return render_template('repositorio.html', tipo=tipo, itens=itens)


# --- 3. USO PRÁTICO DO POLIMORFISMO NA ROTA ---
@app.route('/adicionar/<tipo>', methods=['POST'])
@login_required
def adicionar(tipo):
    titulo = request.form.get('titulo')
    novo_item = None
    
    # Criamos o objeto específico dependendo do tipo
    if tipo == 'resumo':
        conteudo = request.form.get('conteudo')
        novo_item = Resumo(titulo, current_user.id, conteudo)
        
    elif tipo == 'questao':
        pergunta = request.form.get('conteudo')
        resposta = request.form.get('resposta')
        novo_item = Questao(titulo, current_user.id, pergunta, resposta)
        
    elif tipo in ['pdf', 'musica']:
        arquivo = request.files.get('arquivo')
        novo_item = ArquivoDigital(titulo, current_user.id, arquivo, tipo)

    # POLIMORFISMO EM AÇÃO: Não importa qual é a classe filha instanciada acima,
    # todas elas têm o método .salvar() e sabem exatamente como executá-lo!
    if novo_item:
        novo_item.salvar()

    return redirect(url_for('ver_repositorio', tipo=tipo))

if __name__ == '__main__':
    app.run(debug=True)
