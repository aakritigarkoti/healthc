import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk, ImageFilter
import predict
import pandas as pd

class HealthCareChatBot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HealthCare ChatBot")
        self.geometry("600x500")
        background_image = Image.open("health.png")  # Update with your image path
        blurred_image = background_image.filter(ImageFilter.GaussianBlur(radius=3))  # Blur the background image
        self.background_image = ImageTk.PhotoImage(blurred_image)  # Convert blurred image to PhotoImage

        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # white borrderr
        self.border_frame = tk.Frame(self, bg="white", bd=3)
        self.border_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.8)
        # Chat ka area msg display ho rha h jisme
        self.chat_area = scrolledtext.ScrolledText(self.border_frame, wrap=tk.WORD, state='disabled', bg='light grey', bd=0, font=("Arial", 10))
        self.chat_area.place(relwidth=1, relheight=0.9)
        # Entry field for typing messages
        self.entry = tk.Entry(self, font=("Arial", 12))
        self.entry.place(relwidth=0.74, relheight=0.07, relx=0.05, rely=0.87)
        self.entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(self, text="Send", command=self.send_message_from_button)
        self.send_button.place(relwidth=0.15, relheight=0.07, relx=0.8, rely=0.87)


        self.display_message("Health Bot: Hello! I am your HealthCare ChatBot. What is your name?", "bot")

        self.stage = 0
        self.user_name = ""
        self.symptoms = []
        self.symptom_days = 0
        self.current_symptom = ""
        self.related_symptoms = []
        self.current_symptom_index = 0
        self.max_symptoms = 6  # Limit the number of symptoms to 3

    def display_message(self, message, sender):
        self.chat_area.configure(state='normal')
        if sender == "bot":
            self.chat_area.insert(tk.END, message + "\n", 'bot')
        else:
            self.chat_area.insert(tk.END, message + "\n", 'user')
        self.chat_area.configure(state='disabled')
        self.chat_area.yview(tk.END)
    def send_message(self, event):
        user_message = self.entry.get()
        self.entry.delete(0, tk.END)
        self.display_message(f"You: {user_message}", "user")
        self.process_message(user_message)

    def send_message_from_button(self):
        user_message = self.entry.get()
        self.entry.delete(0, tk.END)
        self.display_message(f"You: {user_message}", "user")
        self.process_message(user_message)

    def process_message(self, message):
        if self.stage == 0:
            self.user_name = message
            self.display_message(f"Health Bot: Hello, {self.user_name}. Enter the symptom you are experiencing.", "bot")
            self.stage += 1
        elif self.stage == 1:
            conf, cnf_dis = predict.check_pattern(predict.cols, message.strip())
            if conf == 1:
                self.display_message("Health Bot: Searches related to input:", "bot")
                for num, it in enumerate(cnf_dis):
                    self.display_message(f"{num}) {it}", "bot")
                self.display_message(f"Health Bot: Select the one you meant (0 - {num}):", "bot")
                self.stage += 1
                self.choices = cnf_dis
            else:
                self.display_message("Health Bot: Enter a valid symptom.", "bot")
        elif self.stage == 2:
            try:
                selected_index = int(message.strip())
                self.current_symptom = self.choices[selected_index]
                self.symptoms.append(self.current_symptom)
                self.display_message("Health Bot: Okay. From how many days?", "bot")
                self.stage += 1
            except (ValueError, IndexError):
                self.display_message("Health Bot: Enter a valid number.", "bot")
        elif self.stage == 3:
            try:
                self.symptom_days = int(message.strip())
                self.related_symptoms = self.get_related_symptoms(self.current_symptom)
                self.stage += 1
                self.ask_next_symptom()
            except ValueError:
                self.display_message("Health Bot: Enter a valid number.", "bot")
        elif self.stage == 4:
            response = message.strip().lower()
            if response == "yes":
                self.symptoms.append(self.related_symptoms[self.current_symptom_index])
            self.current_symptom_index += 1
            if self.current_symptom_index < min(len(self.related_symptoms), self.max_symptoms):
                self.ask_next_symptom()
            else:
                self.show_results()

    def ask_next_symptom(self):
        if self.current_symptom_index < len(self.related_symptoms):
            self.display_message(f"Health Bot: Are you experiencing {self.related_symptoms[self.current_symptom_index]}? (yes/no)", "bot")
        else:
            self.show_results()

    def get_related_symptoms(self, primary_symptom):
        df = pd.read_csv('D:\\Study material\\Python\\Healthcare\\Data\\Training.csv')
        related_symptoms = df[df[primary_symptom] == 1].drop(columns=['prognosis']).sum().sort_values(ascending=False)
        return [symptom for symptom in related_symptoms.index if symptom != primary_symptom]

    def show_results(self):
        prediction = predict.sec_predict(self.symptoms)
        disease = prediction[0]

        disease_name = predict.le.inverse_transform([disease])[0]  # Get the disease name from label encoder
        self.display_message(f"Bot: You may have {disease_name}", "bot")

        description = predict.get_disease_description(disease_name)
        self.display_message(f"Bot: {description}", "bot")

        precautions = predict.get_precautions(disease_name)
        self.display_message("Bot: Take the following measures:", "bot")
        for i, precaution in enumerate(precautions, 1):
            self.display_message(f"{i}) {precaution}", "bot")

        condition_message = predict.calc_condition(self.symptoms, self.symptom_days)
        self.display_message(f"Bot: {condition_message}", "bot")

if __name__ == "__main__":
    app = HealthCareChatBot()
    app.chat_area.tag_config('bot', background="lightgreen", justify='left')
    app.chat_area.tag_config('user', background="lightblue", justify='right')
    app.mainloop()
