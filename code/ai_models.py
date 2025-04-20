import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import joblib
from typing import Tuple, List

class AIModels:
    def __init__(self, data_path: str = "../data/raw_data.csv"):
        """Initialize AI models with data path."""
        self.data = pd.read_csv(data_path)
        self.decision_tree = None
        self.rl_agent = self.ReinforcementLearner()

    class ReinforcementLearner:
        """Reinforcement Learning agent for adaptive comfort profiling."""
        def __init__(self):
            self.preferred_temp = 24.0  # Initial preferred temperature
            self.learning_rate = 0.1    # Learning rate for updates
            self.history = []           # Track learning history

        def get_feedback(self, current_temp: float) -> str:
            """Generate simulated feedback based on temperature."""
            if current_temp > 25.0:
                return "too hot"
            elif current_temp < 22.0:
                return "too cold"
            return "just right"

        def update_preference(self, current_temp: float, feedback: str) -> float:
            """Update preferred temperature based on feedback."""
            if feedback == "too hot":
                self.preferred_temp -= self.learning_rate * (current_temp - self.preferred_temp)
            elif feedback == "too cold":
                self.preferred_temp += self.learning_rate * (current_temp - self.preferred_temp)
            self.history.append((current_temp, feedback, self.preferred_temp))
            return self.preferred_temp

    def train_decision_tree(self) -> None:
        """Train a decision tree to classify cooling levels."""
        X = self.data[['Temperature (°C)', 'Occupancy', 'Air Quality (ppm)']]
        y = pd.cut(self.data['Temperature (°C)'], bins=[0, 24, 30, 40], labels=['Low', 'Medium', 'High'])
        self.decision_tree = DecisionTreeClassifier(random_state=42)
        self.decision_tree.fit(X, y)
        joblib.dump(self.decision_tree, 'decision_tree_model.joblib')
        print("Decision tree model trained and saved.")

    def get_rl_recommendation(self, temp: float) -> Tuple[float, str]:
        """Get temperature recommendation from RL agent."""
        feedback = self.rl_agent.get_feedback(temp)
        new_pref = self.rl_agent.update_preference(temp, feedback)
        return new_pref, feedback

    def get_decision_tree_prediction(self, temp: float, occupancy: int, air_quality: int) -> str:
        """Get cooling level from decision tree."""
        if self.decision_tree is None:
            raise ValueError("Decision tree not trained. Call train_decision_tree first.")
        prediction = self.decision_tree.predict([[temp, occupancy, air_quality]])
        return prediction[0]

if __name__ == "__main__":
    # Example usage
    ai = AIModels()
    ai.train_decision_tree()
    print("Testing RL with sample temperatures:")
    for _ in range(5):
        temp = np.random.uniform(20, 30)
        pref, feedback = ai.get_rl_recommendation(temp)
        print(f"Temp: {temp:.1f}°C, Feedback: {feedback}, Preferred: {pref:.1f}°C")