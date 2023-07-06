def create_screen_rectangle(image=None):
    import tkinter as tk
    root = tk.Tk()
    root.attributes('-alpha', .8)  # make window translucent
    root.attributes('-fullscreen', True)  # make window full screen
    root.attributes('-topmost', True)  # keep window above all others
    root.attributes('-transparentcolor', 'yellow')
    root['bg']='yellow'

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    canvas = tk.Canvas(root, bg='yellow')
    canvas.pack(fill='both', expand=True)
    if image:
        import os
        from PIL import Image, ImageTk
        os.system("cls")
        print("image:", image)


        image_window = tk.Toplevel(root)
        image_window.title("New Window")
        image_window.geometry(f"{screen_width}x{screen_height}")
        image_window.attributes('-fullscreen', True)
        image_window.attributes('-alpha', 1.0)
        # image_window.lower()

        image_canvas = tk.Canvas(image_window, bg='black')
        image_canvas.pack(fill='both', expand=True)

        img = Image.open(image)
        photo = ImageTk.PhotoImage(img)
        image_canvas.create_image(0, 0, image=photo, anchor="nw")

    tip_label = tk.Label(root, text="click and drag to select crop area", font=("Cascadia Code", 10), bg="black", fg="white")
    tip_label.place(x=screen_width//2, y=16, anchor="n")
    
    global rectangle_origin
    rectangle_origin = None

    # overlays
    top_overlay = canvas.create_rectangle(0, 0, screen_width, screen_height, fill='black')
    bottom_overlay = canvas.create_rectangle(0, 0, 0, 0, fill='black')
    left_overlay = canvas.create_rectangle(0, 0, 0, 0, fill='black')
    right_overlay = canvas.create_rectangle(0, 0, 0, 0, fill='black')

    def crop_video(x, y, w, h):
        global results
        results = [x, y, w, h]

    def update_tip(message):
        tip_label.config(text=message)

    def on_button_press(event):
        global rectangle_origin
        rectangle_origin = (event.x, event.y)
        update_tip("release to confirm crop, right-click to cancel, escape to quit")

    def on_button_release(event):
        global rectangle_origin
        if rectangle_origin:
            x1, y1 = rectangle_origin
            x2, y2 = event.x, event.y
            crop_video(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))
            update_tip("click and drag to select crop area, escape to quit")
            rectangle_origin = None
            root.destroy()

    def on_right_click(event):
        global rectangle_origin
        rectangle_origin = None
        canvas.coords(top_overlay, 0, 0, screen_width, screen_height)
        update_tip("click and drag to select crop area, escape to quit")

    def on_move(event):
        global rectangle_origin
        if rectangle_origin:
            x1, y1 = rectangle_origin
            x2, y2 = event.x, event.y

            # update overlays
            canvas.coords(top_overlay, 0, 0, screen_width, min(y1, y2))
            canvas.coords(bottom_overlay, 0, max(y1, y2), screen_width, screen_height)
            canvas.coords(left_overlay, 0, min(y1, y2), min(x1, x2), max(y1, y2))
            canvas.coords(right_overlay, max(x1, x2), min(y1, y2), screen_width, max(y1, y2))

    def on_escape_key(event):
        root.destroy()

    root.bind('<Escape>', on_escape_key)
    root.bind('<ButtonPress-1>', on_button_press)
    root.bind('<ButtonRelease-1>', on_button_release)
    root.bind('<Button-3>', on_right_click)
    root.bind('<Motion>', on_move)

    root.mainloop()
    return results
