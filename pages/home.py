from dash import dcc, register_page
import dash_mantine_components as dmc

register_page(__name__, path="/", icon="fa-solid:home")

layout = dmc.Container(
    [
        dmc.Title("Welcome to the home page"),
        dcc.Markdown(
            """
            This is a demo of a multi-page app with nested folders in the `pages` folder.  

            For example:            
            ```
            - app.py 
            - pages
                - chapter1                  
                   |-- webcam.py
            """
        ),
    ]
)
