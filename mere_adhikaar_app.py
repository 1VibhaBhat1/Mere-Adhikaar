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
        "safety_title": "For Your Safety:",
        "privacy_title": "Privacy & Data:",
        "legal_title": "Legal Disclaimer:",
        "danger_title": "In Immediate Danger:",
        "understand": "I Understand - Continue",
        "emergency_header": "🆘 Emergency Contacts",
        "legal_aid_header": "📞 Legal Aid & Support  ",
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
        "mic_button": "🎤 Voice Input",
        "stop_recording": "⏹️ Stop Recording",
    },
    "Hindi": {
        "title": "⚖️ मेरे अधिकार",
        "subtitle": "अपने अधिकार जानें",
        "quick_exit": "🚨 तुरंत बाहर निकलें",
        "safety_title": "आपकी सुरक्षा के लिए:",
        "privacy_title": "गोपनीयता और डेटा:",
        "legal_title": "कानूनी अस्वीकरण:",
        "danger_title": "तत्काल खतरे में:",
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
        "mic_button": "🎤 आवाज़ इनपुट",
        "stop_recording": "⏹️ रिकॉर्डिंग बंद करें",
    },
    "Marathi": {
        "title": "⚖️ माझे अधिकार",
        "subtitle": "तुमचे हक्क जाणा",
        "quick_exit": "🚨 त्वरित बाहेर पडा",
        "safety_title": "तुमच्या सुरक्षेसाठी:",
        "privacy_title": "गोपनीयता आणि डेटा:",
        "legal_title": "कायदेशीर अस्वीकरण:",
        "danger_title": "तात्काळ धोक्यात:",
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
        "mic_button": "🎤 आवाज इनपुट",
        "stop_recording": "⏹️ रेकॉर्डिंग थांबवा",
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

# Safety Warning
if st.session_state.show_safety:
    with st.expander("⚠️ " + ("IMPORTANT SAFETY & PRIVACY" if st.session_state.language == "English" else "महत्वपूर्ण सुरक्षा जानकारी" if st.session_state.language == "Hindi" else "महत्त्वाची सुरक्षा माहिती"), expanded=True):
        if st.session_state.language == "English":
            st.markdown("""
            **For Your Safety:**
            - Use Incognito/Private Mode (Ctrl+Shift+N or Cmd+Shift+N)
            - Quick Exit button redirects to Google
            - Clear chat button deletes conversation
            - Delete browser history after use
            
            **Privacy:**
            - No login required, no personal data collected
            - Messages sent to Claude AI for processing
            - Stored for 30 days then deleted
            - Could be accessed if legally required
            
            **Legal Disclaimer:**
            - This is NOT legal advice
            - For specific advice, consult a lawyer
            - Every case is different
            
            **In Immediate Danger:**
            - Emergency: 112
            - Women's Helpline: 181
            - Police: 100
            """)
        elif st.session_state.language == "Hindi":
            st.markdown("""
            **आपकी सुरक्षा के लिए:**
            - Incognito/Private Mode का उपयोग करें
            - Quick Exit बटन Google पर ले जाता है
            - बातचीत साफ़ करें बटन से हटाएं
            - ब्राउज़र इतिहास साफ़ करें
            
            **गोपनीयता:**
            - कोई लॉगिन नहीं, कोई व्यक्तिगत डेटा नहीं
            - संदेश Claude AI को भेजे जाते हैं
            - 30 दिन के लिए संग्रहीत, फिर हटा दिए जाते हैं
            
            **कानूनी अस्वीकरण:**
            - यह कानूनी सलाह नहीं है
            - विशिष्ट सलाह के लिए वकील से परामर्श करें
            
            **तत्काल खतरे में:**
            - आपातकाल: 112
            - महिला हेल्पलाइन: 181
            - पुलिस: 100
            """)
        else:  # Marathi
            st.markdown("""
            **तुमच्या सुरक्षेसाठी:**
            - Incognito/Private Mode वापरा
            - Quick Exit बटन Google वर नेते
            - संभाषण साफ करा बटनने हटवा
            - ब्राउझर इतिहास साफ करा
            
            **गोपनीयता:**
            - लॉगिन नाही, वैयक्तिक डेटा नाही
            - संदेश Claude AI ला पाठवले जातात
            - 30 दिवसांसाठी संग्रहित, नंतर हटवले जाते
            
            **कायदेशीर अस्वीकरण:**
            - हा कायदेशीर सल्ला नाही
            - विशिष्ट सल्ल्यासाठी वकीलाचा सल्ला घ्या
            
            **तात्काळ धोक्यात:**
            - आपत्कालीन: 112
            - महिला हेल्पलाइन: 181
            - पोलीस: 100
            """)
        
        if st.button(t["understand"]):
            st.session_state.show_safety = False
            st.rerun()

# Sidebar
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
        - Panel Lawyers: nalsa.gov.in/panel-lawyers/
        
        **Maharashtra:**
        - State Legal Services: 9869088444
        - Website: legalservices.maharashtra.gov.in
        
        **Uttar Pradesh:**
        - State Legal Services: 1800-419-0234
        - Website: uttarpradesh.nalsa.gov.in
        
        **Law Schools (Legal Aid):**
        - National Law University, Delhi: 91-9560024612
        - ILS Law College, Pune: 020-25656775
        - Symbiosis Law School, Pune: legalaid@slsp.edu.in
        """)
    elif st.session_state.language == "Hindi":
        st.markdown("""
        **राष्ट्रीय:**
        - NALSA: 011-23382778
        - वेबसाइट: nalsa.gov.in
        - पैनल वकील: nalsa.gov.in/panel-lawyers/
        
        **महाराष्ट्र:**
        - राज्य कानूनी सेवाएं: 9869088444
        - वेबसाइट: legalservices.maharashtra.gov.in
        
        **उत्तर प्रदेश:**
        - राज्य कानूनी सेवाएं: 1800-419-0234
        - वेबसाइट: uttarpradesh.nalsa.gov.in
        
        **लॉ स्कूल (कानूनी सहायता):**
        - नेशनल लॉ यूनिवर्सिटी, दिल्ली: 91-9560024612
        - आईएलएस लॉ कॉलेज, पुणे: 020-25656775
        - सिम्बायोसिस लॉ स्कूल, पुणे: legalaid@slsp.edu.in
        """)
    else:  # Marathi
        st.markdown("""
        **राष्ट्रीय:**
        - NALSA: 011-23382778
        - वेबसाइट: nalsa.gov.in
        - पॅनेल वकील: nalsa.gov.in/panel-lawyers/
        
        **महाराष्ट्र:**
        - राज्य कायदेशीर सेवा: 9869088444
        - वेबसाइट: legalservices.maharashtra.gov.in
        
        **उत्तर प्रदेश:**
        - राज्य कायदेशीर सेवा: 1800-419-0234
        - वेबसाइट: uttarpradesh.nalsa.gov.in
        
        **लॉ स्कूल (कायदेशीर मदत):**
        - नॅशनल लॉ युनिव्हर्सिटी, दिल्ली: 91-9560024612
        - आयएलएस लॉ कॉलेज, पुणे: 020-25656775
        - सिम्बायोसिस लॉ स्कूल, पुणे: legalaid@slsp.edu.in
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

st.markdown("---")

# Voice Input Section - Using components for proper rendering
voice_lang_map = {
    "English": "en-IN",
    "Hindi": "hi-IN", 
    "Marathi": "mr-IN"
}

voice_html = f"""
<html>
<head>
<style>
body {{
    margin: 0;
    padding: 0;
    font-family: sans-serif;
}}
.voice-container {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 10px;
    color: white;
    text-align: center;
}}
.voice-btn {{
    background: white;
    color: #667eea;
    padding: 12px 30px;
    border: none;
    border-radius: 25px;
    cursor: pointer;
    font-size: 18px;
    font-weight: bold;
    margin: 10px 5px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}}
.voice-btn:hover {{
    transform: scale(1.05);
}}
.stop-btn {{
    background: #dc3545;
    color: white;
}}
#status {{
    margin-top: 1rem;
    font-size: 16px;
    font-weight: bold;
    min-height: 24px;
}}
</style>
</head>
<body>
<div class="voice-container">
    <h3 style="margin: 0 0 0.5rem 0;">🎤 Voice Input</h3>
    <p style="margin: 0 0 1rem 0; font-size: 14px;">Click to speak your question</p>
    <button onclick="startRecording()" id="startBtn" class="voice-btn">
        🎤 Start Speaking
    </button>
    <button onclick="stopRecording()" id="stopBtn" class="voice-btn stop-btn" style="display: none;">
        ⏹️ Stop
    </button>
    <div id="status"></div>
</div>

<script>
let recognition = null;

function startRecording() {{
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {{
        document.getElementById('status').innerHTML = '❌ Please use Chrome or Edge';
        return;
    }}
    
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = '{voice_lang_map[st.session_state.language]}';
    
    document.getElementById('startBtn').style.display = 'none';
    document.getElementById('stopBtn').style.display = 'inline-block';
    document.getElementById('status').innerHTML = '🎤 Listening...';
    
    recognition.onresult = function(event) {{
        const transcript = event.results[0][0].transcript;
        document.getElementById('status').innerHTML = '✅ "' + transcript + '"';
        
        // Send to parent Streamlit app
        window.parent.postMessage({{
            type: 'streamlit:setComponentValue',
            value: transcript
        }}, '*');
        
        setTimeout(function() {{
            document.getElementById('startBtn').style.display = 'inline-block';
            document.getElementById('stopBtn').style.display = 'none';
            document.getElementById('status').innerHTML = '✅ Added to chat box below';
        }}, 2000);
    }};
    
    recognition.onerror = function(event) {{
        let msg = '❌ ';
        if (event.error === 'not-allowed') msg += 'Please allow microphone';
        else if (event.error === 'no-speech') msg += 'No speech detected';
        else msg += event.error;
        
        document.getElementById('status').innerHTML = msg;
        document.getElementById('startBtn').style.display = 'inline-block';
        document.getElementById('stopBtn').style.display = 'none';
    }};
    
    recognition.start();
}}

function stopRecording() {{
    if (recognition) recognition.stop();
    document.getElementById('startBtn').style.display = 'inline-block';
    document.getElementById('stopBtn').style.display = 'none';
}}
</script>
</body>
</html>
"""

import streamlit.components.v1 as components
voice_result = components.html(voice_html, height=200)

# If voice input received, add to messages
if voice_result:
    st.session_state.messages.append({"role": "user", "content": voice_result})
    st.rerun()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# System prompt
SYSTEM_PROMPT = """You are Mere Adhikaar (My Rights), an AI assistant helping victims of domestic violence understand their legal rights in India.

CRITICAL BEHAVIORAL RULES:
1. You ONLY help with domestic violence related queries
2. You are an AI assistant, NOT a lawyer, therapist, or counselor
3. If asked non-DV questions, politely redirect
4. If mental health crisis, direct to Tele Manas: 14416
5. Never give personal advice - only general legal information
6. Always include disclaimers

LEGAL KNOWLEDGE: [Same extensive knowledge base as before]

RESPONSE FORMAT:
🚨 [If rights violated]

**WHAT THE LAW SAYS:**
[Explain law simply - cite sections]

**YOUR RIGHTS:**
- [List clearly]

**GENERAL GUIDANCE:**
1. [Action step]
2. [Action step]

**EMERGENCY CONTACTS:**
☎️ 112, 181, 100

**FOR LEGAL ADVICE:**
[Legal aid contacts]

⚠️ SAFETY: [Warnings]

💡 IMPORTANT: This is general information, not legal advice. Consult a lawyer.

Respond in {language}. Use simple, clear language. Be compassionate."""

# Display chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
                raise ValueError("API key not found")
            
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
            message_placeholder.error(f"Error: {str(e)}")

# Footer buttons
st.markdown("---")
col1, col2 = st.columns([1, 1])

with col1:
    if st.button(t["clear_chat"], use_container_width=True):
        st.session_state.messages = []
        st.success("✅ Conversation cleared!")
        time.sleep(1)
        st.rerun()

with col2:
    if st.button(t["show_safety"], use_container_width=True):
        st.session_state.show_safety = True
        st.rerun()

st.markdown("""
<div style='background-color: #f8f9fa; padding: 1rem; border-radius: 5px; margin-top: 1rem;'>
<small>
<b>⚖️ Legal Disclaimer:</b> General legal information only. Not a substitute for legal advice. Consult a lawyer.
<br><br>
<b>🔒 Privacy:</b> Messages processed by Claude AI. Temporarily stored for 30 days. Use incognito mode.
<br><br>
<b>🆘 Emergency:</b> If in immediate danger, call 112 or 181 now.
</small>
</div>
""", unsafe_allow_html=True)
