import PySimpleGUI as sg

def create_row(row_counter, row_number_view):
      row = [
            sg.pin(
            sg.Col([
            [
                sg.Button('X', border_width=0, 
                key=('-DEL-', row_counter)),
                sg.Input(size=(20,1), key=('-CATEGORY-', row_counter)),
                sg.Input(size=(4,1), key=('-%-', row_counter)),
                sg.Text(f'%  Category {row_number_view}', key=('-CATEGORY_NUM-', row_counter))
            ]
            ],
            key=('-ROW-', row_counter)
            
            )
            )
      ]
      return row


def calculate_amt(income, percentage):
     amt = (percentage)/100 * income
     return amt


username_layout = [
        [sg.Text('Enter Username')],
        [sg.Input(key='-USER-')],
        ]

page2_layout = [
    [sg.Text('Monthly Income')],
    [sg.Input(key='-INCOME-')],
    [sg.Text('+', enable_events=True, font='20', key='-ADD_ROW-')],
    [sg.Column([create_row(0, 1)], key='-ROW_PANEL-')],
]


deposit_layout = [
    [sg.Text('Deposit Location')],
    [sg.Combo([], size=(20), key='-DEPOSIT_LOCATION-')],
    [sg.Text('Deposit Amount')],
    [sg.Input(key='-DEPOSIT_AMOUNT-', size=(5)), sg.Text('$')],
]

info_layout = [
      [sg.Text('Amount Remaining: f(amt_left)', key='-TEXT_AMT_LEFT-')],
      [sg.Text('Deposit Amount: f(Category1)', key='-TEXT_DEPOSIT_AMOUNT-')],
      [sg.Text('Amount Spent on f(Category1): f(amt_spent)', key='-TEXT_AMT_SPENT-')],
      [sg.Button('Make Another Deposit', key='-DEPOSIT_BUTTON-')]
]

layout = [
    [sg.VPush(), 
    sg.Column(username_layout, key='-COL1-', visible=True),
    sg.Column(page2_layout, key='-COL2-', visible=False),
    sg.Column(deposit_layout, key='-COL3-', visible=False),
    sg.Column(info_layout, key='-COL4-', visible=False)],
    [sg.VPush()],
    [sg.Button('Next'), sg.Button('Restart')]
]



window = sg.Window('Money Tracker', layout, size=(500, 400))

layout = 1
row_counter = 0
row_number_view = 1
check = 0
user_dict ={}
category_dict = {}
while True:
      event, values = window.read()
      if event == sg.WIN_CLOSED:
                break
      
      if event == 'Next': # Next button on bottom of gui
            
            if layout == 1:
                 username = values['-USER-']
                 if username in user_dict:
                      category_dict = user_dict[username]
                      window['-DEPOSIT_LOCATION-'].update(values=list(category_dict.keys())[0:]) # updates combo element on layout 3


                      window[f'-COL{1}-'].update(visible=False)
                      window[f'-COL{3}-'].update(visible=True)
                      layout = 3
                      continue
            
            if layout == 2: # adds categories and their precnetages to a list, assigns monthly income to a variable
                    percentages = []
                    try:
                         income = int(values['-INCOME-'])
                    except:
                         sg.Popup('Income must be a number')
                         continue
                    i= -1
                    while i < row_number_view-1:
                        i += 1
                        try:
                            if check == 1:
                                sg.Popup('Percentages must be a number')
                                break
                            perc = int(values[('-%-', i)])
                            percentages.append(perc)
                            category_dict[values[('-CATEGORY-', i)]] = [0, calculate_amt(income, perc)]
                            
                        except:
                            check = 1
                            if i == row_number_view-1:
                                 i -= 1
                    
                    if check == 1:
                         check = 0
                         continue
                    
                    if sum(percentages) > 101:
                         sg.Popup('Percentages must not exceed 100%')
                         continue
                            

                    window['-DEPOSIT_LOCATION-'].update(values=list(category_dict.keys())[0:]) # updates combo element on layout 3

            if layout == 3:
                 deposit_location = values['-DEPOSIT_LOCATION-']
                 if deposit_location not in category_dict:
                      sg.Popup('Invalid Category')
                      continue
                 try:
                    deposit_amount = int(values['-DEPOSIT_AMOUNT-'])
                 except:
                      sg.Popup('Deposit must be a number')
                      continue
                 category_dict[deposit_location][0] += deposit_amount
                 
                 window['-TEXT_AMT_LEFT-'].update(f'Amount Available for {deposit_location}: ${int(category_dict[deposit_location][1] - category_dict[deposit_location][0])}')
                 window['-TEXT_DEPOSIT_AMOUNT-'].update(f'Deposit Amount: ${deposit_amount}')
                 window['-TEXT_AMT_SPENT-'].update(f'Amount Spent on {deposit_location}: ${category_dict[deposit_location][0]}')


            window[f'-COL{layout}-'].update(visible=False) # hides current layout
            
            if layout < 4: # makes next layout visible 
                  layout += 1
                  window[f'-COL{layout}-'].update(visible=True)
            else:
                  window[f'-COL{layout}-'].update(visible=True)
         
      elif event == 'Restart': # restart button on bottom of gui
            user_dict[username] = category_dict
            category_dict = {}
            username = ''
            window['-USER-'].update('')

            income = 0
            category_list = []
            percentages = []
            window['-INCOME-'].update('')
            for i in range(row_counter+1):
                window[('-CATEGORY-', i)].update('')
                window[('-%-', i)].update('')
                if i > 0:
                    window['-ROW-', i].update(visible=False)
            values = {}
            row_number_view = 1

            window['-DEPOSIT_AMOUNT-'].update('')

            window[f'-COL{layout}-'].update(visible=False)
            window['-COL1-'].update(visible=True)
            layout = 1

      if layout == 2:
            if row_number_view < 7:
                if event == '-ADD_ROW-': # row adding logic
                    
                    if ('-CATEGORY-', row_number_view) in values.keys(): # Checking if a row already exists before creating a new one (and unhides it if it does)
                        window[('-ROW-', row_number_view)].update(visible=True)
                        row_number_view += 1

                    else: # creates new row
                        row_counter += 1
                        row_number_view += 1
                        window.extend_layout(window['-ROW_PANEL-'], [create_row(row_counter, row_number_view)])
            
            if event[0] == '-DEL-' and event[1] == row_number_view - 1: # deletes the last row 
                row_number_view -= 1
                window[('-ROW-', event[1])].update(visible=False)

      if layout == 4:
           if event == '-DEPOSIT_BUTTON-':
                window['-DEPOSIT_AMOUNT-'].update('')
                window[f'-COL{4}-'].update(visible=False)
                window[f'-COL{3}-'].update(visible=True)
                layout = 3
                continue
# code should be complete?