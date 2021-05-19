import requests
import bs4
from requests_html import HTMLSession
from tkinter import *
import webbrowser

session = HTMLSession()


def window_position():
    screen_width = int(root.winfo_screenwidth())
    screen_height = int(root.winfo_screenheight())

    screen_width = screen_width / 2
    screen_height = screen_height / 2

    window_width = 720
    window_height = 500

    window_width_ = int(window_width / 2)
    window_height_ = int(window_height / 2)

    position_x = int(screen_width - window_width_)
    position_y = int(screen_height - window_height_)

    return window_width, window_height, position_x, position_y


def s_and_t():
    url = 'https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19'
    webbrowser.open(url)


def prevention():
    url = 'https://www.who.int/emergencies/diseases/novel-coronavirus-2019/advice-for-public'
    webbrowser.open(url)


def news():
    url = 'https://www.google.com/search?source=lnms&tbm=nws&sa=X&ved=2ahUKEwikwN6Wna7wAhUPOSsKHSvPAZ8Q_AUoAXoECAEQAw&q=Coronavirus%20World&biw=1920&bih=1001'
    webbrowser.open(url)


def get_free_countries_list():
    url = 'https://www.hindustantimes.com/world-news/9-countries-including-new-zealand-are-now-covid-19-free-here-s-the-list/story-VANsJu5CZxRyXU2OyrDlmO.html'
    webbrowser.open(url)


def get_covid_data():
    url = 'https://www.worldometers.info/coronavirus/'
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    all_data = " "
    blocks = soup.find("div", class_="content-inner").find_all("div", id="maincounter-wrap")
    for block in blocks:
        text = block.find("h1", class_=None).get_text()
        count = block.find("span", class_=None).get_text()
        all_data = all_data + text + "\n" + count + "\n"
    return all_data


get_covid_data()


def get_country_wise_data():
    country_name = textfield.get()
    url = 'https://www.worldometers.info/coronavirus/country/'+country_name
    response = session.get(url)
    all_data = " "
    blocks = response.html.find('#maincounter-wrap')
    for block in blocks:
        try:
            text = block.find('h1', first=True).text
            count = block.find('span', first=True).text
            all_data = all_data + text + "\n" + count + "\n"
        except:
            ""
    main_label['text'] = "\n" + all_data


def get_vacine_data():
    url = 'https://covid19.who.int/'
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    all_data = ""
    text = soup.find_all("span", class_="sc-prOVx fSlcrp")
    num = str(text[1].text)
    num = num.split(" ")
    all_data = all_data + "As of " + text[0].text + ", a total of\n" + num[0] + " vaccination doses\nhave been administered." + "\n"
    return all_data


def reload_data():
    new_data = get_covid_data()
    main_label['text'] = "\n" + new_data



root = Tk()
position = list(window_position())
root.title("Covid-19 Tracker")
root.geometry("{}x{}+{}+{}".format(position[0], position[1], position[2], position[3]))
fonts_l = ("poppins", 20, "bold")
fonts_b = ("poppins", 12, "italic")
root.configure(background="#FAF9F6")

main_frame = Frame(root)
main_frame.pack(fill=BOTH, expand=1)

my_canvas = Canvas(main_frame)
my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

my_scrollbar = Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill=Y)

my_canvas.configure(yscrollcommand=my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

inner_frame = Frame(my_canvas)
my_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

frame = Frame(inner_frame, borderwidth=6, bg="#FAF9F6")
frame.pack()

s_and_t_button = Button(frame, text="Symptoms & Treatments", font=fonts_b, padx=20, pady=10, command=s_and_t)
s_and_t_button.pack(pady=10, side=LEFT)

prevention_button = Button(frame, text="Prevention", font=fonts_b, padx=20, pady=10, command=prevention)
prevention_button.pack(pady=10, side=LEFT)

news_button = Button(frame, text="Latest News", font=fonts_b, padx=20, pady=10, command=news)
news_button.pack(pady=10, side=LEFT)

free_button = Button(frame, text="Covid-free countries", font=fonts_b, padx=20, pady=10, command=get_free_countries_list)
free_button.pack(pady=10, side=LEFT)

main_image = PhotoImage(file="covid_proj.png")
main_image_label = Label(inner_frame, image=main_image)
main_image_label.pack()

textfield_description = Label(inner_frame, text="Search Country-Wise Data:", font=fonts_l, bg="black", fg="white")
textfield_description.pack(pady=10)

textfield = Entry(inner_frame, width=50)
textfield.pack()

country_button = Button(inner_frame, text="Get country data", font=fonts_b, padx=20, pady=10, command=get_country_wise_data)
country_button.pack(pady=10)

main_label = Label(inner_frame, text="\n" + get_covid_data(), font=fonts_l, bg="black", fg="white")
main_label.pack(pady=10)

vaccine_label = Label(inner_frame, text="\n" + get_vacine_data(), font=fonts_l, bg="black", fg="white")
vaccine_label.pack(pady=10)

reload_button = Button(inner_frame, text="Reload data", font=fonts_b, padx=20, pady=10, command=reload_data)
reload_button.pack(pady=10)

root.mainloop()