import os
import tempfile
from flask import Flask, request, jsonify
import easyocr
import cv2
from pyzbar.pyzbar import decode

app = Flask(__name__)

# Initialize EasyOCR reader
reader = easyocr.Reader(["en"], verbose=False)


@app.route("/process-image", methods=["POST"])
def process_image():
    print("Processing image...")
    # Check if the POST request has the file part
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    # Get the uploaded image file
    image_file = request.files["image"]

    # Create a temporary directory if it doesn't exist
    temp_dir = tempfile.mkdtemp()

    # Save the image to the temporary directory
    image_path = os.path.join(temp_dir, image_file.filename)
    image_file.save(image_path)

    # Perform OCR on the image
    text = extract_text(image_path)
    qr_text = decode_qr(image_path)

    # Delete the temporary image file
    os.remove(image_path)

    # Return the OCR results as JSON
    return jsonify({"extractedText": text, "qrText": qr_text})


def extract_text(image_path):
    # Perform text extraction using EasyOCR
    result = reader.readtext(image_path, detail=0)
    return result


def decode_qr(image_path):
    # Read the image
    image = cv2.imread(image_path)

    # Decode QR code
    decoded_objects = decode(image)

    # Extract QR code text if available
    qr_text = [obj.data.decode("utf-8") for obj in decoded_objects]

    return qr_text


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
