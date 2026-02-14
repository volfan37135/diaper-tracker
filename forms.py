from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DecimalField, DateField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional
from datetime import date


SIZE_CHOICES = [
    ('Newborn', 'Newborn'),
    ('Size 1', 'Size 1'),
    ('Size 2', 'Size 2'),
    ('Size 3', 'Size 3'),
    ('Size 4', 'Size 4'),
    ('Size 5', 'Size 5'),
    ('Size 6', 'Size 6'),
    ('Size 7', 'Size 7'),
]

DIAPERS_PER_BOX_CHOICES = [
    ('20', '20'), ('24', '24'), ('32', '32'), ('40', '40'),
    ('50', '50'), ('60', '60'), ('72', '72'), ('80', '80'),
    ('84', '84'), ('92', '92'), ('100', '100'), ('120', '120'),
    ('128', '128'), ('144', '144'), ('160', '160'), ('custom', 'Custom'),
]


class PurchaseForm(FlaskForm):
    date = DateField('Date', default=date.today, validators=[DataRequired()])
    size = SelectField(
        'Diaper Size',
        choices=SIZE_CHOICES,
        validators=[DataRequired()]
    )
    num_boxes = SelectField(
        'Number of Boxes',
        choices=[(str(i), str(i)) for i in range(1, 11)],
        validators=[DataRequired()]
    )
    diapers_per_box = SelectField(
        'Diapers per Box',
        choices=DIAPERS_PER_BOX_CHOICES,
        validators=[DataRequired()]
    )
    custom_diapers_per_box = IntegerField('Custom Quantity', validators=[Optional()])
    brand = StringField('Brand', validators=[DataRequired()])
    cost = DecimalField('Cost ($)', places=2, validators=[
        DataRequired(), NumberRange(min=0.01)
    ])
    date_opened = DateField('Date Opened', validators=[Optional()])


class BrandForm(FlaskForm):
    brand_name = StringField('Brand Name', validators=[DataRequired()])
