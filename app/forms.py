from flask_wtf import FlaskForm
from wtforms import FormField, EmailField, StringField, BooleanField, SubmitField, TextAreaField, FieldList, SelectField, TimeField
from wtforms.validators import DataRequired, Email, Optional, URL

class CTAForm(FlaskForm):
    text = StringField('CTA Text', validators=[DataRequired()])
    link = StringField('CTA Link', validators=[Optional(), URL(message="Invalid URL")])


class TargetAudienceForm(FlaskForm):
    target_audience = StringField('Target Audience', render_kw={"placeholder": "Example: Small businesses on LinkedIn located in the US."})


class AccountSetupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()], render_kw={"placeholder": "Enter your name"})
    
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Your email address"})
    
    password = StringField('password', validators=[DataRequired()], render_kw={"placeholder": "Set up your password to our website"})

    confirm_password = StringField('confirm password', validators=[DataRequired()], render_kw={"placeholder": "your password again"})

    about_yourself = TextAreaField('Tell us about your account', validators=[DataRequired()], 
        render_kw={"placeholder": "Example: I am Hiwa. I train AI to create high-quality AI posts. "
                                  "I think AI can help businesses, but only if used in a controlled "
                                  "way so the content doesn’t hurt the creator, but helps them grow and "
                                  "make money from LinkedIn."})
    
    # CTA FieldList to handle multiple CTAs (text and link)
    ctas = FieldList(FormField(CTAForm), max_entries=10)

    # Manage multiple Target Audiences as a FieldList of FormFields
    target_audience = FieldList(FormField(TargetAudienceForm), min_entries=1)
    
    # Tone selection dropdown with predefined options and descriptions
    tone = SelectField('Tone', choices=[
        ('ai_decide', 'Let the AI decide the best tone for your audience'),
        ('bold', 'Bold - Strong and daring tone that leaves a lasting impression'),
        ('persuasive', 'Persuasive - Convincing tone designed to influence and persuade'),
        ('casual', 'Casual - Relaxed and informal tone for more light-hearted content'),
        ('inspirational', 'Inspirational - Encouraging and motivating tone to inspire your audience'),
        ('professional', 'Professional - Expert tone that builds trust and authority'),
        ('humorous', 'Humorous - Light-hearted tone to entertain and amuse your audience'),
        ('empathetic', 'Empathetic - Caring and understanding tone that connects emotionally'),
        ('confident', 'Confident - Bold and assertive tone that communicates certainty')
        
        
    ], validators=[DataRequired()])

    post_times = FieldList(TimeField('Post Time', validators=[Optional()]))
    
    # Western country time zones dropdown with clearer descriptions
    time_zone = SelectField('Time Zone', choices=[
        ('EST', 'Eastern Standard Time (EST) - Eastern US & Canada'),
        ('PST', 'Pacific Standard Time (PST) - Western US & Canada'),
        ('CST', 'Central Standard Time (CST) - Central US & Canada'),
        ('MST', 'Mountain Standard Time (MST) - Mountain US & Canada'),
        ('CET', 'Central European Time (CET) - Most of Europe'),
        ('BST', 'British Summer Time (BST) - United Kingdom'),
        ('IST', 'Irish Standard Time (IST) - Ireland'),
        ('HST', 'Hawaii-Aleutian Standard Time (HST) - Hawaii, US'),
        ('AKST', 'Alaska Standard Time (AKST) - Alaska, US'),
        ('AEST', 'Australian Eastern Standard Time (AEST) - Eastern Australia'),
        ('NZST', 'New Zealand Standard Time (NZST) - New Zealand')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Save Preferences')

