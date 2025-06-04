from comunidade_impressionadora import app,database,bcrypt
from flask import Flask,render_template,redirect,request,flash,url_for,abort
from comunidade_impressionadora.forms import FormLogin,FormCriarConta,FormEditarPerfil,FormCriarPost
from comunidade_impressionadora.models import Usuario,Post
from flask_login import login_user,logout_user,current_user,login_required
import os
import secrets
from PIL import Image


@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html',posts=posts)


@app.route('/contato')
@login_required
def contato():
    return render_template('contato.html')


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html',lista_usuarios=lista_usuarios)


@app.route('/login',methods=['GET','POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha,form_login.senha.data):
            login_user(usuario,remember=form_login.lembrar_dados.data)
            flash(f'Login feito com Sucesso no e-mail {form_login.email.data}',category='success')
            pagina = request.args.get('next')
            if pagina:
                return redirect(pagina)
            else:
                return redirect(url_for('home'))
        else:
            flash('Não possivel fazer o Login! E-mail ou Senha Incorretos!',category='danger')
    if form_criarconta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
        usuario = Usuario(username=form_criarconta.username.data,email=form_criarconta.email.data,senha=senha_crypt)
        database.session.add(usuario)
        database.session.commit()
        flash(f'Conta Criada com Sucesso no e-mail {form_criarconta.email.data}',category='success')
        return redirect(url_for('home'))
    return render_template('login.html',form_login=form_login,form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Saindo com Sucesso', category="success")
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static',filename=f'foto_perfil/{current_user.foto_perfil}')
    return render_template('perfil.html',foto_perfil=foto_perfil)


@app.route('/post/criar',methods=['GET','POST'])
@login_required
def criarpost():
    form_criarpost = FormCriarPost()
    if form_criarpost.validate_on_submit():
        post = Post(autor=current_user,titulo=form_criarpost.titulo.data,corpo=form_criarpost.corpo.data)
        database.session.add(post)
        database.session.commit()
        return redirect(url_for('home'))
    return render_template('criarpost.html',form_criarpost=form_criarpost)


def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome,ext = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + ext
    caminho_arquivo = os.path.join(app.root_path,'static/foto_perfil',nome_arquivo)
    tamanho = (400,400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_arquivo)
    return nome_arquivo


def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)



@app.route('/editarperfil',methods=['GET','POST'])
@login_required
def editarperfil():
    foto_perfil = url_for('static', filename=f'foto_perfil/{current_user.foto_perfil}')
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Perfil Atualizado com Sucesso',category='success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    return render_template('editarperfil.html',foto_perfil=foto_perfil,form=form)


@app.route('/post/<post_id>',methods=['GET','POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form_editarpost = FormCriarPost()
        if request.method == 'GET':
            form_editarpost.titulo.data = post.titulo
            form_editarpost.corpo.data = post.corpo
        elif form_editarpost.validate_on_submit():
            post.titulo = form_editarpost.titulo.data
            post.corpo = form_editarpost.corpo.data
            flash('Post Atualizado com Sucesso',category='success')
            return redirect('home')
    else:
        form_editarpost = None
    return render_template('post.html',post=post,form_editarpost=form_editarpost)


@app.route('/post/<post_id>/excluir',methods=['GET','POST'])
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluido com Sucesso',category='danger')
        return redirect(url_for('home'))
    else:
        abort(403)
