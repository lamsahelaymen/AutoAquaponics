from main import user_settings

config_path, db_path, img_path = user_settings()
db_name = 'sensor_db.db'

all_we_got_now = ('time', 'pH', 'TDS', 'humidity', 'air_temp', 'water_temp', 'distance')
now_data_types = ("datetime", "float", "float", "float", "float", "float", "float")
end_GOAL = ["pH", "TDS (ppm)", "DO (ppm)", "Phosphate (ppm)", "Nitrate (ppm)", "Ammonia (ppm)", "Air Temperature (\N{DEGREE SIGN}C)",
                   "Air Humidity (%)", "Water Temperature (\N{DEGREE SIGN}C)", "Water Level (cm)", "Flow Rate (GPH)"]

def data_fxn():
    import numpy as np
    N = len(all_we_got_now)
    return tuple(np.random.randint(0,10,size=(N-1))) #N-tuple of random ints from 0 to 10.

def DataLogger():
    from data import Reader, Logger
    from getData import getData
    import numpy as np
    sensor_plot_table = {'SensorData':(all_we_got_now, now_data_types)}
    logger = Logger(db_path, db_name)
    logger.table(sensor_plot_table)
    temp_distance = 60 #to give an arbitrary initial value to getData for the first time the distance sensor fails
    while True:
        temp_distance = np.round(logger.collect_data("SensorData", data_fxn, temp_distance, tsamp=5, nsamp=5),2) #make sure tsamp > 5 seconds or distance sensor will freak
        logger.log_data()
        logger.commit()
        
#DataLogger()