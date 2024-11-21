import os

import pandas as pd

from flask import Flask, request, jsonify, render_template
from amazon_onboarding import driver_amazon_onboarding
from ops_email_onboarding import add_username_on_ops_email
from amazon_onboarding_last_step import amazon_onboarding_password_set
from shell_onboarding import driver_shell_onboarding
from fleetio_onboarding import driver_fleetio_onboarding

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"


# Function to read Excel file
def read_file_excel(file_path, sheet):
    main_list = []
    df = pd.read_excel(file_path, sheet_name=sheet, engine="openpyxl")
    for index, row in df.iterrows():
        main_list.append(dict(zip(df.columns, row)))
    return main_list, df.columns


# Home route to serve the index.html
@app.route("/")
def home():
    return render_template("index.html")


# Upload endpoint
@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        # Save the file temporarily
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        file.save(file_path)

        # Read the file contents
        main_list, columns = read_file_excel(file_path, 0)

        # Remove the file after reading
        os.remove(file_path)

        # Return the contents as a response

        for row in [main_list[0]]:

            first_name, last_name, location = (
                row.get("First Name"),
                row.get("Last Name"),
                row.get("Location"),
            )
            email = (
                f"{first_name.lower()[:4]}{last_name.lower()[:3]}24@flitetransport.com"
            )
            username = f"{first_name.lower()[:4]}{last_name.lower()[:3]}24"
            password = f"{first_name[:4]}{last_name.lower()[:3]}2024"
            phone_number = row.get("Telephone")
            driver_license = row.get("Driver License")
            dob = (
                pd.to_datetime(row.get("DOB")).strftime("%m/%d/%Y")
                if pd.notnull(row.get("DOB"))
                else None
            )
            license_expiry_date = (
                pd.to_datetime(row.get("EXP Date")).strftime("%m/%d/%Y")
                if pd.notnull(row.get("EXP Date"))
                else None
            )

            # ops_email_success = add_username_on_ops_email(username)
            # if ops_email_success:
            #     print("Ops email onboarding successful")
            # else:
            #     print("Ops email onboarding failed")
            #     return jsonify({"error": "Ops email onboarding failed"}), 500

            # amazon_success = driver_amazon_onboarding(
            #     first_name,
            #     last_name,
            #     email,
            #     location,
            #     dob,
            #     license_expiry_date,
            #     driver_license,
            # )
            # if amazon_success:
            #     print("Amazon onboarding successful")
            # else:
            #     print("Amazon onboarding failed")
            #     return jsonify({"error": "Amazon onboarding failed"}), 500

            password_set_success = amazon_onboarding_password_set(
                first_name, last_name, email, password, phone_number
            )
            if password_set_success:
                print("Onboarding driver set password successful")
            else:
                print("Onboarding driver set password failed")
                return jsonify({"error": "Onboarding driver set password failed"}), 500

            driver_shell_onboarding_success, driver_prompt_id = driver_shell_onboarding(
                first_name,
                last_name,
                email,
                driver_license,
                license_expiry_date,
                phone_number,
            )
            if driver_shell_onboarding_success:
                print("Shell onboarding driver successful")
                print("Driver Prompt ID:", driver_prompt_id)
            else:
                print("Shell onboarding driver failed")
                return jsonify({"error": "Shell onboarding driver failed"}), 500

            driver_fleetio_onboarding_success = driver_fleetio_onboarding(
                first_name, last_name, location, username, password
            )
            if driver_fleetio_onboarding_success:
                print("Fleetio onboarding driver successful")
            else:
                print("Fleetio onboarding driver failed")
                return jsonify({"error": "Fleetio onboarding driver failed"}), 500

        return jsonify({"results": "iteration completed"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
