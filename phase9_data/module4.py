# Module 4: Advanced Performance Engineering (15 topics)

topics = [
    {
        "title": "Tail Latency (P95, P99, P99.9 Latency)",
        "subtitle": "టెయిల్ లాటెన్సీ (సగటు వేగం మోసం చేస్తుంది; 99% యూజర్లకు వచ్చే ఆలస్యాన్ని కొలవడం)",
        "why": "ఒక వెబ్ పేజీ లోడ్ అవ్వడానికి బ్యాకెండ్‌లో 100 మైక్రోసర్వీసెస్ పిలవాలి. ప్రతి సర్వీస్ సగటున 10ms తీసుకున్నా, ఒక్క సర్వీస్ P99 లో 2 సెకన్లు ఆలస్యం చేస్తే మొత్తం పేజీ యూజర్‌కు 2 సెకన్లు ఆగిపోతుంది.",
        "explanation": "Average (Mean) లాటెన్సీ ఎప్పుడూ వాస్తవాన్ని దాచిపెడుతుంది. ఒక క్లినిక్‌లో 9 మందికి జ్వరం వచ్చి 5 నిమిషాల్లో మందులిచ్చి పంపారు, ఒక్కడికి గుండెపోటు వచ్చి 2 గంటలు పట్టింది. సగటు సమయం చూస్తే అందరికీ 15 నిమిషాలే పట్టిందని అనిపిస్తుంది! \nPercentiles (P50, P95, P99, P99.9) వాస్తవాన్ని చూపిస్తాయి. P99 అంటే 99% యూజర్ల రిక్వెస్ట్‌లు ఆ సమయం లోపలే ముగిశాయి, కేవలం 1% మంది మాత్రమే అంతకంటే ఎక్కువ సమయం వేచి ఉన్నారు. అమెజాన్ వంటి ఇ-కామర్స్ సైట్లలో ఎక్కువ కొనుగోళ్లు చేసే సంపన్న కస్టమర్లే (ఎక్కువ ఆర్డర్ హిస్టరీ ఉన్నవారు) ఈ P99 బారిన పడతారు.",
        "example": """# లాటెన్సీ పర్సంటైల్స్ లెక్కింపు
import numpy as np

# 1000 రిక్వెస్టుల రెస్పాన్స్ టైమ్స్ (మిల్లీసెకన్లలో)
latencies = [15.2] * 950 + [120.0] * 40 + [2500.0] * 10

print("సగటు లాటెన్సీ (Mean):", round(np.mean(latencies), 2), "ms (అబద్ధం!)")
print("P50 (Median):", round(np.percentile(latencies, 50), 2), "ms")
print("P95:", round(np.percentile(latencies, 95), 2), "ms")
print("P99:", round(np.percentile(latencies, 99), 2), "ms")
print("P99.9 (Worst Tail):", round(np.percentile(latencies, 99.9), 2), "ms (నిజం!)")""",
        "mistake": "సిస్టమ్ హెల్త్ డ్యాష్‌బోర్డులలో కేవలం Average Latency మాత్రమే పెట్టి సంతృప్తి చెందడం; P99 మరియు P99.9 గ్రాఫ్స్ చూడకపోతే అసలైన కస్టమర్ బాధ అర్థం కాదు."
    },
    {
        "title": "Coordinated Omission (Load Testing Measurement Errors)",
        "subtitle": "కోఆర్డినేటెడ్ ఒమిషన్ (లోడ్ టెస్టింగ్ టూల్స్ వేగం కొలిచేటప్పుడు చేసే ఘోరమైన కొలత తప్పు)",
        "why": "JMeter లేదా wrk వంటి లోడ్ టెస్టింగ్ టూల్స్ నడిపినప్పుడు మీ సర్వర్ 1 సెకను పాటు ఫ్రీజ్ అయినా, టూల్స్ 'P99 కేవలం 50ms' అని తప్పుడు రిపోర్టు ఇచ్చి మిమ్మల్ని మోసగిస్తాయి.",
        "explanation": "గిల్ టెనె (Gil Tene) కనిపెట్టిన సమస్య ఇది. లోడ్ టెస్ట్ టూల్ సెకనుకు 100 రిక్వెస్టులు పంపాలి అనుకుందాం. సర్వర్ 10 సెకన్ల పాటు GC Pause లో ఆగిపోయింది. సాంప్రదాయ క్లయింట్ ఆ ఒక్క రిక్వెస్ట్ రెస్పాన్స్ కోసం 10 సెకన్లు నిశ్శబ్దంగా వేచి ఉంది; ఈ 10 సెకన్ల వ్యవధిలో పంపాల్సిన మిగిలిన 1,000 రిక్వెస్టులను అసలు పంపనేలేదు (Omission)! క్లయింట్ మరియు సర్వర్ కలిసి ఈ ఆలస్యాన్ని సమన్వయం చేసుకుని దాచేశాయి. ఈ సమస్య లేని ఆధునిక టూల్స్ (Vegeta, k6, HdrHistogram) నిర్ణీత రేటుతో రిక్వెస్టులను నిరంతరం జనరేట్ చేస్తూ, సర్వర్ బ్లాక్ అయినప్పుడు వచ్చే క్యూయింగ్ టైమ్‌ను కూడా లాటెన్సీకి జోడించి అసలైన రియలిస్టిక్ P99 ని లెక్కిస్తాయి.",
        "example": """# Coordinated Omission లో జరిగే మోసం
# అనుకున్న షెడ్యూల్: ప్రతి 10ms కి ఒక రిక్వెస్ట్ వెళ్లాలి
# వాస్తవంలో: Request #1 సర్వర్‌లో 1000ms ఆగిపోయింది.
# తప్పుడు టూల్: 1 రిక్వెస్ట్ 1000ms పట్టిందని 1 రికార్డు మాత్రమే నోట్ చేసుకుంటుంది.
# నిజాయితీ గల టూల్ (HdrHistogram): ఆ 1000ms లో రావాల్సిన 100 రిక్వెస్టులు కూడా క్యూలో ఆగిపోయినట్లే గుర్తించి, 1000ms, 990ms, 980ms... లాటెన్సీలుగా రికార్డ్ చేస్తుంది!""",
        "mistake": "క్లోజ్డ్-లూప్ (Closed-loop) టెస్టింగ్ టూల్స్ వాడి వచ్చిన లాటెన్సీ నంబర్లను గుడ్డిగా నమ్మడం; ఎల్లప్పుడూ ఓపెన్-లూప్ (Open-model) రేట్-బేస్డ్ బెంచ్‌మార్కింగ్ వాడాలి."
    },
    {
        "title": "Queueing Theory (Little's Law, M/M/1 Queues)",
        "subtitle": "క్యూయింగ్ థియరీ (లిటిల్స్ లా: ట్రాఫిక్ పెరిగినప్పుడు సిస్టమ్ ఎందుకు అకస్మాత్తుగా కుప్పకూలుతుందో చెప్పే గణితం)",
        "why": "సర్వర్ CPU 80% దాటగానే లాటెన్సీ కొద్దిగా పెరగదు; అకస్మాత్తుగా నిలువుగా పైకి లేచి (Hockey Stick Curve) సర్వర్ స్తంభించిపోతుంది. ఎందుకు అలా జరుగుతుందో అర్థం కావాలి.",
        "explanation": "జాన్ లిటిల్ రూపొందించిన ఫార్ములా: $L = \lambda W$. \nఇక్కడ $L$ = సిస్టమ్‌లో ఉన్న మొత్తం రిక్వెస్టులు (Concurrency), $\lambda$ = రాక రేటు (Arrival Rate / RPS), $W$ = ఒక రిక్వెస్ట్ ముగియడానికి పట్టే సమయం (Latency). \nM/M/1 క్యూయింగ్ మోడల్ ప్రకారం, సర్వర్ యుటిలైజేషన్ $\rho = \lambda / \mu$ (ఇక్కడ $\mu$ = ప్రాసెసింగ్ సామర్థ్యం). \nయుటిలైజేషన్ 90% దాటగానే క్యూ వెయిటింగ్ టైమ్ $W = 1 / (\mu - \lambda)$ ఇన్ఫినిటీ వైపు పరిగెడుతుంది. అందుకే సర్వర్లను ఎప్పుడూ 100% సామర్థ్యంతో నడపకూడదు; గరిష్టంగా 60-70% వద్దే ఆటో-స్కేలింగ్ ట్రిగ్గర్ అవ్వాలి.",
        "example": """# Little's Law ద్వారా Concurrency లెక్కింపు
def calculate_concurrent_users(rps, avg_latency_seconds):
    # L = Lambda * W
    return rps * avg_latency_seconds

# సెకనుకు 500 రిక్వెస్టులు (RPS), ఒక్కొక్కటి సగటున 200ms (0.2s) తీసుకుంటే:
concurrency = calculate_concurrent_users(500, 0.2)
print("ఏకకాలంలో సర్వర్ లో ప్రాసెస్ అవుతున్న కనెక్షన్లు:", concurrency) # 100 కనెక్షన్లు
# లాటెన్సీ 2 సెకన్లకు పెరిగితే: 500 * 2 = 1000 కనెక్షన్లు కావాలి! సర్వర్ క్రాష్!""",
        "mistake": "CPU 95% వరకు వెళ్లేవరకు సర్వర్లను స్కేల్ చేయకుండా ఆగడం; 80% దాటగానే క్యూయింగ్ డిలే ఎక్స్‌పోనెన్షియల్ గా పెరుగుతుంది."
    },
    {
        "title": "Backpressure (Producer-Consumer Flow Control)",
        "subtitle": "బ్యాక్‌ప్రెషర్ (వేగంగా డేటా పంపే ప్రొడ్యూసర్‌ను నెమ్మదించమని కన్స్యూమర్ సిగ్నల్ ఇవ్వడం)",
        "why": "ఒక సర్వీస్ సెకనుకు 10,000 మెసేజ్‌లు పంపుతుంటే, డౌన్‌స్ట్రీమ్ సర్వీస్ సెకనుకు కేవలం 500 మాత్రమే ప్రాసెస్ చేయగలిగితే, బఫర్ లేదా మెమరీ నిండిపోయి Out Of Memory (OOM) తో సర్వర్ చస్తుంది.",
        "explanation": "పైపులో నీటి ప్రవాహం ఎక్కువై ట్యాప్ చిన్నదైతే వెనక్కి ఒత్తిడి (Backpressure) వస్తుంది. సాఫ్ట్‌వేర్‌లో కూడా వేగంగా ప్రొడ్యూస్ చేసే వైపుకు 'నేను తీసుకోలేకపోతున్నాను, కొంచెం నెమ్మదించు' అని సిగ్నల్ పంపాలి. TCP విండో సైజ్ (TCP Windowing) లో ఇది సహజంగా ఉంటుంది. అప్లికేషన్ లెవెల్‌లో Reactive Streams (RxJava, Project Reactor, Go Channels) ఈ ఫ్లో కంట్రోల్‌ను అమలు చేస్తాయి. కన్స్యూమర్ తనకు కావాల్సిన బ్యాచ్ సైజును మాత్రమే రిక్వెస్ట్ చేస్తుంది (Pull-based demand).",
        "example": """# Python AsyncIO Queue Backpressure కాన్సెప్ట్
import asyncio

async def consumer(queue):
    while True:
        item = await queue.get()
        await asyncio.sleep(0.1)  # నెమ్మదిగా ప్రాసెస్ చేస్తుంది (10 items/sec)
        queue.task_done()

async def producer(queue):
    for i in range(100):
        # maxsize=5 ఉన్న క్యూ నిండిపోతే producer ఇక్కడే ఆగిపోతుంది (Backpressure!)
        await queue.put(f"item_{i}")
        print(f"Produced item_{i} (Queue size: {queue.qsize()})")

async def main():
    q = asyncio.Queue(maxsize=5) # కేవలం 5 ఐటమ్స్ మాత్రమే బఫర్
    asyncio.create_task(consumer(q))
    await producer(q)""",
        "mistake": "అన్‌బౌండెడ్ క్యూలు (Unbounded In-memory Queues without size limit) వాడటం; ప్రొడ్యూసర్ వేగం పెరిగినప్పుడు మెమరీ మొత్తం నిండిపోయి ప్రాసెస్ కిల్ అవుతుంది."
    },
    {
        "title": "Adaptive Concurrency Control (Dynamic Request Concurrency)",
        "subtitle": "అడాప్టివ్ కాన్‌కరెన్సీ కంట్రోల్ (సర్వర్ పరిస్థితిని బట్టి ఏకకాలంలో అనుమతించే రిక్వెస్టుల సంఖ్యను డైనమిక్‌గా మార్చడం)",
        "why": "సర్వర్‌కు 'గరిష్టంగా 100 కనెక్షన్లు' అని స్టాటిక్ లిమిట్ పెడితే, నెట్‌వర్క్ బాగున్నప్పుడు అది తక్కువ కావచ్చు, లేదా డేటాబేస్ స్లో అయినప్పుడు ఆ 100 కూడా చాలా ఎక్కువై సర్వర్ చనిపోవచ్చు.",
        "explanation": "నెట్‌ఫ్లిక్స్ రూపొందించిన కాన్సెప్ట్ ఇది (TCP Vegas అల్గారిథమ్ ఆధారంగా). సర్వర్ తన ప్రస్తుత లాటెన్సీని నిరంతరం కొలుస్తుంది. లాటెన్సీ తక్కువగా ఉన్నప్పుడు కాన్‌కరెన్సీ లిమిట్‌ను క్రమంగా పెంచుకుంటూ వెళ్తుంది (Additively increase). ఒకవేళ లాటెన్సీ పెరగడం ప్రారంభమైతే లేదా క్యూయింగ్ కనిపిస్తే, సర్వర్ వెంటనే గరిష్ట కనెక్షన్ల సంఖ్యను తగ్గించివేస్తుంది (Multiplicatively decrease). దీనివల్ల సర్వర్ ఏ స్థితిలోనూ ఓవర్‌లోడ్ అవ్వదు.",
        "example": """# TCP Vegas తరహా Adaptive Concurrency Limiter
class AdaptiveLimiter:
    def __init__(self, initial_limit=20):
        self.limit = initial_limit
        self.min_rtt = float('inf')

    def update(self, current_rtt):
        self.min_rtt = min(self.min_rtt, current_rtt)
        # లాటెన్సీ సాధారణం కంటే 20% పెరిగితే లిమిట్ తగ్గించాలి
        if current_rtt > self.min_rtt * 1.2:
            self.limit = max(5, int(self.limit * 0.8)) # 20% తగ్గించడం
            print(f"⚠️ క్యూయింగ్ గుర్తించబడింది! నయా కాన్‌కరెన్సీ లిమిట్: {self.limit}")
        else:
            self.limit += 1 # సామర్థ్యం బాగుంది, +1 పెంచడం

limiter = AdaptiveLimiter(20)
limiter.update(current_rtt=15) # బాగుంది -> limit 21
limiter.update(current_rtt=45) # స్లో అయింది -> limit తగ్గుతుంది""",
        "mistake": "ఉత్పత్తి వాతావరణంలో ఫిక్స్‌డ్ హార్డ్‌కోడెడ్ థ్రెడ్ పూల్ లిమిట్స్ వాడటం; డైనమిక్ క్లౌడ్ వాతావరణంలో అడాప్టివ్ లిమిట్స్ లేకుండా మైక్రోసర్వీసెస్ నిలబడలేవు."
    },
    {
        "title": "Load Shedding (Dropping Requests Under Heavy Overload)",
        "subtitle": "లోడ్ షెడ్డింగ్ (సర్వర్ మునిగిపోతున్నప్పుడు ప్రాణాలను కాపాడుకోవడానికి కొన్ని రిక్వెస్టులను ముందే తిరస్కరించడం)",
        "why": "ఒక పడవలో 10 మంది పట్టే చోట 50 మంది ఎక్కితే అందరూ మునిగిపోతారు; 10 మందిని ఎక్కించుకుని మిగిలిన 40 మందికి 'నో' చెబితే కనీసం ఆ 10 మంది ప్రాణాలైనా దక్కుతాయి.",
        "explanation": "సర్వర్ పై విపరీతమైన ట్రాఫిక్ స్పైక్ వచ్చినప్పుడు, అన్ని రిక్వెస్టులను స్వీకరించి అందరికీ 30 సెకన్ల టైమౌట్ లేదా 500 ఎర్రర్ ఇవ్వడం కంటే, సర్వర్ తన సామర్థ్యానికి మించిన రిక్వెస్టులను వెంటనే '503 Service Unavailable' హెడర్ తో తక్షణం డ్రాప్ (Shed) చేయాలి. దీనివల్ల లోపల ఉన్న రిక్వెస్ట్‌లు మెరుపు వేగంతో ముగుస్తాయి. ముఖ్యంగా, తక్కువ ప్రాధాన్యత ఉన్న పనులను (Analytics, Recommendations, Notifications) ముందుగా డ్రాప్ చేసి, ముఖ్యమైన పేమెంట్స్, చెక్‌అవుట్ రిక్వెస్ట్‌లను కాపాడతారు.",
        "example": """# CPU & క్యూ ఆధారిత Load Shedding మిడిల్‌వేర్
class LoadSheddingMiddleware:
    def __init__(self, max_queue_depth=50):
        self.max_queue_depth = max_queue_depth
        self.current_queue = 0

    def handle_request(self, request, priority="LOW"):
        if self.current_queue > self.max_queue_depth:
            # అధిక లోడ్ లో ఉన్నప్పుడు LOW ప్రయారిటీ రిక్వెస్టులను వెంటనే డ్రాప్ చేయడం
            if priority == "LOW":
                return {"status": 503, "body": "Load Shed: సర్వర్ బిజీగా ఉంది. దయచేసి మళ్లీ ప్రయత్నించండి."}
        
        self.current_queue += 1
        try:
            return self.process(request)
        finally:
            self.current_queue -= 1""",
        "mistake": "లోడ్ షెడ్ చేసేటప్పుడు కూడా భారీ CPU ప్రాసెసింగ్ చేసి చివర్లో రిజెక్ట్ చేయడం; గేట్‌వే లేదా రివర్స్ ప్రాక్సీ లెవెల్ లోనే అతి తక్కువ మైక్రోసెకన్లలో రిక్వెస్ట్ ను డ్రాప్ చేయాలి."
    },
    {
        "title": "Cache Stampede (Simultaneous Cache Misses / Thundering Herd)",
        "subtitle": "క్యాష్ స్టాంపీడ్ (ఒకేసారి క్యాష్ ఎక్స్‌పైర్ అవ్వగానే లక్షలాది రిక్వెస్టులు ఒకేసారి డేటాబేస్ పై దాడి చేయడం)",
        "why": "హోమ్‌పేజీ క్యాష్ కీ సరిగ్గా 10:00:00 AM కి ఎక్స్‌పైర్ అయింది. అదే సెకనులో వచ్చిన 50,000 మంది యూజర్లు క్యాష్ మిస్ అయ్యి అందరూ కలిసి ఒకేసారి MySQL పై ఆ క్వెరీ రన్ చేస్తే డేటాబేస్ అక్కడికక్కడే చస్తుంది.",
        "explanation": "దీన్ని Thundering Herd Problem అని కూడా అంటారు. పరిష్కారాలు: \n1. Mutex Locking / Singleflight: క్యాష్ మిస్ అయినప్పుడు మొదటి ఒక్క రిక్వెస్ట్ మాత్రమే డేటాబేస్‌కు వెళ్తుంది; మిగిలిన 49,999 రిక్వెస్టులు ఆ ఒక్కటి తెచ్చే క్యాష్ కోసం వేచి ఉంటాయి (Go లో `singleflight`, Laravel లో `Cache::lock`). \n2. Probabilistic Early Expiration (XFetch algorithm): కీ పూర్తిగా గడువు ముగిసే ముందే, ట్రాఫిక్‌ను బట్టి సంభావ్యత ఆధారంగా (Probability) ఏదో ఒక రిక్వెస్ట్ బ్యాక్‌గ్రౌండ్ లో క్యాష్‌ను ముందే రీఫ్రెష్ చేస్తుంది.",
        "example": """# Singleflight పద్ధతిలో Cache Stampede నివారణ
import threading
import time

locks = {}
cache = {"home_data": "Old Cached Content", "expiry": time.time() + 1}

def get_home_data():
    if time.time() < cache["expiry"]:
        return cache["home_data"]

    # క్యాష్ ఎక్స్‌పైర్ అయింది - ఒక్క థ్రెడ్ మాత్రమే DB కి వెళ్లాలి
    with locks.setdefault("home_key_lock", threading.Lock()):
        # Double-check lock
        if time.time() < cache["expiry"]:
            return cache["home_data"]

        print("🔍 ఒక్కసారి మాత్రమే డేటాబేస్ నుండి లోడ్ అవుతోంది...")
        fresh_data = "Fresh Data from MySQL"
        cache["home_data"] = fresh_data
        cache["expiry"] = time.time() + 60
        return fresh_data""",
        "mistake": "అన్ని క్యాష్ కీలకు ఒకే విధమైన గడువు (ఉదా: సరిగ్గా 600 సెకన్లు) పెట్టడం; దానికి బదులు కొద్దిగా రాండమ్ జిట్టర్ (ఉదా: 600 + random(1, 60)) కలిపితే అన్ని కీలు ఒకే క్షణంలో ఎక్స్‌పైర్ కావు."
    },
    {
        "title": "Cache Coherence (Multi-Level Cache Consistency)",
        "subtitle": "క్యాష్ కోహెరెన్స్ (లోకల్ మెమరీ క్యాష్ మరియు సెంట్రల్ రెడిస్ క్యాష్ ల మధ్య సమానత్వాన్ని కాపాడటం)",
        "why": "అతి వేగం కోసం సర్వర్ లోకల్ RAM లో (L1 Cache) డేటా ఉంచారు, సెంట్రల్ Redis లో (L2 Cache) కూడా ఉంచారు. ఒక సర్వర్‌లో యూజర్ ప్రొఫైల్ మారినప్పుడు మిగిలిన 10 సర్వర్ల లోకల్ మెమరీలో ఉన్న పాత డేటా ఇన్వాలిడేట్ అవ్వాలి.",
        "explanation": "హార్డ్‌వేర్ CPU కోర్లలో MESI (Modified, Exclusive, Shared, Invalid) ప్రోటోకాల్ లాగా, డిస్ట్రిబ్యూటెడ్ సాఫ్ట్‌వేర్‌లో Pub/Sub ఆధారిత క్యాష్ ఇన్వాలిడేషన్ వాడుతారు. Redis 6+ లో 'Client-side Caching' ఫీచర్ వచ్చింది. ఒక సర్వర్‌లో డేటాబేస్ రికార్డు అప్‌డేట్ అయినప్పుడు, Redis ఆటోమేటిక్ గా అన్ని అప్లికేషన్ సర్వర్లకు ఒక ఇన్వాలిడేషన్ మెసేజ్ పంపి వాటి లోకల్ మెమరీ లోని పాత కీలను క్లియర్ చేస్తుంది.",
        "example": """# Redis Pub/Sub ఆధారిత Local Cache Invalidation
def update_product_price(product_id, new_price):
    # 1. DB అప్‌డేట్ & Redis అప్‌డేట్
    db.update("UPDATE products SET price = ? WHERE id = ?", [new_price, product_id])
    redis.set(f"product:{product_id}", new_price)

    # 2. అన్ని అప్లికేషన్ సర్వర్ల లోకల్ RAM క్యాష్‌లను క్లియర్ చేయడానికి బ్రాడ్‌కాస్ట్
    redis.publish("cache_invalidation_channel", product_id)
    print(f"Product {product_id} క్యాష్ ఇన్వాలిడేషన్ సిగ్నల్ పంపబడింది")""",
        "mistake": "లోకల్ మెమరీ క్యాష్ (In-memory APCu లేదా static variable) కి TTL (Time-to-live) పెట్టకపోవడం; ఇన్వాలిడేషన్ మెసేజ్ మిస్ అయితే ఆ సర్వర్ శాశ్వతంగా పాత డేటాను చూపిస్తుంది."
    },
    {
        "title": "Zero-Copy Networking (Avoiding Memory Copies)",
        "subtitle": "జీరో-కాపీ నెట్‌వర్కింగ్ (డిస్క్ నుండి నెట్‌వర్క్‌కు ఫైల్స్ పంపేటప్పుడు CPU మరియు RAM కాపీలను తప్పించడం)",
        "why": "వీడియో స్ట్రీమింగ్ (Netflix) లేదా పెద్ద ఫైల్స్ డౌన్‌లోడ్ చేసేటప్పుడు సాంప్రదాయ పద్ధతిలో 4 సార్లు మెమరీ కాపీలు మరియు 4 సార్లు Context Switches జరిగి CPU అంతా డేటా కాపీలకే సరిపోతుంది.",
        "explanation": "సాధారణ పద్ధతి: Disk -> OS Kernel Buffer -> User Space App Buffer -> OS Socket Buffer -> NIC (Network Card). \nZero-Copy పద్ధతి: Linux `sendfile()` లేదా `splice()` సిస్టమ్ కాల్ వాడటం. ఇందులో డేటా యూజర్ స్పేస్ (User Application RAM) లోకి అసలు రానే రాదు! డైరెక్ట్ మెమరీ యాక్సెస్ (DMA) ద్వారా డిస్క్ కంట్రోలర్ నుండి నేరుగా నెట్‌వర్క్ కార్డ్ బఫర్‌కు డేటా బదిలీ అవుతుంది. Nginx, Kafka లు భారీ త్రూపుట్ సాధించడానికి ఈ జీరో-కాపీ టెక్నాలజీనే ప్రధాన కారణం.",
        "example": """# Python లో Linux sendfile (Zero-Copy) వినియోగం
import os

def send_large_file_zero_copy(file_fd, socket_fd, file_size):
    # OS లెవెల్ జీరో-కాపీ ట్రాన్స్‌ఫర్ (RAM లోకి కాపీ అవ్వదు)
    bytes_sent = os.sendfile(socket_fd, file_fd, 0, file_size)
    print(f"మెరుపు వేగంతో {bytes_sent} బైట్లు నెట్‌వర్క్‌కు పంపబడ్డాయి (Zero-Copy)!")""",
        "mistake": "పెద్ద ఫైల్స్ పంపేటప్పుడు PHP/Python లో `file_get_contents()` లేదా `read()` వాడి మొత్తం ఫైల్‌ను యూజర్ మెమరీ లోకి లోడ్ చేయడం; సర్వర్ మెమరీ క్షణాల్లో అయిపోతుంది."
    },
    {
        "title": "Connection Multiplexing (Shared Network Connections)",
        "subtitle": "కనెక్షన్ మల్టీప్లెక్సింగ్ (వందల రిక్వెస్టుల కోసం వందల కనెక్షన్లు తెరవకుండా ఒకే TCP కనెక్షన్‌ను పంచుకోవడం)",
        "why": "ప్రతి HTTP/1.1 రిక్వెస్ట్‌కు కొత్త TCP హ్యాండ్‌షేక్ మరియు TLS నెగోషియేషన్ చేస్తే నెట్‌వర్క్ లాటెన్సీ మరియు సర్వర్ సాకెట్ పోర్ట్స్ దండగ.",
        "explanation": "HTTP/2, HTTP/3 మరియు gRPC లలో కనెక్షన్ మల్టీప్లెక్సింగ్ ప్రధాన ఫీచర్. ఒకే ఒక్క TCP కనెక్షన్ పైనే సమాంతరంగా బహుళ బైడైరెక్షనల్ స్ట్రీమ్స్ (Streams with Stream IDs) ద్వారా డేటా ఫ్రేమ్స్ వెళ్తాయి. ఒక రిక్వెస్ట్ స్లో అయినా పక్క స్ట్రీమ్‌లోని వేరే రిక్వెస్ట్ వేగంగా వెళ్లిపోతుంది (No Head-of-line blocking at application layer). డేటాబేస్ సైడ్‌లో PgBouncer Transaction Pooling కూడా కనెక్షన్ మల్టీప్లెక్సింగ్ సూత్రంపైనే పనిచేస్తుంది.",
        "example": """# HTTP/1.1 vs HTTP/2 కనెక్షన్ పోలిక
# HTTP/1.1:
# [Req 1] ---> [Wait Res 1] ---> [Req 2] ---> [Wait Res 2] (లేదా 6 వేర్వేరు TCP కనెక్షన్లు)

# HTTP/2 Multiplexing (ఒకే TCP కనెక్షన్ లో):
# Stream 1: [Req 1 Frame] -------> [Res 1 Frame]
# Stream 3: ----> [Req 2 Frame] -> [Res 2 Frame]
# Stream 5: -------> [Req 3 Frame] --------> [Res 3 Frame]""",
        "mistake": "HTTP/2 వాడినా ప్యాకెట్ లాస్ ఎక్కువగా ఉన్న వైఫై/మొబైల్ నెట్‌వర్క్‌లలో TCP లెవెల్ Head-of-line blocking వస్తుంది; దాని కోసం QUIC / HTTP/3 (UDP-based) వాడాలి."
    },
    {
        "title": "Memory Fragmentation (Allocation Inefficiencies)",
        "subtitle": "మెమరీ ఫ్రాగ్మెంటేషన్ (సర్వర్‌లో 10GB ఖాళీ ఉన్నా కూడా మెమరీ ముక్కలై పెద్ద ఆబ్జెక్ట్‌కు స్థలం దొరక్కపోవడం)",
        "why": "మీ అప్లికేషన్ 3 రోజులు నడిచిన తర్వాత మెమరీ యూసేజ్ భారీగా పెరిగిపోయి చివరకు క్రాష్ అవుతుంది; రీస్టార్ట్ చేస్తే మళ్లీ సాధారణ స్థితికి వస్తుంది.",
        "explanation": "మెమరీలో చిన్న పెద్ద వేలాది ఆబ్జెక్ట్‌లను అలొకేట్ చేసి, డిలీట్ చేసినప్పుడు మధ్య మధ్యలో ఖాళీ గ్యాప్‌లు (Holes) ఏర్పడతాయి. \n1. External Fragmentation: మొత్తం ఖాళీ స్థలం చాలా ఉంటుంది కానీ ఒక పెద్ద 10MB కంటిగ్యువస్ అర్రే కి సరిపోయేంత పెద్ద సింగిల్ బ్లాక్ ఉండదు. \n2. Internal Fragmentation: 33 బైట్ల డేటా కోసం ఆపరేటింగ్ సిస్టమ్ 64 బైట్ల బ్లాక్‌ను కేటాయించడం వల్ల మిగిలిన స్థలం వృధా అవ్వడం. \nRedis మరియు హై-పర్ఫార్మెన్స్ C++/Go సర్వీసులలో డీఫాల్ట్ `glibc malloc` స్థానంలో ఫ్రాగ్మెంటేషన్‌ను అద్భుతంగా నివారించే `jemalloc` లేదా `tcmalloc` మెమరీ అలొకేటర్లను వాడుతారు.",
        "example": """# Redis లో ఫ్రాగ్మెంటేషన్ రేషియో పరిశీలన
'''bash
redis-cli INFO memory
# mem_fragmentation_ratio చూడండి:
# 1.0 - 1.5 మధ్య ఉంటే: అద్భుతం.
# > 1.8 ఉంటే: తీవ్రమైన మెమరీ ఫ్రాగ్మెంటేషన్ ఉంది! (RAM వృధా అవుతోంది)
# ఆన్‌లైన్ లో డీఫ్రాగ్మెంట్ చేయడం:
redis-cli CONFIG SET activedefrag yes
''' """,
        "mistake": "మెమరీ ఫ్రాగ్మెంటేషన్‌ను మెమరీ లీక్ (Memory Leak) అనుకోవడం; లీక్‌లో ఆబ్జెక్ట్స్ రిఫరెన్స్ మిగిలిపోతాయి, ఫ్రాగ్మెంటేషన్‌లో ఆపరేటింగ్ సిస్టమ్ పేజింగ్ సమస్య వస్తుంది."
    },
    {
        "title": "CPU Profiling (Hotspot Identification & Flame Graphs)",
        "subtitle": "CPU ప్రొఫైలింగ్ (కోడ్‌లో CPU సమయాన్ని మింగేస్తున్న అసలైన విలన్ ఫంక్షన్‌ను ఫ్లేమ్ గ్రాఫ్‌తో పట్టుకోవడం)",
        "why": "డెవలపర్లు తరచూ 'ఈ లూప్ వల్ల స్లో అవుతోంది' అని తప్పుడు ఊహలతో అసలైన సమస్యను వదిలేసి అనవసరమైన కోడ్‌ను ఆప్టిమైజ్ చేస్తారు.",
        "explanation": "బ్రెండన్ గ్రెగ్ (Brendan Gregg) కనిపెట్టిన Flame Graphs CPU ప్రొఫైలింగ్‌లో విప్లవం సృష్టించాయి. Linux `perf`, Python `cProfile` లేదా Go `pprof` టూల్స్ సెకనుకు వందలాది సార్లు కాల్ స్టాక్‌ను శాంప్లింగ్ చేస్తాయి. ఫ్లేమ్ గ్రాఫ్‌లో వెడల్పుగా ఉన్న బాక్సులు (Horizontal width) ఎక్కువ CPU సమయాన్ని తింటున్న హాట్‌స్పాట్ ఫంక్షన్లను సూచిస్తాయి. ఆ వెడల్పు బాక్సులను పట్టుకుని ఆప్టిమైజ్ చేస్తే 80% పనితీరు మెరుగుపడుతుంది.",
        "example": """# Python లో cProfile ద్వారా హాట్‌స్పాట్ కనిపెట్టడం
import cProfile
import pstats

def slow_json_serializer():
    import json
    data = [{"id": i, "val": "test"} for i in range(100000)]
    return json.dumps(data)

profiler = cProfile.Profile()
profiler.enable()
slow_json_serializer()
profiler.disable()

stats = pstats.Stats(profiler).sort_stats('cumtime')
stats.print_stats(5) # అత్యధిక సమయం తీసుకున్న టాప్ 5 ఫంక్షన్ల ప్రింట్""",
        "mistake": "ప్రొడక్షన్ లో ఇన్వాసివ్ ట్రేసింగ్ ప్రొఫైలర్లు రన్ చేయడం; శాంప్లింగ్ ప్రొఫైలర్లు (Sampling profilers with <1% overhead) మాత్రమే ప్రొడక్షన్ లో వాడాలి."
    },
    {
        "title": "Lock Contention (Thread Synchronization Bottlenecks)",
        "subtitle": "లాక్ కంటెన్షన్ (ఒకే తాళం చెవి కోసం వందలాది థ్రెడ్స్ కొట్టుకుంటూ సమయం వృధా చేసుకోవడం)",
        "why": "సర్వర్‌కు 64 CPU Cores ఉన్నప్పటికీ, కోడ్‌లో ఉన్న ఒకే ఒక్క Mutex Lock వల్ల అన్ని కోర్లు ఖాళీగా ఉండి కేవలం ఒక్క కోర్ మాత్రమే పనిచేస్తుంది.",
        "explanation": "ఒక షేర్డ్ వేరియబుల్ లేదా రిసోర్స్‌ను రక్షించడానికి ఒకే లాక్ (Mutex) పెట్టినప్పుడు, బహుళ థ్రెడ్స్ ఆ లాక్ దొరక్క నిద్రపోతాయి (Blocking / Context Switching) లేదా నిరంతరం చెక్ చేస్తూ CPU ని వేస్ట్ చేస్తాయి (Spinlocks). \nపరిష్కారాలు: \n1. Lock Striping: ఒకే లాక్ బదులు 16 వేర్వేరు విభాగాలకు 16 వేర్వేరు లాక్స్ పెట్టడం (ఉదా: Java `ConcurrentHashMap`). \n2. Lock-Free Data Structures: లాక్స్ లేకుండా CPU యొక్క అటామిక్ హార్డ్‌వేర్ ఇన్‌స్ట్రక్షన్లను (CAS - Compare-And-Swap) వాడటం.",
        "example": """# Lock Contention vs Lock Striping కాన్సెప్ట్
# బ్యాడ్ విధానం: మొత్తం క్యాష్ డిక్షనరీ కి ఒకే గ్లోబల్ మ్యూటెక్స్
# lock.acquire() -> dict[key] = val -> lock.release()

# గుడ్ విధానం: Lock Striping (16 బకెట్లు, 16 ప్రత్యేక లాక్స్)
class StripedCache:
    def __init__(self, num_stripes=16):
        import threading
        self.stripes = [{} for _ in range(num_stripes)]
        self.locks = [threading.Lock() for _ in range(num_stripes)]

    def set(self, key, value):
        bucket = hash(key) % len(self.stripes)
        with self.locks[bucket]: # కేవలం ఈ ఒక్క బకెట్ లాక్ మాత్రమే తీసుకుంటుంది!
            self.stripes[bucket][key] = value""",
        "mistake": "క్రిటికల్ సెక్షన్ (Lock లోపల ఉండే కోడ్) లోపల నెట్‌వర్క్ HTTP కాల్స్ లేదా డిస్క్ I/O చేయడం; లాక్ హోల్డింగ్ టైమ్ పెరిగి మొత్తం సర్వర్ ఫ్రీజ్ అవుతుంది."
    },
    {
        "title": "NUMA Awareness (Non-Uniform Memory Access)",
        "subtitle": "నూమా అవేర్‌నెస్ (మల్టీ-సాకెట్ సర్వర్లలో సమీపంలోని RAM ని మాత్రమే వాడటం ద్వారా మెమరీ లాటెన్సీని తగ్గించడం)",
        "why": "రెండు లేదా నాలుగు ఫిజికల్ CPU ప్రాసెసర్లు ఉన్న భారీ సర్వర్లలో మెమరీ యాక్సెస్ వేగం ఒక్కోసారి సగానికి పడిపోతుంది.",
        "explanation": "ఆధునిక పెద్ద సర్వర్లలో ప్రతి CPU సాకెట్‌కు దాని స్వంత లోకల్ RAM ఉంటుంది (NUMA Node). CPU 1 తన పక్కనే ఉన్న Local RAM ని చదివితే కేవలం 50 నానోసెకన్లు పడుతుంది; కానీ మదర్‌బోర్డ్ బస్సు (QPI/UPI Interconnect) దాటి పక్కనున్న CPU 2 యొక్క Remote RAM ని చదివితే 150-200 నానోసెకన్లు పడుతుంది (3 రెట్లు ఆలస్యం!). NUMA-aware అప్లికేషన్లు ప్రాసెస్‌ను మరియు దానికి కేటాయించిన మెమరీని ఒకే NUMA నోడ్‌కు కట్టేస్తాయి (CPU Core Affinity / `numactl`). డేటాబేస్, హై-ఫ్రీక్వెన్సీ ట్రేడింగ్ సిస్టమ్స్‌లో ఇది తప్పనిసరి.",
        "example": """# Linux లో NUMA స్టేటస్ చూడటం మరియు బైండ్ చేయడం
'''bash
# సర్వర్ లోని NUMA నోడ్స్ వివరాలు
numactl --hardware

# MySQL లేదా నిర్దిష్ట సర్వీసును లోకల్ NUMA నోడ్ 0 కి మాత్రమే బైండ్ చేసి నడపడం:
numactl --cpunodebind=0 --membind=0 mysqld
''' """,
        "mistake": "MySQL లో `innodb_numa_interleave` ఆన్ చేయకపోవడం; భారీ మల్టీ-సాకెట్ సర్వర్లలో ఒకే నోడ్ RAM నిండిపోయి స్వాపింగ్ (Swapping) కి వెళ్లి DB హ్యాంగ్ అవుతుంది."
    },
    {
        "title": "Kernel Bypass (High-Performance Networking & DPDK)",
        "subtitle": "కెర్నల్ బైపాస్ (ఆపరేటింగ్ సిస్టమ్ నెట్‌వర్క్ స్టాక్ ఆలస్యాన్ని తప్పించి నేరుగా నెట్‌వర్క్ కార్డ్ తో మాట్లాడటం)",
        "why": "సాధారణ లైనక్స్ కెర్నల్ నెట్‌వర్క్ స్టాక్ సెకనుకు గరిష్టంగా 1 మిలియన్ ప్యాకెట్లను మాత్రమే హ్యాండిల్ చేయగలదు; 100Gbps నెట్‌వర్క్‌లలో సెకనుకు 50 మిలియన్ ప్యాకెట్లను ప్రాసెస్ చేయడానికి కెర్నల్ చాలా నెమ్మది.",
        "explanation": "కెర్నల్ బైపాస్ టెక్నాలజీలు (DPDK - Data Plane Development Kit, Solarflare OpenOnload, eBPF XDP) లైనక్స్ నెట్‌వర్క్ స్టాక్‌ను పూర్తిగా పక్కన పెడతాయి. నెట్‌వర్క్ కార్డ్ (NIC) నుండి వచ్చే ప్యాకెట్లు ఆపరేటింగ్ సిస్టమ్ కెర్నల్, ఇంట్రప్ట్స్, కాంటెక్స్ట్ స్విచ్‌లు లేకుండా నేరుగా యూజర్ స్పేస్ అప్లికేషన్ మెమరీ లోకి వస్తాయి. లాటెన్సీ మైక్రోసెకన్ల నుండి నానోసెకన్లకు పడిపోతుంది. క్లౌడ్ గేట్‌వేలు, CDN ఎడ్జ్ ప్రాక్సీలు మరియు హై-స్పీడ్ నెట్‌వర్కింగ్ లో దీన్ని వాడుతారు.",
        "example": """# కెర్నల్ బైపాస్ కాన్సెప్ట్ ఫ్లో
# సాంప్రదాయ మార్గం:
# Network Packet -> NIC -> Hardware Interrupt -> Linux Kernel TCP/IP Stack -> Socket Buffer -> User App (Slow)

# Kernel Bypass (DPDK / XDP):
# Network Packet -> NIC -> Direct Memory Access (DMA) -> User App RAM! (Zero Context Switch, Blazing Fast)""",
        "mistake": "సాధారణ వెబ్ యాప్‌లకు కెర్నల్ బైపాస్ అవసరం అనుకోవడం; కెర్నల్ బైపాస్ వాడితే లైనక్స్ ఇచ్చే ఫైర్‌వాల్ (iptables), సాధారణ నెట్‌వర్క్ టూల్స్ పనిచేయవు."
    }
]
