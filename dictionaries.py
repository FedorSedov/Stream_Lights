from yeelight import flows

lights = {     # Использован словарь, так как потом будут не только bulb, но и другие типы устройств
    'bulb': []
}

brackets = {
    'bracket': []
}

brackets_classes = []

twitch = []

donation_link = []
donation_link_full = []

bulbs = []

previous_rgb = [0, 0, 255]

effects = {
    'RGB': [],
    'Disco': [flows.disco(120)],
    'Christmas': [flows.christmas()],
    'Alarm': [flows.alarm()],
    'Lsd': [flows.lsd()],
    'Police': [flows.police()],
    'Police2': [flows.police2()],
    'Strobe': [flows.strobe()],
    'Strobe_color': [flows.strobe_color()]
}

saved_effects = {
    'follow_effect': [],
    'sub_effect': [],
    'follow_duration': [],
    'sub_duration': []
}


def sort_brackets():
    brackets_classes.sort(key=lambda x: x.min)
    brackets['bracket'].sort(key=lambda y: y[0])
