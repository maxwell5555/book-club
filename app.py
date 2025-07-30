import os
import oci
from flask import Flask, jsonify, render_template
from apscheduler.schedulers.background import BackgroundScheduler
from threading import Lock

from load_spells import load_spells_from_ods

app = Flask(__name__)

# Globals
wizard_data = []
data_lock = Lock()

# OCI Object Storage setup
object_storage_client = oci.object_storage.ObjectStorageClient(
    config={}, signer=oci.auth.signers.InstancePrincipalsSecurityTokenSigner()
)
namespace = object_storage_client.get_namespace().data
bucket_name = "book-club"
object_name = "Book_Club_Data_2024.ods"
local_path = "/opt/bookclub/Book_Club_Data_2024.ods"

def fetch_and_update_spell_data():
    try:
        print("⏬ Downloading latest ODS file from OCI...")
        with open(local_path, "wb") as f:
            response = object_storage_client.get_object(namespace, bucket_name, object_name)
            for chunk in response.data.raw.stream(1024 * 1024, decode_content=False):
                f.write(chunk)

        print("📖 Parsing spell data...")
        records = load_spells_from_ods(local_path)

        with data_lock:
            global wizard_data
            wizard_data = records

        print(f"✅ Loaded {len(records)} spells successfully.")
    except Exception as e:
        print(f"❌ Failed to fetch or parse ODS: {e}")

# API endpoint for frontend
@app.route('/')
def index():
    return render_template('index.html')

@app.route("/data")
def get_data():
    with data_lock:
        return jsonify(spells=wizard_data)

@app.route('/stats')
def stats():
    return render_template('stats.html')

# Run fetch job hourly
scheduler = BackgroundScheduler()
scheduler.add_job(func=fetch_and_update_spell_data, trigger="interval", hours=1)
scheduler.start()

# Run once at startup
fetch_and_update_spell_data()

if __name__ == "__main__":
    app.run()
