#import all needed libraries
import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

#read medical data .csv file
def get_Medical_Data():
    return pd.read_csv('Medical_insurance.csv', encoding='latin')

#load medical data .csv file
MedicalData = get_Medical_Data()

def show_main_page():
    #destroy main page
    home_frame.destroy()
    #display main page
    create_main_page()

#creating destroy window for quit button
def quit_program():
    root.destroy()

def create_main_page():
    #create from from graphs
    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    #vertical scrollbar
    vertical_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
    vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #horizontal scrollbar
    horizontal_scrollbar = ttk.Scrollbar(frame, orient=tk.HORIZONTAL)
    horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    #create canvas for scrollbar
    canvas = tk.Canvas(frame, yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    #assign command to scrollbar to actually scroll
    vertical_scrollbar.config(command=canvas.yview)
    horizontal_scrollbar.config(command=canvas.xview)

    #frame for graphs
    inner_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=inner_frame, anchor=tk.NW)

    #update scroll
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    inner_frame.bind("<Configure>", on_configure)

    #function for creating histogram
    def create_histogram(ax, data, xlabel, ylabel):
        ax.hist(data)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

    #lists containing titles and ylabels for plot 
    titles = ['BMI', 'Sex', 'Children', 'Smoker', 'Region', 'Age', 'Charges']
    ylabels = ['Frequency', 'Frequency', 'Frequency', 'Frequency', 'Frequency', 'Frequency', 'Frequency']


    #for loop to iterate of the names of columns, titles, y label. zip combines them into tuple
    for i, (column, title, ylabel) in enumerate(zip(['bmi', 'sex', 'children', 'smoker', 'region', 'age', 'charges'], 
                                                    titles,
                                                    ylabels)):
        #sizing plot
        fig, ax = plt.subplots(figsize=(5, 4))
        #call variables from creating histogram function in the correct layout
        create_histogram(ax, MedicalData[column.lower()], title, ylabel)
        #draw the graph
        fig.canvas.draw()

        #canvas to plot the graph
        canvas_widget = FigureCanvasTkAgg(fig, master=inner_frame)
        canvas_widget.draw()
        canvas_widget.get_tk_widget().grid(row=i, column=0, pady=10)

    #description title
    description_title1 = tk.Label(inner_frame, text="DESCRIPTION", font=("Helvetica", 24, "bold"))
    description_title1.grid(row=len(titles), column=0)

    #explanation for graphs
    explanation = tk.Label(inner_frame, text="In the bar charts there does not seem to be skewed distributions where one column is higher than the rest. The children and smoker graphs maybe be skewed.")
    explanation.grid(row=len(titles)+1, column=0)

    #another line to explain charges graph
    charges_explanation = tk.Label(inner_frame, text="Other variables, such as charges, were too skewed.")
    charges_explanation.grid(row=len(titles)+2, column=0)

    #load randomforest.png
    random_forest_image = Image.open("RandomForest.png")
    random_forest_photo = ImageTk.PhotoImage(random_forest_image)

    #create label and grid it into the canvas
    random_forest_label = tk.Label(inner_frame, image=random_forest_photo)
    random_forest_label.image = random_forest_photo
    random_forest_label.grid(row=len(titles)+3, column=0, pady=10)

    #description title for random forest image
    description_title2 = tk.Label(inner_frame, text="DESCRIPTION", font=("Helvetica", 24, "bold"))
    description_title2.grid(row=len(titles)+4, column=0)

    #explanation of image
    random_forest_explanation = tk.Label(inner_frame, text="Random Forest Regressor predicts the BMI using medical insurance information. The bar charts show the prediction for 4 tests blue being the actual BMI and orange is the Predicted BMI. Based on the model the BMI for person 4 is 33. The model has average accuracy of 85.49.")
    random_forest_explanation.grid(row=len(titles)+5, column=0, columnspan=2, pady=10)

#tkinter window
root = tk.Tk()
root.title("Medical Data")

#title
title = tk.Label(root, text="MEDICAL DATA ANALYSIS AND PREDICTION OF BMI", font=("Helvetica", 16, "bold"))
title.pack()

#window size
root.geometry("1920x1080")

#home page in root window
home_frame = ttk.Frame(root)
home_frame.pack(fill=tk.BOTH, expand=True)

#button for main page with shwo main page command
main_page_button = ttk.Button(home_frame, text="Main Page", command=show_main_page)
main_page_button.pack(pady=10)

#quit program button same quit program command
quit_button = ttk.Button(home_frame, text="Quit", command=quit_program)
quit_button.pack(pady=10)

# event loop
root.mainloop()
