import flet as ft
import requests
import socket
from langchain.chat_models import init_chat_model
import json
from langchain_core.messages import HumanMessage, SystemMessage
api_key = "44e219fffa2a2b5852895fd8fe5bc463"
GROQ_API_KEY = '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'

model = init_chat_model('llama3-8b-8192', model_provider='groq', api_key=GROQ_API_KEY)

system = system = '''You are an AI that generates movie recommendations in **valid JSON format only**. 
Always return the response in the following strict JSON format:

{
  "movies": [
    {
      "title": "Movie Title",
      "plot": "A short description of the movie."
    },
    {
      "title": "Another Movie Title",
      "plot": "Another short description."
    }
  ]
}

IMPORTANT RULES:
1. Always return JSON in the exact format above. 
2. Never include extra text, explanations, or formatting.
3. The response should start with `{` and end with `}`.
4. If you cannot find a match, return an empty list like this:
   { "movies": [] }'''
# the class for the movie reults data
class results(ft.Card):
    def __init__ (self,movie,plot,image):
        super().__init__()
        self.content=ft.Container(content=ft.Column([ft.Image(src=image),ft.ListTile(
        title=ft.Text(movie,weight='Bold'),
        subtitle=ft.Text(plot)),]),padding=10)
# where the app starts
def main(page:ft.Page):
    prompt = ft.TextField(hint_text='Enter prompt here',multiline=True,bgcolor='black')
    prompt_container = ft.Container(content = prompt,bgcolor='black',
    gradient=ft.LinearGradient(begin=ft.alignment.center_left,end= ft.alignment.center_right,colors=[ft.Colors.PURPLE,ft.Colors.PINK]),padding=2,border_radius=5)
    result_column = ft.Column([],scroll='auto', expand=True)
    def clear(e):
        prompt.value = ''
        page.update()
    def is_connected():
        
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)  
            return True
        except OSError:
            return False
    def respond(e):
        
        if not is_connected():
            page.snack_bar = ft.SnackBar(ft.Text("No internet connection. Please connect and try again.",color='white'), bgcolor="black")
            page.snack_bar.open = True
            page.update()
            return  
        data = prompt.value
        messages = [
        SystemMessage(system),
        HumanMessage(data),]
        a= model.invoke(messages)
        default_image = 'C:/Users/owner pc/Desktop/Simile/IMG-20241110-WA0015.jpg'
        con = a.content
        page.go('/results')
        try:
            data = json.loads(con)
            movies = data['movies']
            for movie in movies:
                
                response = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie['title']}")
                data = response.json()
                if data["results"]:  
                    movie_id = data["results"][0]["id"]
                    
                    response = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}")
                    data = response.json()
                    poster_path = data["poster_path"]
                    image_url = f"https://image.tmdb.org/t/p/w400/{poster_path}" if poster_path else default_image

                    result_column.controls.append(results(movie['title'], movie['plot'], image_url))
                else:
                    result_column.controls.append(results(movie['title'], movie['plot'], default_image))
                
                

                print(con)
                page.update()
        except json.JSONDecodeError as e:
            result_column.controls.append(ft.Row([ft.Icon(ft.Icons.ERROR),ft.Text('Error pasrsing prompt, please rephrase and try again',color='red',width=200)]))
            print(con)
            page.update()
        except KeyError as e:
            result_column.controls.append(ft.Row([ft.Icon(ft.Icons.ERROR),ft.Text('Error accessing data, please rephrase and try again',color='red',width=200)]))
            print(con)
            page.update()
        except:
            result_column.controls.append(ft.Row([ft.Icon(ft.Icons.ERROR),ft.Text('No match Found, please rephrase and try again',color='red',width=200)]))
            print(con)
            page.update()
    def route_change(e):
        page.views.clear()
        page.views.append(
            ft.View(
                '/',[ft.SafeArea(content=ft.Column([
                    ft.Row([ft.Text('Find Films That Match Your Mood & Favourite Plots',weight='Bold',size=20,width=300,color='white',text_align=ft.TextAlign.CENTER),],alignment=ft.MainAxisAlignment.CENTER),
                            
                            ft.Row([ft.Text('Find movies that resonate with you. Our app has got the perfect recommendations for you. Try it out now and elevate your movie nights!',width=300,text_align=ft.TextAlign.CENTER)],alignment=ft.MainAxisAlignment.CENTER),
                            prompt_container,
                            ft.Row([ft.Container(on_click=respond,padding=10,width=100,border_radius=10,bgcolor='black',content=ft.Text('Generate',color='white',text_align=ft.TextAlign.CENTER),gradient=ft.LinearGradient(begin=ft.alignment.center_left,end= ft.alignment.center_right,colors=[ft.Colors.PURPLE,ft.Colors.PINK])),ft.TextButton('Clear',icon=ft.Icons.DELETE,on_click=clear)],alignment=ft.MainAxisAlignment.CENTER)
                            
                            ],spacing=20))
                            ],))
        if page.route == '/':
            result_column.controls.clear()
        if page.route == '/results':
            page.views.append(
                ft.View(
                    '/store',[ft.Row([ft.IconButton(icon=ft.Icons.ARROW_BACK,on_click= lambda e: page.go('/')),ft.Text('Movies',weight='bold',size=20)]),result_column],
                )
            )
        page.update()
    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    page.window.width=360
    page.window.height=600
    page.scroll = 'adpative'
    page.theme_mode = 'dark'
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)
    print(page.route)

ft.app(main)