throughput_thread_no_i_o = {
    4: {"Min": 0, "Max": 70, "Avg": 8, "Stdev": 3},
    16: {"Min": 0, "Max": 70, "Avg": 8, "Stdev": 4},
    32: {"Min": 0, "Max": 60, "Avg": 8, "Stdev": 4},
    80: {"Min": 0, "Max": 60, "Avg": 8, "Stdev": 4},
    160: {"Min": 0, "Max": 70, "Avg": 8, "Stdev": 4},
}

throughput_thread_with_i_o = {
    4: {"Min": 0, "Max": 10, "Avg": 0, "Stdev": 0},
    16: {"Min": 2, "Max": 10, "Avg": 3, "Stdev": 1},
    32: {"Min": 1, "Max": 10, "Avg": 5, "Stdev": 2},
    80: {"Min": 0, "Max": 20, "Avg": 5, "Stdev": 2},
    160: {"Min": 0, "Max": 10, "Avg": 5, "Stdev": 2},
}

latency_thread_no_i_o = {
    4: {
        "1%": 34.992,
        "25%": 123.443,
        "50%": 136.866,
        "75%": 141.063,
        "90%": 145.098,
        "99%": 903.391,
        "99.9%": 1712.951,
        "99.99%": 1997.485,
        "99.999%": 1997.485,
    },
    16: {
        "1%": 26.295,
        "25%": 107.348,
        "50%": 155.024,
        "75%": 165.887,
        "90%": 172.861,
        "99%": 979.836,
        "99.9%": 1749.463,
        "99.99%": 1999.088,
        "99.999%": 1999.088,
    },
    32: {
        "1%": 25.972,
        "25%": 111.139,
        "50%": 154.223,
        "75%": 167.438,
        "90%": 173.023,
        "99%": 898.801,
        "99.9%": 1663.715,
        "99.99%": 1926.033,
        "99.999%": 1926.033,
    },
    80: {
        "1%": 24.714,
        "25%": 110.446,
        "50%": 155.185,
        "75%": 168.017,
        "90%": 174.221,
        "99%": 973.910,
        "99.9%": 1745.101,
        "99.99%": 1977.900,
        "99.999%": 1977.900,
    },
    160: {
        "1%": 24.623,
        "25%": 107.072,
        "50%": 155.684,
        "75%": 166.606,
        "90%": 172.662,
        "99%": 966.246,
        "99.9%": 1725.919,
        "99.99%": 1987.044,
        "99.999%": 1987.044,
    },
}

latency_thread_with_i_o = {
    4: {
        "1%": 116.237,
        "25%": 1039.642,
        "50%": 1041.266,
        "75%": 1043.158,
        "90%": 1046.783,
        "99%": 1049.543,
        "99.9%": 1085.045,
        "99.99%": 1085.045,
        "99.999%": 1085.045,
    },
    16: {
        "1%": 129.965,
        "25%": 259.864,
        "50%": 260.356,
        "75%": 260.949,
        "90%": 262.089,
        "99%": 267.233,
        "99.9%": 325.405,
        "99.99%": 334.413,
        "99.999%": 334.413,
    },
    32: {
        "1%": 100.721,
        "25%": 170.406,
        "50%": 184.046,
        "75%": 194.215,
        "90%": 204.920,
        "99%": 250.307,
        "99.9%": 453.850,
        "99.99%": 521.160,
        "99.999%": 521.160,
    },
    80: {
        "1%": 80.559,
        "25%": 166.398,
        "50%": 183.912,
        "75%": 202.596,
        "90%": 224.292,
        "99%": 1024.402,
        "99.9%": 1696.588,
        "99.99%": 1971.096,
        "99.999%": 1971.096,
    },
    160: {
        "1%": 92.758,
        "25%": 166.846,
        "50%": 185.149,
        "75%": 203.082,
        "90%": 222.262,
        "99%": 1129.550,
        "99.9%": 1855.882,
        "99.99%": 1964.070,
        "99.999%": 1964.070,
    },
}

throughput_worker_no_i_o = {
    4: {"Min": 49, "Max": 131, "Avg": 60, "Stdev": 4},
    16: {"Min": 210, "Max": 414, "Avg": 250, "Stdev": 14},
    32: {"Min": 111, "Max": 470, "Avg": 340, "Stdev": 128},
    80: {"Min": 89, "Max": 757, "Avg": 288, "Stdev": 228},
    160: {"Min": 58, "Max": 636, "Avg": 269, "Stdev": 183},
}
throughput_worker_with_i_o = {
    4: {"Min": 0, "Max": 10, "Avg": 0, "Stdev": 0},
    16: {"Min": 3, "Max": 10, "Avg": 3, "Stdev": 1},
    32: {"Min": 4, "Max": 10, "Avg": 8, "Stdev": 2},
    80: {"Min": 9, "Max": 20, "Avg": 19, "Stdev": 2},
    160: {"Min": 9, "Max": 20, "Avg": 18, "Stdev": 3},
}

latency_worker_no_i_o = {
    4: {
        "1%": 16.277,
        "25%": 16.419,
        "50%": 16.465,
        "75%": 16.512,
        "90%": 16.649,
        "99%": 17.323,
        "99.9%": 18.829,
        "99.99%": 19.135,
        "99.999%": 19.596,
    },
    16: {
        "1%": 3.647,
        "25%": 3.811,
        "50%": 3.880,
        "75%": 4.033,
        "90%": 4.118,
        "99%": 4.347,
        "99.9%": 4.626,
        "99.99%": 4.975,
        "99.999%": 5.160,
    },
    32: {
        "1%": 1.035,
        "25%": 2.062,
        "50%": 2.158,
        "75%": 2.258,
        "90%": 2.420,
        "99%": 4.634,
        "99.9%": 5.825,
        "99.99%": 7.348,
        "99.999%": 10.534,
    },
    80: {
        "1%": 0.949,
        "25%": 1.237,
        "50%": 1.371,
        "75%": 1.565,
        "90%": 2.541,
        "99%": 6.427,
        "99.9%": 11.114,
        "99.99%": 16.346,
        "99.999%": 22.005,
    },
    160: {
        "1%": 1.050,
        "25%": 1.227,
        "50%": 1.617,
        "75%": 2.166,
        "90%": 4.459,
        "99%": 10.044,
        "99.9%": 16.866,
        "99.99%": 23.845,
        "99.999%": 29.548,
    },
}

latency_worker_with_i_o = {
    4: {
        "1%": 103.584,
        "25%": 1036.919,
        "50%": 1037.501,
        "75%": 1038.182,
        "90%": 1038.552,
        "99%": 1039.036,
        "99.9%": 1039.222,
        "99.99%": 1039.222,
        "99.999%": 1039.222,
    },
    16: {
        "1%": 99.267,
        "25%": 259.642,
        "50%": 259.819,
        "75%": 259.967,
        "90%": 260.365,
        "99%": 264.613,
        "99.9%": 264.929,
        "99.99%": 264.972,
        "99.999%": 264.972,
    },
    32: {
        "1%": 98.013,
        "25%": 110.651,
        "50%": 128.871,
        "75%": 148.840,
        "90%": 150.321,
        "99%": 152.160,
        "99.9%": 153.629,
        "99.99%": 154.235,
        "99.999%": 154.235,
    },
    80: {
        "1%": 51.438,
        "25%": 51.738,
        "50%": 51.873,
        "75%": 52.035,
        "90%": 52.277,
        "99%": 52.686,
        "99.9%": 53.708,
        "99.99%": 54.048,
        "99.999%": 54.050,
    },
    160: {
        "1%": 51.405,
        "25%": 51.849,
        "50%": 52.147,
        "75%": 52.468,
        "90%": 52.778,
        "99%": 53.860,
        "99.9%": 55.092,
        "99.99%": 56.161,
        "99.999%": 56.223,
    },
}

# (worker, thread)
latency_worker_thread_compination = {
    (80, 1): latency_worker_with_i_o[80],
    (4, 20): {
        "1%": 51.946,
        "25%": 52.922,
        "50%": 54.477,
        "75%": 61.470,
        "90%": 64.340,
        "99%": 70.672,
        "99.9%": 82.004,
        "99.99%": 91.425,
        "99.999%": 92.073,
    },
    (3, 27): {
        "1%": 52.378,
        "25%": 60.045,
        "50%": 70.217,
        "75%": 78.932,
        "90%": 85.772,
        "99%": 100.836,
        "99.9%": 111.900,
        "99.99%": 125.839,
        "99.999%": 128.930,
    },
    (2, 40): {
        "1%": 54.781,
        "25%": 92.388,
        "50%": 101.569,
        "75%": 109.882,
        "90%": 119.829,
        "99%": 143.831,
        "99.9%": 173.346,
        "99.99%": 196.774,
        "99.999%": 196.774,
    },
    (8, 10): {
        "1%": 51.863,
        "25%": 52.133,
        "50%": 52.261,
        "75%": 52.539,
        "90%": 67.013,
        "99%": 84.976,
        "99.9%": 90.803,
        "99.99%": 93.582,
        "99.999%": 95.590,
    },
}
# (worker, thread)
throughput_worker_thread_compination = {
    (80, 1): throughput_worker_with_i_o[80],
    (4, 20): {"Min": 9, "Max": 20, "Avg": 17, "Stdev": 4},
    (3, 27): {"Min": 5, "Max": 20, "Avg": 14, "Stdev": 4},
    (2, 40): {"Min": 4, "Max": 20, "Avg": 10, "Stdev": 2},
    (8, 10): {"Min": 9, "Max": 20, "Avg": 18, "Stdev": 3},
}

combination_system_usage = {
    (8, 10): {
        "CPU": {
            "usage": [
                61.8,
                122.5,
                159.2,
                184.0,
                201.9,
                216.5,
                226.7,
                235.3,
                242.5,
                248.4,
            ],
            "time_stamp": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        },
        "MEMORY": {
            "usage": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "time_stamp": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        },
    },
    (80, 1): {
        "CPU": {
            "usage": [
                451.6,
                352.6,
                342.6,
                340.2,
                337.3,
                334.9,
                332.4,
                330.5,
                329.5,
                327.5,
            ],
            "time_stamp": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        },
        "MEMORY": {
            "usage": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            "time_stamp": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        },
    },
}