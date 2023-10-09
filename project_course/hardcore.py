BLOCKS = []

BLOCKS.append({
    0: {
        "type":"TaskMainDisplayTask",
        "WCET":0.411,
        "time_period":250,
        "priority":10,
        "nested": [
            1
        ]
    },
    1: {
        "type":"DrivingControlResource",
        "WCET":0.22,
        "time_period":250,
        "priority":10,
        "nested": []
    }
})

BLOCKS.append({
    0: {
        "type":"TaskMainColorSensorTask",
        "WCET":0.068,
        "time_period":100,
        "priority":2,
        "nested": [1, 2]
    },
    1: {
        "type":"DrivingControlResource",
        "WCET":0.028,
        "time_period":100,
        "priority":2,
        "nested": []
    },
    2: {
        "type":"DrivingControlResource",
        "WCET":0.02,
        "time_period":100,
        "priority":2,
        "nested": []
    }
})

BLOCKS.append({
    0: {
        "type":"TaskMainSonarSensorTask",
        "WCET":0.114,
        "time_period":100,
        "priority":5,
        "nested": [1,2,3,4,5,6,7,8]
    },
    1: {
        "type":"DrivingControlResource",
        "WCET":0.019,
        "time_period":100,
        "priority":5,
        "nested": []
    },
    2: {
        "type":"DrivingControlResource",
        "WCET":0.018,
        "time_period":100,
        "priority":5,
        "nested": []
    },
    3: {
        "type":"DrivingControlResource",
        "WCET":0.01,
        "time_period":100,
        "priority":5,
        "nested": []
    },
    4: {
        "type":"DrivingControlResource",
        "WCET":0.018,
        "time_period":100,
        "priority":5,
        "nested": []
    },
    5: {
        "type":"DrivingControlResource",
        "WCET":0.012,
        "time_period":100,
        "priority":5,
        "nested": []
    },
    6: {
        "type":"DrivingControlResource",
        "WCET":0.019,
        "time_period":100,
        "priority":5,
        "nested": []
    },
    7: {
        "type":"DrivingControlResource",
        "WCET":0.022,
        "time_period":100,
        "priority":5,
        "nested": []
    },
    8: {
        "type":"DrivingControlResource",
        "WCET":0.019,
        "time_period":100,
        "priority":5,
        "nested": []
    }
})

BLOCKS.append({
    0: {
        "type":"TaskMainMotorControlTask",
        "WCET":0.074,
        "time_period":50,
        "priority":1,
        "nested": [1]
    },
    1: {
        "type":"DrivingControlResource",
        "WCET":0.071,
        "time_period":50,
        "priority":1,
        "nested": []
    }
})