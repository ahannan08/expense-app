# Expense Predictor Application

## Overview
The Expense Predictor Application is a full-stack project that allows users to enter their expense details, predict future expenses using a machine learning model, and store the data in a PostgreSQL database. The application is built using Python (Jupyter Notebook) for ML modeling, React.js for the frontend, and PostgreSQL for the database.
![image](https://github.com/user-attachments/assets/c7011ea4-3710-42bc-a698-8ab41c7e5ef1)


## Features
- **User Expense Input:** Users provide a detailed overview of their expenses.
- **Machine Learning Prediction:** A trained ML model predicts future expenses based on historical data.
- **Database Storage:** Expense data and predictions are stored in a PostgreSQL database.
- **Interactive UI:** Built using React.js for seamless user interaction.

## Tech Stack
- **Frontend:** React.js
- **Backend & ML Model:** Python (Jupyter Notebook)
- **Database:** PostgreSQL

## Setup & Installation
### Prerequisites
- Node.js & npm (for React frontend)
- Python & Jupyter Notebook (for ML model development)
- PostgreSQL (for database management)

### Backend (Python & Jupyter Notebook)
1. Clone the repository:
   ```sh
   git clone <repo-url>
   cd expense-predictor
   ```
2. Create a virtual environment and install dependencies:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run Jupyter Notebook to train and test the ML model:
   ```sh
   jupyter notebook
   ```

### Frontend (React.js)
1. Navigate to the frontend directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   npm install
   ```
3. Start the development server:
   ```sh
   npm start
   ```

### Database (PostgreSQL)
1. Create a PostgreSQL database and update database credentials in the backend configuration.
2. Run migrations (if applicable) to set up the necessary tables.

## Usage
1. Enter expense details in the UI.
2. Submit the details to process and predict future expenses.
3. View and analyze predictions.
4. Data is saved for future reference and insights.

## Future Enhancements
- Improve the ML model for higher accuracy.
- Add authentication for user-specific expense tracking.
- Implement data visualization for better insights.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss the proposed changes.

## License
This project is licensed under the MIT License.

