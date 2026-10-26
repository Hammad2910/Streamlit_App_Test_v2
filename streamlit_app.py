
import streamlit as st
import requests

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="EduPredict | Student Analytics",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------
st.markdown("""
<style>
    .stApp {
        background-color: #f4f7fb;
    }

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #172554;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .section-title {
        color: #1e293b;
        font-size: 21px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    .result-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        text-align: center;
        margin-top: 20px;
    }

    .pass-result {
        color: #15803d;
        font-size: 32px;
        font-weight: 800;
    }

    .fail-result {
        color: #dc2626;
        font-size: 32px;
        font-weight: 800;
    }

    div.stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 10px;
        height: 50px;
        font-size: 17px;
        font-weight: 600;
        border: none;
    }

    div.stButton > button:hover {
        background-color: #1d4ed8;
        color: white;
    }

    [data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 13px;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HEADER
# -----------------------------------
st.markdown(
    '<div class="main-title">🎓 EduPredict</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Student Performance Prediction System'
    '</div>',
    unsafe_allow_html=True
)

st.divider()

# -----------------------------------
# MAIN LAYOUT
# -----------------------------------
left, right = st.columns([1.2, 1], gap="large")

with left:

    st.markdown(
        '<div class="section-title">📋 Student Information</div>',
        unsafe_allow_html=True
    )

    st.write("Enter the student's academic information.")

    with st.container(border=True):

        study_hours = st.slider(
            "📚 Daily Study Hours",
            min_value=0.0,
            max_value=10.0,
            value=4.0,
            step=0.5,
            help="Average number of hours spent studying daily."
        )

        prev_score = st.slider(
            "📝 Previous Exam Score",
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=1.0,
            help="Student's score in the previous examination."
        )

        st.write("")

        predict = st.button(
            "🚀 Generate Prediction",
            use_container_width=True
        )

with right:

    st.markdown(
        '<div class="section-title">📊 Input Summary</div>',
        unsafe_allow_html=True
    )

    st.write("Review the selected student information.")

    st.metric(
        "Daily Study Hours",
        f"{study_hours} hrs"
    )

    st.metric(
        "Previous Exam Score",
        f"{prev_score}/100"
    )

    st.metric(
        "Academic Score Percentage",
        f"{prev_score:.1f}%"
    )

    st.info(
        "The AI model analyzes the provided information "
        "to estimate the student's academic outcome."
    )

# -----------------------------------
# PREDICTION
# -----------------------------------
if predict:

    st.divider()

    st.markdown(
        '<div class="section-title">🔍 Prediction Results</div>',
        unsafe_allow_html=True
    )

    try:

        with st.spinner("Analyzing student performance..."):

            response = requests.post(
                f"{API_URL}/predict",
                json={
                    "study_hours": study_hours,
                    "prev_score": prev_score
                },
                timeout=10
            )

        if response.status_code == 200:

            result = response.json()

            prediction = result["prediction"]
            result_label = result["result_label"]
            confidence = result["confidence"] * 100

            # Prediction result
            if prediction == 1:

                st.success("🎉 Positive Prediction")

                st.markdown(
                    f'<div class="result-card">'
                    f'<div class="pass-result">'
                    f'✓ {result_label}'
                    f'</div>'
                    f'<p>Predicted academic outcome</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            else:

                st.error("⚠️ Negative Prediction")

                st.markdown(
                    f'<div class="result-card">'
                    f'<div class="fail-result">'
                    f'✕ {result_label}'
                    f'</div>'
                    f'<p>Predicted academic outcome</p>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            # Confidence score
            st.write("### Model Confidence")

            st.progress(
                max(0.0, min(1.0, confidence / 100))
            )

            st.metric(
                "Prediction Confidence",
                f"{confidence:.1f}%"
            )

            # Detailed response
            with st.expander("View Technical API Response"):
                st.json(result)

        else:

            st.error(
                f"API Error: {response.status_code}"
            )

    except requests.exceptions.ConnectionError:

        st.error(
            "Unable to connect to FastAPI. "
            "Please make sure the backend server is running."
        )

    except requests.exceptions.Timeout:

        st.error(
            "The prediction request timed out. "
            "Please try again."
        )

    except (requests.exceptions.RequestException, ValueError, KeyError) as e:

        st.error(f"An error occurred: {e}")

# -----------------------------------
# FOOTER
# -----------------------------------
st.divider()

st.markdown(
    '<div class="footer">'
    'EduPredict | AI-Powered Academic Analytics '
    '| Built with Streamlit & FastAPI'
    '</div>',
    unsafe_allow_html=True
)
