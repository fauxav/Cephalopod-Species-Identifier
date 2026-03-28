# app.py
from flask import Flask, render_template_string, request
from main_app import train_model, predict_species

app = Flask(__name__)

# Train model once once server starts
model = train_model()

HTML = """
<!doctype html>
<html>
  <head>
    <title>Cephalopod Species Identifier</title>
    <style>
      @font-face {
          font-family: 'Tatuagem';
          src: url('{{ url_for('static', filename='fonts/Vtks_Tatuagem2.ttf') }}') format('truetype');
          font-weight: normal;
          font-style: normal;
          }

      /* keyframes for wave animation */
      @keyframes wave {
        0% {
          transform: translateY(0) skewX(0);
        }
        50% {
          transform: translateY(-2px) skewX(1deg); /* Move up and tilt right */
        }
        100% {
          transform: translateY(0) skewX(0);
        }
      }

      body {
        background-color: #222a43; /* Dark gray blue */
        color: white;
        font-family: 'Tatuagem', sans-serif;
        text-align: center;
        padding: 40px;
        position: relative;
        overflow-x: hidden;
        
        /* Star background */
        background-image: url('{{ url_for('static', filename='images/stars.png') }}'); 
        background-repeat: repeat;
        background-attachment: fixed;
        background-size: 100px auto; 
        background-blend-mode: multiply;
      }

      /* Small cuttlefish */
      body::before {
        content: "";
        position: fixed;
        top: 20px; /* Back to top */
        left: 20px;
        width: 300px; /* Small fixed size */
        height: 300px; 
        background-image: url('/static/images/cuttle.png');
        background-repeat: no-repeat;
        background-size: contain;
        opacity: 0.25; 
        pointer-events: none;
        z-index: -1;
      }

      /* Large cuttlefish */
      body::after {
        content: "";
        position: fixed;
        bottom: 0;
        right: 0;
        width: 60%;
        height: 60%;
        background-image: url('/static/images/cuttle.png');
        background-repeat: no-repeat;
        background-size: contain;
        opacity: 0.13;
        pointer-events: none;
        z-index: -1;
      }

      /* Octopus */
      #octopus-corner {
        position: fixed;
        bottom: -130px;
        left: -50px;
        width: 600px; /* Size for the octopus */
        height: 600px;
        background-image: url('/static/images/octo.png');
        background-repeat: no-repeat;
        background-size: contain;
        opacity: 0.2; /* Subtle opacity */
        pointer-events: none;
        z-index: -1;
      }

      textarea {
        width: 60%;
        height: 180px;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px;
        border: 2px solid white;
        background: #222a43; /* Dark gray blue */
        color: white;
        resize: none;
        position: relative;
        z-index: 2;
      }

      button {
        margin-top: 20px;
        padding: 12px 25px;
        background-color: white;
        color: #001f3f;
        font-family: 'Tatuagem', sans-serif;
        border-radius: 10px;
        font-size: 20px;
        cursor: pointer;
        border: none;
        padding-left: 25px;
        
        /* Apply wave animation */
        animation: wave 1.5s infinite alternate ease-in-out; 
        z-index: 3; 
        /* smoothness */
        transition: transform 0.3s ease; 
      }

      button:hover {
        background-color: #cccccc;
        /* Disable animation on hover and reset transform/box-shadow */
        animation: none; 
        transform: scale(1) translateY(0) skewX(0); 
        box-shadow: none;
      }

      h1 {
        font-size: 48px;
        margin-bottom: 20px;
        position: relative;
        z-index: 2;
      }

      /* Container for the DNA prompt and icons */
      .prompt-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px; 
      }

      /* Styling for the prompt text itself */
      .prompt-container p {
        margin: 0 15px; /* Space between text and icons */
        font-size: 24px;
        position: static; 
        z-index: 2;
      }

      /* Icon on the left side of the text */
      .prompt-container::before,
      /* Icon on the right side of the text */
      .prompt-container::after {
        content: "";
        display: block;
        width: 25px; /* Size of the icon */
        height: 25px;
        background-image: url('{{ url_for('static', filename='images/button.png') }}');
        background-repeat: no-repeat;
        background-size: contain;
        opacity: 0.7; 
      }
    </style>
  </head>
  <body>
    <div id="octopus-corner"></div> <h1>Cephalopod Species Identifier</h1>
    
    <div class="prompt-container">
      <p>Paste your DNA barcode below:</p>
    </div>
    
    <form method="post">
      <textarea name="sequence">{{ seq or "" }}</textarea><br>
      <button type="submit">Identify Species</button>
    </form>

    {% if prediction %}
      <h2>Your species is {{ prediction }} :D !!</h2>
    {% endif %}
  </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    seq = ""
    if request.method == "POST":
        seq = request.form.get("sequence", "")
        if seq.strip():
            prediction = predict_species(model, seq)
    return render_template_string(HTML, prediction=prediction, seq=seq)

if __name__ == "__main__":
    app.run(debug=True)