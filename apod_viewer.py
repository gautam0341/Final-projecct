from tkinter import *
import apod_desktop
import calendar

# Initialize the image cache
apod_desktop.init_apod_cache(parent_dir="/script templates/apod_desktop.py")

# Define a function to update the displayed APOD image


def update_apod_image():
    selected_date = calendar.selection_get().date()
    apod_path = apod_desktop.get_apod_file_path(selected_date)
    if apod_path:
        apod_image = PhotoImage(file=apod_path)
        apod_label.config(image=apod_image)
        apod_label.image = apod_image
        apod_label.pack()
    else:
        apod_label.pack_forget()


# Create the GUI
root = Tk()
root.geometry('600x400')
root.title('APOD Viewer')

# Add a calendar widget for selecting the APOD date
Calendar = calendar.Calendar(root, selectmode='day', date_pattern='yyyy-mm-dd',
                             font=('Arial', 12), cursor='hand2', bordercolor='white')
Calendar.pack(padx=20, pady=20)
Calendar.selection_set(apod_desktop.get_latest_apod_date())

# Add a button to update the displayed APOD image
update_button = Button(root, text='Update', command=update_apod_image)
update_button.pack(pady=10)

# Add a label for displaying the APOD image
apod_label = Label(root)
apod_label.pack(pady=10)

# Update the displayed APOD image when the calendar date is changed
Calendar.bind('<<CalendarSelected>>', lambda event: update_apod_image())

root.mainloop()
