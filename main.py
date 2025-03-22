import flet as ft

def main(page:ft.Page):
    page.scroll='adaptive'
    page.window.width=320
    page.window.height=570
    page.theme_mode = 'dark'
    def select(e):
        pass
    main = ft.SafeArea(content=
    ft.Column([
        ft.Row([ft.Text('Describe the Movie Plot Here',weight='Bold',size=20,width=180),ft.Container(padding=10,border_radius=10,bgcolor='black',content=ft.Text('Generate',color='white'))],alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.TextField(hint_text='Enter prompt here',multiline=True,border_color='purple'),
        ft.Text('Select the Genre',weight='Bold',size=15),
        ft.Row([ft.Chip(on_select=select,label=ft.Text('Series')),ft.Chip(label=ft.Text('Anime'),on_select=select),ft.Chip(on_select=select,label=ft.Text('Anime')),ft.Chip(label=ft.Text('Anime'),on_select=select),ft.Chip(label=ft.Text('Anime'),on_select=select)],wrap=True),
        ft.Text('Select the Year',weight='Bold',size=15),
        ft.Dropdown(value='Nollywood',options=[ft.dropdown.Option('Hollywood'),ft.dropdown.Option('Tollywood'),ft.dropdown.Option('Bollywood')])
    ]))
    page.add(main)
    
    
    
    
    
ft.app(main)