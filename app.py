import asyncio
import base64
import dash
from dash import dcc, html, Output, Input, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from quart import Quart, websocket
import threading
from video_camera import VideoCamera


# app = dash.Dash(__name__, use_pages=True)

server = Quart(__name__)
app = dash.Dash(__name__, use_pages=True)


def create_nav_link(icon, label, href):
    return dcc.Link(
        dmc.Group(
            [
                dmc.ThemeIcon(
                    DashIconify(icon=icon, width=18),
                    size=30,
                    radius=30,
                    variant="light",
                ),
                dmc.Text(label, size="sm", color="gray"),
            ]
        ),
        href=href,
        style={"textDecoration": "none"},
    )


sidebar = dmc.Navbar(
    fixed=True,
    width={"base": 300},
    position={"top": 80},
    height=300,
    children=[
        dmc.ScrollArea(
            offsetScrollbars=True,
            type="scroll",
            children=[
                dmc.Group(
                    direction="column",
                    children=[
                        create_nav_link(
                            icon="radix-icons:rocket",
                            label="Home",
                            href="/",
                        ),
                    ],
                ),
                dmc.Divider(
                    label="Chapter 1", style={"marginBottom": 20, "marginTop": 20}
                ),
                dmc.Group(
                    direction="column",
                    children=[
                        create_nav_link(
                            icon=page["icon"], label=page["name"], href=page["path"]
                        )
                        for page in dash.page_registry.values()
                        if page["path"].startswith("/chapter1")
                    ],
                ),
            ],
        )
    ],
)


app.layout = dmc.Container(
    [
        dmc.Header(
            height=70,
            children=[dmc.Text("Company Logo")],
            style={"backgroundColor": "#228be6"},
        ),
        sidebar,
        dmc.Container(
            dash.page_container,
            size="lg",
            pt=20,
            style={"marginLeft": 300},
        ),
    ],
    fluid=True,
)

# app.clientside_callback("function(m){return m? m.data : '';}", Output("video", "src"), Input(f"ws", "message"))


@app.callback(
    Output("dummy_text", "children"),
    Input("run_button", "n_clicks")
)
def on_click_run(n):
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if trigger_id == "run_button":
        @server.websocket("/stream")
        async def stream():
            camera = VideoCamera(0)  # zero means webcam
            while True:
                frame = camera.get_frame()
                await websocket.send(f"data:image/jpeg;base64, {base64.b64encode(frame).decode()}")
        return "Run button clicked"
    else:
        raise dash.exceptions.PreventUpdate


if __name__ == "__main__":
    # app.run_server(debug=True)
    threading.Thread(target=app.run_server(debug=True)).start()
    server.run()
