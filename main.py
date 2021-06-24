from flask import Flask, render_template, request, flash, session
from flask_bootstrap import Bootstrap
import os, shutil
from werkzeug.utils import secure_filename
from forms import GenerateQrForm
import qrcode
from datetime import datetime


# QR code generator function -------------------------------------------------------------------------------------------
def generate_qr(data="https://www.youtube.com/channel/UCFOVnO-D9CeAm3GJqP5m6qg"):
    qr_generator = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=1)
    qr_generator.add_data(data)
    qr_generator.make(fit=True)
    image = qr_generator.make_image(fill_color="black", back_color="white")
    # generated image is a PIL object
    current_date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    image_path = f"static/img/qr_codes/qr_code_{current_date}.png"
    image.save(image_path)

    return image_path


# Deletes all previous QR Codes ----------------------------------------------------------------------------------------
def delete_qr_codes():
    directory = "static/img/qr_codes/"
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s. Reason: %s" % (file_path, e))


# Main code ------------------------------------------------------------------------------------------------------------
app = Flask(__name__)
Bootstrap(app)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


@app.route("/", methods=["POST", "GET"])
def home():
    qr_form = GenerateQrForm()

    if qr_form.validate_on_submit():
        # Remove all previous QR codes
        delete_qr_codes()
        # Remove all previous flash messages
        session.pop("_flashes", None)
        # Get data to encode -------------------------------------------------------------------------------------------
        data_to_encode = request.form["data_entry"]
        # generate QR code
        image_path = generate_qr(data_to_encode)
        # flash("QR code generated successfully.")
        return render_template("qr_generator.html", form=qr_form, data=data_to_encode, qr_code=image_path)

    return render_template("qr_generator.html", form=qr_form, data=None, qr_code=None)


# ----------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
