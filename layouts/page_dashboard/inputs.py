from dash import Input

from layouts.page_dashboard import dropdown_date, dropdown_messages_date

in_value_dropdown_date = Input(dropdown_date, "value")
in_value_dropdown_messages_date = Input(dropdown_messages_date, "value")
