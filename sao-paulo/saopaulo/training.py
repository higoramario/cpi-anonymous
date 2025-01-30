import bikescience.input_data as input
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from sklearn.externals import joblib

weather = input.load_per_hour_weather()
usage_variation = input.load_usage_variation()
socioeconomic = input.load_socioeconomic()
geographical = input.load_stations_hexagons()

samples = usage_variation.merge(weather, on='per_hour', how='inner').merge(geographical, left_on='id', right_on='station_id', how='inner').merge(socioeconomic, on='hex_id', how='inner')

X = samples[['temp_inst', 'temp_max', 'temp_min', 'umid_inst', 'umid_max', 'umid_min', 'pto_orvalho_inst', 'pto_orvalho_max', 'pto_orvalho_min', 'pressao', 'pressao_max', 'pressao_min', 'vento_direcao', 'vento_vel', ' vento_rajada', 'radiacao', 'precipitacao', 'job_qty', 'population', 'education_qty', 'health_qty', '0_2_salaries', '2_3_salaries', '3_5_salaries', '5_10_salaries', 'above_10_salaries']]
y = samples['free_bikes_increase']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

rf = RandomForestRegressor()
n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
bootstrap = [True, False]

random_grid = {'n_estimators': n_estimators, 'max_features': max_features, 'max_depth': max_depth, 'min_samples_split': min_samples_split, 'min_samples_leaf': min_samples_leaf, 'bootstrap': bootstrap}

rf_random = RandomizedSearchCV(estimator=rf, param_distributions=random_grid, n_iter=100, cv=3, verbose=2, random_state=42, n_jobs = -1)
rf_random.fit(X_train, y_train)
joblib.dump(rf_random.best_estimator_, 'model.pkl')
print(rf_random.best_params_)
