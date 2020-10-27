#!/usr/bin/env python3


"""
High level representation of Points of Interest on CDR2020 Table (to be used in Behavior Trees).

- Points in (x, y, a) for x & y in meters, a in degrees.
- Zones in (x0, y0, x1, y1) for x & y in meters.
"""


RED_CUPS = {
    'GOB2': {"X": 0.3, "Y": 1.6},
    'GOB3': {"X": 0.45, "Y": 0.92},
    'GOB5': {"X": 0.67, "Y": 1.9},
    'GOB7': {"X": 1.005, "Y": 0.045},
    'GOB9': {"X": 1.1, "Y": 1.2},
    'GOB11': {"X": 1.335, "Y": 0.35},
    'GOB13': {"X": 1.605, "Y": 0.045},
    'GOB15': {"X": 1.73, "Y": 0.8},
    'GOB17': {"X": 1.935, "Y": 0.35},
    'GOB19': {"X": 2.05, "Y": 1.6},
    'GOB22': {"X": 2.55, "Y": 1.49},
    'GOB23': {"X": 2.7, "Y": 0.8},
    # Cups in ECUEIL_BLEU:
    'GOB25': {"X": -0.067, "Y": 0.55},
    'GOB27': {"X": -0.067, "Y": 0.4},
    'GOB29': {"X": -0.067, "Y": 0.25},
    # Cups in ECUEIL_JAUNE:
    'GOB31': {"X": 3.067, "Y": 0.475},
    'GOB33': {"X": 3.067, "Y": 0.325},
    # Cups in ECUEIL_1 & ECUEIL_2 following the Scenario 1:
    'GOB36': {"X": 0.775, "Y": 2.067},
    'GOB39': {"X": 1, "Y": 2.067},
    'GOB41': {"X": 2.075, "Y": 2.067},
    'GOB42': {"X": 2.15, "Y": 2.067},
    'GOB44': {"X": 2.3, "Y": 2.067},
}


GREEN_CUPS = {
    'GOB1': {"X": 0.3, "Y": 0.8},
    'GOB4': {"X": 0.45, "Y": 1.49},
    'GOB6': {"X": 0.95, "Y": 1.6},
    'GOB8': {"X": 1.065, "Y": 0.35},
    'GOB10': {"X": 1.27, "Y": 0.8},
    'GOB12': {"X": 1.395, "Y": 0.045},
    'GOB14': {"X": 1.665, "Y": 0.35},
    'GOB16': {"X": 1.9, "Y": 1.2},
    'GOB18': {"X": 1.995, "Y": 0.045},
    'GOB20': {"X": 2.33, "Y": 1.9},
    'GOB21': {"X": 2.55, "Y": 0.92},
    'GOB24': {"X": 2.7, "Y": 1.6},
    # Cups in ECUEIL_BLEU:
    'GOB26': {"X": -0.067, "Y": 0.475},
    'GOB28': {"X": -0.067, "Y": 0.325},
    # Cups in ECUEIL_JAUNE:
    'GOB30': {"X": 3.067, "Y": 0.55},
    'GOB32': {"X": 3.067, "Y": 0.4},
    'GOB34': {"X": 3.067, "Y": 0.25},
    # Cups in ECUEIL_1 & ECUEIL_2 following the Scenario 1:
    'GOB35': {"X": 0.7, "Y": 2.067},
    'GOB37': {"X": 0.85, "Y": 2.067},
    'GOB38': {"X": 0.925, "Y": 2.067},
    'GOB40': {"X": 2, "Y": 2.067},
    'GOB43': {"X": 2.225, "Y": 2.067},
}


ZONES = {
    # 'CHENAL_BLEU_ROUGE_1': (0, 0.9, 0.4, 0.93),
    # 'CHENAL_BLEU_VERT_1': (0, 1.47, 0.4, 1.5),
    # 'CHENAL_BLEU_ROUGE_2': (1.25, 0, 1.35, 0.3),
    # 'CHENAL_BLEU_VERT_2': (1.05, 0, 1.15, 0.3),
    # 'CHENAL_JAUNE_ROUGE_1': (2.6, 1.47, 3, 1.5),
    # 'CHENAL_JAUNE_VERT_1': (2.6, 0.9, 3, 0.93),
    # 'CHENAL_JAUNE_ROUGE_2': (1.85, 0, 1.95, 0.3),
    # 'CHENAL_JAUNE_VERT_2': (1.65, 0, 1.75, 0.3),
    'PORT_BLEU_1': (0, 0.93, 0.4, 1.47),
    'PORT_BLEU_2': (1.75, 0, 1.85, 0.3),
    'PORT_JAUNE_1': (2.6, 0.93, 3, 1.47),
    'PORT_JAUNE_2': (1.15, 0, 1.25, 0.3)
}


elements = {
    'ECUEIL_BLEU': {"X": 0, "Y": 0.4, "Rot": 180},
    'ECUEIL_JAUNE': {"X": 3, "Y": 0.4, "Rot": 0},
    'ECUEIL_1': {"X": 0.85, "Y": 2, "Rot": 90},
    'ECUEIL_2': {"X": 2.15, "Y": 2, "Rot": 90},
    'MANCHE1': {"X": 0.23, "Y": 0, "Rot": -90},
    'MANCHE2': {"X": 0.635, "Y": 0, "Rot": -90},
    'MANCHE3': {"X": 2.365, "Y": 0, "Rot": -90},
    'MANCHE4': {"X": 2.77, "Y": 0, "Rot": -90},
    'PHARE_BLEU': {"X": 0.225, "Y": 2, "Rot": 90},
    'PHARE_JAUNE': {"X": 2.775, "Y": 2, "Rot": 90},

    'CHENAL_BLEU_VERT_1': {"X": 0.2, "Y": 1.485, "Rot": 90},
    # 'CHENAL_BLEU_VERT_2': {"X": 1.7, "Y": 0.15, "Rot": 0},
    'CHENAL_BLEU_ROUGE_1': {"X": 0.2, "Y": 0.915, "Rot": 90},
    # 'CHENAL_BLEU_ROUGE_2': {"X": 1.9, "Y": 0.15, "Rot": 0},

    'CHENAL_JAUNE_VERT_1': {"X": 1.8, "Y": 0.915, "Rot": 90},
    # 'CHENAL_JAUNE_VERT_2': {"X": 1.2, "Y": 0.15, "Rot": 180},
    'CHENAL_JAUNE_ROUGE_1': {"X": 1.8, "Y": 1.485, "Rot": 90},
    # 'CHENAL_JAUNE_ROUGE_2': {"X": 1.3, "Y": 0.15, "Rot": 180},

    # 'ARUCO42': {"X": 1.5, "Y": 0.75},
    'GOB1': {"X": 0.3, "Y": 0.8},
    'GOB2': {"X": 0.3, "Y": 1.6},
    'GOB3': {"X": 0.45, "Y": 0.92},
    'GOB4': {"X": 0.45, "Y": 1.49},
    'GOB5': {"X": 0.67, "Y": 1.9},
    'GOB6': {"X": 0.95, "Y": 1.6},
    'GOB7': {"X": 1.005, "Y": 0.045, "Rot": 90},
    'GOB8': {"X": 1.065, "Y": 0.35, "Rot": 90},
    'GOB9': {"X": 1.1, "Y": 1.2},
    'GOB10': {"X": 1.27, "Y": 0.8},
    'GOB11': {"X": 1.335, "Y": 0.35, "Rot": 90},
    'GOB12': {"X": 1.395, "Y": 0.045, "Rot": 90},
    'GOB13': {"X": 1.605, "Y": 0.045, "Rot": 90},
    'GOB14': {"X": 1.665, "Y": 0.35, "Rot": 90},
    'GOB15': {"X": 1.73, "Y": 0.8},
    'GOB16': {"X": 1.9, "Y": 1.2},
    'GOB17': {"X": 1.935, "Y": 0.35, "Rot": 90},
    'GOB18': {"X": 1.995, "Y": 0.045, "Rot": 90},
    'GOB19': {"X": 2.05, "Y": 1.6},
    'GOB20': {"X": 2.33, "Y": 1.9},
    'GOB21': {"X": 2.55, "Y": 0.92},
    'GOB22': {"X": 2.55, "Y": 1.49},
    'GOB23': {"X": 2.7, "Y": 0.8},
    'GOB24': {"X": 2.7, "Y": 1.6},
    # 'GOB25': (-0.067, 0.55),
    # 'GOB26': (-0.067, 0.475),
    # 'GOB27': (-0.067, 0.4),
    # 'GOB28': (-0.067, 0.325),
    # 'GOB29': (-0.067, 0.25),
    # 'GOB30': (3.067, 0.55),
    # 'GOB31': (3.067, 0.475),
    # 'GOB32': (3.067, 0.4),
    # 'GOB33': (3.067, 0.325),
    # 'GOB34': (3.067, 0.25),
    # 'GOB35': (0.7, 2.067),
    # 'GOB36': (0.775, 2.067),
    # 'GOB37': (0.85, 2.067),
    # 'GOB38': (0.925, 2.067),
    # 'GOB39': (1, 2.067),
    # 'GOB40': (2, 2.067),
    # 'GOB41': (2.075, 2.067),
    # 'GOB42': (2.15, 2.067),
    # 'GOB43': (2.225, 2.067),
    # 'GOB44': (2.3, 2.067),
}
