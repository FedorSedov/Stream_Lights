


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = gui.Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()

'''size = str(ui.follower_duration.value())
ui.follower_duration_line.setText(size)

size = str(ui.sub_duration.value())
ui.sub_duration_line.setText(size)'''

'''with open('saved_effects.txt') as json_file:
    data = json.load(json_file)
    for b in data:
        ui.follower_effect.setCurrentText(data['follow_effect'][0])
        ui.follower_duration.setValue(int(data['follow_duration'][0]))
        ui.sub_effect.setCurrentText(data['sub_effect'][0])
        ui.sub_duration.setValue(int(data['sub_duration'][0]))
    dictionaries.saved_effects['follow_effect'].append(data['follow_effect'][0])
    dictionaries.saved_effects['follow_duration'].append(data['follow_duration'][0])
    dictionaries.saved_effects['sub_effect'].append(data['sub_effect'][0])
    dictionaries.saved_effects['sub_duration'].append(data['sub_duration'][0])'''

'''with open('Twitch.txt') as json_file:
    data = json.load(json_file)
    for b in data:
        dictionaries.twitch.append(b)
        ui.twitch_login.setText(b)
with open('Donation.txt') as json_file:
    data = json.load(json_file)
    for d in data:
        dictionaries.donation_link.append(d)
        ui.donation_link.setText(d)
with open('Lights.txt') as json_file:
    data = json.load(json_file)
    for b in data['bulb']:
        dictionaries.lights['bulb'].append(b)
        ui.ui_list.insertItem(0, b)
with open('Brackets.txt') as json_file1:
    data = json.load(json_file1)
    for p in data['bracket']:
        dictionaries.brackets['bracket'].append(p)
        bracket = classes.donation_bracket(p[0], p[1], p[2])
        dictionaries.brackets_classes.append(bracket)
        rowPosition = ui.ui_table.rowCount()
        ui.ui_table.insertRow(rowPosition)
        ui.ui_table.setItem(rowPosition, 0, QtWidgets.QTableWidgetItem(str(bracket.min)))
        ui.ui_table.setItem(rowPosition, 1, QtWidgets.QTableWidgetItem(str(bracket.max)))
        ui.ui_table.setItem(rowPosition, 2, QtWidgets.QTableWidgetItem(str(bracket.color)))'''

#initiazile button presses
'''ui.add_light_button.clicked.connect(add_light_to_list)
ui.pushButton_4.clicked.connect(ui.add_donation_bracket)
ui.save_twitch.clicked.connect(ui.save_twitch_f)
ui.donation_link_save.clicked.connect(ui.donation_link_save_f)
ui.pushButton_3.clicked.connect(ui.start)
ui.save_follower_settings.clicked.connect(ui.selected_follow_effect)
ui.save_sub_settings.clicked.connect(ui.selected_sub_effect)
ui.test_follower.clicked.connect(ui.test_follower_f)
ui.follower_duration.valueChanged.connect(ui.changed_value)
ui.sub_duration.valueChanged.connect(ui.sub_changed_value)
ui.follower_duration_line.textChanged.connect(ui.follower_text_changed)
ui.sub_duration_line.textChanged.connect(ui.sub_text_changed)'''

#initialize functions


sys.exit(app.exec_())

