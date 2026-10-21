import reflex as rx

config = rx.Config(
    app_name="front",
    plugins=[
        rx.plugins.RadixThemesPlugin(
            theme=rx.theme(accent_color="green", radius="large", appearance="inherit"),
        ),
        rx.plugins.SitemapPlugin(),
    ],
)
