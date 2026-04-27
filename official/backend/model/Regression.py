import backend.model.Clean as Clean
import backend.model.Degree as DegreeModule
from sklearn.linear_model import LinearRegression


class Regression:
    def __init__(self):
        clean = Clean.Clean()
        self.data = clean.degree_year_pivot()
        self.models = {}
        self._fit_all()

    def _fit_all(self):
        X = self.data.index.values.reshape(-1, 1)
        for col in self.data.columns:                
            y = self.data[col].values
            model = LinearRegression()
            model.fit(X, y)
            self.models[col] = model

    def predict(self, deg: DegreeModule.Degree, year: int) -> int: 
        if deg.value not in self.models:
            raise ValueError(f"Unknown degree: '{deg}'. Choose from: {list(DegreeModule.Degree)}")
        return round(self.models[deg.value].predict([[year]])[0])

    def predict_all(self, year: int) -> dict:
        return {deg.name: self.predict(deg, year) for deg in DegreeModule.Degree}

    def print_data(self):
        print(self.data.to_string())