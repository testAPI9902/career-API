import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from resume_parser import parse_resume
from career_model import CareerPathRecommender

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend_career_paths():
    # Check if a file was uploaded
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    uploaded_file = request.files['resume']
    
    # Ensure the file is a PDF
    if uploaded_file.filename == '' or not uploaded_file.filename.endswith('.pdf'):
        return jsonify({'error': 'Invalid file type. Please upload a PDF.'}), 400

    # Parse the resume
    resume_data = parse_resume(uploaded_file)

    # Initialize the recommender
    recommender = CareerPathRecommender()

    # Get recommendations
    career_paths = recommender.get_recommendations(resume_data)

    # Check if recommendations are available
    if isinstance(career_paths, str):
        return jsonify({'recommendations': career_paths}), 200
    else:
        return jsonify({'error': 'No recommendations available.'}), 404

if __name__ == "__main__":
    app.run(debug=False)
