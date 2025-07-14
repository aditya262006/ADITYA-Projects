import io
import webbrowser
import requests
from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk, Image

class NewsApp:
    def __init__(self):
        self.api_key = '74e0191b9704cf8c733744174b78a23e'
        self.base_url = 'http://api.mediastack.com/v1/news'
        self.index = 0
        self.articles = []
        self.photo = None

        self.root = Tk()
        self.root.geometry('800x700')
        self.root.resizable(0, 0)
        self.root.title('News App')
        self.root.configure(background='black')

        self.create_widgets()
        self.fetch_news()
        self.root.mainloop()

    def create_widgets(self):
        header = Label(self.root, text="News App", bg="#1f1f1f", fg="white",
                       font=("Helvetica", 16, 'bold'))
        header.pack(fill=X)

        # Filters
        filter_frame = Frame(self.root, bg='black')
        filter_frame.pack(pady=5)

        self.country_var = StringVar(value='in')
        OptionMenu(filter_frame, self.country_var, 'in', 'us', command=self.change_filter).pack(side=LEFT, padx=5)

        self.category_var = StringVar(value='general')
        OptionMenu(filter_frame, self.category_var, 'general', 'business', 'sports', 'technology', 'entertainment',
                   command=self.change_filter).pack(side=LEFT, padx=5)

        self.content_frame = Frame(self.root, bg='black')
        self.content_frame.pack(expand=True, fill=BOTH)

        self.nav_frame = Frame(self.root, bg='black')
        self.nav_frame.pack(pady=10)

    def fetch_news(self):
        self.clear_content()
        country = self.country_var.get()
        category = self.category_var.get()

        url = (
            f"{self.base_url}?"
            f"access_key={self.api_key}"
            f"&countries={country}"
            f"&categories={category}"
            f"&languages=en"
            f"&sort=published_desc"
            f"&limit=20"
        )

        try:
            response = requests.get(url).json()
            self.articles = response.get('data', [])
            self.index = 0
            if self.articles:
                self.show_article(self.index)
            else:
                Label(self.content_frame, text="No articles found.", bg="black", fg="white").pack()
        except Exception as e:
            print("Error fetching news:", e)
            Label(self.content_frame, text="Failed to load news.", bg="black", fg="red").pack()

    def show_article(self, index):
        self.clear_content()
        article = self.articles[index]

        # Load image
        try:
            img_url = article.get('image') or 'https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg'
            raw_data = urlopen(img_url, timeout=5).read()
            im = Image.open(io.BytesIO(raw_data)).resize((400, 250))
            self.photo = ImageTk.PhotoImage(im)
            img_label = Label(self.content_frame, image=self.photo)
            img_label.pack()
        except:
            pass

        # Title
        Label(self.content_frame, text=article.get('title', 'No Title'), bg='black', fg='white',
              wraplength=380, font=("Helvetica", 14, 'bold')).pack(pady=(10, 5))

        # Source and Date
        source = article.get('source', 'Unknown')
        date = article.get('published_at', '')[:10]
        Label(self.content_frame, text=f"{source} | {date}", bg='black', fg='gray').pack()

        # Description
        Label(self.content_frame, text=article.get('description', 'No Description'), bg="black", fg="white",
              wraplength=380, justify="left", font=("Helvetica", 11)).pack(pady=10)

        # Navigation Buttons
        for widget in self.nav_frame.winfo_children():
            widget.destroy()

        if index > 0:
            Button(self.nav_frame, text='⬅ Prev', command=lambda: self.show_article(index - 1)).pack(side=LEFT, padx=5)
        Button(self.nav_frame, text='Read More', command=lambda: self.open_link(article.get('url'))).pack(side=LEFT, padx=5)
        if index < len(self.articles) - 1:
            Button(self.nav_frame, text='Next ➡', command=lambda: self.show_article(index + 1)).pack(side=LEFT, padx=5)

    def open_link(self, url):
        if url:
            webbrowser.open(url)

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def change_filter(self, _=None):
        self.fetch_news()

# Run the app
if __name__ == "__main__":
    NewsApp()
