from dash import callback, html, dcc
from flask import request

from data_storage import data_store
from layouts import (
  page_data_status,
  page_dashboard,
  page_settings,
  page_data_status_telegram
)
from reactivity import out_children_router_view, in_pathname_url
import layouts
from reactivity.storage.background_task import out_storage_background_task
from reactivity.storage.background_task_progress import out_storage_background_task_progress
from reactivity.storage.global_state import state_storage_global_state
from reactivity.storage.missing_data_counter import out_storage_missing_data_counter


def create_login_page():
    return html.Div([
        html.H1("Login", style={'textAlign': 'center', 'marginBottom': '30px'}),
        html.Form([
            html.Div([
                html.Label("Username:", style={'display': 'block', 'marginBottom': '5px'}),
                dcc.Input(
                    id='username',
                    type='text',
                    name='username',
                    style={'width': '100%', 'padding': '8px', 'marginBottom': '15px'}
                ),
            ]),
            html.Div([
                html.Label("Password:", style={'display': 'block', 'marginBottom': '5px'}),
                dcc.Input(
                    id='password',
                    type='password',
                    name='password',
                    style={'width': '100%', 'padding': '8px', 'marginBottom': '15px'}
                ),
            ]),
            html.Button(
                'Login',
                type='submit',
                style={
                    'width': '100%',
                    'padding': '10px',
                    'backgroundColor': '#007bff',
                    'color': 'white',
                    'border': 'none',
                    'borderRadius': '4px',
                    'cursor': 'pointer'
                }
            ),
        ], action='/login', method='post', style={'maxWidth': '300px', 'margin': '0 auto'})
    ], style={'textAlign': 'center', 'padding': '50px', 'maxWidth': '400px', 'margin': '0 auto'})


@callback(
  [
    out_children_router_view,
    out_storage_background_task_progress,
    out_storage_background_task,
    out_storage_missing_data_counter
  ],
  in_pathname_url,
  state_storage_global_state,
  prevent_initial_call=True
)
def display_page(pathname, global_state):
  session = request.cookies.get('session')
  session_value = "session_value"  # Replace this with your actual expected session value

  if session != session_value:
    return create_login_page(), *data_store.get_storage_update()

  print("-" * 20)
  print(f"entre a la pagina con el estate {data_store.global_state}")
  print("-" * 20)

  data = data_store.get_storage_update()

  if pathname == "/dash":
    return layouts.page_dashboard.layout, *data
  elif pathname.startswith("/dash/load_data"):
    return layouts.page_data_status.layout, *data
  elif pathname.startswith("/dash/telegram"):
    return layouts.page_data_status_telegram.layout, *data
  elif pathname.startswith("/dash/settings"):
    return layouts.page_settings.layout, *data
  else:
    return page_dashboard.layout, *data
