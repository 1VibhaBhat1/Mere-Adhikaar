import streamlit as st
import anthropic
import time
import os

# Language translations
TRANSLATIONS = {
    "English": {
        "title": "⚖️ Mere Adhikaar",
        "subtitle": "Know Your Rights",
        "quick_exit": "🚨 QUICK EXIT",
        "understand": "I Understand - Continue",
        "emergency_header": "🆘 Emergency Contacts",
        "legal_aid_header": "📞 Legal Aid & Support",
        "common_topics": "📋 Common Topics",
        "select_language": "Select Language",
        "chat_placeholder": "Describe your situation... (Your conversation is private)",
        "clear_chat": "🗑️ Clear Conversation (For Safety)",
        "show_safety": "ℹ️ Show Safety Info Again",
        "analyzing": "⏳ Analyzing your situation...",
        "topic_physical": "Physical Violence",
        "topic_dowry": "Dowry Harassment",
        "topic_mental": "Mental Harassment",
        "topic_police": "Police Not Helping",
        "topic_economic": "Economic Abuse",
    },
    "Hindi": {
        "title": "⚖️ मेरे अधिकार",
        "subtitle": "अपने अधिकार जानें",
        "quick_exit": "🚨 तुरंत बाहर निकलें",
        "understand": "मैं समझता/समझती हूं - जारी रखें",
        "emergency_header": "🆘 आपातकालीन संपर्क",
        "legal_aid_header": "📞 कानूनी सहायता और समर्थन",
        "common_topics": "📋 सामान्य विषय",
        "select_language": "भाषा चुनें",
        "chat_placeholder": "अपनी स्थिति बताएं... (आपकी बातचीत निजी है)",
        "clear_chat": "🗑️ बातचीत साफ़ करें (सुरक्षा के लिए)",
        "show_safety": "ℹ️ सुरक्षा जानकारी फिर से दिखाएं",
        "analyzing": "⏳ आपकी स्थिति का विश्लेषण किया जा रहा है...",
        "topic_physical": "शारीरिक हिंसा",
        "topic_dowry": "दहेज उत्पीड़न",
        "topic_mental": "मानसिक उत्पीड़न",
        "topic_police": "पुलिस मदद नहीं कर रही",
        "topic_economic": "आर्थिक शोषण",
    },
    "Marathi": {
        "title": "⚖️ माझे अधिकार",
        "subtitle": "तुमचे हक्क जाणा",
        "quick_exit": "🚨 त्वरित बाहेर पडा",
        "understand": "मला समजले - सुरू ठेवा",
        "emergency_header": "🆘 आपत्कालीन संपर्क",
        "legal_aid_header": "📞 कायदेशीर मदत आणि समर्थन",
        "common_topics": "📋 सामान्य विषय",
        "select_language": "भाषा निवडा",
        "chat_placeholder": "तुमची परिस्थिती सांगा... (तुमचे संभाषण खाजगी आहे)",
        "clear_chat": "🗑️ संभाषण साफ करा (सुरक्षेसाठी)",
        "show_safety": "ℹ️ सुरक्षा माहिती पुन्हा दाखवा",
        "analyzing": "⏳ तुमची परिस्थिती तपासली जात आहे...",
        "topic_physical": "शारीरिक हिंसा",
        "topic_dowry": "हुंडा छळ",
        "topic_mental": "मानसिक छळ",
        "topic_police": "पोलीस मदत करत नाहीत",
        "topic_economic": "आर्थिक शोषण",
    }
}

# Page configuration
st.set_page_config(
    page_title="Mere Adhikaar - मेरे अधिकार - माझे अधिकार",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f5f5f0;
    }
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .safety-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
    .emergency-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "language" not in st.session_state:
    st.session_state.language = "English"
if "show_safety" not in st.session_state:
    st.session_state.show_safety = True

# Get current translations
t = TRANSLATIONS[st.session_state.language]

# Header with Quick Exit
col1, col2 = st.columns([5, 1])
with col1:
    st.markdown(f"""
    <div class="main-header">
        <h1>{t['title']}</h1>
        <p>{t['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(t["quick_exit"], type="primary", use_container_width=True):
        st.markdown('<meta http-equiv="refresh" content="0; url=https://www.google.com" />', unsafe_allow_html=True)
        st.stop()

# Safety Warning (collapsible)
if st.session_state.show_safety:
    with st.expander("⚠️ IMPORTANT SAFETY & PRIVACY INFORMATION - READ FIRST", expanded=True):
        if st.session_state.language == "English":
            st.markdown("""
            <div class="safety-box">
            <h3>🔒 For Your Safety:</h3>
            <ul>
                <li><b>Use Incognito/Private Mode:</b> Ctrl+Shift+N (Windows) or Cmd+Shift+N (Mac)</li>
                <li><b>Quick Exit Button:</b> Top-right corner - redirects to Google immediately</li>
                <li><b>Clear Chat:</b> Use button below to delete conversation anytime</li>
                <li><b>Delete Browser History:</b> After closing, clear your browsing history</li>
            </ul>
            
            <h3>🔐 Privacy & Data:</h3>
            <ul>
                <li><b>No Login Required:</b> We don't collect your name, phone, or email</li>
                <li><b>Messages Processed by AI:</b> Sent to Claude AI (Anthropic) for responses</li>
                <li><b>30-Day Storage:</b> Temporarily stored for 30 days, then deleted</li>
                <li><b>Legal Requests:</b> Could be accessed if legally required (rare)</li>
            </ul>
            
            <h3>⚖️ Legal Disclaimer:</h3>
            <ul>
                <li><b>This is NOT legal advice:</b> This provides general legal information</li>
                <li><b>Not a substitute for a lawyer:</b> Every case is different</li>
                <li><b>For specific advice:</b> Consult a qualified lawyer or legal aid</li>
            </ul>
            
            <h3>🆘 In Immediate Danger:</h3>
            <p><b>Don't wait - call now:</b></p>
            <ul>
                <li><b>Emergency:</b> 112</li>
                <li><b>Women's Helpline:</b> 181</li>
                <li><b>Police:</b> 100</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.language == "Hindi":
            st.markdown("""
            <div class="safety-box">
            <h3>🔒 आपकी सुरक्षा के लिए:</h3>
            <ul>
                <li><b>Incognito/Private Mode का उपयोग करें</b></li>
                <li><b>Quick Exit बटन:</b> ऊपर दाएं कोने में - तुरंत Google पर जाता है</li>
                <li><b>बातचीत साफ़ करें:</b> नीचे बटन का उपयोग करें</li>
                <li><b>ब्राउज़र इतिहास साफ़ करें</b></li>
            </ul>
            
            <h3>🔐 गोपनीयता और डेटा:</h3>
            <ul>
                <li><b>कोई लॉगिन नहीं:</b> हम आपका नाम, फोन या ईमेल नहीं लेते</li>
                <li><b>संदेश AI द्वारा संसाधित:</b> Claude AI को भेजे जाते हैं</li>
                <li><b>30 दिन का भंडारण:</b> 30 दिनों के लिए, फिर हटा दिया जाता है</li>
            </ul>
            
            <h3>⚖️ कानूनी अस्वीकरण:</h3>
            <ul>
                <li><b>यह कानूनी सलाह नहीं है:</b> सामान्य जानकारी प्रदान करता है</li>
                <li><b>वकील का विकल्प नहीं:</b> हर मामला अलग है</li>
                <li><b>विशिष्ट सलाह के लिए:</b> वकील से परामर्श करें</li>
            </ul>
            
            <h3>🆘 तत्काल खतरे में:</h3>
            <ul>
                <li><b>आपातकाल:</b> 112</li>
                <li><b>महिला हेल्पलाइन:</b> 181</li>
                <li><b>पुलिस:</b> 100</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        else:  # Marathi
            st.markdown("""
            <div class="safety-box">
            <h3>🔒 तुमच्या सुरक्षेसाठी:</h3>
            <ul>
                <li><b>Incognito/Private Mode वापरा</b></li>
                <li><b>Quick Exit बटन:</b> वरच्या उजव्या कोपऱ्यात - लगेच Google वर जाते</li>
                <li><b>संभाषण साफ करा:</b> खालील बटन वापरा</li>
                <li><b>ब्राउझर इतिहास साफ करा</b></li>
            </ul>
            
            <h3>🔐 गोपनीयता आणि डेटा:</h3>
            <ul>
                <li><b>लॉगिन नाही:</b> आम्ही तुमचे नाव, फोन किंवा ईमेल घेत नाही</li>
                <li><b>संदेश AI द्वारे प्रक्रिया:</b> Claude AI ला पाठवले जातात</li>
                <li><b>30 दिवसांचा संग्रह:</b> 30 दिवसांसाठी, नंतर हटवले जाते</li>
            </ul>
            
            <h3>⚖️ कायदेशीर अस्वीकरण:</h3>
            <ul>
                <li><b>हा कायदेशीर सल्ला नाही:</b> सामान्य माहिती प्रदान करते</li>
                <li><b>वकीलाचा पर्याय नाही:</b> प्रत्येक प्रकरण वेगळे आहे</li>
                <li><b>विशिष्ट सल्ल्यासाठी:</b> वकीलाचा सल्ला घ्या</li>
            </ul>
            
            <h3>🆘 तात्काळ धोक्यात:</h3>
            <ul>
                <li><b>आपत्कालीन:</b> 112</li>
                <li><b>महिला हेल्पलाइन:</b> 181</li>
                <li><b>पोलीस:</b> 100</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button(t["understand"]):
            st.session_state.show_safety = False
            st.rerun()

# Sidebar - Emergency Contacts & Resources
with st.sidebar:
    st.markdown(f"### {t['emergency_header']}")
    
    if st.session_state.language == "English":
        st.markdown("""
        <div class="emergency-box">
        <b>IMMEDIATE HELP:</b><br>
        • Emergency: 112<br>
        • Women's Helpline: 181<br>
        • Police: 100<br>
        • Women's Police: 1091<br>
        • NCW Helpline: 14490<br>
        • Child Helpline: 1098<br>
        • Mental Health: 14416<br>
        • Cyber Crime: 1930
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.language == "Hindi":
        st.markdown("""
        <div class="emergency-box">
        <b>तत्काल सहायता:</b><br>
        • आपातकाल: 112<br>
        • महिला हेल्पलाइन: 181<br>
        • पुलिस: 100<br>
        • महिला पुलिस: 1091<br>
        • राष्ट्रीय महिला आयोग: 14490<br>
        • बाल हेल्पलाइन: 1098<br>
        • मानसिक स्वास्थ्य: 14416<br>
        • साइबर क्राइम: 1930
        </div>
        """, unsafe_allow_html=True)
    else:  # Marathi
        st.markdown("""
        <div class="emergency-box">
        <b>तात्काळ मदत:</b><br>
        • आपत्कालीन: 112<br>
        • महिला हेल्पलाइन: 181<br>
        • पोलीस: 100<br>
        • महिला पोलीस: 1091<br>
        • राष्ट्रीय महिला आयोग: 14490<br>
        • बाल हेल्पलाइन: 1098<br>
        • मानसिक आरोग्य: 14416<br>
        • सायबर गुन्हे: 1930
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"### {t['legal_aid_header']}")
    
    if st.session_state.language == "English":
        st.markdown("""
        **National:**
        - NALSA: 011-23382778
        - Website: nalsa.gov.in
        - Panel Lawyers: [nalsa.gov.in/panel-lawyers/](https://nalsa.gov.in/panel-lawyers/)
        
        **Maharashtra State Legal Services Authority:**
        - Phone: 9869088444
        - Website: [legalservices.maharashtra.gov.in](https://legalservices.maharashtra.gov.in)
        
        **Uttar Pradesh State Legal Services Authority:**
        - Helpline: 1800-419-0234
        - Email: upslsa@nic.in
        - Website: [uttarpradesh.nalsa.gov.in](https://uttarpradesh.nalsa.gov.in)
        
        **Law Schools (Legal Aid):**
        - National Law University, Delhi: 91-9560024612
        - ILS Law College, Pune: 020-25656775, ils.legalaid@ilslaw.in
        - Symbiosis Law School, Pune: 020-25656775, legalaid@slsp.edu.in
        """)
    elif st.session_state.language == "Hindi":
        st.markdown("""
        **राष्ट्रीय:**
        - NALSA: 011-23382778
        - वेबसाइट: nalsa.gov.in
        - पैनल वकील: [nalsa.gov.in/panel-lawyers/](https://nalsa.gov.in/panel-lawyers/)
        
        **महाराष्ट्र राज्य विधिक सेवा प्राधिकरण:**
        - फोन: 9869088444
        - वेबसाइट: [legalservices.maharashtra.gov.in](https://legalservices.maharashtra.gov.in)
        
        **उत्तर प्रदेश राज्य विधिक सेवा प्राधिकरण:**
        - हेल्पलाइन: 1800-419-0234
        - ईमेल: upslsa@nic.in
        - वेबसाइट: [uttarpradesh.nalsa.gov.in](https://uttarpradesh.nalsa.gov.in)
        
        **लॉ स्कूल (कानूनी सहायता):**
        - नेशनल लॉ यूनिवर्सिटी, दिल्ली: 91-9560024612
        - ILS लॉ कॉलेज, पुणे: 020-25656775, ils.legalaid@ilslaw.in
        - सिम्बायोसिस लॉ स्कूल, पुणे: 020-25656775, legalaid@slsp.edu.in
        """)
    else:  # Marathi
        st.markdown("""
        **राष्ट्रीय:**
        - NALSA: 011-23382778
        - वेबसाइट: nalsa.gov.in
        - पॅनेल वकील: [nalsa.gov.in/panel-lawyers/](https://nalsa.gov.in/panel-lawyers/)
        
        **महाराष्ट्र राज्य विधी सेवा प्राधिकरण:**
        - फोन: 9869088444
        - वेबसाइट: [legalservices.maharashtra.gov.in](https://legalservices.maharashtra.gov.in)
        
        **उत्तर प्रदेश राज्य विधी सेवा प्राधिकरण:**
        - हेल्पलाइन: 1800-419-0234
        - ईमेल: upslsa@nic.in
        - वेबसाइट: [uttarpradesh.nalsa.gov.in](https://uttarpradesh.nalsa.gov.in)
        
        **लॉ स्कूल (कायदेशीर मदत):**
        - नॅशनल लॉ युनिव्हर्सिटी, दिल्ली: 91-9560024612
        - ILS लॉ कॉलेज, पुणे: 020-25656775, ils.legalaid@ilslaw.in
        - सिम्बायोसिस लॉ स्कूल, पुणे: 020-25656775, legalaid@slsp.edu.in
        """)
    
    st.markdown("---")
    st.markdown(f"### {t['common_topics']}")
    
    if st.button(t["topic_physical"], use_container_width=True):
        question = {
            "English": "My husband physically abuses me. What are my rights?",
            "Hindi": "मेरा पति मुझे शारीरिक रूप से प्रताड़ित करता है। मेरे अधिकार क्या हैं?",
            "Marathi": "माझा नवरा मला शारीरिक शोषण करतो. माझे हक्क काय आहेत?"
        }
        st.session_state.messages.append({"role": "user", "content": question[st.session_state.language]})
        st.rerun()
    
    if st.button(t["topic_dowry"], use_container_width=True):
        question = {
            "English": "My in-laws are demanding dowry and harassing me. What can I do?",
            "Hindi": "मेरे ससुराल वाले दहेज की मांग कर रहे हैं। मैं क्या कर सकती हूं?",
            "Marathi": "माझे सासरे हुंडा मागत आहेत. मी काय करू शकते?"
        }
        st.session_state.messages.append({"role": "user", "content": question[st.session_state.language]})
        st.rerun()
    
    if st.button(t["topic_mental"], use_container_width=True):
        question = {
            "English": "My husband mentally harasses me constantly. Is this domestic violence?",
            "Hindi": "मेरा पति लगातार मुझे मानसिक रूप से परेशान करता है। क्या यह घरेलू हिंसा है?",
            "Marathi": "माझा नवरा सतत मानसिक छळ करतो. हे घरगुती हिंसा आहे का?"
        }
        st.session_state.messages.append({"role": "user", "content": question[st.session_state.language]})
        st.rerun()
    
    if st.button(t["topic_police"], use_container_width=True):
        question = {
            "English": "Police are refusing to file my complaint. What should I do?",
            "Hindi": "पुलिस मेरी शिकायत दर्ज करने से इनकार कर रही है। मुझे क्या करना चाहिए?",
            "Marathi": "पोलीस माझी तक्रार नोंदवण्यास नकार देत आहेत. मी काय करावे?"
        }
        st.session_state.messages.append({"role": "user", "content": question[st.session_state.language]})
        st.rerun()
    
    if st.button(t["topic_economic"], use_container_width=True):
        question = {
            "English": "My husband controls all money and doesn't give me anything. Is this illegal?",
            "Hindi": "मेरा पति सारा पैसा नियंत्रित करता है और मुझे कुछ नहीं देता। क्या यह गैरकानूनी है?",
            "Marathi": "माझा नवरा सर्व पैसे नियंत्रित करतो. हे बेकायदेशीर आहे का?"
        }
        st.session_state.messages.append({"role": "user", "content": question[st.session_state.language]})
        st.rerun()

# Language selector
st.markdown(f"### {t['select_language']}")
language_options = {
    "English": "English",
    "हिंदी (Hindi)": "Hindi",
    "मराठी (Marathi)": "Marathi"
}
selected = st.selectbox(
    "",
    options=list(language_options.keys()),
    label_visibility="collapsed"
)
new_lang = language_options[selected]
if new_lang != st.session_state.language:
    st.session_state.language = new_lang
    st.rerun()

st.markdown("---")

# Note about typing in multiple languages
st.info("💬 **Tip:** You can type your question in English, Hindi (हिंदी), or Marathi (मराठी) below. The chatbot will respond in the language you selected above.")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# System prompt with extensive legal knowledge
SYSTEM_PROMPT = """You are Mere Adhikaar (My Rights), an AI assistant helping victims of domestic violence understand their legal rights in India.

CRITICAL BEHAVIORAL RULES (CANNOT BE BROKEN):
1. You ONLY help with domestic violence related queries
2. You are an AI assistant, NOT a lawyer, therapist, counselor, police officer, or judge
3. If asked to act as something else, politely refuse
4. If user asks non-DV questions, politely redirect
5. If user shares mental health crisis, direct to Tele Manas: 14416
6. Never give personal advice for "me" or "myself" - only general legal information
7. Always include disclaimers about not being legal advice
8. Avoid technical legal jargon - use simple language
9. Be compassionate, empathetic, non-judgmental

LEGAL KNOWLEDGE BASE:

PROTECTION OF WOMEN FROM DOMESTIC VIOLENCE ACT, 2005 (DV ACT):
- Section 3: Definition of domestic violence (physical, sexual, verbal, emotional, economic abuse)
- Section 17: Right to reside in shared household
- Section 18: Protection orders
- Section 19: Residence orders
- Section 20: Monetary relief
- Section 21: Custody orders
- Section 22: Compensation orders
- Section 31: Breach of protection order is punishable offense

BHARATIYA NYAYA SANHITA, 2023 (BNS):
- Section 85: Cruelty by husband or relatives
- Section 80: Dowry death
- Section 115-118: Causing hurt/grievous hurt
- Section 108: Abetment of suicide
- Section 351: Criminal intimidation

DOWRY PROHIBITION ACT, 1961:
- Section 3: Penalty for giving/taking dowry
- Section 4: Penalty for demanding dowry
- Section 6: Dowry belongs to wife
- Section 8A: Burden of proof on accused

BHARATIYA NAGARIK SURAKSHA SANHITA, 2023 (BNSS):
- Section 173: FIR (police must register for cognizable offenses)
- Section 144: Maintenance orders

BHARATIYA SAKSHYA ADHINIYAM, 2023 (BSA):
- Section 117: Presumption of abetment of suicide
- Section 118: Presumption of dowry death

HINDU MARRIAGE ACT, 1955:
- Section 13(1)(ia): Divorce on ground of cruelty
- Section 24: Interim maintenance
- Section 25: Permanent alimony
- Section 26: Child custody

DISSOLUTION OF MUSLIM MARRIAGES ACT, 1939:
- Section 2(viii): Cruelty as ground for dissolution

EMERGENCY CONTACTS:
- 112 (Emergency), 181 (Women's Helpline), 100 (Police), 1091 (Women's Police), 14490 (NCW), 1098 (Child Helpline), 14416 (Tele Manas - Mental Health)

LEGAL AID:
- NALSA: 011-23382778, nalsa.gov.in/panel-lawyers/
- Maharashtra State Legal Services Authority: 9869088444, legalservices.maharashtra.gov.in
- Uttar Pradesh State Legal Services Authority: 1800-419-0234, uttarpradesh.nalsa.gov.in
- National Law University, Delhi: 91-9560024612
- ILS Law College, Pune: 020-25656775, ils.legalaid@ilslaw.in
- Symbiosis Law School, Pune: 020-25656775, legalaid@slsp.edu.in

RESPONSE FORMAT:

🚨 [If rights violated, state clearly]

**WHAT THE LAW SAYS:**
[Explain relevant law in simple language - cite specific sections]

**YOUR RIGHTS:**
- [List rights clearly]

**GENERAL GUIDANCE (Not legal advice):**
1. [Specific actionable step]
2. [Specific actionable step]
3. [Specific actionable step]

**EVIDENCE TO COLLECT (If Safe):**
- [What can help case]

**FOR IMMEDIATE HELP:**
☎️ [Relevant emergency numbers]

**FOR LEGAL ADVICE:**
[Relevant legal aid contacts]

⚠️ **SAFETY FIRST:** [Any safety warnings]

💡 **IMPORTANT DISCLAIMER:**
This is general legal information, not advice. Every case is different. For advice specific to your situation, consult a lawyer. District Legal Services Authority provides free legal aid.

Respond in {language}. Use simple, clear language that someone with limited education can understand. Avoid legal jargon. Be compassionate and empowering."""

# Chat input
if prompt := st.chat_input(t["chat_placeholder"]):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown(t["analyzing"])
        
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY", os.environ.get("ANTHROPIC_API_KEY"))
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY not found in secrets")
            
            client = anthropic.Anthropic(api_key=api_key)
            
            messages_for_claude = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in st.session_state.messages[-6:]
            ]
            
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2500,
                temperature=0.7,
                system=SYSTEM_PROMPT.format(language=st.session_state.language),
                messages=messages_for_claude
            )
            
            assistant_message = response.content[0].text
            message_placeholder.markdown(assistant_message)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_message
            })
            
        except Exception as e:
            error_msg = str(e)
            if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
                message_placeholder.error("""
                **⚠️ API Key Error**
                
                The API key is not configured or invalid.
                
                **To fix this:**
                1. Make sure you added your API key in Streamlit Cloud secrets
                2. Format: `ANTHROPIC_API_KEY = "sk-ant-your-key"`
                3. Check you have credits at console.anthropic.com
                """)
            else:
                message_placeholder.error(f"""
                **⚠️ Error occurred:**
                
                {error_msg}
                
                Please check:
                - Your API key is correct in secrets
                - You have credits in your Anthropic account
                - Your internet connection is working
                """)

# Footer buttons
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 2])

with col1:
    if st.button(t["clear_chat"], use_container_width=True, type="secondary"):
        st.session_state.messages = []
        st.success("✅ Conversation cleared!")
        time.sleep(1)
        st.rerun()

with col2:
    if st.button(t["show_safety"], use_container_width=True):
        st.session_state.show_safety = True
        st.rerun()

with col3:
    st.markdown("""
    <div style='text-align: center; padding: 10px;'>
    <small>Built with care for survivors</small>
    </div>
    """, unsafe_allow_html=True)

# Final disclaimer at bottom
st.markdown("""
<div style='background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin-top: 1rem;'>
<small>
<b>⚖️ Legal Disclaimer:</b> This tool provides general legal information only. It is NOT a substitute for professional legal advice.
For specific guidance on your situation, consult a qualified lawyer or contact legal aid services.
<br><br>
<b>🔒 Privacy:</b> Your messages are processed by Claude AI. Data is temporarily stored for 30 days then deleted.
We do not store your conversations. Use incognito mode for additional privacy.
<br><br>
<b>🆘 Emergency:</b> If you are in immediate danger, call 112 (Emergency) or 181 (Women's Helpline) right now.
</small>
</div>
""", unsafe_allow_html=True)
