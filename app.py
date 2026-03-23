import streamlit as st
import pandas as pd
import pickle

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Churn Intelligence",
    page_icon="📡",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS for Premium UI & Dropdown Fix ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=DM+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Global Spacing ── */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

/* ── Section headings ── */
.section-heading {
    font-family: 'DM Mono', monospace;
    font-size: 0.70rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #9ca3af;
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 2.2rem 0 1rem;
    font-weight: 500;
}
.section-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
}

/* ── Widget labels ── */
div[data-testid="stSelectbox"] label,
div[data-testid="stSlider"] label,
div[data-testid="stNumberInput"] label {
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em;
    margin-bottom: 6px !important;
    color: #d1d5db !important;
}

/* ── Selectbox & Number Input Containers ── */
div[data-testid="stSelectbox"] > div > div, 
div[data-testid="stNumberInput"] > div > div {
    background-color: rgba(17, 24, 39, 0.6) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    font-size: 0.9rem !important;
    min-height: 44px !important;
    padding: 2px 6px !important;
    transition: all 0.25s ease !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1) !important;
}

div[data-testid="stSelectbox"] > div > div:hover, 
div[data-testid="stNumberInput"] > div > div:hover {
    border-color: rgba(125,211,188,0.4) !important;
    background-color: rgba(17, 24, 39, 0.8) !important;
}

div[data-testid="stSelectbox"] > div > div:focus-within, 
div[data-testid="stNumberInput"] > div > div:focus-within {
    border-color: #7dd3bc !important;
    box-shadow: 0 0 0 1px rgba(125,211,188,0.3), inset 0 2px 4px rgba(0,0,0,0.1) !important;
}

/* ── FIX: Dropdown List Blending into Background ── */
div[data-baseweb="popover"] > div {
    background-color: #1f2937 !important;
    border: 1px solid rgba(125,211,188,0.4) !important;
    border-radius: 10px !important;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.7) !important;
    overflow: hidden !important;
    z-index: 999999 !important;
}
div[data-baseweb="popover"] li {
    font-size: 0.9rem !important;
    padding: 10px 14px !important;
    color: #e5e7eb !important;
    transition: background-color 0.2s ease, color 0.2s ease !important;
}
div[data-baseweb="popover"] li:hover {
    background-color: rgba(125,211,188,0.15) !important;
    color: #7dd3bc !important;
}
div[data-baseweb="popover"] li[aria-selected="true"] {
    background-color: rgba(125,211,188,0.2) !important;
    color: #7dd3bc !important;
    font-weight: 600 !important;
}

/* ── Number input text ── */
div[data-testid="stNumberInput"] input {
    border-radius: 10px !important;
    font-size: 0.9rem !important;
    min-height: 44px !important;
    color: #e5e7eb !important;
}

/* ── Spacing ── */
div[data-testid="stSelectbox"],
div[data-testid="stNumberInput"],
div[data-testid="stSlider"] {
    margin-bottom: 12px !important;
}

/* ── Internet notice ── */
.inet-notice {
    background: linear-gradient(90deg, rgba(125,211,188,0.1), rgba(125,211,188,0.03));
    border-left: 3px solid #7dd3bc;
    border-radius: 8px;
    padding: 0.8rem 1.2rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    color: #7dd3bc;
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* ── Disabled service pills ── */
.svc-pill {
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    background: rgba(17, 24, 39, 0.4);
    transition: transform 0.2s ease, background 0.2s ease;
}
.svc-pill:hover {
    background: rgba(17, 24, 39, 0.6);
    transform: translateY(-1px);
}
.svc-pill-name { font-size: 0.85rem; color: #9ca3af; font-weight: 500; }
.svc-pill-val  {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    color: #6b7280;
}

/* ── Predict button ── */
div[data-testid="stButton"] > button {
    width: 100%;
    padding: 0.85rem 0;
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    color: #0d0f14 !important;
    background: linear-gradient(135deg, #7dd3bc 0%, #5ab3a0 100%) !important;
    border: none !important;
    border-radius: 12px !important;
    margin-top: 2rem;
    box-shadow: 0 6px 20px rgba(125,211,188,0.25) !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(125,211,188,0.35) !important;
    opacity: 0.95 !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(1px) !important;
    box-shadow: 0 4px 12px rgba(125,211,188,0.2) !important;
}

/* ── Result card ── */
.result-card {
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    margin-top: 2rem;
    display: flex;
    align-items: flex-start;
    gap: 1.2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    animation: slideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    opacity: 0;
    transform: translateY(10px);
}

@keyframes slideUp {
    to { opacity: 1; transform: translateY(0); }
}

.result-card.churn {
    background: linear-gradient(145deg, rgba(239,68,68,0.08), rgba(239,68,68,0.02));
    border: 1px solid rgba(239,68,68,0.3);
    box-shadow: 0 8px 24px rgba(239,68,68,0.1);
}
.result-card.stay {
    background: linear-gradient(145deg, rgba(125,211,188,0.08), rgba(125,211,188,0.02));
    border: 1px solid rgba(125,211,188,0.3);
    box-shadow: 0 8px 24px rgba(125,211,188,0.1);
}
.result-icon   { font-size: 2.2rem; flex-shrink: 0; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2)); }
.result-verdict {
    font-size: 1.15rem; font-weight: 600;
    margin: 0 0 0.3rem; letter-spacing: -0.01em;
}
.result-card.churn .result-verdict { color: #f87171; }
.result-card.stay  .result-verdict { color: #7dd3bc; }
.result-desc {
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem; color: #9ca3af; margin: 0 0 1.2rem;
}

.prob-row {
    display: flex; justify-content: space-between;
    align-items: center; margin-bottom: 6px;
}
.prob-label { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #6b7280; }
.prob-pct   { font-family: 'DM Mono', monospace; font-size: 0.9rem; font-weight: 600; }
.result-card.churn .prob-pct { color: #f87171; }
.result-card.stay  .prob-pct { color: #7dd3bc; }

.prob-track {
    background: rgba(255,255,255,0.06);
    border-radius: 100px; height: 6px; overflow: hidden;
    position: relative;
}
.prob-fill  { 
    height: 100%; 
    border-radius: 100px; 
    transition: width 1s cubic-bezier(0.16, 1, 0.3, 1);
}
.prob-fill.churn { background: linear-gradient(90deg, #ef4444, #f87171); box-shadow: 0 0 10px rgba(248,113,113,0.5); }
.prob-fill.stay  { background: linear-gradient(90deg, #5ab3a0, #7dd3bc); box-shadow: 0 0 10px rgba(125,211,188,0.5); }


/* ── Action Plan / Retention Tips UI ── */
.action-plan {
    margin-top: 1.5rem;
    padding: 1.5rem;
    border-radius: 14px;
    background: linear-gradient(145deg, rgba(31, 41, 55, 0.4), rgba(17, 24, 39, 0.6));
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    opacity: 0;
    transform: translateY(10px);
}
.action-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #e5e7eb;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.action-list { list-style: none; padding: 0; margin: 0; }
.action-item {
    font-size: 0.9rem;
    color: #d1d5db;
    background: rgba(255,255,255,0.03);
    border-left: 3px solid #f87171;
    padding: 0.9rem 1.2rem;
    margin-bottom: 0.8rem;
    border-radius: 8px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    transition: transform 0.2s ease, background 0.2s ease;
}
.action-item:hover {
    background: rgba(255,255,255,0.05);
    transform: translateX(4px);
    border-color: #ef4444;
}

/* ── Upgrade Card UI ── */
.upgrade-card {
    background: linear-gradient(145deg, rgba(125, 211, 188, 0.08), rgba(125, 211, 188, 0.02));
    border: 1px dashed rgba(125, 211, 188, 0.3);
    border-radius: 12px;
    padding: 1.4rem;
    margin-top: 0.5rem;
}
.upgrade-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #7dd3bc;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.upgrade-text {
    font-size: 0.9rem;
    color: #9ca3af;
    line-height: 1.6;
    margin-bottom: 1.2rem;
}
.upgrade-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-bottom: 1.2rem;
}
.upgrade-pill {
    font-size: 0.8rem;
    font-weight: 500;
    background: rgba(125, 211, 188, 0.1);
    color: #7dd3bc;
    padding: 8px 12px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
    border: 1px solid rgba(125, 211, 188, 0.15);
}
.upgrade-footer {
    font-family: 'DM Mono', monospace;
    font-size: 0.75rem;
    font-weight: 500;
    color: #7dd3bc;
    background: rgba(125,211,188,0.1);
    padding: 0.8rem;
    border-radius: 8px;
    text-align: center;
    border-left: 3px solid #5ab3a0;
}

/* ── Footer ── */
.footer {
    text-align: center; margin-top: 3.5rem; padding-top: 1.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem; color: #4b5563;
    letter-spacing: 0.1em; text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)


# ── Load artifacts ─────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    with open("model.pkl", "rb") as f:
        m = pickle.load(f)
    with open("scaler.pkl", "rb") as f:
        s = pickle.load(f)
    return m, s

model, scaler = load_artifacts()


# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("## 📡 Churn Risk Assessment")
st.caption("Fill in the customer profile — the model will estimate churn probability instantly.")
st.divider()


# ══════════════════════════════════════════════════════════════
#  SECTION 1 — Demographics
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="section-heading">👤 &nbsp; Demographics</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
with col2:
    senior = st.selectbox("Senior Citizen", ["No", "Yes"])


# ══════════════════════════════════════════════════════════════
#  SECTION 2 — Account & Billing
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="section-heading">💳 &nbsp; Account &amp; Billing</div>', unsafe_allow_html=True)

tenure = st.slider("Tenure (months)", 0, 72, 12)

col3, col4 = st.columns(2)
with col3:
    monthly = st.number_input("Monthly Charges ($)", 0.0, 10000.0, 50.0, step=0.5)

# TotalCharges auto-calculated by monthly * tenure; no artificial cap
with col4:
    total = float(monthly) * float(tenure)
    st.number_input("Total Charges ($)", value=total, min_value=0.0, step=0.1, format="%.2f", disabled=True)

col5, col6 = st.columns(2)
with col5:
    contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
with col6:
    payment = st.selectbox("Payment Method", [
        "Electronic check", "Mailed check",
        "Bank transfer (automatic)", "Credit card (automatic)",
    ])

phone = st.selectbox("Phone Service", ["Yes", "No"])


# ══════════════════════════════════════════════════════════════
#  SECTION 3 — Internet & Add-ons
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="section-heading">🌐 &nbsp; Internet &amp; Add-on Services</div>', unsafe_allow_html=True)

internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

ADDON_SERVICES = [
    "Online Security", "Device Protection",
    "Tech Support", "Streaming Movies", "Streaming TV",
]

if internet == "No":
    st.markdown("""
    <div class="inet-notice">
      ℹ &nbsp; No internet service — all add-ons are automatically disabled.
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    for idx, label in enumerate(ADDON_SERVICES):
        with (col_a if idx % 2 == 0 else col_b):
            st.markdown(f"""
            <div class="svc-pill">
              <span class="svc-pill-name">{label}</span>
              <span class="svc-pill-val">— No</span>
            </div>
            """, unsafe_allow_html=True)

    online_sec = device = tech = stream_movies = stream_tv = "No"

else:
    col_a, col_b = st.columns(2)
    with col_a:
        online_sec    = st.selectbox("Online Security",  ["Yes", "No"])
        tech          = st.selectbox("Tech Support",      ["Yes", "No"])
        stream_tv     = st.selectbox("Streaming TV",      ["Yes", "No"])
    with col_b:
        device        = st.selectbox("Device Protection", ["Yes", "No"])
        stream_movies = st.selectbox("Streaming Movies",  ["Yes", "No"])


# ══════════════════════════════════════════════════════════════
#  Predict 
# ══════════════════════════════════════════════════════════════
predict = st.button("Run Churn Prediction →")

if predict:
    data = {
        "gender":           [1 if gender == "Male" else 0],
        "SeniorCitizen":    [1 if senior == "Yes" else 0],
        "tenure":           [tenure],
        "MonthlyCharges":   [monthly],
        "TotalCharges":     [total],
        "PhoneService":     [1 if phone == "Yes" else 0],
        "OnlineSecurity":   [1 if online_sec == "Yes" else 0],
        "DeviceProtection": [1 if device == "Yes" else 0],
        "TechSupport":      [1 if tech == "Yes" else 0],
        "StreamingMovies":  [1 if stream_movies == "Yes" else 0],
        "StreamingTV":      [1 if stream_tv == "Yes" else 0],
    }
    df = pd.DataFrame(data)

    df = pd.concat([
        df,
        pd.get_dummies(pd.Series([contract]), prefix="Contract"),
        pd.get_dummies(pd.Series([internet]), prefix="InternetService"),
        pd.get_dummies(pd.Series([payment]),  prefix="PaymentMethod"),
    ], axis=1)

    df = df.reindex(columns=model.feature_names_in_, fill_value=0)

    num_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
    df[num_cols] = scaler.transform(df[num_cols])

    prediction  = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1]
    pct         = round(probability * 100, 1)
    kind        = "churn" if prediction == 1 else "stay"
    icon        = "⚠️" if prediction == 1 else "✅"
    verdict     = "Customer is likely to churn" if prediction == 1 else "Customer is likely to stay"

    st.markdown(f"""
    <div class="result-card {kind}">
      <div class="result-icon">{icon}</div>
      <div style="flex:1">
        <p class="result-verdict">{verdict}</p>
        <p class="result-desc">Churn probability &nbsp;·&nbsp; {pct}%</p>
        <div class="prob-row">
          <span class="prob-label">0% — no risk</span>
          <span class="prob-pct">{pct}%</span>
          <span class="prob-label">100% — certain</span>
        </div>
        <div class="prob-track">
          <div class="prob-fill {kind}" style="width:{pct}%"></div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    #  RETENTION LOGIC & DYNAMIC ACTION PLAN 
    # ══════════════════════════════════════════════════════════════
    if prediction == 1:
        tips = []
        if contract == "Month-to-month":
            tips.append("Offer discounts for long-term contracts (1 or 2 year plans).")
        if monthly > 70:
            tips.append("Provide discounts or better pricing plans to reduce monthly charges.")
        if tenure < 12:
            tips.append("Engage new customers with offers and support to increase retention.")
        if payment == "Electronic check":
            tips.append("Encourage switching to automatic payment methods.")
            
        tips_html = ""
        if tips:
            items = "".join([f'<li class="action-item"><span style="font-size: 1.1rem;">🎯</span> <span>{t}</span></li>' for t in tips])
            tips_html = f"""
            <div class="action-plan">
                <div class="action-title">🛑 Retention Action Plan</div>
                <ul class="action-list">
                    {items}
                </ul>
            </div>
            """
            
        upgrade_html = ""
        if internet == "No":
            upgrade_html = """
            <div class="action-plan" style="margin-top: 1rem; padding: 0; background: transparent; border: none; box-shadow: none;">
                <div class="upgrade-card">
                    <div class="upgrade-title">💡 Upgrade Opportunity</div>
                    <div class="upgrade-text">
                        Customer currently has no internet service.<br>
                        <span style="color:#e5e7eb;">👉 Adding internet can unlock the following services:</span>
                    </div>
                    <div class="upgrade-grid">
                        <div class="upgrade-pill">🛡️ Online Security</div>
                        <div class="upgrade-pill">📱 Device Protection</div>
                        <div class="upgrade-pill">🛠️ Tech Support</div>
                        <div class="upgrade-pill">🎬 Streaming TV & Movies</div>
                    </div>
                    <div class="upgrade-footer">
                        ℹ️ Offering bundled internet + services can significantly reduce churn.
                    </div>
                </div>
            </div>
            """
            
        if tips_html or upgrade_html:
            st.markdown(tips_html + upgrade_html, unsafe_allow_html=True)


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">ChurnIQ · ML Classification · Powered by scikit-learn</div>', unsafe_allow_html=True)
