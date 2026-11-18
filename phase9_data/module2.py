# Module 2: Advanced Microservices & Architecture Patterns (16 topics)

topics = [
    {
        "title": "Cell-Based Architecture (Failure Blast Radius Reduction)",
        "subtitle": "సెల్-బేస్డ్ ఆర్కిటెక్చర్ (ఒక ప్రాంతంలో సమస్య వస్తే మొత్తం సిస్టమ్ ఆగిపోకుండా సెల్స్ గా విభజించడం)",
        "why": "ఒక పెద్ద మైక్రోసర్వీసెస్ సిస్టమ్‌లో డేటాబేస్ లేదా సర్వీస్ డౌన్ అయితే ప్రపంచవ్యాప్తంగా ఉన్న లక్షల మంది యూజర్లందరికీ ఒకేసారి సర్వీస్ ఆగిపోకూడదు (Blast radius నియంత్రణ).",
        "explanation": "AWS, Uber, Slack లు ఈ విధానాన్ని పాటిస్తాయి. పూర్తి అప్లికేషన్ స్టాక్‌ను (APIs, Database, Caches, Queues) చిన్న చిన్న స్వతంత్ర 'Cells' గా నకిలీ చేస్తారు. ఉదాహరణకు, యూజర్ ఐడీల ఆధారంగా Cell 1 (యూజర్లు 1-1M), Cell 2 (యూజర్లు 1M-2M) గా విడదీస్తారు. ఒక రూటర్ ట్రాఫిక్‌ను సరైన సెల్‌కి మళ్లిస్తుంది. Cell 2 లోని డేటాబేస్ క్రాష్ అయినా కేవలం ఆ 1M యూజర్లకు మాత్రమే అంతరాయం కలుగుతుంది; మిగిలిన ప్రపంచమంతా ఏ సమస్యా లేకుండా పనిచేస్తుంది.",
        "example": """# Cell Router ట్రాఫిక్ డైరెక్షన్ లాజిక్
class CellRouter:
    def __init__(self, cell_endpoints):
        self.cells = cell_endpoints

    def route_request(self, user_id):
        # User ID ని హ్యాష్ చేసి తగిన సెల్‌కి పంపడం
        cell_index = hash(user_id) % len(self.cells)
        target_cell = self.cells[cell_index]
        return f"User {user_id} రిక్వెస్ట్ Cell: {target_cell} కి పంపబడింది"

router = CellRouter(["cell-us-east-1a", "cell-us-east-1b", "cell-us-east-1c"])
print(router.route_request("user_9845"))
print(router.route_request("user_1204"))""",
        "mistake": "సెల్స్ మధ్య క్రాస్-సెల్ కమ్యూనికేషన్ (Cross-cell calls) ఎక్కువగా జరిగితే Blast Radius పెరుగుతుంది; సెల్స్ ఎల్లప్పుడూ వీలైనంత వరకు పూర్తి స్వతంత్రంగా ఉండాలి."
    },
    {
        "title": "Bulkhead Isolation (Resource Isolation)",
        "subtitle": "బల్క్‌హెడ్ ఐసోలేషన్ (ఓడలోని గదుల విభజన లాగా ఒక సర్వీస్ వైఫల్యం ఇతర సర్వీసులను ముంచకుండా కాపాడటం)",
        "why": "ఒక నాన్-క్రిటికల్ సర్వీస్ (ఉదా: PDF Report Generator) నెమ్మదిస్తే, అది మొత్తం సర్వర్ థ్రెడ్స్ మరియు డేటాబేస్ కనెక్షన్లను తినేసి, ప్రధానమైన లాగిన్ లేదా పేమెంట్ సర్వీసులను కూడా డౌన్ చేయకుండా చూడాలి.",
        "explanation": "ఓడ అడుగుభాగంలో నీరు చేరినప్పుడు మొత్తం ఓడ మునిగిపోకుండా లోపల పలు విభాగాలుగా (Bulkheads) ఉక్కు గోడలతో వేరుచేస్తారు. సాఫ్ట్‌వేర్‌లో కూడా అదే సూత్రం. Laravel/PHP లో ఒకే PHP-FPM పూల్ లేదా ఒకే Database Connection Pool ను అన్నిటికీ వాడకుండా, విమర్శనాత్మక పేమెంట్స్‌కు ప్రత్యేక DB Pool (10 కనెక్షన్లు), రిపోర్ట్ జనరేషన్‌కు వేరే DB Pool (3 కనెక్షన్లు) పెడతారు. రిపోర్ట్ సర్వీస్ హ్యాంగ్ అయినా పేమెంట్స్ పూల్ సురక్షితంగా ఉంటుంది.",
        "example": """# Thread Pool Bulkhead Isolation
from concurrent.futures import ThreadPoolExecutor

# వేర్వేరు సర్వీసులకు ప్రత్యేక థ్రెడ్ పూల్స్ కేటాయించడం
payment_pool = ThreadPoolExecutor(max_workers=10, thread_name_prefix="Payment")
analytics_pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix="Analytics")

def process_payment(order_id):
    return payment_pool.submit(lambda: f"Payment Processed for {order_id}")

def generate_report():
    # ఇది స్లో అయినా Payment Pool కి ఎటువంటి ఆటంకం కలగదు
    return analytics_pool.submit(lambda: "Long Report Generated")""",
        "mistake": "అన్ని రకాల బాహ్య API కాలింగ్స్‌కు ఒకే గ్లోబల్ HTTP Client పూల్ వాడటం; థర్డ్ పార్టీ పేమెంట్ గేట్‌వే నెమ్మదిస్తే మొత్తం అప్లికేషన్ థ్రెడ్స్ అయిపోతాయి."
    },
    {
        "title": "Strangler Fig Pattern (Legacy Modernization)",
        "subtitle": "స్ట్రాంగ్లర్ ఫిగ్ ప్యాటర్న్ (పాత మోనోలిత్ కోడ్‌ను ఒక్కసారే కాకుండా క్రమంగా కొత్త మైక్రోసర్వీసెస్‌గా మార్చడం)",
        "why": "15 ఏళ్ల నాటి భారీ లెగసీ PHP మోనోలిత్‌ను స్క్రాచ్ నుండి మళ్లీ రాసి ఒకేసారి రిలీజ్ (Big Bang rewrite) చేస్తే 80% ప్రాజెక్ట్‌లు ఫెయిల్ అవుతాయి. వ్యాపారం ఆగకుండా దశలవారీగా ఆధునీకరించాలి.",
        "explanation": "స్ట్రాంగ్లర్ అత్తి చెట్టు ఒక పాత చెట్టుపై మొలకెత్తి క్రమంగా దాని చుట్టూ పెరిగి చివరకు పాత చెట్టును పూర్తిగా భర్తీ చేస్తుంది. అదేవిధంగా, మోనోలిత్ ముందు ఒక API Gateway (Nginx లేదా Kong) పెడతారు. కొత్త ఫీచర్లను కొత్త మైక్రోసర్వీస్‌లో రాస్తారు. పాత ఫీచర్లను ఒక్కొక్కటిగా కొత్త సర్వీస్‌లోకి మైగ్రేట్ చేసి, గేట్‌వేలో రూటింగ్‌ను పాత మోనోలిత్ నుండి కొత్త సర్వీస్‌కు మళ్లిస్తారు. చివరికి పాత మోనోలిత్‌లో ఏమీ మిగలనప్పుడు దాన్ని డీకమిషన్ చేస్తారు.",
        "example": """# Nginx రివర్స్ ప్రాక్సీ కాన్ఫిగరేషన్ (Strangler Fig)
# /api/v2/orders కొత్త మైక్రోసర్వీస్ కి వెళ్తుంది
# మిగిలిన పాత ట్రాఫిక్ అంతా పాత PHP మోనోలిత్ కి వెళ్తుంది
'''
location /api/v2/orders {
    proxy_pass http://new-order-microservice:8080;
}

location / {
    proxy_pass http://legacy-php-monolith:80;
}
''' """,
        "mistake": "డేటాబేస్ మైగ్రేషన్‌ను ప్లాన్ చేయకుండా కేవలం API ఎండ్‌పాయింట్లను మాత్రమే మార్చడం; డేటా మోడల్ సింక్రొనైజేషన్ ముందే చేయకపోతే డేటా అసమానతలు వస్తాయి."
    },
    {
        "title": "Anti-Corruption Layer (Domain Protection)",
        "subtitle": "యాంటీ-కరప్షన్ లేయర్ (లెగసీ లేదా బయటి సిస్టమ్స్ చెత్త డేటా మోడల్స్ కొత్త మైక్రోసర్వీస్ డొమైన్‌ను కలుషితం చేయకుండా అడ్డుగోడ)",
        "why": "పాత 15 ఏళ్ల లెగసీ సిస్టమ్ లేదా క్లిష్టమైన థర్డ్ పార్టీ ERP (SAP) డేటా మోడల్స్ చాలా అస్తవ్యస్తంగా ఉంటాయి. వాటిని నేరుగా మీ సరికొత్త Clean Architecture మైక్రోసర్వీస్‌లో వాడితే మీ కొత్త కోడ్ కూడా కలుషితం అవుతుంది.",
        "explanation": "రెండు విభిన్న బౌండెడ్ కాంటెక్స్ట్‌ల (Bounded Contexts) మధ్య ఒక అడాప్టర్ లేదా ట్రాన్స్‌లేటర్ లాంటి Anti-Corruption Layer (ACL) ని నిర్మిస్తారు. లెగసీ సిస్టమ్ ఇచ్చే వింత కాలమ్ పేర్లను (ఉదా: `CUST_DTL_01_X`), మీ కొత్త సిస్టమ్ అర్థం చేసుకునే అందమైన డొమైన్ ఎంటిటీలుగా (`CustomerProfile`) ఈ లేయర్ మారుస్తుంది. దీంతో రేపు లెగసీ సిస్టమ్ మారినా మీ కోర్ డొమైన్ లాజిక్ మారదు.",
        "example": """# Anti-Corruption Layer (ACL) Adapter
class LegacySAPClient:
    def fetch_raw_user(self, sap_id):
        # పాత క్రూరమైన ఫార్మాట్
        return {"USR_ID_RAW": sap_id, "TXT_NM": "Naveen", "FLG_ACT": "Y"}

class UserAntiCorruptionLayer:
    def __init__(self, sap_client):
        self.sap = sap_client

    def get_clean_user(self, user_id):
        raw = self.sap.fetch_raw_user(user_id)
        # మన సరికొత్త Clean Domain Model లోకి మార్చడం
        return {
            "id": raw["USR_ID_RAW"],
            "name": raw["TXT_NM"],
            "is_active": raw["FLG_ACT"] == "Y"
        }

acl = UserAntiCorruptionLayer(LegacySAPClient())
print(acl.get_clean_user("SAP_9921"))""",
        "mistake": "ACL లో వ్యాపార లాజిక్ (Business Rules) రాయడం; ACL కేవలం డేటా ట్రాన్స్‌లేషన్ మరియు ప్రొటోకాల్ అడాప్టేషన్ మాత్రమే చేయాలి."
    },
    {
        "title": "Backend for Frontend (BFF)",
        "subtitle": "బ్యాకెండ్ ఫర్ ఫ్రంటెండ్ (మొబైల్, వెబ్, ఐఓటీ క్లయింట్ల అవసరాలకు తగిన ప్రత్యేక బ్యాకెండ్ లేయర్)",
        "why": "మొబైల్ యాప్‌కు తక్కువ డేటా మరియు తక్కువ బ్యాండ్‌విడ్త్ కావాలి; వెబ్ డెస్క్‌టాప్ డాష్‌బోర్డ్‌కు విస్తృతమైన చార్ట్స్ మరియు పెద్ద టేబుల్స్ కావాలి. ఒకే భారీ జెనరిక్ API రాస్తే మొబైల్‌లో అనవసరమైన ఓవర్‌హెడ్ పెరుగుతుంది.",
        "explanation": "సాంప్రదాయకంగా ఒకే API గేట్‌వే అన్ని డివైసెస్‌కి సర్వ్ చేస్తుంది. కానీ BFF ప్యాటర్న్‌లో Mobile App కోసం ప్రత్యేకంగా ఒక Node.js/FastAPI BFF సర్వీస్, Web App కోసం మరో BFF సర్వీస్ పెడతారు. మొబైల్ BFF బ్యాకెండ్ మైక్రోసర్వీసెస్ నుండి 5 వేర్వేరు కాల్స్ చేసి డేటాను కుదించి ఒకే చిన్న JSON గా మొబైల్ స్క్రీన్‌కు పంపుతుంది. నెట్‌వర్క్ రౌండ్‌ట్రిప్స్ తగ్గి యాప్ వేగం విపరీతంగా పెరుగుతుంది.",
        "example": """# Mobile BFF Aggregator ఎండ్ పాయింట్
class MobileBFF:
    def get_home_screen(self, user_id):
        user = user_service.get_user(user_id)
        orders = order_service.get_recent_orders(user_id, limit=2)
        # అనవసరమైన ఫీల్డ్స్ తీసేసి కేవలం మొబైల్ స్క్రీన్‌కు కావాల్సినవి మాత్రమే పంపడం
        return {
            "welcome_name": user["first_name"],
            "unread_count": 3,
            "latest_order_status": orders[0]["status"] if orders else None
        }""",
        "mistake": "BFF లో డేటాబేస్ టేబుల్స్ క్రియేట్ చేసి బిజినెస్ లాజిక్ రాయడం; BFF కేవలం డేటా అగ్రిగేషన్, ఫిల్టరింగ్ మాత్రమే చేయాలి."
    },
    {
        "title": "Sidecar Pattern (Supporting Functionality in Separate Process)",
        "subtitle": "సైడ్‌కార్ ప్యాటర్న్ (మోటార్ సైకిల్‌కు పక్కన అటాచ్ చేసిన సైడ్‌కార్ లాగా సహాయక ఫీచర్లను వేరే ప్రాసెస్‌లో నడపడం)",
        "why": "ప్రతి మైక్రోసర్వీస్ కోడ్‌లోనూ లాగింగ్, మెట్రిక్స్ కలెక్షన్, mTLS సర్టిఫికెట్ మేనేజ్‌మెంట్ లాజిక్ రాసుకుంటూ పోతే కోడ్ డూప్లికేషన్ మరియు లాంగ్వేజ్ లాక్-ఇన్ ఏర్పడుతుంది.",
        "explanation": "కుబెర్‌నెటిస్ (Kubernetes) పాడ్‌లో మీ మెయిన్ అప్లికేషన్ కంటైనర్‌తో పాటు ఇంకొక చిన్న హెల్పర్ కంటైనర్‌ను (Sidecar) నడుపుతారు. మీ మెయిన్ యాప్ కేవలం లోకల్‌హోస్ట్‌కు లాగ్స్ రాస్తుంది లేదా HTTP రిక్వెస్ట్ చేస్తుంది. సైడ్‌కార్ కంటైనర్ (ఉదా: Envoy, Fluentbit) దాన్ని తీసుకొని mTLS ద్వారా ఎన్‌క్రిప్ట్ చేసి పంపడం లేదా Datadog కి లాగ్స్ పంపడం చూసుకుంటుంది. మెయిన్ యాప్ ఏ లాంగ్వేజ్ (PHP/Python/Go) లో రాసినా సైడ్‌కార్ మారదు.",
        "example": """# Kubernetes Pod లో సైడ్‌కార్ డెఫినిషన్ కాన్సెప్ట్
'''yaml
apiVersion: v1
kind: Pod
metadata:
  name: order-service-pod
spec:
  containers:
  - name: main-app
    image: my-laravel-order-app:v1
  - name: envoy-sidecar  # సైడ్‌కార్ ప్రాక్సీ
    image: envoyproxy/envoy:v1.28
    ports:
    - containerPort: 15001
''' """,
        "mistake": "సైడ్‌కార్ చాలా ఎక్కువ మెమరీని మరియు CPUని తినేలా కాన్ఫిగర్ చేయడం; వందల పాడ్స్ ఉన్నప్పుడు సైడ్‌కార్ మెమరీ ఓవర్‌హెడ్ భారీ క్లౌడ్ బిల్లుకు దారితీస్తుంది."
    },
    {
        "title": "Ambassador Pattern (Outbound Communication Proxy)",
        "subtitle": "అంబాసిడర్ ప్యాటర్న్ (బయటి సర్వీసులకు వెళ్లే ట్రాఫిక్‌ను మేనేజ్ చేసే రాయబారి ప్రాక్సీ)",
        "why": "మీ అప్లికేషన్ థర్డ్ పార్టీ బ్యాంకింగ్ లేదా పేమెంట్ API లను పిలిచేటప్పుడు రీట్రైలు, సర్క్యూట్ బ్రేకింగ్, సెక్యూరిటీ టోకెన్ ఇంజెక్షన్ వంటి సంక్లిష్ట నెట్‌వర్క్ పనులను మీ యాప్ కోడ్ చేయకూడదు.",
        "explanation": "అంబాసిడర్ అనేది మీ అప్లికేషన్ పక్కనే ఉండే ఒక అవుట్‌బౌండ్ ప్రాక్సీ (Outbound Proxy). మీ యాప్ కేవలం లోకల్ `http://localhost:9000/charge` కు కాల్ చేస్తుంది. అంబాసిడర్ ప్రాక్సీ ఆ రిక్వెస్ట్‌కు సరైన ఆథరైజేషన్ హెడర్లను చేర్చి, అవసరమైతే రీట్రైలు చేసి, సర్క్యూట్ ఓపెన్ అయితే ఫాల్‌బ్యాక్ ఇచ్చి రియల్ స్ట్రైప్ API కి సురక్షితంగా చేరుస్తుంది.",
        "example": """# Ambassador Proxy బిహేవియర్
class AmbassadorProxy:
    def forward_payment(self, payload):
        # టోకెన్ రిఫ్రెష్ మరియు ఎన్‌క్రిప్షన్ ఆటోమేటిక్ గా చేస్తుంది
        headers = {"Authorization": "Bearer SECURE_ROTATED_TOKEN"}
        try:
            return external_bank_api.post("/pay", json=payload, headers=headers, timeout=2.0)
        except TimeoutError:
            return {"status": "FAILED", "reason": "Bank timeout - Circuit open"}""",
        "mistake": "అంబాసిడర్ మరియు సైడ్‌కార్ ప్యాటర్న్లను కన్ఫ్యూజ్ అవ్వడం; అంబాసిడర్ ప్రత్యేకంగా బాహ్య ప్రపంచపు అవుట్‌బౌండ్ ట్రాఫిక్ కోసమే రూపొందించబడింది."
    },
    {
        "title": "Service Mesh (Istio, Linkerd, Envoy)",
        "subtitle": "సర్వీస్ మెష్ (మైక్రోసర్వీసెస్ మధ్య కమ్యూనికేషన్‌ను ఆటోమేటిక్‌గా రక్షించి, ట్రాక్ చేసే నెట్‌వర్క్ లేయర్)",
        "why": "వందల కొద్దీ మైక్రోసర్వీసులు ఉన్నప్పుడు సర్వీస్-టు-సర్వీస్ mTLS ఎన్‌క్రిప్షన్, ట్రాఫిక్ స్ప్లిటింగ్ (Canary), ట్రేసింగ్ ఒక్కొక్క మైక్రోసర్వీస్ లో కోడ్ రాయడం అసాధ్యం.",
        "explanation": "సర్వీస్ మెష్ అనేది ఒక ఇన్‌ఫ్రాస్ట్రక్చర్ లేయర్. ప్రతి మైక్రోసర్వీస్ పాడ్‌లో Envoy సైడ్‌కార్ ప్రాక్సీని ఇంజెక్ట్ చేస్తారు. రెండు సర్వీసులు మాట్లాడుకున్నప్పుడు నేరుగా కాకుండా ఈ సైడ్‌కార్ల ద్వారానే ట్రాఫిక్ వెళ్తుంది (Data Plane). Istio వంటి Control Plane వీటికి సెక్యూరిటీ పాలసీలు, ట్రాఫిక్ రూల్స్ అందిస్తుంది. డెవలపర్లు కోడ్‌లో ఒక్క లైన్ కూడా రాయకుండానే ఆటోమేటిక్ mTLS ఎన్‌క్రిప్షన్, డిస్ట్రిబ్యూటెడ్ ట్రేసింగ్, రేట్ లిమిటింగ్ లభిస్తాయి.",
        "example": """# Istio VirtualService Canary Routing (90% v1, 10% v2)
'''yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: order-route
spec:
  hosts:
  - order-service
  http:
  - route:
    - destination:
        host: order-service
        subset: v1
      weight: 90
    - destination:
        host: order-service
        subset: v2
      weight: 10
''' """,
        "mistake": "కేవలం 3 లేదా 4 చిన్న మైక్రోసర్వీసులు ఉన్న ప్రాజెక్ట్‌లలో కూడా Istio ని సెటప్ చేయడం; చిన్న ప్రాజెక్ట్‌లకు సర్వీస్ మెష్ మెయింటెనెన్స్ మరియు నెట్‌వర్క్ లాటెన్సీ భారమవుతుంది."
    },
    {
        "title": "Choreography vs Orchestration (Workflow Coordination)",
        "subtitle": "కొరియోగ్రఫీ vs ఆర్కెస్ట్రేషన్ (ఈవెంట్ డ్రివెన్ డ్యాన్స్ vs సెంట్రల్ డైరెక్టర్ ఆర్డర్స్)",
        "why": "ఆర్డర్, పేమెంట్, ఇన్వెంటరీ, షిప్పింగ్ వంటి బహుళ సర్వీసుల మధ్య జరిగే సుదీర్ఘమైన వ్యాపార ప్రక్రియలను (Workflows) ఎలా సమన్వయం చేయాలో తేల్చుకోవాలి.",
        "explanation": "Choreography లో సెంట్రల్ కంట్రోలర్ ఉండదు; డ్యాన్సర్లు ఒకరిని చూసి ఒకరు స్టెప్పులేసినట్లు, ఒక సర్వీస్ Kafka లో ఈవెంట్ పబ్లిష్ చేయగానే (ఉదా: `OrderCreated`), దాన్ని విని పేమెంట్ సర్వీస్ పేమెంట్ చేసి `PaymentDone` ఈవెంట్ ఇస్తుంది, దాన్ని విని ఇన్వెంటరీ పనిచేస్తుంది. లోపలి కప్లింగ్ తక్కువ కానీ ప్రక్రియ ఎక్కడ ఆగిందో ట్రాక్ చేయడం కష్టం. \nOrchestration లో ఒక ఆర్కెస్ట్రా కండక్టర్ లాగా సెంట్రల్ సర్వీస్ (Temporal, Camunda, AWS Step Functions) ఉంటుంది. అది ఆర్డర్ సర్వీస్ కి 'నువ్వు చెయ్', తర్వాత పేమెంట్ సర్వీస్ కి 'ఇప్పుడు నీ వంతు' అని నేరుగా ఆదేశిస్తుంది. ఫ్లో మొత్తం స్పష్టంగా తెలుస్తుంది.",
        "example": """# Orchestration ఫ్లో ఉదాహరణ (Temporal Style)
class OrderWorkflowOrchestrator:
    def process_checkout(self, order):
        # దశ 1: పేమెంట్
        pay_res = payment_service.charge(order.amount)
        if not pay_res.success:
            return "Failed at Payment"

        # దశ 2: ఇన్వెంటరీ రిజర్వేషన్
        inv_res = inventory_service.reserve(order.items)
        if not inv_res.success:
            # కాంపెన్సేషన్ (Compensate)
            payment_service.refund(order.amount)
            return "Failed at Inventory - Refunded!"

        # దశ 3: షిప్పింగ్
        shipping_service.dispatch(order.address)
        return "Order Completed Successfully" """,
        "mistake": "వందల ఈవెంట్లు ఉన్న క్లిష్టమైన ప్రాసెస్ లో ప్యూర్ కొరియోగ్రఫీ వాడితే 'Event Spaghetti' ఏర్పడి ఏ ఈవెంట్ ఎవరిని పిలుస్తోందో ఎవరికీ అర్థం కాదు."
    },
    {
        "title": "Saga Compensation (Failed Distributed Transactions Recovery)",
        "subtitle": "సాగ కాంపెన్సేషన్ (డిస్ట్రిబ్యూటెడ్ ట్రాన్సాక్షన్ ఫెయిల్ అయినప్పుడు మునుపటి మార్పులను వెనక్కి తిప్పే చర్యలు)",
        "why": "మైక్రోసర్వీసెస్ లో 2PC లాంటి సాంప్రదాయ డేటాబేస్ `ROLLBACK` లు పనిచేయవు; ఇప్పటికే వేరే సర్వీస్ డేటాబేస్ లో కమిట్ అయిన రికార్డును సరిచేయడానికి ప్రతికూల చర్య (Compensating action) తీసుకోవాలి.",
        "explanation": "Saga ప్యాటర్న్ లో ప్రతి లోకల్ ట్రాన్సాక్షన్ $T_i$ కి దానికి వ్యతిరేకమైన కాంపెన్సేటింగ్ ట్రాన్సాక్షన్ $C_i$ ముందే రాసి ఉంచుతారు. ఉదాహరణకు, 'డబ్బు డెబిట్ చేయడం' అనేది $T_1$ అయితే, దానికి కాంపెన్సేషన్ $C_1$ 'డబ్బు రీఫండ్ చేయడం'. ఆర్డర్ ప్రాసెస్ లో 4వ దశ ఫెయిల్ అయితే, సాగా ఇంజిన్ రివర్స్ ఆర్డర్ లో $C_3, C_2, C_1$ లను అమలు చేసి అకౌంట్స్ మరియు ఇన్వెంటరీ ని యథాస్థితికి తీసుకువస్తుంది.",
        "example": """# Saga Compensation లాజిక్
class SagaManager:
    def __init__(self):
        self.compensations = []

    def execute(self):
        try:
            # Step 1: Reserve Hotel
            hotel_service.book()
            self.compensations.append(lambda: hotel_service.cancel_booking())

            # Step 2: Book Flight
            flight_service.book()
            self.compensations.append(lambda: flight_service.cancel_flight())

            # Step 3: Rent Car (అనుకోకుండా ఫెయిల్ అయింది)
            raise Exception("Car Rental Unavailable!")
        except Exception as e:
            print("🚨 సాగా ఫెయిల్ అయింది! కాంపెన్సేషన్స్ అమలు అవుతున్నాయి...")
            for comp in reversed(self.compensations):
                comp()
            print("అన్ని రిజర్వేషన్లు రద్దు చేయబడ్డాయి (Rollback Done).")""",
        "mistake": "కాంపెన్సేటింగ్ యాక్షన్లు ఎల్లప్పుడూ Idempotent గా ఉండాలి; నెట్‌వర్క్ ఫెయిల్యూర్‌లో రీఫండ్ కాల్ రెండుసార్లు జరిగితే డబుల్ రీఫండ్ కాకూడదు."
    },
    {
        "title": "Outbox Pattern (Database + Event Publishing Consistency)",
        "subtitle": "అవుట్‌బాక్స్ ప్యాటర్న్ (డేటాబేస్ సేవ్ మరియు మెసేజ్ క్యూ పబ్లిష్ రెండూ అటామిక్ గా జరిగేలా చూడటం)",
        "why": "Laravel లో `$order->save(); Event::dispatch(new OrderCreated);` అని రాసినప్పుడు, డేటాబేస్ సేవ్ అయ్యాక సర్వర్ క్రాష్ అయితే ఈవెంట్ పోతుంది; లేదా ఈవెంట్ వెళ్లి డేటాబేస్ రోల్‌బ్యాక్ అయితే ఫాంటమ్ ఈవెంట్ వెళ్తుంది (Dual-write problem).",
        "explanation": "ఈ సమస్యను పరిష్కరించడానికి ఒకే డేటాబేస్ ట్రాన్సాక్షన్ లో మీ బిజినెస్ టేబుల్ (`orders`) తో పాటు ఒక ప్రత్యేకమైన `outbox` టేబుల్ లో కూడా ఈవెంట్ మెసేజ్ ను ఇన్సర్ట్ చేస్తారు. ట్రాన్సాక్షన్ అటామిక్ కాబట్టి రెండూ సేవ్ అవుతాయి లేదా రెండూ ఫెయిల్ అవుతాయి. తర్వాత ఒక ప్రత్యేక బ్యాక్‌గ్రౌండ్ వర్కర్ లేదా Debezium (CDC) ఆ `outbox` టేబుల్ నుండి మెసేజ్‌లను చదివి Kafka లేదా RabbitMQ కి పంపి, పంపిన వాటిని 'PUBLISHED' గా మార్క్ చేస్తుంది.",
        "example": """# Laravel / SQL Outbox Pattern కాన్సెప్ట్
# DB::transaction లోనే రెండు టేబుల్స్ లో రాయడం:
'''sql
BEGIN TRANSACTION;
INSERT INTO orders (id, user_id, total) VALUES (501, 10, 2500);
INSERT INTO outbox_messages (id, event_type, payload, status) 
VALUES (uuid(), 'OrderCreated', '{"order_id": 501, "total": 2500}', 'PENDING');
COMMIT;
''' 
# బ్యాక్‌గ్రౌండ్ వర్కర్ కేవలం 'PENDING' ఈవెంట్లను మాత్రమే Kafka కి పంపుతుంది""",
        "mistake": "అవుట్‌బాక్స్ వర్కర్ ప్రతి సెకనుకు `SELECT * FROM outbox` అని పోలింగ్ చేస్తే డేటాబేస్‌పై లోడ్ పెరుగుతుంది; హై-స్కేల్ లో Change Data Capture (CDC) వాడటం మేలు."
    },
    {
        "title": "Inbox Pattern (Duplicate Event Processing Prevention)",
        "subtitle": "ఇన్‌బాక్స్ ప్యాటర్న్ (మెసేజ్ బ్రోకర్ నుండి డూప్లికేట్ ఈవెంట్లు వచ్చినా ఒకేసారి ప్రాసెస్ అయ్యేలా చూడటం)",
        "why": "Kafka, RabbitMQ లు 'At-least-once' డెలివరీని ఇస్తాయి. నెట్‌వర్క్ బ్లింక్ వల్ల ఒకే పేమెంట్ మెసేజ్ కస్టమర్‌కి రెండుసార్లు అందితే ఖాతా నుండి రెండుసార్లు డబ్బు కట్ కాకూడదు.",
        "explanation": "రిసీవింగ్ సర్వీస్ లో ఒక `inbox` టేబుల్ మెయింటైన్ చేస్తారు. మెసేజ్ అందినప్పుడు దాని `message_id` ని `inbox` టేబుల్ లో అటామిక్ గా ఇన్సర్ట్ చేస్తారు. ఒకవేళ ఆ ఐడీ ఇప్పటికే ఉంటే (Duplicate Key Constraint), ఆ మెసేజ్ ను స్కిప్ చేసి బ్రోకర్‌కు వెంటనే ACK పంపుతారు. దీంతో బిజినెస్ ఆపరేషన్ ఖచ్చితంగా ఒకే ఒక్కసారి మాత్రమే అమలవుతుంది (Idempotent Consumer).",
        "example": """# Inbox Pattern Idempotency చెక్
class InboxConsumer:
    def process_incoming_event(self, event):
        msg_id = event["message_id"]
        # అటామిక్ గా ఇన్‌బాక్స్ లో ఇన్సర్ట్ చేయడానికి ప్రయత్నించడం
        inserted = db.execute("INSERT IGNORE INTO inbox (message_id) VALUES (?)", [msg_id])
        if not inserted:
            print(f"⚠️ డూప్లికేట్ ఈవెంట్ గుర్తించబడింది ({msg_id})! ప్రాసెస్ స్కిప్ చేయబడింది.")
            return

        # వ్యాపార లాజిక్ అమలు
        account_service.deduct_balance(event["user_id"], event["amount"])
        print(f"✅ ఈవెంట్ విజయవంతంగా ప్రాసెస్ చేయబడింది: {msg_id}")""",
        "mistake": "మెసేజ్ ప్రాసెస్ చేయడం పూర్తయిన తర్వాత ఇన్‌బాక్స్ టేబుల్ లో రాయడం; అలా చేస్తే ప్రాసెసింగ్ మధ్యలో క్రాష్ అయితే డూప్లికేట్స్ వచ్చే ప్రమాదం ఉంటుంది."
    },
    {
        "title": "Change Data Capture (CDC)",
        "subtitle": "చేంజ్ డేటా క్యాప్చర్ (డేటాబేస్ లో జరిగే ప్రతి ఇన్సర్ట్, అప్‌డేట్‌ను రియల్-టైమ్ స్ట్రీమ్ గా మార్చడం)",
        "why": "అప్లికేషన్ కోడ్ ద్వారా కాకుండా, డేటాబేస్ లెవెల్ లోనే జరిగే ప్రతి మార్పును పట్టుకొని ఎలాస్టిక్‌సెర్చ్, రెడిస్ లేదా డేటా లేక్‌కి జీరో లాగ్‌తో సమన్వయం చేయాలి.",
        "explanation": "MySQL లో ప్రతి మార్పు `binlog` లో రాయబడుతుంది; Postgres లో `WAL` (Write-Ahead Log) లో రికార్డ్ అవుతుంది. Debezium వంటి CDC టూల్స్ ఈ ట్రాన్సాక్షన్ లాగ్స్‌ను నేరుగా టెయిల్ (Tail) చేసి, డేటాబేస్‌పై ఎటువంటి పర్ఫార్మెన్స్ లోడ్ పడకుండా ప్రతి INSERT, UPDATE, DELETE ను క్షణాల్లో Kafka ఈవెంట్‌గా ప్రసారం చేస్తాయి. మైక్రోసర్వీసెస్ మధ్య డేటా సింక్ చేయడానికి ఇది అత్యంత శక్తివంతమైన విధానం.",
        "example": """# Debezium CDC ఈవెంట్ JSON రూపం (Kafka లో కనిపించేది)
{
  "op": "u", # 'u' అంటే Update, 'c' అంటే Create, 'd' అంటే Delete
  "before": {"id": 101, "status": "PENDING"},
  "after": {"id": 101, "status": "SHIPPED"},
  "source": {"db": "shop_db", "table": "orders", "ts_ms": 1716902400000}
}""",
        "mistake": "CDC కి బదులుగా క్రోన్ జాబ్స్ పెట్టి `SELECT * WHERE updated_at > NOW() - 5m` అని పోలింగ్ చేయడం; ఇది డిలీట్ అయిన రికార్డులను పట్టుకోలేదు మరియు DB ని స్లో చేస్తుంది."
    },
    {
        "title": "Event Sourcing (Storing State as Stream of Events)",
        "subtitle": "ఈవెంట్ సోర్సింగ్ (ప్రస్తుత స్థితిని కాకుండా జరిగిన ప్రతి ఈవెంట్ చరిత్రను భద్రపరచడం)",
        "why": "సాంప్రదాయ బ్యాంక్ అకౌంట్ లో కేవలం ప్రస్తుత బ్యాలెన్స్ మాత్రమే స్టోర్ చేస్తే, ఆ బ్యాలెన్స్ ఎలా వచ్చిందో ఆడిట్ చేయడానికి వీలుండదు; ప్రతి లావాదేవీని ఎప్పటికీ చెరిపివేయలేని (Immutable) చరిత్రగా ఉంచాలి.",
        "explanation": "సాంప్రదాయ CRUD లో `UPDATE users SET balance = 500` అని పాత విలువను తుడిచివేస్తాం. Event Sourcing లో ఎప్పుడూ UPDATE లేదా DELETE లు ఉండవు. కేవలం APPEND మాత్రమే: `AccountOpened ($0)`, `Deposited (+$1000)`, `Withdrew (-$500)`. ప్రస్తుత బ్యాలెన్స్ కావాలంటే ఈ ఈవెంట్లన్నింటినీ మొదటి నుండి ప్లే (Replay) చేస్తారు. పనితీరు వేగవంతం కోసం నిర్ణీత విరామాలలో స్నాప్‌షాట్స్ (Snapshots) తీసుకుంటారు.",
        "example": """# Event Sourcing సింపుల్ బ్యాంక్ అకౌంట్
class BankAccountEventSourced:
    def __init__(self):
        self.events = []
        
    def apply_event(self, event):
        self.events.append(event)
        
    def get_current_balance(self):
        # మొదటి నుండి అన్ని ఈవెంట్లను కూడిక/తీసివేత చేసి స్టేట్ పొందడం
        balance = 0
        for ev in self.events:
            if ev["type"] == "DEPOSIT": balance += ev["amount"]
            elif ev["type"] == "WITHDRAW": balance -= ev["amount"]
        return balance

acc = BankAccountEventSourced()
acc.apply_event({"type": "DEPOSIT", "amount": 1000})
acc.apply_event({"type": "WITHDRAW", "amount": 300})
print("ఖాతా ప్రస్తుత నిల్వ:", acc.get_current_balance()) # 700""",
        "mistake": "లక్షల కొద్దీ ఈవెంట్లు ఉన్నప్పుడు స్నాప్‌షాట్ లేకుండా ప్రతిసారీ మొదటి నుండి రీప్లే చేయడం; ఇది సిస్టమ్ బూట్ టైమ్‌ను విపరీతంగా పెంచుతుంది."
    },
    {
        "title": "CQRS (Command and Query Responsibility Segregation)",
        "subtitle": "CQRS (రాయడానికి ఒక డేటాబేస్, వేగంగా చదవడానికి మరో డేటాబేస్ వేరుచేయడం)",
        "why": "ఒకే రిలేషనల్ డేటాబేస్ పై భారీ Writes మరియు భారీ క్లిష్టమైన JOIN లతో కూడిన Reads రెండూ ఒకేసారి నడిస్తే డేటాబేస్ లాక్స్ మరియు స్లో క్వెరీలతో కుప్పకూలిపోతుంది.",
        "explanation": "Greg Young రూపొందించిన CQRS లో రెండు వేర్వేరు మోడల్స్ ఉంటాయి. \nCommands (రైట్స్): INSERT, UPDATE, DELETE లు కఠినమైన వ్యాపార నియమాలతో కూడిన రిలేషనల్ డేటాబేస్ (MySQL/Postgres) లో జరుగుతాయి. \nQueries (రీడ్స్): యూజర్ ఇంటర్‌ఫేస్ కోసం ఎలాస్టిక్‌సెర్చ్, రెడిస్ లేదా డి-నార్మలైజ్డ్ రీడ్ టేబుల్స్ నుండి జాయిన్స్ లేకుండా మెరుపు వేగంతో డేటాను చదువుతారు. కమాండ్స్ జరిగినప్పుడు ఈవెంట్ల ద్వారా రీడ్ మోడల్ అసింక్రోనస్‌గా అప్‌డేట్ అవుతుంది.",
        "example": """# CQRS స్ట్రక్చర్ ఉదాహరణ
class OrderCommandHandler:
    def handle_create_order(self, cmd):
        # 1. వాలిడేట్ & కోర్ DB లో సేవ్
        order_id = mysql_db.insert_order(cmd.user_id, cmd.items)
        # 2. రీడ్ మోడల్ సింక్ కోసం ఈవెంట్ పంపడం
        event_bus.publish("OrderCreated", {"order_id": order_id, "items": cmd.items})

class OrderQueryHandler:
    def get_order_summary_for_ui(self, order_id):
        # జాయిన్స్ లేకుండా ఎలాస్టిక్‌సెర్చ్ లేదా రీడ్ వ్యూ నుండి నేరుగా సింగిల్ లుకప్
        return elasticsearch.get_doc(index="orders_read_view", id=order_id)""",
        "mistake": "రైట్ జరిగిన వెంటనే రీడ్ మోడల్ లో డేటా కనిపించడానికి కొన్ని మిల్లీసెకన్ల సమయం (Eventual consistency lag) పడుతుంది; వెంటనే UI లో కనిపించాలని గట్టి లాక్స్ పెడితే CQRS ప్రయోజనం పోతుంది."
    },
    {
        "title": "Materialized Views (Precomputed Read Models)",
        "subtitle": "మెటీరియలైజ్డ్ వ్యూస్ (క్లిష్టమైన జాయిన్స్ ఫలితాన్ని ముందే లెక్కించి రెడీగా ఉంచడం)",
        "why": "లక్షల రికార్డులు ఉన్న టేబుల్స్ పై 5 టేబుల్స్ JOIN చేసి అగ్రిగేషన్స్ (SUM, AVG) చేయడం ప్రతి పేజ్ లోడ్ లో చాలా ఆలస్యం అవుతుంది.",
        "explanation": "సాధారణ SQL వ్యూ (Standard View) అనేది కేవలం సేవ్ చేసిన క్వెరీ మాత్రమే; కాల్ చేసిన ప్రతిసారీ అది మళ్లీ റన్ అవుతుంది. కానీ Materialized View ఆ క్వెరీ ఫలితాన్ని నిజమైన టేబుల్ లాగా డిస్క్ మీద భౌతికంగా సేవ్ చేసి ఉంచుతుంది. డేటాబేస్ ట్రిగ్గర్స్ ద్వారా లేదా CDC ఈవెంట్స్ ద్వారా అసలు టేబుల్స్ మారినప్పుడు ఈ వ్యూ ఇంక్రిమెంటల్ గా అప్‌డేట్ అవుతుంది. క్వెరీ టైమ్ 10 సెకన్ల నుండి 2 మిల్లీసెకన్లకు పడిపోతుంది.",
        "example": """# PostgreSQL Materialized View సింటాక్స్
'''sql
CREATE MATERIALIZED VIEW monthly_sales_summary AS
SELECT 
    product_id, 
    DATE_TRUNC('month', order_date) as month, 
    SUM(amount) as total_revenue,
    COUNT(id) as total_orders
FROM orders
GROUP BY product_id, DATE_TRUNC('month', order_date);

-- డేటా మారినప్పుడు రిఫ్రెష్ చేయడం:
REFRESH MATERIALIZED VIEW CONCURRENTLY monthly_sales_summary;
''' """,
        "mistake": "పీక్ ట్రాఫిక్ సమయంలో `REFRESH MATERIALIZED VIEW` ని భారీ క్వెరీలతో సింక్రోనస్‌గా రన్ చేయడం; దాని బదులు `CONCURRENTLY` ఫ్లాగ్ వాడాలి లేదా అసింక్రోనస్ బ్యాచ్ షెడ్యూల్ చేయాలి."
    }
]
