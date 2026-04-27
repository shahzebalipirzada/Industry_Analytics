from flask import Flask, jsonify, send_from_directory
import backend.model.Regression as RegressionModule
import backend.model.Degree as DegreeModule
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

regression = RegressionModule.Regression()

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/pivot', methods=['GET'])
def get_pivot():
    df = regression.data
    return jsonify({
        'years':   df.index.tolist(),
        'degrees': df.columns.tolist(),
        'data':    {str(year): row for year, row in df.to_dict(orient='index').items()}
    })


@app.route('/predict/<string:degree>/<int:year>', methods=['GET'])
def predict(degree, year):
    try:
        deg = DegreeModule.Degree(degree)
        result = regression.predict(deg, year)
        return jsonify({'degree': degree, 'year': year, 'predicted_students': result})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
    
@app.route('/degree/<string:degree>', methods=['GET'])
def get_degree(degree):
    try:
        deg    = DegreeModule.Degree(degree)
        series = regression.data[deg.value]

        first       = series.iloc[0]
        last        = series.iloc[-1]
        years_span  = len(series) - 1
        growth_rate = round(((last - first) / first * 100), 2) if first != 0 else None

        return jsonify({
            'degree': deg.value,
            'data': {
                int(year): int(count)
                for year, count in series.items()
            },
            'stats': {
                'mean':        round(series.mean(), 2),
                'peak':        {
                    'year':  int(series.idxmax()),
                    'count': int(series.max())
                },
                'total':       int(series.sum()),
                'growth_rate': growth_rate,       # % change first to last year
            }
        })

    except KeyError:
        return jsonify({'error': f"Degree '{degree}' not found in data"}), 404
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)