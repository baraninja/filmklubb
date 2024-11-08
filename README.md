# 🎬 Filmklubb App

Welcome to the **Filmklubb App**! This Streamlit-based web application allows film enthusiasts to share their movie preferences, analyze group dynamics, and receive curated movie recommendations tailored for the entire group. Whether you're organizing a movie night with friends or managing a film club, this app streamlines the process of gathering preferences and generating insightful analyses.

## 📝 Table of Contents

- [🎬 Filmklubb App](#-filmklubb-app)
  - [🛠️ Features](#️-features)
  - [📸 Screenshots](#-screenshots)
  - [🚀 Getting Started](#-getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Configuration](#configuration)
    - [Running the App](#running-the-app)
  - [🔧 Usage](#-usage)
    - [Submit Preferences](#submit-preferences)
    - [View Analysis](#view-analysis)
    - [Get Recommendations](#get-recommendations)
  - [🛠️ Technologies Used](#️-technologies-used)
  - [🤝 Contributing](#-contributing)
  - [📄 License](#-license)
  - [📫 Contact](#-contact)
  - [🙏 Acknowledgments](#-acknowledgments)

## 🛠️ Features

- **User Preference Submission:** Allows users to input their favorite movie genres, preferred time periods, language preferences, quality markers, and moods.
- **Group Preferences Analysis:** Aggregates and analyzes the collective preferences of all users to identify trends and patterns.
- **Dynamic Visualizations:** Presents data through interactive charts and metrics for an intuitive understanding of group dynamics.
- **Group Movie Recommendations:** Generates tailored movie recommendations based on the analyzed group preferences.
- **Responsive Design:** Ensures optimal viewing and interaction across various devices and screen sizes.
- **Secure Data Handling:** Utilizes environment variables to manage sensitive information like database URIs and API keys securely.

## 📸 Screenshots

*Include screenshots of your app here to give users a visual overview.*

![App Header](static/screenshots/header.png)
*App Header showcasing the title and description.*

![Submit Preferences](static/screenshots/submit_preferences.png)
*User interface for submitting movie preferences.*

![View Analysis](static/screenshots/view_analysis.png)
*Dashboard displaying group preferences analysis with charts and metrics.*

![Get Recommendations](static/screenshots/get_recommendations.png)
*Section for generating and viewing group movie recommendations.*

## 🚀 Getting Started

Follow these instructions to set up and run the Filmklubb App on your local machine.

### Prerequisites

- **Python 3.7+**: Ensure you have Python installed. You can download it from [here](https://www.python.org/downloads/).
- **MongoDB Database**: The app uses MongoDB to store user preferences. You can set up a free cluster using [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
- **Anthropic API Key**: Required for generating movie recommendations. Obtain an API key from [Anthropic](https://www.anthropic.com/).

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/filmklubb-app.git
   cd filmklubb-app
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python -m venv myenv
   ```

3. **Activate the Virtual Environment**

   - **Windows:**

     ```bash
     myenv\Scripts\activate
     ```

   - **macOS/Linux:**

     ```bash
     source myenv/bin/activate
     ```

4. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   *If you don't have a `requirements.txt`, create one with the necessary packages:*

   ```bash
   pip install streamlit pymongo python-dotenv plotly
   ```

### Configuration

1. **Set Up Environment Variables**

   Create a `.env` file in the root directory of the project to store sensitive information.

   ```bash
   touch .env
   ```

   Add the following variables to the `.env` file:

   ```env
   MONGODB_URI=your_mongodb_connection_string
   ANTHROPIC_API_KEY=your_anthropic_api_key
   ```

   - **`MONGODB_URI`**: Your MongoDB connection string. Replace `your_mongodb_connection_string` with your actual URI.
   - **`ANTHROPIC_API_KEY`**: Your Anthropic API key. Replace `your_anthropic_api_key` with your actual API key.

2. **Directory Structure**

   Ensure your project directory has the following structure:

   ```
   filmklubb-app/
   ├── app.py
   ├── recommendation_engine.py
   ├── analysis.py
   ├── requirements.txt
   ├── .env
   ├── static/
   │   ├── logo.png
   │   └── screenshots/
   │       ├── header.png
   │       ├── submit_preferences.png
   │       ├── view_analysis.png
   │       └── get_recommendations.png
   └── .streamlit/
       └── style.css
   ```

   - **`app.py`**: Main Streamlit application file.
   - **`recommendation_engine.py`**: Handles the logic for generating movie recommendations.
   - **`analysis.py`**: Contains functions for analyzing user preferences and generating visualizations.
   - **`static/`**: Contains static assets like logos and screenshots.
   - **`.streamlit/style.css`**: Custom CSS for styling the app.

### Running the App

Start the Streamlit app using the following command:

```bash
streamlit run app.py
```

This will launch the app locally, typically accessible at `http://localhost:8501` in your web browser.

## 🔧 Usage

### Submit Preferences

1. **Navigate to "Submit Preferences"**

   - Enter your name and select your favorite genres, preferred time periods, language preferences, quality markers, and moods.
   - Click on the **"Submit Preferences"** button to save your inputs.

2. **Validation**

   - Ensure all fields are filled out. The app will prompt you if any required fields are missing.

### View Analysis

1. **Navigate to "View Analysis"**

   - Access comprehensive analyses of the group's movie preferences.
   - **Overview Metrics:** Displays active users, average genres per user, average moods per user, and total preferences.
   - **Distributions:** Visual charts showing genre and mood distributions.
   - **Trends:** Insights into submission trends over time.
   - **Correlations:** Heatmaps illustrating correlations between genres and moods.
   - **Language Preferences:** Charts depicting preferred movie languages.

2. **Interactive Visualizations**

   - Hover over charts for more detailed information.
   - Use tabs to navigate between different analytical sections.

### Get Recommendations

1. **Navigate to "Get Recommendations"**

   - Initiate the group movie recommendation process.
   - Observe the simulated progress bar indicating the recommendation generation stages.

2. **View Recommendations**

   - Once processed, view a curated list of movie recommendations tailored to the group's collective preferences.

## 🛠️ Technologies Used

- **[Streamlit](https://streamlit.io/):** Framework for building interactive web applications.
- **[MongoDB](https://www.mongodb.com/):** NoSQL database for storing user preferences.
- **[PyMongo](https://pymongo.readthedocs.io/):** Python driver for MongoDB.
- **[Python-dotenv](https://saurabh-kumar.com/python-dotenv/):** Loads environment variables from a `.env` file.
- **[Plotly](https://plotly.com/python/):** Library for creating interactive visualizations.
- **[Anthropic API](https://www.anthropic.com/):** API used for generating movie recommendations.

## 🤝 Contributing

Contributions are welcome! If you'd like to enhance the Filmklubb App, follow these steps:

1. **Fork the Repository**

2. **Create a New Branch**

   ```bash
   git checkout -b feature/YourFeatureName
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add some feature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeatureName
   ```

5. **Open a Pull Request**

   Describe your changes and submit the pull request for review.

## 📄 License

This project is licensed under the [MIT License](LICENSE).

## 📫 Contact

**Anders Barane**

- **Email:** anders.barane@gmail.com

Feel free to reach out for any queries or collaborations!

## 🙏 Acknowledgments

- **Streamlit Community:** For providing an excellent platform for building data-driven web apps.
- **MongoDB:** For offering a robust NoSQL database solution.
- **Anthropic:** For their powerful AI APIs that enhance recommendation capabilities.
- **OpenAI:** Inspiration and guidance from their extensive documentation and community support.

---
*Happy Movie Watching! 🎥🍿*
