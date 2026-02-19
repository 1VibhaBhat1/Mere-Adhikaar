import streamlit as st
import anthropic
import os

# Page config
st.set_page_config(
    page_title="Mere Adhikaar - मेरे अधिकार - माझे अधिकार",
    page_icon="⚖️",
    layout="wide"
)

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "English"

# Translations
TRANSLATIONS = {
    "English": {
        "title": "⚖️ Mere Adhikaar",
        "subtitle": "Know Your Rights in Your Language",
        "quick_exit": "🚨 QUICK EXIT",
        "emergency": "🆘 Emergency Contacts",
        "legal_aid": "📞 Legal Aid",
        "chat_placeholder": "Type your question here...",
        "clear": "🗑️ Clear Chat",
        "analyzing": "⏳ Analyzing...",
    },
    "Hindi": {
        "title": "⚖️ मेरे अधिकार",
        "subtitle": "अपनी भाषा में अपने अधिकार जानें",
        "quick_exit": "🚨 तुरंत बाहर निकलें",
        "emergency": "🆘 आपातकालीन संपर्क",
        "legal_aid": "📞 कानूनी सहायता",
        "chat_placeholder": "अपना सवाल यहां लिखें...",
        "clear": "🗑️ बातचीत साफ़ करें",
        "analyzing": "⏳ विश्लेषण हो रहा है...",
    },
    "Marathi": {
        "title": "⚖️ माझे अधिकार",
        "subtitle": "तुमच्या भाषेत तुमचे हक्क जाणा",
        "quick_exit": "🚨 त्वरित बाहेर पडा",
        "emergency": "🆘 आपत्कालीन संपर्क",
        "legal_aid": "📞 कायदेशीर मदत",
        "chat_placeholder": "तुमचा प्रश्न येथे लिहा...",
        "clear": "🗑️ संभाषण साफ करा",
        "analyzing": "⏳ तपासत आहे...",
    }
}

t = TRANSLATIONS[st.session_state.language]

# Header
col1, col2 = st.columns([5, 1])
with col1:
    st.title(t["title"])
    st.caption(t["subtitle"])
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t["quick_exit"], type="primary"):
        st.markdown('<meta http-equiv="refresh" content="0; url=https://www.google.com" />', unsafe_allow_html=True)

# Language selector
lang_display = st.selectbox(
    "Language / भाषा / भाषा",
    ["English", "हिंदी (Hindi)", "मराठी (Marathi)"],
    label_visibility="visible"
)
new_lang = "English" if "English" in lang_display else "Hindi" if "Hindi" in lang_display else "Marathi"
if new_lang != st.session_state.language:
    st.session_state.language = new_lang
    st.rerun()

# Sidebar
with st.sidebar:
    st.header(t["emergency"])
    
    if st.session_state.language == "English":
        st.markdown("""
        **IMMEDIATE HELP:**
        - **112** - Emergency
        - **181** - Women's Helpline
        - **100** - Police
        - **1091** - Women's Police
        - **14490** - NCW Helpline
        - **1098** - Child Helpline
        - **14416** - Mental Health
        - **1930** - Cyber Crime
        """)
    elif st.session_state.language == "Hindi":
        st.markdown("""
        **तत्काल सहायता:**
        - **112** - आपातकाल
        - **181** - महिला हेल्पलाइन
        - **100** - पुलिस
        - **1091** - महिला पुलिस
        - **14490** - NCW हेल्पलाइन
        - **1098** - बाल हेल्पलाइन
        - **14416** - मानसिक स्वास्थ्य
        - **1930** - साइबर क्राइम
        """)
    else:
        st.markdown("""
        **तात्काळ मदत:**
        - **112** - आपत्कालीन
        - **181** - महिला हेल्पलाइन
        - **100** - पोलीस
        - **1091** - महिला पोलीस
        - **14490** - NCW हेल्पलाइन
        - **1098** - बाल हेल्पलाइन
        - **14416** - मानसिक आरोग्य
        - **1930** - सायबर गुन्हे
        """)
    
    st.markdown("---")
    st.header(t["legal_aid"])
    
    if st.session_state.language == "English":
        st.markdown("""
        **National:**
        - NALSA: 011-23382778
        - [Panel Lawyers](https://nalsa.gov.in/panel-lawyers/)
        
        **Maharashtra:**
        - State: 9869088444
        - [Website](https://legalservices.maharashtra.gov.in)
        
        **Uttar Pradesh:**
        - State: 1800-419-0234
        - [Website](https://uttarpradesh.nalsa.gov.in)
        
        **Law Schools:**
        - NLU Delhi: 91-9560024612
        - ILS Pune: 020-25656775
        - Symbiosis: legalaid@slsp.edu.in
        """)
    elif st.session_state.language == "Hindi":
        st.markdown("""
        **राष्ट्रीय:**
        - NALSA: 011-23382778
        - [पैनल वकील](https://nalsa.gov.in/panel-lawyers/)
        
        **महाराष्ट्र:**
        - राज्य: 9869088444
        - [वेबसाइट](https://legalservices.maharashtra.gov.in)
        
        **उत्तर प्रदेश:**
        - राज्य: 1800-419-0234
        - [वेबसाइट](https://uttarpradesh.nalsa.gov.in)
        
        **लॉ स्कूल:**
        - NLU दिल्ली: 91-9560024612
        - ILS पुणे: 020-25656775
        - Symbiosis: legalaid@slsp.edu.in
        """)
    else:
        st.markdown("""
        **राष्ट्रीय:**
        - NALSA: 011-23382778
        - [पॅनेल वकील](https://nalsa.gov.in/panel-lawyers/)
        
        **महाराष्ट्र:**
        - राज्य: 9869088444
        - [वेबसाइट](https://legalservices.maharashtra.gov.in)
        
        **उत्तर प्रदेश:**
        - राज्य: 1800-419-0234
        - [वेबसाइट](https://uttarpradesh.nalsa.gov.in)
        
        **लॉ स्कूल:**
        - NLU दिल्ली: 91-9560024612
        - ILS पुणे: 020-25656775
        - Symbiosis: legalaid@slsp.edu.in
        """)

# Safety notice
with st.expander("⚠️ Safety & Privacy"):
    if st.session_state.language == "English":
        st.warning("""
        **Safety:** Use incognito mode • Quick exit button above • Clear chat after use
        
        **Privacy:** No login required • Messages sent to AI • Not stored permanently
        
        **Disclaimer:** This is NOT legal advice • Call 112/181 for emergencies • Consult a lawyer
        """)
    elif st.session_state.language == "Hindi":
        st.warning("""
        **सुरक्षा:** Incognito mode का उपयोग करें • Quick exit बटन ऊपर • बातचीत साफ़ करें
        
        **गोपनीयता:** लॉगिन नहीं • संदेश AI को भेजे जाते हैं • स्थायी रूप से संग्रहीत नहीं
        
        **अस्वीकरण:** यह कानूनी सलाह नहीं है • आपात स्थिति में 112/181 पर कॉल करें • वकील से परामर्श करें
        """)
    else:
        st.warning("""
        **सुरक्षा:** Incognito mode वापरा • Quick exit बटन वर • संभाषण साफ करा
        
        **गोपनीयता:** लॉगिन नाही • संदेश AI ला पाठवले जातात • कायमस्वरूपी संग्रहित नाहीत
        
        **अस्वीकरण:** हा कायदेशीर सल्ला नाही • आपत्कालीन परिस्थितीत 112/181 वर कॉल करा • वकीलाचा सल्ला घ्या
        """)

st.markdown("---")

# Chat display
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# System prompt
SYSTEM_PROMPT = """You are Mere Adhikaar (My Rights), an AI assistant helping domestic violence victims in India.

LAWS: DV Act 2005 (protection/residence/monetary relief orders), BNS 2023 Section 85 (cruelty), Section 80 (dowry death), Dowry Prohibition Act 1961, BNSS 2023 (FIR/maintenance), BSA 2023 (evidence), Hindu Marriage Act, Muslim Marriage Act

EMERGENCY: 112, 181 (Women's Helpline), 100 (Police), 1091 (Women's Police)
LEGAL AID: NALSA 011-23382778, https://nalsa.gov.in/panel-lawyers/, Maharashtra 9869088444, UP 1800-419-0234

FORMAT:
🚨 [State violation if any]

**WHAT THE LAW SAYS:**
[Explain sections simply in {language}]

**YOUR RIGHTS:**
- [List clearly]

**STEPS YOU CAN TAKE:**
1. [Action with safety warnings]

**GET HELP:**
☎️ [Contacts]

💡 **IMPORTANT:** General information only, NOT legal advice. Consult a lawyer. Call 181 for immediate help.

Respond in {language}. Use simple, compassionate language."""

# Chat input
if prompt := st.chat_input(t["chat_placeholder"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown(t["analyzing"])
        
        try:
            api_key = st.secrets["ANTHROPIC_API_KEY"]
            client = anthropic.Anthropic(api_key=api_key)
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2500,
                system=SYSTEM_PROMPT.format(language=st.session_state.language),
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[-6:]]
            )
            
            answer = response.content[0].text
            placeholder.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            placeholder.error(f"⚠️ Error: {str(e)}")

# Footer
st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    if st.button(t["clear"]):
        st.session_state.messages = []
        st.rerun()
with col2:
    st.caption("Built for survivors of domestic violence")
