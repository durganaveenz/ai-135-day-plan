# Module 5: Advanced Security Architecture (16 topics)

topics = [
    {
        "title": "Zero Trust Architecture (Never Trust, Always Verify)",
        "subtitle": "జీరో ట్రస్ట్ ఆర్కిటెక్చర్ (ఆఫీస్ నెట్‌వర్క్ లోపల ఉన్నా ఎవరినీ నమ్మొద్దు; ప్రతి రిక్వెస్ట్ నూ ధృవీకరించు)",
        "why": "సాంప్రదాయ క్యాజిల్-అండ్-మోట్ (Castle-and-moat / VPN) సెక్యూరిటీలో హ్యాకర్ ఒక్కసారి ఆఫీస్ వైఫై లేదా VPN లోకి ప్రవేశిస్తే మొత్తం ఇంటర్నల్ సర్వర్లన్నీ సులభంగా హ్యాక్ అయిపోతాయి.",
        "explanation": "జీరో ట్రస్ట్ యొక్క మూల సూత్రం: 'Never Trust, Always Verify'. నెట్‌వర్క్ లొకేషన్‌తో (Corporate IP, VPN) సంబంధం లేదు. ప్రతి ఒక్క రిక్వెస్ట్ - అది బయటి నుండి వచ్చినా లేదా పక్కనే ఉన్న సర్వర్ నుండి వచ్చినా - మూడు విషయాలను ఖచ్చితంగా నిరూపించుకోవాలి: \n1. యూజర్ లేదా వర్క్‌లోడ్ ఎవరో నిరూపించే ఐడెంటిటీ (Mutual TLS / JWT). \n2. ఏ డివైస్ నుండి వస్తున్నారో ఆ డివైస్ హెల్త్/కంప్లయన్స్ చెక్. \n3. ఆ నిర్దిష్ట సమయంలో ఆ రిసోర్స్ యాక్సెస్ చేయడానికి లీస్ట్ ప్రివిలేజ్ పర్మిషన్ ఉందా లేదా అనే డైనమిక్ పాలసీ చెక్.",
        "example": """# Zero Trust పాలసీ ఎవాల్యుయేషన్ కాన్సెప్ట్
def evaluate_zero_trust_access(request):
    # 1. ఐడెంటిటీ చెక్ (Identity)
    if not verify_mtls_identity(request.client_cert):
        return "DENY: అపరిచిత క్లయింట్ ఐడెంటిటీ"
    # 2. డివైస్ పోశ్చర్ చెక్ (Device Compliance)
    if not request.device.is_disk_encrypted or not request.device.has_edr_agent:
        return "DENY: నాన్-కంప్లైంట్ డివైస్"
    # 3. కాంటెక్స్చువల్ రిస్క్ స్కోర్ (Risk & Location)
    if request.geo_ip.is_tor_or_vpn or request.anomaly_score > 0.7:
        return "STEP_UP_MFA: అదనపు వెరిఫికేషన్ అవసరం"
    return "ALLOW: ప్రాప్యత మంజూరు చేయబడింది" """,
        "mistake": "'మాది ప్రైవేట్ AWS VPC లోపల ఉంది కాబట్టి మైక్రోసర్వీసెస్ మధ్య ఆథెంటికేషన్ అక్కర్లేదు' అనుకోవడం; జీరో ట్రస్ట్‌లో VPC లోపల కూడా ప్రతి కమ్యూనికేషన్ mTLS తో ఎన్‌క్రిప్ట్ మరియు ఆథరైజ్ కావాలి."
    },
    {
        "title": "OAuth 2.1 (Modern OAuth Security Recommendations)",
        "subtitle": "OAuth 2.1 (పాత బలహీనమైన పద్ధతులను తీసేసి భద్రతను పటిష్టం చేసిన ఆధునిక స్టాండర్డ్)",
        "why": "పాత OAuth 2.0 లో ఉన్న Implicit Flow మరియు PKCE లేని ఆథరైజేషన్ కోడ్ ఫ్లో వల్ల బ్రౌజర్లలో టోకెన్లు దొంగిలించబడే ప్రమాదం ఉంది.",
        "explanation": "OAuth 2.1 అనేది సరికొత్త వెర్షన్ కాదు; ఇది గత 10 ఏళ్లలో వచ్చిన అత్యుత్తమ సెక్యూరిటీ ప్రాక్టీసుల ఏకీకరణ (Consolidation). ప్రధాన మార్పులు: \n1. Implicit Grant Flow పూర్తిగా రద్దు చేయబడింది (టోకెన్లు URL లో రాకూడదు). \n2. Resource Owner Password Credentials Grant (యూజర్‌నేమ్ పాస్‌వర్డ్ నేరుగా యాప్‌కి ఇవ్వడం) తొలగించబడింది. \n3. అన్ని రకాల క్లయింట్లకు (Single Page Apps, Mobile, Server-side) తప్పనిసరిగా PKCE (Proof Key for Code Exchange) వాడాలి. \n4. రీడైరెక్ట్ URI లు ఖచ్చితమైన మ్యాచ్ (Exact string matching) అయి ఉండాలి (వైల్డ్‌కార్డ్స్ నిషిద్ధం).",
        "example": """# PKCE (Proof Key for Code Exchange) ఫ్లో
import hashlib
import base64
import secrets

# 1. క్లయింట్ ఒక సీక్రెట్ కోడ్ వెరిఫైయర్ ని సృష్టిస్తుంది
code_verifier = secrets.token_urlsafe(64)

# 2. దాన్ని SHA256 హ్యాష్ చేసి Code Challenge గా ఆథరైజేషన్ సర్వర్‌కు పంపుతుంది
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).decode().rstrip("=")

print("Code Challenge (Login URL లో వెళ్లేది):", code_challenge)
# లాగిన్ అయిన తర్వాత ఆథరైజేషన్ కోడ్ మార్పిడికి code_verifier పంపాలి!""",
        "mistake": "React లేదా Vue SPA లలో యాక్సెస్ టోకెన్లను బ్రౌజర్ `localStorage` లో దాచడం; XSS దాడి జరిగితే టోకెన్ మొత్తం చోరీ అవుతుంది (HttpOnly SameSite కుకీలు వాడాలి)."
    },
    {
        "title": "Token Exchange (RFC 8693)",
        "subtitle": "టోకెన్ ఎక్స్ఛేంజ్ (మైక్రోసర్వీసెస్ చైన్‌లో యూజర్ ఐడెంటిటీని కోల్పోకుండా టోకెన్లను మార్చుకోవడం)",
        "why": "యూజర్ పంపిన పూర్తి అధికారాలున్న సూపర్ అడ్మిన్ JWT టోకెన్‌ను మైక్రోసర్వీస్ 1 నుండి 2, 3, 4 లకు అలాగే ఫార్వర్డ్ చేస్తే, డౌన్‌స్ట్రీమ్ చిన్న సర్వీస్ హ్యాక్ అయినా మొత్తం సిస్టమ్ రాజీపడుతుంది.",
        "explanation": "RFC 8693 స్టాండర్డ్ ప్రకారం ఒక మైక్రోసర్వీస్ తనకు అందిన ఒరిజినల్ టోకెన్‌ను ఆథరైజేషన్ సర్వర్ (Keycloak/Okta) కి ఇచ్చి, 'నా డౌన్‌స్ట్రీమ్ Inventory Service కోసం దానికి మాత్రమే సరిపోయే తక్కువ అధికారాలున్న (Downscoped / Audience-restricted) కొత్త టోకెన్ ఇవ్వండి' అని ఎక్స్ఛేంజ్ చేసుకుంటుంది. దీనివల్ల ప్రతీ సర్వీస్‌కు కేవలం దానికి అవసరమైన స్కోప్ మాత్రమే లభిస్తుంది (Principle of Least Privilege).",
        "example": """# RFC 8693 Token Exchange HTTP రిక్వెస్ట్
'''http
POST /token HTTP/1.1
Host: auth.company.com
Content-Type: application/x-www-form-urlencoded

grant_type=urn:ietf:params:oauth:grant-type:token-exchange
&subject_token=ORIGINAL_USER_JWT
&subject_token_type=urn:ietf:params:oauth:token-type:access_token
&audience=inventory-service
&scope=read:stock
''' 
# ఫలితంగా ఇన్వెంటరీ సర్వీస్ ఆడియన్స్ మాత్రమే ఉన్న సరికొత్త టోకెన్ లభిస్తుంది!""",
        "mistake": "ఒక సర్వీస్ నుండి మరొక సర్వీస్ కి కమ్యూనికేట్ చేయడానికి ఒరిజినల్ యూజర్ టోకెన్ ని గుడ్డిగా ఫార్వర్డ్ చేయడం లేదా గ్లోబల్ మాస్టర్ సర్వీస్ కీని వాడటం."
    },
    {
        "title": "DPoP (Demonstrating Proof-of-Possession)",
        "subtitle": "DPoP (దొంగిలించబడిన బేరర్ టోకెన్లను హ్యాకర్లు వాడకుండా అడ్డుకునే క్రిప్టోగ్రాఫిక్ కవచం)",
        "why": "సాంప్రదాయ Bearer Token అంటే కరెన్సీ నోటు లాంటిది; ఎవడు దొంగిలిస్తే వాడే దాన్ని ఖర్చు పెట్టేయవచ్చు. టోకెన్ చోరీ అయినా వేరొకరు వాడకుండా లాక్ చేయాలి.",
        "explanation": "RFC 9449 రూపొందించిన DPoP లో క్లయింట్ వద్ద ఒక ప్రైవేట్ కీ ఉంటుంది. క్లయింట్ API కి కాల్ చేసిన ప్రతిసారీ Bearer టోకెన్‌తో పాటు, ఆ నిర్దిష్ట రిక్వెస్ట్ URL మరియు HTTP Method పై తన ప్రైవేట్ కీతో డిజిటల్ సంతకం చేసి ఒక `DPoP` హెడర్‌ను పంపుతుంది. సర్వర్ ఆ సంతకాన్ని సరిచూస్తుంది. ఒకవేళ మధ్యలో హ్యాకర్ కేవలం యాక్సెస్ టోకెన్‌ను దొంగిలించినా, క్లయింట్ యొక్క ప్రైవేట్ కీ హ్యాకర్ వద్ద ఉండదు కాబట్టి ఆ టోకెన్ పూర్తిగా నిరుపయోగం అవుతుంది.",
        "example": """# DPoP హెడర్ తో API రిక్వెస్ట్ నిర్మాణం
# రిక్వెస్ట్ హెడర్స్:
# Authorization: DPoP <access_token>
# DPoP: <jwt_signed_with_client_private_key>
#
# DPoP JWT పేలోడ్:
# {
#   "jti": "random_unique_id",
#   "htm": "POST",
#   "htu": "https://api.example.com/checkout",
#   "iat": 1716902400
# }""",
        "mistake": "DPoP ప్రూఫ్స్ లో 'jti' (JWT ID) ని సర్వర్ సైడ్ క్యాష్ చేసి రీప్లే చెక్ చేయకపోవడం; రీప్లే ప్రొటెక్షన్ లేకపోతే మ్యాన్-ఇన్-ది-మిడిల్ అటాకర్ అదే రిక్వెస్ట్‌ను మళ్లీ పంపవచ్చు."
    },
    {
        "title": "Mutual TLS Authentication (mTLS Workload Identity)",
        "subtitle": "మ్యూచువల్ TLS (కేవలం క్లయింట్ మాత్రమే కాదు, సర్వర్ కూడా క్లయింట్ ఎవరో క్రిప్టోగ్రాఫిక్ సర్టిఫికెట్ తో వెరిఫై చేయడం)",
        "why": "సాధారణ HTTPS లో బ్రౌజర్ మాత్రమే సర్వర్ నిజమైనదో కాదో చెక్ చేస్తుంది. కానీ మైక్రోసర్వీసెస్ లో సర్వర్ కూడా క్లయింట్ నిజమైన 'Payment-Service' అవునా కాదా అని కచ్చితంగా ధృవీకరించాలి.",
        "explanation": "సాధారణ TLS లో వన్-వే ఆథెంటికేషన్ ఉంటుంది. mTLS లో టూ-వే (Two-way) హ్యాండ్‌షేక్ జరుగుతుంది. క్లయింట్ మరియు సర్వర్ రెండింటి వద్ద విశ్వసనీయ అంతర్గత CA (Certificate Authority) జారీ చేసిన X.509 డిజిటల్ సర్టిఫికెట్లు మరియు ప్రైవేట్ కీలు ఉంటాయి. TCP కనెక్షన్ ఏర్పడే క్షణంలోనే నెట్‌వర్క్ హార్డ్‌వేర్/కెర్నల్ లెవెల్‌లోనే రెండు సర్వీసులూ ఒకదాని సర్టిఫికెట్‌ను మరొకటి చెక్ చేసుకుంటాయి. నకిలీ సర్వీస్ ఏదైనా ప్రవేశిస్తే TCP కనెక్షనే ఓపెన్ అవ్వదు.",
        "example": """# Python Requests లో mTLS తో సర్వీస్ కాల్
import requests

response = requests.get(
    "https://internal-ledger.bank.local/accounts/1",
    cert=('/etc/certs/payment-client.crt', '/etc/certs/payment-client.key'), # మన సర్టిఫికెట్
    verify='/etc/certs/internal-ca-root.crt' # సర్వర్ ని నమ్మడానికి మన రూట్ CA
)
print("mTLS కనెక్షన్ సక్సెస్:", response.status_code)""",
        "mistake": "సర్టిఫికెట్ గడువు ముగింపు (Expiration) తేదీలను పర్యవేక్షించకపోవడం; ఒకేసారి సర్టిఫికెట్ expire అయితే అర్ధరాత్రి మొత్తం మైక్రోసర్వీసెస్ నెట్‌వర్క్ డెడ్ అయిపోతుంది."
    },
    {
        "title": "SPIFFE / SPIRE (Workload Identity Framework)",
        "subtitle": "స్పిఫీ / స్పైర్ (క్లౌడ్ మరియు కుబెర్‌నెటిస్ లో ప్రతి మైక్రోసర్వీస్ కు ఒక ఆధార్ కార్డు లాంటి క్రిప్టోగ్రాఫిక్ ఐడెంటిటీ ఇవ్వడం)",
        "why": "డైనమిక్ క్లౌడ్ వాతావరణంలో పాడ్స్ సెకన్లలో పుడుతుంటాయి, చస్తుంటాయి. వాటి IP అడ్రస్‌లు నిరంతరం మారుతుంటే వాటిని నమ్మడం ఎలా?",
        "explanation": "SPIFFE (Secure Production Identity Framework for Everyone) అనేది ఒక ఓపెన్ స్టాండర్డ్. ఇది ప్రతి వర్క్‌లోడ్‌కు ఒక యూనివర్సల్ URI ఐడెంటిటీని ఇస్తుంది (ఉదా: `spiffe://prod.internal/ns/finance/sa/payment-worker`). \nSPIRE అనేది దీని సాఫ్ట్‌వేర్ ఇంప్లిమెంటేషన్. ఇది కుబెర్‌నెటిస్ నోడ్ పై నడుస్తూ, ఆ పాడ్ యొక్క కర్నల్ సమాచారాన్ని (cgroups, namespace) పరిశీలించి దానికి ఆటోమేటిక్ గా షార్ట్-లైవ్డ్ (1 గంట గడువున్న) X.509 SVID సర్టిఫికెట్‌ను ఇంజెక్ట్ చేస్తుంది. సీక్రెట్స్ మరియు పాస్‌వర్డ్స్ తో పనిలేకుండా వర్క్‌లోడ్స్ పరస్పరం నమ్మకం ఏర్పరచుకుంటాయి.",
        "example": """# SPIFFE ID నిర్మాణం
# Format: spiffe://<trust-domain>/workload-path
#
# spiffe://bank.internal/billing/stripe-charge
# spiffe://bank.internal/audit/logger
#
# ఇవి X.509 సర్టిఫికెట్ లోని SAN (Subject Alternative Name) లో పొందుపరచబడతాయి.""",
        "mistake": "ట్రస్ట్ డొమైన్ (Trust Domain) బౌండరీలను సరిగ్గా డిజైన్ చేయకపోవడం; స్టేజింగ్ మరియు ప్రొడక్షన్ లకు వేర్వేరు ట్రస్ట్ డొమైన్స్ ఉండాలి."
    },
    {
        "title": "Fine-Grained Authorization (Resource & Action Level)",
        "subtitle": "ఫైన్-గ్రెయిన్డ్ ఆథరైజేషన్ (కేవలం 'Admin' కాకుండా 'యూజర్ 500 డాలర్ల లోపు సోమవారం మాత్రమే అప్రూవ్ చేయవచ్చు' అనే సూక్ష్మ అనుమతులు)",
        "why": "కేవలం 'User', 'Admin' అనే ముతక (Coarse-grained) రోల్స్ తో ఆధునిక బ్యాంకింగ్ లేదా హెల్త్‌కేర్ యాప్‌ల క్లిష్టమైన అనుమతులను నియంత్రించలేము.",
        "explanation": "Fine-Grained Authorization లో కేవలం రోల్ చూసి యాక్సెస్ ఇవ్వరు. యాక్సెస్ అడిగిన సమయం, రిసోర్స్ యజమాని ఎవరు, ఆ రిసోర్స్ ప్రస్తుతం ఏ స్థితిలో ఉంది (Draft vs Published), అడిగిన చర్య ఏమిటి (Read, Edit, Approve, Export) వంటి ప్రతి అంశాన్ని విశ్లేషిస్తారు. ఓపెన్ పాలసీ ఏజెంట్ (OPA) లేదా AWS Verified Permissions లాంటి డీకపుల్డ్ ఆథరైజేషన్ ఇంజిన్లు అప్లికేషన్ కోడ్ నుండి పాలసీలను వేరుచేసి మైక్రోసెకన్లలో నిర్ణయాలు ఇస్తాయి.",
        "example": """# Open Policy Agent (Rego) Fine-Grained పాలసీ
'''rego
package authz

default allow = false

# మెడికల్ రికార్డులను కేవలం ఆ పేషెంట్ అసైన్ చేసిన డాక్టర్ మాత్రమే ఎడిట్ చేయవచ్చు
allow {
    input.action == "EDIT"
    input.resource_type == "medical_record"
    input.user.role == "DOCTOR"
    input.user.id == input.resource.assigned_doctor_id
    not input.resource.is_archived
}
''' """,
        "mistake": "ఆథరైజేషన్ లాజిక్‌ను అప్లికేషన్ కోడ్‌లోని `if ($user->isAdmin())` కండిషన్లలో హార్డ్‌కోడ్ చేయడం; పాలసీలు మారినప్పుడల్లా కోడ్ రీడిప్లాయ్ చేయాల్సి వస్తుంది."
    },
    {
        "title": "ABAC / ReBAC (Attribute & Relationship-Based Access)",
        "subtitle": "ABAC / ReBAC (లక్షణాలు మరియు రిలేషన్‌షిప్‌ల ఆధారంగా అనుమతులను నిర్ణయించడం)",
        "why": "సాంప్రదాయ RBAC (Role-Based Access Control) లో కంపెనీ పెరిగేకొద్దీ వేలాది రోల్స్ పుట్టుకొచ్చి (Role Explosion) మేనేజ్ చేయడం అసాధ్యం అవుతుంది.",
        "explanation": "ABAC (Attribute-Based Access Control): యూజర్ లక్షణాలు (డిపార్ట్‌మెంట్, సెక్యూరిటీ క్లియరెన్స్), రిసోర్స్ లక్షణాలు (కాన్ఫిడెన్షియల్, కంట్రీ), ఎన్విరాన్‌మెంట్ లక్షణాలు (సమయం, లొకేషన్) కలిపి నియమాలు రాస్తారు. \nReBAC (Relationship-Based Access Control): Google Drive లేదా Facebook లో లాగా రిలేషన్‌షిప్స్ ఆధారంగా అనుమతులు వస్తాయి. ఉదాహరణకు: 'ఈ ఫైల్ ఉన్న ఫోల్డర్‌ను చూసే వ్యూయర్లకు ఈ ఫైల్ కూడా రీడ్-ఓన్లీ అవుతుంది' (Nested inheritance through graph traversal).",
        "example": """# ReBAC గ్రాఫ్ ఆధారిత రిలేషన్ షిప్ నిర్వచనం
# Document: Roadmap.pdf
# Folder: Engineering (Owner of Roadmap.pdf)
# Group: TechLeads (Member of Engineering)
# User: Naveen (Member of TechLeads)

# ReBAC ఇంజిన్ గ్రాఫ్ ట్రావర్స్ చేసి:
# Naveen -> TechLeads -> Engineering -> Roadmap.pdf
# కాబట్టి Naveen కి Roadmap.pdf పై స్వయంచాలకంగా View పర్మిషన్ లభిస్తుంది!""",
        "mistake": "ReBAC కోసం లోతైన గ్రాఫ్ క్వెరీలను సాధారణ MySQL లో సెల్ఫ్-జాయిన్స్ తో చేయడం; నెస్టెడ్ గ్రూపులు పెరిగేకొద్దీ క్వెరీలు అత్యంత నెమ్మదిస్తాయి."
    },
    {
        "title": "Zanzibar Authorization Model (Google Zanzibar)",
        "subtitle": "జాంజిబార్ ఆథరైజేషన్ మోడల్ (బిలియన్ల కొద్దీ యూజర్లకు రిలేషన్‌షిప్ పర్మిషన్లను మైక్రోసెకన్లలో అందించే గూగుల్ ఆర్కిటెక్చర్)",
        "why": "Google Drive, YouTube, Google Cloud లలో బిలియన్ల కొద్దీ డాక్యుమెంట్లు మరియు వీడియోల పర్మిషన్లను 10 మిల్లీసెకన్ల లోపు 99.999% లభ్యతతో చెక్ చేయాలి.",
        "explanation": "గూగుల్ 2019 లో ప్రచురించిన వైట్ పేపర్ ఆధారంగా రూపొందిన ఆర్కిటెక్చర్ ఇది (ఓపెన్ సోర్స్ ప్రత్యామ్నాయాలు: Ory Keto, OpenFGA, Auth0 Fine-Grained Authorization). ఇది మొత్తం ప్రపంచ అనుమతులను సరళమైన టపుల్స్ గా (Relation Tuples: `object#relation@user`) స్టోర్ చేస్తుంది. ఉదా: `doc:101#viewer@user:kiran`. 'Zookies' అనే కన్సిస్టెన్సీ టోకెన్ల ద్వారా డేటాబేస్ రెప్లికాస్ నుండి చదివేటప్పుడు పాత అనుమతులు రాకుండా 'New Enemy Problem' ను అద్భుతంగా నివారిస్తుంది.",
        "example": """# OpenFGA / Zanzibar టపుల్ ఉదాహరణ
# "user:naveen is an editor of document:design-doc"
[
    {"user": "user:naveen", "relation": "editor", "object": "document:design-doc"},
    {"user": "document:design-doc#editor", "relation": "viewer", "object": "document:design-doc"}
]
# చెక్ క్వెరీ:
# check(user=user:naveen, relation=viewer, object=document:design-doc) -> ALLOWED!""",
        "mistake": "New Enemy Problem ని పట్టించుకోకపోవడం: పర్మిషన్ రద్దు చేయబడిన యూజర్, రెప్లికేషన్ లాగ్ వల్ల కొన్ని సెకన్ల పాటు పాత రీడ్ రెప్లికా నుండి సీక్రెట్ డాక్యుమెంట్‌ను చూడగలగడం."
    },
    {
        "title": "Capability-Based Security (Unforgeable Access Capabilities)",
        "subtitle": "కెపాసిబిలిటీ-బేస్డ్ సెక్యూరిటీ (యాక్సెస్ కంట్రోల్ లిస్ట్ కాకుండా చేతిలో ఉన్న ప్రత్యేకమైన టిక్కెట్ ఆధారంగా అధికారం)",
        "why": "సెంట్రల్ ACL డేటాబేస్‌ను ప్రతిసారీ క్వెరీ చేయకుండా, సురక్షితమైన టోకెన్ ద్వారా క్లయింట్ తనకు ఇచ్చిన పరిమిత పనిని మాత్రమే చేసేలా చూడటం.",
        "explanation": "సాధారణ ACL లో హోటల్ మేనేజర్ దగ్గర లిస్ట్ ఉంటుంది (నీ పేరు లిస్ట్‌లో ఉంటేనే లోపలికి రానిస్తాడు). Capability Security లో హోటల్ రూమ్ కీ-కార్డ్ లాంటిది. కీ ఎవరి చేతిలో ఉంటే వారే గది తెరుస్తారు; మేనేజర్‌ను అడగాల్సిన పనిలేదు. AWS S3 Presigned URLs దీనికి అత్యుత్తమ ఉదాహరణ. మీ బ్యాకెండ్ సర్వర్ ఒక క్రిప్టోగ్రాఫిక్ సిగ్నేచర్‌తో కూడిన URL ను క్రియేట్ చేసి యూజర్‌కు ఇస్తుంది. యూజర్ నేరుగా ఆ URL తో నిర్దిష్ట ఫైల్‌ను మాత్రమే 15 నిమిషాల పాటు అప్‌లోడ్ లేదా డౌన్‌లోడ్ చేసుకోగలడు.",
        "example": """# S3 Presigned URL - కెపాసిబిలిటీ సెక్యూరిటీ ఉదాహరణ
import boto3

s3 = boto3.client('s3')
# ఈ లింక్ ఉన్న ఎవరైనా కేవలం ఈ ఒక్క ఫైల్ ను మాత్రమే 10 నిమిషాలు డౌన్‌లోడ్ చేయగలరు
presigned_url = s3.generate_presigned_url(
    'get_object',
    Params={'Bucket': 'confidential-invoices', 'Key': 'inv_2026_11.pdf'},
    ExpiresIn=600
)
print("డౌన్‌లోడ్ కెపాసిబిలిటీ URL:", presigned_url)""",
        "mistake": "కెపాసిబిలిటీ టోకెన్ లేదా URL కి ఎక్కువ ఎక్స్‌పైరీ సమయం (ఉదా: 7 రోజులు) ఇవ్వడం; అది ఎవరి చేతికి చిక్కినా దుర్వినియోగం అవుతుంది కాబట్టి కొద్ది నిమిషాల గడువు మాత్రమే ఉండాలి."
    },
    {
        "title": "Certificate Rotation (Automated Certificate Lifecycle)",
        "subtitle": "సర్టిఫికెట్ రొటేషన్ (మానవ ప్రమేయం లేకుండా TLS సర్టిఫికెట్లను ఆటోమేటిక్‌గా రీన్యూ చేయడం)",
        "why": "ప్రపంచవ్యాప్తంగా జరిగే 80% మేజర్ అవుటేజ్‌లకు ప్రధాన కారణం: ఎవరో ఒక ఇంజనీర్ సర్టిఫికెట్ ఎక్స్‌పైరీ డేట్ గుర్తుపెట్టుకోకపోవడం మరియు సమయానికి మాన్యువల్ గా రీన్యూ చేయకపోవడం.",
        "explanation": "ఆధునిక ఆర్కిటెక్చర్‌లో సర్టిఫికెట్లు ఎక్కువ కాలం (1 సంవత్సరం) ఉండకూడదు; అవి కేవలం 30 నుండి 90 రోజులు మాత్రమే ఉండాలి. Kubernetes లో `cert-manager` డెమోన్ ACME ప్రోటోకాల్ (Let's Encrypt / HashiCorp Vault) తో అనుసంధానించబడి ఉంటుంది. సర్టిఫికెట్ గడువు ముగియడానికి 30 రోజుల ముందే అది ఆటోమేటిక్ గా కొత్త కీ పెయిర్ ను జనరేట్ చేసి, ఛాలెంజ్ పూర్తి చేసి, రహస్యంగా పోడ్స్ రీస్టార్ట్ లేకుండా ఇన్-మెమరీ సర్టిఫికెట్‌ను రీలోడ్ చేస్తుంది.",
        "example": """# Kubernetes cert-manager Issuer కాన్ఫిగరేషన్
'''yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: api-tls-cert
spec:
  secretName: api-tls-secret
  duration: 2160h # 90 రోజులు
  renewBefore: 720h # 30 రోజుల ముందే ఆటో-రొటేట్ అవ్వాలి
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  dnsNames:
  - api.mynests.com
''' """,
        "mistake": "సర్టిఫికెట్ ఫైల్ మారినప్పుడు వెబ్ సర్వర్ (Nginx/Envoy) కి `reload` సిగ్నల్ ఇవ్వకపోవడం; డిస్క్ లో కొత్త ఫైల్ ఉన్నా మెమరీలో పాత ఎక్స్‌పైర్డ్ సర్టిఫికెట్ రన్ అవుతూనే ఉంటుంది."
    },
    {
        "title": "Secret Zero Problem (Initial Secret Bootstrap)",
        "subtitle": "సీక్రెట్ జీరో సమస్య (రహస్యాలను దాచే లాకర్ తాళంచెవిని ఎక్కడ దాచాలి అనే ప్రారంభ చిక్కుముడి)",
        "why": "డేటాబేస్ పాస్‌వర్డ్‌లను Vault లో దాచాం బానే ఉంది; కానీ ఆ Vault ను తెరవడానికి సర్వర్‌కు కావాల్సిన 'మొదటి పాస్‌వర్డ్' (Secret Zero) ని ఎక్కడ దాచాలి?",
        "explanation": "సర్వర్ కోడ్ లో లేదా కాన్ఫిగ్ ఫైల్ లో ఏ ఒక్క సీక్రెట్ ని కూడా హార్డ్‌కోడ్ చేయకూడదు. ఈ సమస్యను పరిష్కరించడానికి క్లౌడ్ ప్రొవైడర్ హార్డ్‌వేర్ ఐడెంటిటీని వాడుతారు. ఉదాహరణకు AWS EC2 / EKS లోని IAM Roles (Instance Metadata Service - IMDSv2). మీ వర్క్‌లోడ్ రన్ అయ్యే వర్చువల్ మెషీన్ యొక్క హైపర్‌వైజర్ ఆటోమేటిక్ గా తాత్కాలిక టోకెన్ ఇస్తుంది. HashiCorp Vault ఆ AWS మెటాడేటాను వెరిఫై చేసి, ఆ మెషీన్‌కు సీక్రెట్లను యాక్సెస్ చేసే తాత్కాలిక అనుమతిని మంజూరు చేస్తుంది. ఎక్కడా హార్డ్‌కోడెడ్ సీక్రెట్ ఉండదు.",
        "example": """# AWS IAM Role ఆధారంగా Vault లాగిన్ (No Hardcoded Secrets!)
import hvac
import requests

# 1. AWS EC2 Instance Metadata నుండి తాత్కాలిక సిగ్నేచర్ పొందడం
# 2. ఆ సిగ్నేచర్‌తో Vault లోకి లాగిన్ అవ్వడం
client = hvac.Client(url='https://vault.internal:8200')
client.auth.aws.iam_login(
    access_key="DYNAMIC_TEMP_KEY",
    secret_key="DYNAMIC_TEMP_SECRET",
    session_token="TEMP_TOKEN",
    role="order-service-role"
)
# ఇప్పుడు మనం సురక్షితంగా డేటాబేస్ సీక్రెట్లను పొందవచ్చు!
db_secret = client.secrets.kv.v2.read_secret_version(path='database/creds')""",
        "mistake": "సీక్రెట్ జీరో ని తప్పించుకోవడానికి `.env` ఫైల్స్ ని లేదా ప్రైవేట్ కీలను గిట్‌హబ్ రిపోజిటరీలలో కమిట్ చేయడం."
    },
    {
        "title": "Envelope Encryption (DEK & KEK Hierarchy)",
        "subtitle": "ఎన్వలప్ ఎన్‌క్రిప్షన్ (ఉత్తరాన్ని కవర్‌లో పెట్టి, కవర్‌ను బీరువా తాళంతో భద్రపరిచే రెండు అంచెల ఎన్‌క్రిప్షన్)",
        "why": "100GB డేటాను ఎన్‌క్రిప్ట్ చేయడానికి నేరుగా AWS KMS ని పిలిస్తే నెట్‌వర్క్ నెమ్మదిస్తుంది మరియు KMS ఏపీఐ బిల్లు లక్షల్లోకి వెళ్తుంది.",
        "explanation": "Envelope Encryption లో రెండు తాళంచెవులు ఉంటాయి: \n1. Data Encryption Key (DEK): ఒక లోకల్ వేగవంతమైన సిమెట్రిక్ కీ (AES-256). దీనితో పెద్ద మొత్తంలో ఉన్న డేటాను లోకల్ మెమరీలోనే మెరుపు వేగంతో ఎన్‌క్రిప్ట్ చేస్తారు. \n2. Key Encryption Key (KEK / Master Key): ఇది AWS KMS లేదా HSM హార్డ్‌వేర్ లోపల శాశ్వతంగా భద్రంగా ఉంటుంది. \nడేటా ఎన్‌క్రిప్ట్ అయిన వెంటనే, ఆ DEK కీని KEK తో ఎన్‌క్రిప్ట్ చేసి, ఆ ఎన్‌క్రిప్టెడ్ DEK ని ఎన్‌క్రిప్ట్ అయిన డేటా పక్కనే భద్రపరుస్తారు (ఎన్వలప్ లాగా). మెమరీ లోని ప్లెయిన్ DEK ని వెంటనే తుడిచివేస్తారు.",
        "example": """# Envelope Encryption కాన్సెప్ట్ ఫ్లో
# 1. AWS KMS ని అడగండి: "నాకు ఒక DEK ఇవ్వండి"
# KMS రెండు ఇస్తుంది:
#    a) Plaintext DEK (RAM లో డేటా ఎన్‌క్రిప్ట్ చేయడానికి)
#    b) Encrypted DEK (డిస్క్ లో దాచడానికి)

# 2. Plaintext DEK తో మీ 1GB ఫైల్ ని AES తో ఎన్‌క్రిప్ట్ చేయండి.
# 3. RAM నుండి Plaintext DEK ని వెంటనే తుడిచివేయండి (del plaintext_dek).
# 4. Encrypted File + Encrypted DEK రెండింటినీ S3 లో సేవ్ చేయండి. సురక్షితం!""",
        "mistake": "డేటా ఎన్‌క్రిప్ట్ చేసిన తర్వాత కూడా Plaintext DEK ని మెమరీ నుండి ఫ్రీ చేయకుండా లాగ్స్ లో ప్రింట్ చేయడం."
    },
    {
        "title": "KMS / HSM (Key Management & Hardware Security Modules)",
        "subtitle": "KMS / HSM (క్రిప్టోగ్రాఫిక్ కీలు ఎప్పటికీ బయటకు రాని అత్యంత సురక్షితమైన హార్డ్‌వేర్ చిప్స్)",
        "why": "సర్వర్ ఆపరేటింగ్ సిస్టమ్ హ్యాక్ అయినా లేదా రూట్ పాస్‌వర్డ్ దొంగిలించబడినా, ఎన్‌క్రిప్షన్ మాస్టర్ కీలను హ్యాకర్లు కాపీ చేయలేరు.",
        "explanation": "HSM (Hardware Security Module) అనేది FIPS 140-2 Level 3 సర్టిఫైడ్ ప్రత్యేక హార్డ్‌వేర్ అప్లయెన్స్. ఎవరైనా సర్వర్‌ను భౌతికంగా తెరిచి చిప్‌ను తాకడానికి ప్రయత్నించినా అది సెల్ఫ్-డిస్ట్రక్ట్ అయ్యి కీలను తుడిచివేస్తుంది. మాస్టర్ ప్రైవేట్ కీ ఎప్పటికీ ఆ HSM చిప్ నుండి బయటకు రాదు. మీరు డేటాను చిప్ లోపలికి పంపితే అది లోపలే సంతకం లేదా ఎన్‌క్రిప్షన్ చేసి ఫలితాన్ని మాత్రమే బయటకు ఇస్తుంది. AWS KMS, Google Cloud KMS లు తెరవెనుక ఈ డెడికేటెడ్ HSM క్లస్టర్ల పైనే పనిచేస్తాయి.",
        "example": """# AWS KMS ద్వారా డేటా సంతకం (కీ ఎప్పటికీ బయటకు రాదు)
import boto3

kms = boto3.client('kms')
response = kms.sign(
    KeyId='alias/financial-signing-key', # HSM లోపల ఉన్న కీ
    Message=b'Approved Transaction $500,000',
    MessageType='RAW',
    SigningAlgorithm='RSASSA_PKCS1_V1_5_SHA_256'
)
# సంతకం KMS హార్డ్‌వేర్ లోపలే జరిగి వచ్చింది!
signature = response['Signature']""",
        "mistake": "ప్రైవేట్ కీలను అప్లికేషన్ సర్వర్ ఫైల్ సిస్టమ్‌లో `.pem` ఫైల్స్ గా స్టోర్ చేయడం; సర్వర్ పై RCE దాడి జరిగితే కీలు దొంగిలించబడతాయి."
    },
    {
        "title": "Software Supply Chain Security (SBOM, SLSA, Sigstore)",
        "subtitle": "సాఫ్ట్‌వేర్ సప్లై చైన్ సెక్యూరిటీ (మీ కోడ్ లో వాడే ఓపెన్ సోర్స్ ప్యాకేజీలు హ్యాక్ కాకుండా కాపాడటం)",
        "why": "మీరు సొంతంగా రాసిన కోడ్ 100% సేఫ్ కావచ్చు; కానీ `composer require` లేదా `npm install` చేసినప్పుడు ఒక థర్డ్-పార్టీ లైబ్రరీ ద్వారా మాల్వేర్ మీ సర్వర్ లోకి ప్రవేశించవచ్చు (SolarWinds, Log4j, XZ Utils తరహా దాడులు).",
        "explanation": "ఆధునిక ఎంటర్‌ప్రైజ్ సెక్యూరిటీలో మూడు పిల్లర్స్ ఉంటాయి: \n1. SBOM (Software Bill of Materials): మీ అప్లికేషన్‌లో వాడిన ప్రతి చిన్న లైబ్రరీ, వెర్షన్, లైసెన్స్ వివరాల డిజిటల్ లిస్ట్ (CycloneDX / SPDX ఫార్మాట్). \n2. SLSA (Supply-chain Levels for Software Artifacts): కోడ్ కమిట్ నుండి ప్రొడక్షన్ బైనరీ వరకు ప్రతి దశ ట్యాంపర్-ప్రూఫ్ గా జరిగిందని ఇచ్చే గ్యారెంటీ. \n3. Sigstore / Cosign: ప్రొడక్షన్ లోకి వెళ్లే ప్రతి డాకర్ ఇమేజ్ పై CI/CD పైప్‌లైన్ లో క్రిప్టోగ్రాఫిక్ డిజిటల్ సంతకం చేసి, కుబెర్‌నెటిస్ లో అడ్మిషన్ కంట్రోలర్ ద్వారా ధృవీకరించిన తర్వాతే రన్ చేయడం.",
        "example": """# Cosign తో డాకర్ ఇమేజ్ సంతకం & వెరిఫికేషన్
'''bash
# 1. CI/CD లో డాకర్ ఇమేజ్ పై డిజిటల్ సంతకం చేయడం
cosign sign --key k8s://cosign-keys/my-key myregistry.com/order-api:v1.0

# 2. కుబెర్‌నెటిస్ క్లస్టర్ లో ఆ ఇమేజ్ వెరిఫై అయితేనే రన్ చేయడం
cosign verify --key k8s://cosign-keys/my-key.pub myregistry.com/order-api:v1.0
''' """,
        "mistake": "డాకర్ ఫైల్స్ లో ఇమేజ్ టాగ్ లను `image:latest` అని వాడటం; లేటెస్ట్ టాగ్ మారే అవకాశం ఉంది కాబట్టి ఖచ్చితమైన SHA256 డైజెస్ట్ (`image@sha256:...`) మాత్రమే వాడాలి."
    },
    {
        "title": "Confidential Computing (Protecting Data in Use)",
        "subtitle": "కాన్ఫిడెన్షియల్ కంప్యూటింగ్ (డేటా RAM లో ప్రాసెస్ అవుతున్నప్పుడు కూడా క్లౌడ్ అడ్మిన్లు లేదా హ్యాకర్లు చూడకుండా ఎన్‌క్రిప్ట్ చేయడం)",
        "why": "డేటా డిస్క్ లో ఉన్నప్పుడు (At Rest) ఎన్‌క్రిప్ట్ చేశాం, నెట్‌వర్క్ లో వెళ్తున్నప్పుడు (In Transit) TLS పెట్టాం; కానీ CPU మరియు RAM లో ఎగ్జిక్యూట్ అవుతున్నప్పుడు (In Use) క్లౌడ్ ప్రొవైడర్ ఇంజనీర్లు లేదా మెమరీ డంప్ హ్యాకర్లు దాన్ని చదవగలరు.",
        "explanation": "హార్డ్‌వేర్ ఆధారిత Trusted Execution Environments (TEEs - AMD SEV-SNP, Intel SGX, AWS Nitro Enclaves) దీనికి పరిష్కారం. ఇవి CPU చిప్ లెవెల్‌లోనే ఒక సురక్షితమైన ఎన్‌క్లేవ్ (Hardware isolated enclave) ను సృష్టిస్తాయి. ఆ ఎన్‌క్లేవ్ మెమరీ మొత్తం డైనమిక్ హార్డ్‌వేర్ కీలతో ఎన్‌క్రిప్ట్ అయి ఉంటుంది. సర్వర్‌ను నడుపుతున్న హైపర్‌వైజర్, లైనక్స్ రూట్ యూజర్ లేదా క్లౌడ్ ప్రొవైడర్ స్వయంగా మెమరీని డంప్ చేసినా కేవలం చెత్త (Ciphertext) మాత్రమే కనిపిస్తుంది. అత్యంత సున్నితమైన AI మోడల్స్, హెల్త్‌కేర్ డేటా ప్రాసెసింగ్ కు ఇది ముఖ్యం.",
        "example": """# Confidential Computing ఎన్‌క్లేవ్ భావన
# Regular App:
# App Code & Memory -> OS Kernel & Hypervisor can read everything!

# Confidential Computing (AWS Nitro Enclaves / AMD SEV):
# [Secure CPU Enclave] -> Memory is encrypted in silicon hardware!
# Hypervisor / Root OS has NO ACCESS to memory encryption keys.
# రిమోట్ అటెస్టేషన్ (Remote Attestation) ద్వారా కోడ్ ట్యాంపర్ కాలేదని నిరూపిస్తుంది.""",
        "mistake": "సాధారణ డాకర్ కంటైనర్ ఐసోలేషన్‌ను కాన్ఫిడెన్షియల్ కంప్యూటింగ్ అనుకోవడం; సాధారణ లైనక్స్ కంటైనర్లను హోస్ట్ రూట్ యూజర్ సులభంగా మెమరీ ఇన్‌స్పెక్ట్ చేయగలడు."
    }
]
