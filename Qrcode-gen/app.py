from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__)

# Define a function to generate QR codes from a given link


def generate_qr_code(link):
    # Create a QRCode object with specific settings
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=0,
    )

    # Add the input link to the QRCode
    qr.add_data(link)
    qr.make(fit=True)

    # Generate the QR code image
    img = qr.make_image(fill_color="black", back_color="white")

    # Convert the QR code image to base64
    img_byte_array = io.BytesIO()
    img.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    base64_img = base64.b64encode(img_byte_array.read()).decode('utf-8')
    return f'data:image/png;base64,{base64_img}'


@app.route('/')
def index():
    return render_template('index.html', qr_code=None)


@app.route('/generate_qrcode', methods=['POST'])
def generate_qrcode_route():
    # Get the link from the form submitted by the user
    link = request.form['link']

    # Generate the QR code based on the user's input
    qr_code = generate_qr_code(link)

    return render_template('index.html', qr_code=qr_code)


if __name__ == '__main__':
    app.run(debug=True)
