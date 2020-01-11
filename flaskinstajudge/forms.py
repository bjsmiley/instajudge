from wtforms import Form, StringField, TextAreaField, PasswordField, validators, FieldList, FormField



# class ImageUrlForm(Form):
#     url = StringField('Url', [validators.Length(min=4,max=100)])

# class ImageUrlsForm(Form):
#     """A form for one or more addresses"""
#     urls = FieldList(FormField(ImageUrlForm), min_entries=1)

class SignInForm(Form):
    username = StringField('Username', [validators.Length(min=1,max=100)])
    password = PasswordField('Password',[validators.DataRequired()])