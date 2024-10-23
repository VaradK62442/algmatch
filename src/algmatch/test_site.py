from stableMatchings.hospitalResidentsProblem.hrResidentOptimal import HRResidentOptimal

example = {
    'residents': {
        1: [4,2,1],
        2: [3,1,4],
        3: [2,3,1],
        4: [3,4,1],
        5: [1,4,3],
        6: [2,3,1],
        7: [4,1,3],
        8: [3,4,2]
    },
    'hospitals': {
        1: {
            'capacity': 2,
            'preferences': [2,7,1,5,4,6,3]
        },
        2: {
            'capacity': 2,
            'preferences': [8,1,3,6]
        },
        3: {
            'capacity': 2,
            'preferences': [3,5,2,6,8,7,4]
        },
        4: {
            'capacity': 3,
            'preferences': [5,8,2,4,7,1]
        },
    }
}

hrro = HRResidentOptimal(dictionary=example)
hrro.run()
print(hrro.stable_matching)