import flet as ft
from langchain.chat_models import init_chat_model
import json
from langchain_core.messages import HumanMessage, SystemMessage

GROQ_API_KEY = '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'

model = init_chat_model('llama3-8b-8192', model_provider='groq', api_key=GROQ_API_KEY)

system = '''I am a movie recommendation system. Given a user-input movie plot, respond with a JSON object containing
a single key "movies" with a value of a list of movie objects. Each movie object should have two keys: "title" and "plot".
Ensure all responses are in JSON format. only JSON don't make any other output ever'''
class results(ft.Card):
    def __init__ (self,movie,plot):
        super().__init__()
        
        self.content=ft.Container(content=ft.Column([ft.Image(src='C:/Users/owner pc/Desktop/Simile/IMG-20241110-WA0015.jpg'),ft.ListTile(
        leading=ft.Icon(ft.icons.ALBUM),
        title=ft.Text(movie),
        subtitle=ft.Text(plot)),
        ft.Row([ft.TextButton("Buy tickets"), ft.TextButton("Listen")],alignment=ft.MainAxisAlignment.END)]),width=400,padding=10)
     
def main(page: ft.Page):
    def respond(e):
        messages = [
        SystemMessage(system),
        HumanMessage("i want a movie where its about two men bonding"),]
        a= model.invoke(messages)
        con = a.content
        print(con)
        try:
            data = json.loads(con)
            movies = data['movies']
            for movie in movies:
                page.add(results(movie['title'],movie['plot']))
                
                
        except json.JSONDecodeError as e:
            print("\nError parsing JSON:")
            page.controls.clear()
            page.add(ft.Text(e))
        except KeyError as e:
            print("\nError accessing JSON data:")
            page.controls.clear()
            page.add(ft.Text(e))
    page.scroll = 'adaptive'
    page.theme_mode = 'dark'
    
    page.add(ft.ElevatedButton(text='Generate a movie',on_click=respond))

ft.app(main)