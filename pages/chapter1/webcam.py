import asyncio
import base64
import dash, cv2
from dash import html, callback, clientside_callback
import dash_bootstrap_components as dbc
import threading

from dash.dependencies import Output, Input
from quart import Quart, websocket
from dash_extensions import WebSocket


dash.register_page(__name__, icon="uil:webcam")
delay_between_frames = 0.05  # add delay (in seconds) if CPU usage is too high

# Create small Dash application for UI.
layout = html.Div([
    dbc.Label("Test text", id="dummy_text"),
    html.Br(),
    dbc.Button(html.P("Run", className="card-text"), id="run_button", n_clicks=0),
    html.Br(),
    html.Img(style={'width': '40%', 'padding': 10}, id="video"),
    WebSocket(url=f"ws://127.0.0.1:5000/stream", id="ws")
])
# Copy data from websocket to Img element.
# app.clientside_callback("function(m){return m? m.data : '';}", Output("video", "src"), Input(f"ws", "message"))
# clientside_callback("function(m){return m? m.data : '';}", Output("video", "src"), Input(f"ws", "message"))


# @callback(
#     Output("dummy_text", "children"),
#     Input("run_button", "n_clicks")
# )
# def on_click_run(n):
#     ctx = dash.callback_context
#     trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
#     if trigger_id == "run_button":
#         @server.websocket("/stream")
#         async def stream():
#             camera = VideoCamera(0)  # zero means webcam
#             while True:
#                 if delay_between_frames is not None:
#                     await asyncio.sleep(delay_between_frames)  # add delay if CPU usage is too high
#                 frame = camera.get_frame()
#                 await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")
#         return "Run button clicked"
#     else:
#         raise dash.exceptions.PreventUpdate


# if __name__ == '__main__':
#     # threading.Thread(target=app.run_server).start()
#     server.run()
