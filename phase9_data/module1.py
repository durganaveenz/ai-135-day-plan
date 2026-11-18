# Module 1: Advanced Distributed Systems (15 topics)

topics = [
    {
        "title": "Consensus Algorithms (Raft, Paxos, Leader Election)",
        "subtitle": "కన్సెన్సస్ అల్గారిథమ్స్ (నెట్‌వర్క్‌లోని సర్వర్లన్నీ ఒకే లీడర్‌పై ఏకాభిప్రాయానికి రావడం)",
        "why": "డిస్ట్రిబ్యూటెడ్ సిస్టమ్‌లలో ఒకే సమయంలో పలు సర్వర్లు పనిచేస్తాయి. నెట్‌వర్క్ ఫెయిల్యూర్‌లు లేదా సర్వర్ క్రాష్‌లు జరిగినప్పుడు కూడా సిస్టమ్ అంతా ఒకే నిజమైన లీడర్‌ను ఎన్నుకోవడానికి మరియు డేటా మార్పులపై అందరూ ఏకీభవించడానికి కన్సెన్సస్ అల్గారిథమ్స్ తప్పనిసరి.",
        "explanation": "PHP/Laravel లో సాధారణంగా ఒకే MySQL Master లేదా ఒక Redis instance ఉంటుంది కాబట్టి ఏది లీడర్ అనే గందరగోళం ఉండదు. కానీ Spanner, Etcd, Consul, Kafka వంటి డిస్ట్రిబ్యూటెడ్ సిస్టమ్స్‌లో 5 సర్వర్లు ఉంటే, వాటిలో ఏది 'Leader' కావాలి, ఏవి 'Followers' కావాలి అని తేల్చడానికి Paxos లేదా Raft ని వాడుతారు. Raft లో ప్రతి సర్వర్ 3 స్థితులలో (Leader, Follower, Candidate) ఉంటుంది. లీడర్ నుండి Heartbeat రావడం ఆగితే Follower లు Candidate గా మారి Election Timeout తో ఓట్లు అడుగుతాయి. మెజారిటీ (Quorum: (N/2)+1) ఓట్లు వచ్చిన నోడ్ కొత్త Leader గా మారుతుంది.",
        "example": """# Raft Leader Election సిమ్యులేషన్ ఉదాహరణ
class RaftNode:
    def __init__(self, node_id, total_nodes):
        self.node_id = node_id
        self.state = "Follower"  # ప్రారంభంలో అందరూ Followers
        self.term = 0
        self.votes = 0
        self.total_nodes = total_nodes

    def heartbeat_timeout(self):
        # లీడర్ నుండి సిగ్నల్ రాకపోతే Candidate గా మారి ఓటింగ్ మొదలుపెడుతుంది
        self.state = "Candidate"
        self.term += 1
        self.votes = 1  # తనకు తానే ఓటు వేసుకుంటుంది
        print(f"Node {self.node_id} Candidate గా మారింది for Term {self.term}")
        
    def request_vote(self, from_node):
        majority = (self.total_nodes // 2) + 1  # 5 నోడ్స్‌కు కనీసం 3 ఓట్లు
        self.votes += 1
        if self.votes >= majority:
            self.state = "Leader"
            print(f"🎉 Node {self.node_id} లీడర్ అయింది! (ఓట్లు: {self.votes}/{self.total_nodes})")

cluster = [RaftNode(i, 5) for i in range(1, 6)]
cluster[0].heartbeat_timeout()
cluster[0].request_vote(2)
cluster[0].request_vote(3)  # 3వ ఓటు రాగానే Leader అవుతుంది""",
        "mistake": "Raft క్లస్టర్‌లో ఎల్లప్పుడూ బేసి సంఖ్యలో (Odd number: 3, 5, 7) మాత్రమే నోడ్స్ ఉండాలి; సరి సంఖ్య (4 లేదా 6) పెడితే నెట్‌వర్క్ విభజన జరిగినప్పుడు సమాన ఓట్లతో టై (Split-vote) ఏర్పడుతుంది."
    },
    {
        "title": "Distributed Transactions (2PC, 3PC, Transaction Coordinator)",
        "subtitle": "డిస్ట్రిబ్యూటెడ్ ట్రాన్సాక్షన్స్ (బహుళ సర్వర్లలో అటామిక్ కమిట్ సాధించడం)",
        "why": "ఒక ఆర్డర్ ప్లేస్ అయినప్పుడు Order Service (MySQL), Payment Service (Postgres), Inventory Service (MongoDB) వంటి వేర్వేరు డేటాబేస్‌లలో డేటా సేవ్ అవ్వాలి. ఏ ఒక్కటి ఫెయిలైనా మొత్తం ఆపరేషన్ రోల్‌బ్యాక్ కావాలి.",
        "explanation": "Laravel లో `DB::transaction()` కేవలం ఒకే డేటాబేస్ కనెక్షన్‌కు మాత్రమే గ్యారెంటీ ఇస్తుంది. బహుళ వేర్వేరు డేటాబేస్‌లు ఉన్నప్పుడు Two-Phase Commit (2PC) వాడుతారు. ఇందులో ఒక Transaction Coordinator ఉంటుంది. \nPhase 1 (Prepare Phase): కోఆర్డినేటర్ అన్ని పార్టిసిపెంట్ సర్వర్లకు 'మీరు కమిట్ చేయడానికి సిద్ధమా?' అని అడుగుతుంది. సర్వర్లు తమ డేటాను లాక్ చేసి 'VOTE_COMMIT' లేదా 'VOTE_ABORT' అని సమాధానమిస్తాయి. \nPhase 2 (Commit Phase): అందరూ సిద్ధమైతేనే 'GLOBAL_COMMIT' పంపుతుంది; ఒక్కరు తిరస్కరించినా 'GLOBAL_ABORT' పంపి అందరినీ రోల్‌బ్యాక్ చేస్తుంది. 3PC (Three-Phase Commit) లో Pre-Commit దశను చేర్చి నెట్‌వర్క్ బ్లాకింగ్‌ను తగ్గిస్తారు.",
        "example": """# 2-Phase Commit (2PC) ఆర్కిటెక్చర్ ఫ్లో
def run_2pc_transaction(coordinator, participants, tx_data):
    # Phase 1: Prepare
    prepared_ok = []
    for p in participants:
        status = p.prepare(tx_data)  # Resource Lock + WAL లో రాయడం
        if status == "PREPARED":
            prepared_ok.append(p)
        else:
            # ఒక్కటి ఫెయిల్ అయినా వెంటనే Abort చేయాలి
            coordinator.broadcast_rollback(prepared_ok)
            return "Transaction Aborted!"

    # Phase 2: Commit (అన్నీ ఆమోదించిన తర్వాతే)
    coordinator.broadcast_commit(participants)
    return "Transaction Committed Globally!" """,
        "mistake": "2PC లో కోఆర్డినేటర్ సర్వర్ Phase 1 తర్వాత క్రాష్ అయితే, ఇతర సర్వర్లన్నీ డేటాబేస్ లాక్స్‌ను పట్టుకుని శాశ్వతంగా బ్లాక్ (Blocking protocol) అయిపోతాయి; అందుకే ఆధునిక మైక్రోసర్వీసెస్‌లో 2PC బదులు Saga Pattern ని ఎక్కువగా వాడుతారు."
    },
    {
        "title": "Vector Clocks (Distributed Event Ordering)",
        "subtitle": "వెక్టర్ క్లాక్స్ (డిస్ట్రిబ్యూటెడ్ సిస్టమ్‌లలో ఈవెంట్ల మధ్య కారణ-ఫలిత సంబంధాన్ని గుర్తించడం)",
        "why": "డిస్ట్రిబ్యూటెడ్ సిస్టమ్‌లలో సర్వర్ల గడియారాలు (Wall-clock time) ఎప్పుడూ ఖచ్చితంగా సింక్ కావు (NTP drift). ఒక సర్వర్‌లో 10:00:01 సమయం ఉంటే, మరో సర్వర్‌లో 10:00:03 ఉండవచ్చు. కాబట్టి కేవలం timestamps చూసి ఏ ఈవెంట్ ముందు జరిగిందో చెప్పలేం.",
        "explanation": "Laravel లో మనం సాధారణంగా `created_at` timestamp ను నమ్ముతాం. కానీ Amazon DynamoDB లేదా Riak లాంటి మల్టీ-మాస్టర్ డిస్ట్రిబ్యూటెడ్ డేటాబేస్‌లలో వేర్వేరు డేటాసెంటర్ల నుండి ఒకే రికార్డ్‌పై అప్‌డేట్స్ వచ్చినప్పుడు ఏది ముందు, ఏది కాన్‌ఫ్లిక్ట్ అని కనిపెట్టడానికి Vector Clock వాడుతారు. ప్రతి సర్వర్ ఒక కౌంటర్ వెక్టర్‌ను (ఉదా: [NodeA: 1, NodeB: 0, NodeC: 2]) నిర్వహిస్తుంది. ఒక నోడ్ డేటాను మార్చినప్పుడల్లా తన స్థానాన్ని +1 పెంచుతుంది. మెసేజ్ అందినప్పుడు వేరే నోడ్ వెక్టర్ గమనించి, ఇది పాత డేటానా, కొత్తదా, లేదా ఏకకాలంలో జరిగిన మార్పా (Concurrent conflict) అని గుర్తిస్తుంది.",
        "example": """# Vector Clock కాన్‌ఫ్లిక్ట్ డిటెక్షన్
vc_server1 = {"A": 2, "B": 1}  # సర్వర్ 1 వెక్టర్
vc_server2 = {"A": 1, "B": 2}  # సర్వర్ 2 వెక్టర్

def compare_vector_clocks(v1, v2):
    # రెండు గడియారాల్లో ఒకదాని కన్నా మరొకటి స్పష్టంగా పెద్దది కాకపోతే Conflict ఉన్నట్లు
    v1_greater = any(v1[k] > v2[k] for k in v1)
    v2_greater = any(v2[k] > v1[k] for k in v2)
    
    if v1_greater and v2_greater:
        return "⚠️ CONCURRENT CONFLICT: అప్లికేషన్ మర్జ్ చేయాలి!"
    elif v1_greater:
        return "V1 కొత్తది (V1 succeeds V2)"
    return "V2 కొత్తది"

print(compare_vector_clocks(vc_server1, vc_server2))""",
        "mistake": "వెక్టర్ క్లాక్ సమయాన్ని (Time of day) కొలవదు; ఇది కేవలం ఈవెంట్ల మధ్య 'Causality' (దేని ప్రభావం వల్ల ఏది జరిగింది)ని మాత్రమే కొలుస్తుంది."
    },
    {
        "title": "Logical Clocks (Lamport Clock, Hybrid Logical Clock)",
        "subtitle": "లాజికల్ క్లాక్స్ (భౌతిక సమయంతో సంబంధం లేకుండా ఈవెంట్లను క్రమబద్ధీకరించడం)",
        "why": "సర్వర్ల భౌతిక క్లాక్ డ్రిఫ్ట్ వల్ల ఈవెంట్ లాగ్‌లు గజిబిజి కాకుండా, 'Event A definitely happened before Event B' అనే వరుస క్రమాన్ని స్థిరంగా లెక్కించడానికి లాజికల్ క్లాక్స్ కావాలి.",
        "explanation": "లెస్లీ లాంపోర్ట్ కనిపెట్టిన Lamport Clock ఒక సాధారణ పూర్ణాంకం (Integer Counter). ప్రతి నోడ్ ఈవెంట్ జరిగినప్పుడు తన కౌంటర్‌ను +1 పెంచుతుంది. ఒక నోడ్ మరొక నోడ్‌కు సందేశం పంపినప్పుడు తన ప్రస్తుత లాంపోర్ట్ టైమ్‌ను కూడా పంపుతుంది. అందుకున్న నోడ్ `max(local_clock, received_clock) + 1` చేసి తన కౌంటర్‌ను ముందుకు జరుపుతుంది. ఆధునిక కాక్‌రోచ్‌డీబీ (CockroachDB) మరియు Spanner వంటి డిస్ట్రిబ్యూటెడ్ DB లు Hybrid Logical Clock (HLC) ను వాడుతాయి. ఇది ఫిజికల్ టైమ్ (NTP) మరియు లాంపోర్ట్ కౌంటర్‌ల కలయిక.",
        "example": """# Lamport Logical Clock ఇంప్లిమెంటేషన్
class LamportClock:
    def __init__(self, node_name):
        self.node = node_name
        self.time = 0

    def local_event(self):
        self.time += 1
        print(f"[{self.node}] లోకల్ ఈవెంట్: టైమ్ = {self.time}")

    def send_message(self):
        self.time += 1
        print(f"[{self.node}] సందేశం పంపబడింది with Clock = {self.time}")
        return self.time

    def receive_message(self, sent_time):
        self.time = max(self.time, sent_time) + 1
        print(f"[{self.node}] సందేశం అందింది! అప్‌డేట్ అయిన క్లాక్ = {self.time}")

node_a = LamportClock("Server-A")
node_b = LamportClock("Server-B")

node_a.local_event()
msg_time = node_a.send_message()
node_b.receive_message(msg_time)""",
        "mistake": "లాంపోర్ట్ క్లాక్ రెండు ఈవెంట్లకు ఒకే టైమ్‌స్టాంప్ ఇస్తే, టై-బ్రేకర్ కోసం నోడ్ ఐడీ (Node ID) వాడతారు. అయితే, L(A) < L(B) అయినంత మాత్రాన A వలన B జరిగింది అని చెప్పలేం (దాని కోసం Vector Clocks వాడాలి)."
    },
    {
        "title": "Conflict-Free Replicated Data Types (CRDTs)",
        "subtitle": "CRDTs (సెంట్రల్ లాక్ లేకుండానే డేటా కాన్‌ఫ్లిక్ట్స్‌ను ఆటోమేటిక్‌గా పరిష్కరించే డేటా స్ట్రక్చర్స్)",
        "why": "Figma, Google Docs లాంటి కొలాబొరేటివ్ యాప్స్‌లో లేదా నెట్‌వర్క్ కనెక్షన్ పోయినప్పుడు ఆఫ్‌లైన్‌లో డేటా మార్చి తిరిగి ఆన్‌లైన్‌కి వచ్చినప్పుడు, సెంట్రల్ డేటాబేస్ లాక్స్ లేకుండానే అందరి డేటా ఒకేలా కలిసిపోవాలి (Eventual Consistency).",
        "explanation": "Laravel లో ఇద్దరు యూజర్లు ఒకే `posts` రికార్డ్‌ను ఒకేసారి అప్‌డేట్ చేస్తే లాస్ట్ రైటర్ విన్స్ (LWW) జరిగి ఒకరి డేటా పోతుంది. కానీ CRDT లు మ్యాథమెటికల్ ల్యాటిస్ (Semi-lattice) సూత్రంపై పనిచేస్తాయి. ఆపరేషన్లు ఏ క్రమంలో వచ్చినా (Commutative, Associative, Idempotent) కలిపినప్పుడు ఒకే తుది ఫలితం వస్తుంది. ఉదాహరణకు: Grow-only Counter (Pn-Counter), Observed-Removed Set (OR-Set). Redis 7+ లో కూడా CRDT ఆధారిత ఆటోమేటిక్ మల్టీ-రీజియన్ డేటా రెప్లికేషన్ అందుబాటులో ఉంది.",
        "example": """# Grow-only Set (G-Set) CRDT ఉదాహరణ
class GSetCRDT:
    def __init__(self):
        self.items = set()

    def add(self, element):
        self.items.add(element)

    def merge(self, other_gset):
        # రెండు నోడ్స్ డేటాను కలిపినా డూప్లికేట్స్ రావు, క్రమంతో సంబంధం లేదు
        self.items = self.items.union(other_gset.items)

node1 = GSetCRDT()
node2 = GSetCRDT()

node1.add("User_1_Like")
node2.add("User_2_Like")

# నెట్‌వర్క్ పునరుద్ధరించబడినప్పుడు Merge ఆపరేషన్
node1.merge(node2)
print("నోడ్ 1 ఫైనల్ స్టేట్:", node1.items)  # {'User_1_Like', 'User_2_Like'}""",
        "mistake": "CRDT లు కేవలం నిర్దిష్ట డేటా రకాలకు (Sets, Counters, Text Buffers) మాత్రమే పనిచేస్తాయి; సంక్లిష్టమైన Relational Foreign Key constraints ఉన్న డేటాకు CRDT లు నేరుగా సరిపోవు."
    },
    {
        "title": "Quorum-Based Systems (Read Quorum, Write Quorum)",
        "subtitle": "కోరం ఆధారిత వ్యవస్థలు (మెజారిటీ ఓటింగ్‌తో డేటా ఖచ్చితత్వాన్ని కాపాడటం)",
        "why": "డిస్ట్రిబ్యూటెడ్ డేటాబేస్‌లలో అన్ని సర్వర్లు ప్రతి క్షణం అందుబాటులో ఉండకపోవచ్చు. కొన్ని సర్వర్లు డౌన్ అయినా కూడా సరైన లేటెస్ట్ డేటాను మాత్రమే చదవడానికి Quorum ఫార్ములా అవసరం.",
        "explanation": "Amazon Dynamo, Apache Cassandra వంటి సిస్టమ్స్ ఈ విధానాన్ని వాడుతాయి. మొత్తం రెప్లికాస్ సంఖ్య $N$, రైట్ చేయాల్సిన నోడ్స్ $W$, రీడ్ చేయాల్సిన నోడ్స్ $R$ అనుకుంటే, స్ట్రాంగ్ కన్సిస్టెన్సీ కోసం నియమం: $R + W > N$. \nఉదాహరణకు 5 సర్వర్లు ($N=5$) ఉంటే, మనం కనీసం 3 సర్వర్లలో రాసి ($W=3$), 3 సర్వర్ల నుండి చదివితే ($R=3$), అప్పుడు $3 + 3 = 6 > 5$. కాబట్టి మనం చదివే 3 సర్వర్లలో కనీసం ఒక సర్వర్‌లో ఖచ్చితంగా అత్యంత తాజా రైట్ డేటా ఉంటుంది. దాన్ని టైమ్‌స్టాంప్ చూసి కనిపెట్టవచ్చు.",
        "example": """# Quorum కన్సిస్టెన్సీ చెకింగ్ లాజిక్
def is_strongly_consistent(N, W, R):
    if (W + R) > N:
        return f"✅ Strong Consistency గ్యారెంటీ! (W={W} + R={R} > N={N})"
    else:
        return f"⚠️ Weak/Eventual Consistency: పాత డేటా (Stale read) వచ్చే ప్రమాదం ఉంది!"

print(is_strongly_consistent(N=5, W=3, R=3)) # Strong
print(is_strongly_consistent(N=5, W=2, R=2)) # Weak (2+2 = 4 < 5)""",
        "mistake": "$W + R > N$ ఉంటే లేటెస్ట్ డేటా వస్తుంది కానీ, Concurrent Writes జరిగినప్పుడు కాన్‌ఫ్లిక్ట్స్ రాకుండా ఉండాలంటే అదనంగా వెక్టర్ క్లాక్స్ లేదా LWW అవసరం."
    },
    {
        "title": "Split-Brain Problem (Multiple Leaders Formation)",
        "subtitle": "స్ప్లిట్-బ్రెయిన్ సమస్య (నెట్‌వర్క్ విభజన వల్ల ఒకే క్లస్టర్‌లో ఇద్దరు లీడర్లు ఏర్పడటం)",
        "why": "డేటాసెంటర్ల మధ్య నెట్‌వర్క్ కేబుల్ కట్ అయితే, క్లస్టర్ రెండు ముక్కలుగా విడిపోతుంది. రెండు వైపులా ఉన్న సర్వర్లు తమను తామే లీడర్‌గా భావించి వేర్వేరు డేటాను రాస్తే డేటాబేస్ శాశ్వతంగా కరప్ట్ అయిపోతుంది.",
        "explanation": "PHP/MySQL లో మాస్టర్-మాస్టర్ రెప్లికేషన్‌లో రెండు సర్వర్లూ ఒకదానికొకటి పింగ్ చేసుకోలేక రెండూ Writes తీసుకోవడం ప్రారంభిస్తే వచ్చేదే స్ప్లిట్-బ్రెయిన్. దీన్ని నివారించడానికి 'Majority Quorum' సూత్రాన్ని పాటిస్తారు. మొత్తం 5 నోడ్స్ ఉంటే, నెట్‌వర్క్ కట్ అయినప్పుడు 3 నోడ్స్ ఉన్న వైపు మాత్రమే కొత్త లీడర్‌ను ఎన్నుకునే అర్హత ఉంటుంది; 2 నోడ్స్ ఉన్న మైనారిటీ భాగం ఆటోమేటిక్‌గా రీడ్-ఓన్లీ మోడ్‌లోకి వెళ్లిపోతుంది లేదా షట్‌డౌన్ అవుతుంది.",
        "example": """# Split-Brain నివారణకు Quorum చెక్
TOTAL_NODES = 5
MAJORITY_NEEDED = (TOTAL_NODES // 2) + 1  # 3

def handle_network_partition(visible_nodes_count):
    if visible_nodes_count >= MAJORITY_NEEDED:
        return "🟢 Quorum ఉంది: లీడర్ కొనసాగవచ్చు / కొత్త లీడర్ ఎన్నిక సాధ్యం."
    else:
        return "🔴 Quorum లేదు (Minority Partition): రైట్స్ నిలిపివేయబడ్డాయి (Read-Only Mode)!"

print("పార్టిషన్ 1 (3 నోడ్స్):", handle_network_partition(3))
print("పార్టిషన్ 2 (2 నోడ్స్):", handle_network_partition(2))""",
        "mistake": "రెండు నోడ్స్ ఉన్న క్లస్టర్‌లో ($N=2$) ఒక నోడ్ డౌన్ అయితే మెజారిటీ ($2/2+1=2$) సాధించలేక మొత్తం సిస్టమ్ ఆగిపోతుంది; అందుకే ఎప్పుడూ కనీసం 3 నోడ్స్ ఉండాలి."
    },
    {
        "title": "Fencing Tokens (Stale Distributed Lock Holders Prevention)",
        "subtitle": "ఫెన్సింగ్ టోకెన్స్ (గడువు ముగిసిన లాక్ హోల్డర్స్ డేటాను పాడుచేయకుండా నిరోధించడం)",
        "why": "డిస్ట్రిబ్యూటెడ్ లాక్ (Redis/Zookeeper) తీసుకున్న ప్రాసెస్ ఏదైనా గార్బేజ్ కలెక్షన్ (GC Pause) లేదా నెట్‌వర్క్ లాగ్ వల్ల ఆగిపోతే, లాక్ లీజు గడువు ముగిసి వేరే ప్రాసెస్‌కి వెళ్లిపోవచ్చు. పాత ప్రాసెస్ మేల్కొని డేటాను ఓవర్‌రైట్ చేయకుండా కాపాడాలి.",
        "explanation": "Laravel లో మనం `Cache::lock('order-process', 10)->block(5)` వాడతాం. క్లయింట్ 1 లాక్ తీసుకుంది, కానీ 15 సెకన్లు ఏదో కారణంతో నిద్రపోయింది. ఈలోపు Redis లాక్ గడువు ముగిసి క్లయింట్ 2 కి లాక్ లభించింది. ఇప్పుడు క్లయింట్ 1 మేల్కొని నేరుగా స్టోరేజ్‌కి వెళ్లి రాస్తే క్లయింట్ 2 మార్పులు పోతాయి. దీనికి పరిష్కారం 'Fencing Token'. లాక్ సర్వర్ ప్రతి లాక్‌తో పాటు క్రమంగా పెరిగే నంబర్‌ను (Monotonic Counter: 31, 32, 33...) ఇస్తుంది. స్టోరేజ్ సర్వర్ తన వద్ద ఉన్న టోకెన్ కంటే పెద్ద టోకెన్ ఉన్న రైట్స్‌ను మాత్రమే అంగీకరిస్తుంది.",
        "example": """# Storage లో Fencing Token ధృవీకరణ
class StorageServer:
    def __init__(self):
        self.last_fencing_token = 0
        self.data = ""

    def write(self, token, new_data):
        if token <= self.last_fencing_token:
            raise Exception(f"❌ తిరస్కరించబడింది! పాత టోకెన్: {token}. ప్రస్తుత గరిష్ట టోకెన్: {self.last_fencing_token}")
        self.last_fencing_token = token
        self.data = new_data
        print(f"✅ విజయవంతంగా సేవ్ అయింది: {new_data} (టోకెన్: {token})")

storage = StorageServer()
storage.write(token=101, new_data="Client 2 రాసిన డేటా")
# Client 1 ఆలస్యంగా పాత టోకెన్ తో వచ్చింది
try:
    storage.write(token=100, new_data="Client 1 లేట్ రైట్")
except Exception as e:
    print(e)""",
        "mistake": "లాక్ సర్వర్ కేవలం 'True/False' మాత్రమే రిటర్న్ చేస్తే సరిపోదు; Fencing Token లేకుండా డిస్ట్రిబ్యూటెడ్ లాక్స్ వాడటం ప్రమాదకరం."
    },
    {
        "title": "Consistent Hashing (Distributed Data Partitioning)",
        "subtitle": "కన్సిస్టెంట్ హ్యాషింగ్ (నోడ్స్ మారినప్పుడు అతి తక్కువ డేటాను మాత్రమే రీ-డిస్ట్రిబ్యూట్ చేయడం)",
        "why": "సాంప్రదాయ `hash(key) % N` వాడితే, క్లస్టర్‌లో ఒక్క కొత్త సర్వర్ చేరినా లేదా పోయినా 99% క్యాష్ లేదా డేటా మొత్తం వేరే సర్వర్లలోకి మారిపోయి (Cache stampede) డేటాబేస్ క్రాష్ అవుతుంది.",
        "explanation": "Consistent Hashing లో $0$ నుండి $2^{32}-1$ వరకు ఉండే ఒక వర్చువల్ సర్కిల్ (Hash Ring) ఉంటుంది. సర్వర్లను మరియు డేటా కీలను అదే రింగ్ మీద హ్యాష్ చేసి ఉంచుతారు. ఒక కీ తన హ్యాష్ విలువ నుండి సవ్యదిశలో (Clockwise) నడిస్తే వచ్చే మొదటి సర్వర్‌లో సేవ్ అవుతుంది. ఒక కొత్త సర్వర్ చేరినప్పుడు, కేవలం దానికి ఆనుకుని ఉన్న సర్వర్ నుండి కొంత డేటా మాత్రమే కొత్త సర్వర్‌కి మారుతుంది; మిగిలిన సర్వర్ల డేటా స్థిరంగా ఉంటుంది. వర్చువల్ నోడ్స్ (Vnodes) వాడటం ద్వారా డేటా అన్ని సర్వర్లకు సమతుల్యంగా పంపిణీ అవుతుంది.",
        "example": """# సింపుల్ Consistent Hash Ring కాన్సెప్ట్
import bisect
import hashlib

class ConsistentHashRing:
    def __init__(self, nodes=None):
        self.ring = []
        self.node_map = {}
        for node in (nodes or []):
            self.add_node(node)

    def _hash(self, key):
        return int(hashlib.md5(key.encode()).hexdigest(), 16)

    def add_node(self, node):
        h = self._hash(node)
        bisect.insort(self.ring, h)
        self.node_map[h] = node

    def get_node(self, key):
        if not self.ring: return None
        h = self._hash(key)
        idx = bisect.bisect_right(self.ring, h) % len(self.ring)
        return self.node_map[self.ring[idx]]

ring = ConsistentHashRing(["Redis-Node-1", "Redis-Node-2", "Redis-Node-3"])
print("user_101 వెళ్లాల్సిన నోడ్:", ring.get_node("user_101"))
print("user_102 వెళ్లాల్సిన నోడ్:", ring.get_node("user_102"))""",
        "mistake": "వర్చువల్ నోడ్స్ (vnodes) వాడకపోతే రింగ్ మీద సర్వర్లు అసమాన దూరాలలో ఉండి కొన్ని సర్వర్లపై ఎక్కువ లోడ్ (Hotspots) పడే అవకాశం ఉంది."
    },
    {
        "title": "Gossip Protocol (Node-to-Node State Propagation)",
        "subtitle": "గాసిప్ ప్రోటోకాల్ (మనుషులు పుకార్లు వ్యాప్తి చేసినట్లు సర్వర్ల సమాచారం నెట్‌వర్క్‌లో వ్యాపించడం)",
        "why": "వేల కొద్దీ సర్వర్లు ఉన్నప్పుడు ఒకే సెంట్రల్ సర్వర్‌పై ఆధారపడితే అది బాటిల్‌నెక్ అవుతుంది. ప్రతి సర్వర్ హెల్త్ మరియు స్టేట్ మొత్తం క్లస్టర్‌కు తక్కువ నెట్‌వర్క్ ఓవర్‌హెడ్‌తో చేరాలి.",
        "explanation": "Apache Cassandra మరియు HashiCorp Consul లు ఈ Gossip Protocol ను వాడుతాయి. ఇందులో ప్రతి సర్వర్ నిర్ణీత వ్యవధిలో (ఉదా: 1 సెకనుకు ఒకసారి) క్లస్టర్‌లోని యాదృచ్ఛికంగా (Random గా) ఎంచుకున్న 2 లేదా 3 ఇతర సర్వర్లకు తన వద్ద ఉన్న తాజా సమాచారాన్ని (Heartbeats, Node statuses) పంపుతుంది. సమాచారం అందుకున్న సర్వర్లు మళ్లీ ఇతర సర్వర్లకు చేరవేస్తాయి. గణిత శాస్త్రం ప్రకారం $O(\log N)$ రౌండ్లలో మొత్తం క్లస్టర్ అంతటా పూర్తి డేటా సమన్వయం అవుతుంది.",
        "example": """# Gossip Protocol మెసేజ్ స్ప్రెడింగ్ సిమ్యులేషన్
import random

nodes = {f"Node_{i}": {"status": "OK", "rumor": False} for i in range(1, 11)}
nodes["Node_1"]["rumor"] = "Server_5 is DOWN!"  # ప్రారంభ సమాచారం

def gossip_round(nodes):
    informed = [k for k, v in nodes.items() if v["rumor"]]
    for src in informed:
        targets = random.sample(list(nodes.keys()), 2)
        for t in targets:
            nodes[t]["rumor"] = nodes[src]["rumor"]

# 3 రౌండ్ల గాసిప్ తర్వాత ఎంతమందికి తెలిసిందో చూడండి
for round_no in range(1, 4):
    gossip_round(nodes)
    count = sum(1 for v in nodes.values() if v["rumor"])
    print(f"రౌండ్ {round_no} తర్వాత సమాచారం తెలిసిన నోడ్స్: {count}/10")""",
        "mistake": "Gossip ప్రోటోకాల్ అధిక ట్రాఫిక్ తీసుకోకుండా UDP ప్యాకెట్లను వాడుతుంది; ప్యాకెట్ డ్రాప్స్ అయినా ఎవెంచువల్ కన్వర్జెన్స్ జరుగుతుంది కానీ రియల్-టైమ్ మైక్రోసెకన్ గ్యారెంటీ ఉండదు."
    },
    {
        "title": "Failure Detectors (Node Failure Identification)",
        "subtitle": "ఫెయిల్యూర్ డిటెక్టర్స్ (సర్వర్ నిజంగా చనిపోయిందా లేక నెట్‌వర్క్ మాత్రమే స్లో అయిందా అని కనిపెట్టడం)",
        "why": "నెట్‌వర్క్ లాగ్ వల్ల చిన్న డిలే రాగానే సర్వర్ చనిపోయిందని భావించి ఫెయిలోవర్ ట్రిగ్గర్ చేస్తే అనవసరమైన రీ-బ్యాలెన్సింగ్ మరియు సిస్టమ్ అస్థిరత ఏర్పడుతుంది.",
        "explanation": "హార్ట్‌బీట్ ఆధారిత సాధారణ డిటెక్టర్లలో '5 సెకన్లు పింగ్ రాకపోతే Dead' అని ఫిక్స్డ్ థ్రెషోల్డ్ పెడతారు. కానీ క్లౌడ్ నెట్‌వర్క్‌లలో తాత్కాలిక ట్రాఫిక్ స్పైక్స్ సహజం. దీని కోసం 'Phi Accrual Failure Detector' (Cassandra & Akka లో వాడేది) వంటి అడాప్టివ్ పద్ధతులను వాడుతారు. ఇది గత హార్ట్‌బీట్ విరామాల హిస్టరీని విశ్లేషించి, ఒక అనుమానం తీవ్రత విలువను ($\Phi$) లెక్కిస్తుంది. $\Phi > 8$ అయితే నెట్‌వర్క్ స్లో అని, $\Phi > 12$ అయితే సర్వర్ ఖచ్చితంగా క్రాష్ అయిందని వర్గీకరిస్తుంది.",
        "example": """# Phi Accrual ఆధారిత కాన్సెప్ట్
import math

class FailureDetector:
    def __init__(self, threshold=8):
        self.threshold = threshold
        self.intervals = [1.0, 0.9, 1.1, 1.0] # సాధారణ 1 సెకను హార్ట్‌బీట్ చరిత్ర

    def calculate_phi(self, elapsed_since_last_heartbeat):
        mean = sum(self.intervals) / len(self.intervals)
        # లాగ్-స్కేల్ పై అనుమానం సంభావ్యతను లెక్కించడం
        prob = math.exp(-elapsed_since_last_heartbeat / mean)
        phi = -math.log10(prob) if prob > 0 else 20
        return phi

detector = FailureDetector()
print("1.2 సెకన్లు ఆలస్యం: Phi =", round(detector.calculate_phi(1.2), 2))
print("8.0 సెకన్లు ఆలస్యం: Phi =", round(detector.calculate_phi(8.0), 2), "-> 🚨 Declare Node DEAD!")""",
        "mistake": "ఫిక్స్‌డ్ హార్ట్‌బీట్ టైమర్‌లు వాడటం వలన తాత్కాలిక GC Pause లేదా క్లౌడ్ నెట్‌వర్క్ ఫ్లిక్కర్లలో అనవసరమైన ఫాల్స్ అలారమ్స్ వస్తాయి."
    },
    {
        "title": "Byzantine Fault Tolerance (BFT)",
        "subtitle": "బైజాంటైన్ ఫాల్ట్ టాలరెన్స్ (మోసపూరిత లేదా హ్యాక్ అయిన నోడ్స్ మధ్య కూడా కన్సెన్సస్ సాధించడం)",
        "why": "సాధారణ క్రాష్ ఫాల్ట్ టాలరెన్స్ (Raft/Paxos) లో సర్వర్లు పనిచేస్తాయి లేదా ఆగిపోతాయి. కానీ కొన్ని సర్వర్లు హ్యాక్ అయి కావాలనే తప్పుడు డేటాను ప్రసారం చేసే వాతావరణంలో (Blockchain, Mission Critical) కూడా సిస్టమ్ రక్షణ పొందాలి.",
        "explanation": "ప్రాచీన బైజాంటైన్ జనరల్స్ సమస్య నుండి ఈ పేరు వచ్చింది. క్లస్టర్‌లో $f$ సంఖ్యలో మోసపూరిత నోడ్స్ ఉంటే, సరైన నిర్ణయం తీసుకోవడానికి మొత్తం కనీసం $3f + 1$ నోడ్స్ అవసరం. అంటే 1 నోడ్ మోసం చేయగలదని అనుమానిస్తే కనీసం 4 నోడ్స్ ఉండాలి ($3(1)+1=4$). ప్రాక్టికల్ బైజాంటైన్ ఫాల్ట్ టాలరెన్స్ (PBFT) లో ప్రీ-ప్రిపేర్, ప్రిపేర్, కమిట్ అనే మూడు దశల్లో డిజిటల్ సిగ్నేచర్ల ద్వారా వెరిఫై చేస్తూ ఏకాభిప్రాయానికి వస్తారు.",
        "example": """# BFT కనీస నోడ్స్ లెక్కింపు
def bft_min_nodes_required(faulty_or_malicious_nodes):
    return (3 * faulty_or_malicious_nodes) + 1

def crash_fault_min_nodes(faulty_nodes): # Raft / Paxos
    return (2 * faulty_nodes) + 1

malicious = 2
print(f"2 దురుద్దేశపూర్వక నోడ్స్ ను తట్టుకోవడానికి BFT కి కావాల్సిన నోడ్స్: {bft_min_nodes_required(malicious)}")
print(f"2 సాధారణ క్రాష్ నోడ్స్ ను తట్టుకోవడానికి Raft కి కావాల్సిన నోడ్స్: {crash_fault_min_nodes(malicious)}")""",
        "mistake": "సంస్థ లోపల ప్రైవేట్ మైక్రోసర్వీసెస్ క్లస్టర్‌లలో BFT వాడటం అనవసరం; అక్కడ Raft సరిపోతుంది. BFT భారీగా నెట్‌వర్క్ మెసేజ్ ఓవర్‌హెడ్ కలిగిస్తుంది."
    },
    {
        "title": "Linearizability (Strong Operation Ordering Guarantees)",
        "subtitle": "లీనియరైజబిలిటీ (మొత్తం క్లస్టర్ ఒకే ఒక సింగిల్ మెషీన్ లాగా నిజ సమయంలో స్పందించడం)",
        "why": "బ్యాంకింగ్ లేదా అటామిక్ రిజిస్ట్రేషన్ సిస్టమ్స్‌లో ఒక ఖాతాదారుడు డబ్బు జమ చేయగానే, వెంటనే ప్రపంచంలో ఎక్కడి నుండైనా చూసినా ఆ కొత్త బ్యాలెన్స్ మాత్రమే కనిపించాలి; ఒక్క మిల్లీసెకను కూడా పాత బ్యాలెన్స్ కనిపించకూడదు.",
        "explanation": "లీనియరైజబిలిటీ అనేది డిస్ట్రిబ్యూటెడ్ సిస్టమ్స్‌లో అత్యంత కఠినమైన కన్సిస్టెన్సీ మోడల్ (CAP థియరమ్‌లోని 'C'). ఒక రైట్ ఆపరేషన్ ముగిసిందని క్లయింట్‌కి రెస్పాన్స్ వెళ్లిన క్షణం నుండి, ఆ తర్వాత ప్రారంభమయ్యే ఏ రీడ్ ఆపరేషన్ అయినా ఖచ్చితంగా ఆ కొత్త విలువను మాత్రమే చదవాలి. Etcd, Google Spanner లు లీనియరైజబుల్ గ్యారెంటీలను ఇస్తాయి. దీని కోసం నెట్‌వర్క్ లాటెన్సీ మరియు త్రూపుట్‌ను త్యాగం చేయాల్సి ఉంటుంది.",
        "example": """# Linearizable Read Guarantee భావన
global_data_store = {"account_balance": 100}

def linearizable_write(new_balance):
    # అటామిక్ గా అన్ని కోరం నోడ్స్ లో రాసిన తర్వాతే రిటర్న్ అవుతుంది
    global_data_store["account_balance"] = new_balance
    return "WRITE_ACK"

def linearizable_read():
    # Write ACK వచ్చిన తర్వాత జరిగే రీడ్ ఎల్లప్పుడూ లేటెస్ట్ డేటానే ఇవ్వాలి
    return global_data_store["account_balance"]

linearizable_write(250)
print("తదుపరి చదివిన బ్యాలెన్స్:", linearizable_read()) # ఖచ్చితంగా 250 మాత్రమే రావాలి""",
        "mistake": "MySQL Read Replica నుండి చదివినప్పుడు అది లీనియరైజబుల్ కాదు, ఎందుకంటే రెప్లికేషన్ లాగ్ వల్ల కొన్ని మిల్లీసెకన్లు పాత డేటా కనిపించవచ్చు."
    },
    {
        "title": "Sequential Consistency (Distributed Operation Ordering)",
        "subtitle": "సీక్వెన్షియల్ కన్సిస్టెన్సీ (ప్రతి ప్రాసెస్ రాసిన క్రమంలోనే అందరికీ ఈవెంట్లు కనిపించడం)",
        "why": "గ్లోబల్ రియల్-టైమ్ క్లాక్ సమన్వయం చాలా ఖరీదైనది. కాబట్టి గ్లోబల్ సమయం కన్నా, ప్రతి ప్రోగ్రామ్ చేసిన పనుల వరుస క్రమం మారకుండా ఉండటం ముఖ్యమైన సందర్భాల్లో ఇది ఉపయోగపడుతుంది.",
        "explanation": "లెస్లీ లాంపోర్ట్ నిర్వచించిన ఈ విధానంలో, క్లస్టర్‌లోని అన్ని నోడ్స్ ఆపరేషన్లను ఖచ్చితంగా ఒకే క్రమంలో అమలు చేసినట్లు అంగీకరిస్తాయి. ఒక ప్రాసెస్ A రాసిన ఆర్డర్ ఎప్పుడూ తిరగబడదు. అయితే లీనియరైజబిలిటీ లాగా ఇది వాస్తవ భౌతిక సమయానికి (Real-time Wall Clock) కట్టుబడి ఉండదు; ఒక నోడ్ కొంచెం ఆలస్యంగా డేటాను అప్‌డేట్ చేసినా, ఆపరేషన్ల సీక్వెన్స్ అందరికీ ఒకే విధంగా ఉంటుంది. Apache ZooKeeper దీనికి మంచి ఉదాహరణ.",
        "example": """# Sequential Consistency సీక్వెన్స్
# Process 1: Write(x, 1) -> Write(x, 2)
# Process 2: Read(x) -> Read(x)

# Sequential Consistency లో సాధ్యమయ్యే ఫలితాలు:
# Read 1 = 1, Read 2 = 2 (సరైన సీక్వెన్స్)
# Read 1 = 0, Read 2 = 1 (కొంచెం ఆలస్యంగా చదివినా క్రమం సరిగ్గా ఉంది)
# కానీ Read 1 = 2, Read 2 = 1 రావడం ఎప్పటికీ అసాధ్యం!""",
        "mistake": "సీక్వెన్షియల్ కన్సిస్టెన్సీ అంటే లీనియరైజబిలిటీ కాదు; ఇందులో చదివే డేటా తాజాది కాకపోవచ్చు కానీ క్రమం మాత్రం తప్పుదు."
    },
    {
        "title": "Causal Consistency (Causally Related Events Ordering)",
        "subtitle": "కాసల్ కన్సిస్టెన్సీ (కారణం-ఫలితం సంబంధం ఉన్న ఈవెంట్లు మాత్రమే సరైన వరుసలో కనిపించడం)",
        "why": "సోషల్ మీడియా లేదా చాట్ అప్లికేషన్స్‌లో ఒక ప్రశ్న పోస్ట్ చేసిన తర్వాతే దానికి వచ్చిన సమాధానం కనిపించాలి. సమాధానం ముందు వచ్చి ప్రశ్న వెనుక వస్తే యూజర్ కన్ఫ్యూజ్ అవుతారు.",
        "explanation": "Causal Consistency అనేది కారణ-ఫలిత సంబంధం ఉన్న ఈవెంట్లను (Causally related events) మాత్రమే ఖచ్చితమైన క్రమంలో ఉంచుతుంది. ఒకదానితో ఒకటి సంబంధం లేని రెండు స్వతంత్ర ఈవెంట్లు (Concurrent events) ఏ క్రమంలో కనిపించినా ఫర్వాలేదు. ఇది లీనియరైజబిలిటీ కంటే చాలా వేగంగా పనిచేస్తుంది మరియు నెట్‌వర్క్ పార్టిషన్స్ సమయంలో కూడా అధిక లభ్యతను (High Availability under CAP theorem) ఇస్తుంది.",
        "example": """# Causal Dependency ట్రాకింగ్
# Post A: "రేపు ఆఫీస్ ఉందా?" (కారణం)
# Post B: "లేదు, సెలవు!" (ఫలితం - Post A కి ప్రత్యుత్తరం)

def render_feed(posts):
    # Post B ఖచ్చితంగా Post A తర్వాతే డిస్‌ప్లే అవ్వాలి
    sorted_feed = sorted(posts, key=lambda x: x.get("depends_on_id", 0))
    for p in sorted_feed:
        print(f"[{p['id']}] {p['text']}")

feed = [
    {"id": 2, "text": "లేదు, సెలవు!", "depends_on_id": 1},
    {"id": 1, "text": "రేపు ఆఫీస్ ఉందా?", "depends_on_id": 0}
]
render_feed(feed)""",
        "mistake": "రెండు స్వతంత్ర పోస్టుల మధ్య Causal సంబంధం ఉండదు కాబట్టి, యూజర్ 1 కి ముందు కనిపించిన పోస్ట్ యూజర్ 2 కి వెనుక కనిపించవచ్చు; దాన్ని బగ్ అనుకోకూడదు."
    }
]
