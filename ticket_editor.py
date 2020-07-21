import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import colorchooser
from copy import deepcopy


class TicketEditor(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title('Receipt Editor')
        self.resizable(False,False)
        self.fields = dict()
        self.line = 0

        self.text_frame = ttk.LabelFrame(self,text="Layout Preview:")
        self.text_frame.grid(row=0,column=0,ipadx=2,ipady=2,padx=2,pady=2,sticky='N,S')

        self.text = tk.Text(self.text_frame, width=50)
        self.text.grid(row=0,column=0,ipadx=2,ipady=2,padx=2,pady=2,sticky='N,E,S,W')

        self.options_frame = ttk.LabelFrame(self, text="Layout Options:")
        self.options_frame.grid(row=0,column=1,ipadx=2,ipady=2,padx=2,pady=2,sticky='N,E,S,W')

        self.field_name = tk.StringVar()
        self.f_entry_label = ttk.LabelFrame(self.options_frame, text="Tag Key:")
        self.f_entry_label.grid(row=0,column=0,sticky="E,W")

        self.option_f_entry = ttk.Entry(self.f_entry_label, textvar= self.field_name)
        self.option_f_entry.grid(row=0,column=0, pady=2, sticky='N,S,E,W')

        self.fonts = tk.StringVar()
        self.font_label = ttk.LabelFrame(self.options_frame, text="Available Fonts:")
        self.font_label.grid(row=2,column=0,columnspan=2, sticky = "E,W")

        self.font_default = 'Times New Roman'
        self.font_list = tk.Listbox(self.font_label, listvariable=self.fonts)
        self.font_list.grid(row=2,column=0,columnspan=2, sticky="E,W")
        self.font_list.bind('<ButtonRelease-1>', self.setText)
        self._fonts_add()

        self.color_label = ttk.LabelFrame(self.options_frame, text='Color Chooser:')
        self.color_label.grid(row=3,column=0,sticky="E,W")

        self.color_value = ((0.0, 0.0, 0.0), '#000000')
        self.color_option = ttk.Button(self.color_label, text="Color...", command=self.colorOpen)
        self.color_option.grid(row=0,column=0,sticky="N,E,S,W")

        self.color_preview = tk.Canvas(self.color_label,height=10,width=20, bg=self.color_value[1])
        self.color_preview.grid(row=0,column=1,sticky="N,E,S,W")

        self.font_options = ttk.LabelFrame(self.options_frame, text='Font Options')
        self.font_options.grid(row=4,column=0,sticky="N,S,E,W")
        ##font dressings##
        self.bold_val = tk.IntVar()
        self.f_bold = tk.Checkbutton(self.font_options, text='Bold', variable=self.bold_val)
        self.f_bold.grid(row=0,column=0,sticky="W")

        self.ital_val = tk.IntVar()
        self.f_ital = tk.Checkbutton(self.font_options, text='Italics', variable=self.ital_val)
        self.f_ital.grid(row=0,column=1,sticky="E")

        self.under_val = tk.IntVar()
        self.f_undln = tk.Checkbutton(self.font_options, text='Underline', variable=self.under_val)
        self.f_undln.grid(row=1,column=0,sticky="E,W")
        ##end font dressings##
        ##font_size##
        self.size_val = tk.IntVar()
        self.size_val.set(12)

        self.f_size = ttk.Entry(self.font_options,width=5 ,textvariable=str(self.size_val), justify=tk.RIGHT)
        self.f_size.grid(row=2,column=0,sticky="E,W")

        self.f_adjust = ttk.Frame(self.font_options)
        self.f_adjust.grid(row=2,column=1,sticky="N,S,E,W")

        self.f_increase = tk.Button(self.f_adjust,text='+',command=self.size_val_up)
        self.f_increase.grid(row=0,column=0)

        self.f_decrease = tk.Button(self.f_adjust,text='- ',command=self.size_val_dwn)
        self.f_decrease.grid(row=0,column=1)
        ##end font_size##
        self.just_options = ttk.Frame(self.options_frame)
        self.just_options.grid(row=5,column=0,sticky="E,W")
        ##justifications##
        self.just_setting = tk.IntVar()
        self.just_left = tk.Checkbutton(self.just_options, text='L', variable=self.just_setting, onvalue=0)
        self.just_left.grid(row=0,column=0,sticky="W")

        self.just_cent = tk.Checkbutton(self.just_options, text='C', variable=self.just_setting, onvalue=1)
        self.just_cent.grid(row=0,column=1, sticky="E,W")

        self.just_right = tk.Checkbutton(self.just_options, text='R', variable=self.just_setting, onvalue=2)
        self.just_right.grid(row=0,column=2, sticky="E")

        self.option_f_confirm = ttk.Button(self.options_frame,  text="Add Text Tag", command=self.tagAttrSet)
        self.option_f_confirm.grid(row=6,column=0, sticky= "S,W,E")

    def size_val_up(self):
        val = self.size_val.get()
        if val == 26:
            return
        else:
            val += 1
            self.size_val.set(val)


    def size_val_dwn(self):
        val = self.size_val.get()
        if val == 0:
            return
        else:
            val -=1
            self.size_val.set(val)

    def colorOpen(self):
        _c = colorchooser.askcolor("Blue", title="Select a Color")
        self.color_preview['bg'] = _c[1]
        self.color_value = _c

    def tagAttrSet(self):
        text_dict = dict()
        text_key = self.option_f_entry.get()
        text_key = text_key.replace(' ','')

        text = self.font_default
        weight = self.bold_val.get()
        if weight:
            _w = "bold"
        else:
            _w = "normal"

        ital = self.ital_val.get()
        if ital:
            _i = "italic"
        else:
            _i = "roman"

        fontEx = dict(
            family=text,
            size=self.size_val.get(),
            weight=_w,
            slant=_i,
            underline=bool(self.under_val.get()))

        j_int = self.just_setting.get()
        if j_int == 0:
            _fj = 'left'
        elif j_int == 1:
            _fj = 'center'
        elif j_int == 2:
            _fj = 'right'
        else:
            print("There's an error with the justification values!")

        text_dict['font'] = deepcopy(fontEx)
        text_dict['justify'] = _fj
        text_dict['color'] = self.color_value[1]

        self.fields[text_key] = deepcopy(text_dict)
        _fontExample = font.Font(**fontEx)
        self.text.tag_configure(text_key, font=_fontExample, justify=_fj)
        self.text.insert('end',text_key + '\n', (text_key) )

        self.option_f_entry.delete('0','end')

        print(self.fields)
    def setText(self,event):
        font_indx = self.font_list.curselection()
        text_sel = self.font_list.get(font_indx)
        self.font_default = text_sel

    def _fonts_add(self):
        _ = list(font.families())
        avail = ' '.join(_)
        self.fonts.set(_)

if __name__ == '__main__':
    main = TicketEditor()

    main.mainloop()
