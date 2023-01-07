from flask import Flask, render_template, url_for, request
import pandas as pd
import numpy as np
import pickle

# load the model from disk
app = Flask(__name__)


def model_name(model_code):
    if model_code == "linreg":
        return "linear regression"
    elif model_code == "ann":
        return "artificial neural network"
    elif model_code == "knn":
        return "k nearest neighbour"
    elif model_code == "desreg":
        return "decision tree regression"
    elif model_code == "lasreg":
        return "lasso regression"
    elif model_code == "randreg":
        return "random forest regression"
    elif model_code == "xgboost":
        return "XG Boost regression"
    else:
        return "unknown"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict', methods=['POST'])
def predict():
    year = request.form.get("year")
    model = request.form.get("model")

    df = pd.read_csv('year_wise_data/real_{}.csv'.format(year))
    pm = df.iloc[:, -1].values
    loaded_model = pickle.load(open('models/{}.pkl'.format(model), 'rb'))

    my_prediction = loaded_model.predict(df.iloc[:, :-1].values)
    my_prediction = my_prediction.tolist()

    diff = [pm[i] - my_prediction[i] for i in range(len(my_prediction))]
    count = 0
    for i in range(len(pm)):
        if abs(diff[i]) >= 30:
            count += 1
    return render_template('result.html', prediction=[round(i, 2) for i in my_prediction], model=model_name(model),
                           year=year, pm=pm, len=len(my_prediction), diff=diff, count=count)


if __name__ == '__main__':
    app.run(debug=True)
