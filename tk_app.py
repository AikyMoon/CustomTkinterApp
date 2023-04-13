import customtkinter 
import os
from PIL import Image
import requests


help_text = "Для получения класса вашей жалобы сделайте следующее:\n"\
            "1. Нажмите на вкладку 'Предсказание'\n"\
            "2. Введите текст жалобы в текстовое поле\n"\
            "3. Нажмите на кнопку 'Классифицировать'\n"\
            "4. Получите вашу категорию жалобы"

about_text = "Разработчик: Грязнев Захар\n"\
             "Если возникли вопросы, обращайтесь на почту: tuzat369@gmail.com"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Классификатор жалоб")
        self.geometry("700x450")

        # создание сетки
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # загрузка логотипа
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(26, 26))


        # создание фрейма навигации
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)


        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Классификатор", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)


        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Предсказание",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")


        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Помощь",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")


        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="О нас",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")


        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"], command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # начальный фрейм
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)
        
        self.start_label = customtkinter.CTkLabel(master=self.home_frame, text="  Введите вашу жалобу ниже", image=self.logo_image, compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.start_label.grid(row = 0, column = 0, padx=20, pady=10)

        self.entry_field = customtkinter.CTkTextbox(master=self.home_frame, corner_radius=10, width=250, height=150)
        self.entry_field.grid(row = 1, column = 0)

        self.predict_button = customtkinter.CTkButton(master=self.home_frame, text="Определить категорию", command=self.predict)
        self.predict_button.grid(row = 1, column = 1, padx = (0, 40))

        # создание фрейма документации
        self.help_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.help_text = customtkinter.CTkLabel(master=self.help_frame, width=200, text=help_text, wraplength=500, font=customtkinter.CTkFont(size=18, weight="bold"))
        self.help_text.grid(row = 0, column = 0, padx = 30, pady = 100, columnspan = 2)

        # создание фрейма about
        self.about_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.about_text = customtkinter.CTkLabel(master=self.about_frame, width=200, text=about_text, wraplength=500, font=customtkinter.CTkFont(size=18, weight="bold"))
        self.about_text.grid(row = 0, column = 0, padx = 30, pady = 100, columnspan = 2)

        # установка начального фрейма
        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        # установка цвета выбранной кнопки
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "help" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "about" else "transparent")

        # показать выбранный фрейм
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "help":
            self.help_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.help_frame.grid_forget()
        if name == "about":
            self.about_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.about_frame.grid_forget()


    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("help")

    def frame_3_button_event(self):
        self.select_frame_by_name("about")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    
    def predict(self):
        text = self.entry_field.get("1.0",'end-1c')
        pred = requests.post("http://127.0.0.1:5000/predict", json={"reason": text}).json()["prediction"]
        self.end_label = customtkinter.CTkLabel(master=self.home_frame, text=f"Ваша категория: {pred}", compound = "center",  font=customtkinter.CTkFont(size=14, weight="bold"), wraplength=300)
        self.end_label.grid(row = 2, column = 0, columnspan = 2, pady = 10)
        self.entry_field.delete("1.0",'end-1c')



if __name__ == "__main__":
    app = App()
    app.mainloop()

