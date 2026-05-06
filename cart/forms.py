from django import forms

class ProductChoices(forms.Form):

    STICKER_COUNT = [
        ("1", "1 принт"),
        ("3", "3 принти"),
    ]
    choices_count_sticker = forms.ChoiceField(
        choices=STICKER_COUNT,
        widget=forms.RadioSelect,
        initial="1",
        required=False
    )

    PRINT_POSITION = [
        ("FRONT", "Спереду"),
        ("BACK", "Ззаду"),
    ]
    choices_position = forms.ChoiceField(
        choices=PRINT_POSITION,
        widget=forms.RadioSelect,
        initial="FRONT",
        required=False
    )
    EMBROIDERY = [
        ("YES", "З вишивкою"),
        ("NO", "Без вишивки")
    ]

    choices_embroidery = forms.ChoiceField(
        choices=EMBROIDERY,
        widget=forms.RadioSelect,
        initial="YES",
        required=False
    )