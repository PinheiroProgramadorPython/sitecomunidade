from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,EmailField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from comunidade_impressionadora.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(),Email()])
    senha = PasswordField(validators=[DataRequired(),Length(6,20)])
    confirma_senha = PasswordField(validators=[DataRequired(),EqualTo("senha")])
    botao_submit_criar_conta = SubmitField('criar conta')

    def validate_email(self,email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já esta Cadastrado! Faça Login ou Cadastre-se com outro E-mail')


class FormLogin(FlaskForm):
    email = StringField(validators=[Email(),DataRequired()])
    senha = PasswordField(validators=[Length(6,20)])
    lembrar_dados = BooleanField()
    botao_submit_login = SubmitField('login')


class FormEditarPerfil(FlaskForm):
    username = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto do Perfil',validators=[FileAllowed(['jpg', 'jpeg', 'png', 'PNG', 'JPG'])])
    curso_excel = BooleanField('Excel Impressionador')
    curso_vba = BooleanField('VBA impressionador')
    curso_ppt = BooleanField('Aprentaçãoes impressionadoras')
    curso_powerbi = BooleanField('Power Bi impressionador')
    curso_sql = BooleanField('SQL impressionador')
    curso_python = BooleanField('Python impressionador')
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self,email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuário com esse E-mail! Cadastre outro E-mail')


class FormCriarPost(FlaskForm):
    titulo = StringField(validators=[DataRequired()])
    corpo = TextAreaField(validators=[DataRequired(),Length(2,150)])
    botao_submit_criarpost = SubmitField('Criar Post')
