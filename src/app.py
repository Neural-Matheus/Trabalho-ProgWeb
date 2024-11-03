from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint

app = Flask(__name__)
app.config['SECRET_KEY'] = '2461be02c858c8b55257781503426241'

# Definindo o Blueprint
main_bp = Blueprint('main', __name__)

@main_bp.route('/login')
def login():
    return render_template('model/html/pagina_login.html')

@main_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        flash(f'Recebido cadastro com email: {email}')
        return redirect(url_for('main.login'))

    return render_template('model/html/pagina_cadastro.html')

# Registrando o Blueprint
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)
