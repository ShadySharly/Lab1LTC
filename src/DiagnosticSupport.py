from pyswip import Prolog
from tkinter import*
from tkinter import messagebox

pl = Prolog()

################################################################################
# HECHOS
pl.assertz("problem(gpu,bad_video_output,stuttering,high_temperature)")
pl.assertz("problem(cpu,bad_video_output,high_temperature,blue_screen)")
pl.assertz("problem(hdmi,bad_video_output,stuttering,discolored_output)")
pl.assertz("problem(ram,blue_screen,slow_performance,halting)")
pl.assertz("problem(hdd,corrupt_data,slow_performance,halting)")
pl.assertz("problem(power_supply,booting_crash,high_temperature,burning_smell)")
pl.assertz("problem(cooling_fan,slow_performance,high_temperature,blue_screen)")
pl.assertz("problem(sata,booting_crash,corrupt_data,halting)")
pl.assertz("problem(motherboard,blue_screen,random_restarts,burning_smell)")
pl.assertz("problem(case_interface,no_audio,random_restarts,booting_crash)")
pl.assertz("problem(sound_card,no_audio,halting,booting_crash)")

# REGLAS
pl.assertz("""problem_query(X, U, V, W) :-
    problem(X, U, V, W) ; problem(X, U, W, V) ; problem(X, W, U, V) ;
    problem(X, W, V, U) ; problem(X, V, W, U) ; problem(X, V, U, W)""")

#################################################################################
# SUBRUTINAS
def filter_results(query):
    filtered = []
    for problem in query:
        if problem['X'] not in filtered:
            filtered.append(problem['X'])
    return filtered

def possible_results(u, v):
    possible = []
    for problem in pl.query("problem_query(X, "+u+", "+v+", _)"):
        if problem['X'] not in possible:
            possible.append(problem['X'])
    return possible

def clear_text():
    q1_entry.delete(0, END)
    q2_entry.delete(0, END)
    q3_entry.delete(0, END)
    text_field.delete("1.0","end")

def diagnose():
    if q1_text.get() == '' or q2_text.get() == '' or q3_text.get() == '':
        messagebox.showerror('Required Fields', 'Para omitir un campo escriba "_"')
        return

    elif q1_text.get() == '_' and q2_text.get() == '_' and q3_text.get() == '_':
        messagebox.showerror('Required Fields', 'Debe ingresar al menos un campo para determinar el diagnostico')
        return

    U = q1_text.get()
    V = q2_text.get()
    W = q3_text.get()

    diag = pl.query("problem_query(X, "+U+", "+V+", "+W+")")

    #Filtrado de resultados
    filtered_diag = filter_results(diag)
    outputMessage = ''

    #Resultados
    if len(filtered_diag) == 0:
        outputMessage += 'Unable to find exact problem.\n'
        print("Unable to find exact problem.\n")

        possible_diag = possible_results(U, V)
        if len(possible_diag) > 0:
            outputMessage += "Possible problems ("+U+", "+V+"):"
            print("Possible problems ("+U+", "+V+"):")
            for diag in possible_diag:
                outputMessage += "\t"+diag
                print("\t"+diag)

        possible_diag = possible_results(U, W)
        if len(possible_diag) > 0:
            outputMessage += "Possible problems ("+U+", "+W+"):"
            print("Possible problems ("+U+", "+W+"):")
            for diag in possible_diag:
                outputMessage += "\t"+diag
                print("\t"+diag)

        possible_diag = possible_results(V, W)
        if len(possible_diag) > 0:
            outputMessage += "Possible problems ("+V+", "+W+"):"
            print("Possible problems ("+V+", "+W+"):")
            for diag in possible_diag:
                outputMessage += "\t"+diag
                print("\t"+diag)

    elif len(filtered_diag) == 1:
        outputMessage += "Exact problem found: "+filtered_diag[0]
        print("Exact problem found: "+filtered_diag[0])
        
    else:
        outputMessage += "Not enough data provided.\n"
        print("Not enough data provided.\n")

        print("Possible problems:")
        for problem in filtered_diag:
            outputMessage += problem
            print(problem)

    text_field.insert(END, outputMessage)


####################################################
################# INTERFAZ #########################
####################################################
        
# Create window object
app = Tk()

# CONSULTA 1
q1_text = StringVar()
q1_label = Label(app, text = 'Consulta 1', font = ('bold', 14), pady = 20)
q1_label.grid(row = 0, column = 0)
q1_entry = Entry(app, textvariable = q1_text)
q1_entry.grid(row = 0, column = 1)

# CONSULTA 2
q2_text = StringVar()
q2_label = Label(app, text = 'Consulta 2', font = ('bold', 14))
q2_label.grid(row = 0, column = 2)
q2_entry = Entry(app, textvariable = q2_text)
q2_entry.grid(row = 0, column = 3)

# CONSULTA 3
q3_text = StringVar()
q3_label = Label(app, text = 'Consulta 3', font = ('bold', 14))
q3_label.grid(row = 1, column = 0)
q3_entry = Entry(app, textvariable = q3_text)
q3_entry.grid(row = 1, column = 1)

# TEXT FIELD
text_field = Text(app, height = 8, width = 60) 
text_field.grid(row=3, column=0, columnspan=3, rowspan=6, pady=20, padx=20)

# BUTTONS
clear_btn = Button(app, text='Limpiar', width=12, command = clear_text)
clear_btn.grid(row=1, column=3)

diagnose_btn = Button(app, text='Diagnosticar', width=12, command = diagnose)
diagnose_btn.grid(row=1, column=2)

exit_btn = Button(app, text='Salir', width=12, command = app.quit)
exit_btn.grid(row=8, column=3)

app.title ('Soporte de Diagnostico de Hardware')
app.geometry('700x350')



# Start program
app.mainloop()


