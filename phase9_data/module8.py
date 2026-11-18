# Module 8: Advanced Cloud-Native Architecture (14 topics)

topics = [
    {
        "title": "Kubernetes Operators (Custom Resource Automation)",
        "subtitle": "కుబెర్‌నెటిస్ ఆపరేటర్స్ (ఒక సీనియర్ డెవొప్స్ ఇంజనీర్ మెదడును కోడ్ రూపంలో కుబెర్‌నెటిస్ లోపల పెట్టడం)",
        "why": "డేటాబేస్ బ్యాకప్‌లు తీయడం, ఫెయిలోవర్ హ్యాండిల్ చేయడం, క్లస్టర్ స్కేలింగ్ వంటి పనులను రోజూ మనుషులు మాన్యువల్ గా చేయడం సమయం వృధా మరియు లోపభూయిష్టం.",
        "explanation": "Operator Pattern అనేది కుబెర్‌నెటిస్ కంట్రోలర్ సిద్ధాంతంపై నిర్మించబడింది. ఇది ఒక ప్రత్యేకమైన సాఫ్ట్‌వేర్ ఎక్స్‌టెన్షన్. ఉదాహరణకు, 'Postgres Operator' ని ఇన్‌స్టాల్ చేస్తే, మీరు కేవలం `kind: PostgresCluster, replicas: 3` అని ఒక చిన్న YAML రాస్తే చాలు. ఆ ఆపరేటర్ స్వయంగా మాస్టర్ నోడ్‌ను క్రియేట్ చేస్తుంది, రెప్లికాస్ సెటప్ చేస్తుంది, WAL రెప్లికేషన్ కాన్ఫిగర్ చేస్తుంది, మాస్టర్ డౌన్ అయితే ఆటోమేటిక్ గా రెప్లికాను ప్రమోట్ చేస్తుంది (Human Operator బదులు Software Operator). Go లో Operator SDK లేదా Python లో Kopf లైబ్రరీతో వీటిని రాస్తారు.",
        "example": """# Python Kopf లైబ్రరీతో సింపుల్ Kubernetes Operator
'''python
import kopf
import kubernetes

@kopf.on.create('mynests.com', 'v1', 'mysqlclusters')
def create_mysql_cluster(spec, name, namespace, logger):
    replicas = spec.get('replicas', 1)
    logger.info(f"MySQL క్లస్టర్ {name} ({replicas} రెప్లికాస్ తో) ఆటోమేటిక్ గా సృష్టించబడుతోంది...")
    # ఇక్కడ StatefulSet, Services, PersistentVolumeClaims ను ఆటోమేటిక్ గా కోడ్ ద్వారా సృష్టిస్తుంది
''' """,
        "mistake": "ఆపరేటర్ రికన్సిలియేషన్ లాజిక్ లో Idempotency పాటించకపోవడం; ఆపరేటర్ ప్రతి కొన్ని సెకన్లకు మళ్లీ మళ్లీ ఎగ్జిక్యూట్ అవుతుంది కాబట్టి ప్రతి చర్య రిపీటబుల్ గా ఉండాలి."
    },
    {
        "title": "Custom Resource Definitions (CRDs)",
        "subtitle": "కస్టమ్ రిసోర్స్ డెఫినిషన్స్ (కుబెర్‌నెటిస్ డిక్షనరీని మన సొంత కొత్త ఆబ్జెక్ట్‌లతో విస్తరించడం)",
        "why": "కుబెర్‌నెటిస్ లో కేవలం Pod, Deployment, Service మాత్రమే ఉంటాయి. మన స్వంత వ్యాపార వస్తువులను (ఉదా: `Database`, `MachineLearningModel`, `BackupJob`) కుబెర్‌నెటిస్ ఆబ్జెక్ట్‌లుగా మార్చాలి.",
        "explanation": "CRD అనేది కుబెర్‌నెటిస్ API సర్వర్‌కు కొత్త REST ఎండ్‌పాయింట్లను జోడించే ఒక శక్తివంతమైన సాధనం. మీరు ఒక CRD ని అప్లై చేయగానే, కుబెర్‌నెటిస్ API సర్వర్ ఆ కొత్త రకాన్ని నేర్చుకుంటుంది. ఆ తర్వాత మీరు `kubectl get databases` లేదా `kubectl apply -f my-ml-pipeline.yaml` అని నేటివ్ కుబెర్‌నెటిస్ కమాండ్స్ లాగానే వాడవచ్చు. ఈ డేటా అంతా etcd లో భద్రంగా స్టోర్ అవుతుంది.",
        "example": """# AIModel CRD నిర్వచనం
'''yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: aimodels.ai.mynests.com
spec:
  group: ai.mynests.com
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          properties:
            spec:
              type: object
              properties:
                modelName: {type: string}
                minReplicas: {type: integer}
  scope: Namespaced
  names:
    plural: aimodels
    singular: aimodel
    kind: AIModel
''' """,
        "mistake": "CRD లో OpenAPI v3 స్కీమా వాలిడేషన్ రాయకపోవడం; యూజర్లు తప్పుడు ఫీల్డ్స్ తో YAML అప్లై చేసినప్పుడు సిస్టమ్ ఎర్రర్స్ తో క్రాష్ అవుతుంది."
    },
    {
        "title": "Control Plane vs Data Plane (Infrastructure Architecture)",
        "subtitle": "కంట్రోల్ ప్లేన్ vs డేటా ప్లేన్ (పాలసీలు నిర్ణయించే మెదడు vs ట్రాఫిక్ తీసుకెళ్లే కండరాలు)",
        "why": "నియంత్రణ వ్యవస్థ మరియు వాస్తవ ట్రాఫిక్ వ్యవస్థ రెండూ కలిసిపోతే, మేనేజ్‌మెంట్ సాఫ్ట్‌వేర్ క్రాష్ అయినప్పుడు లైవ్ కస్టమర్ ట్రాఫిక్ కూడా ఆగిపోతుంది.",
        "explanation": "క్లౌడ్-నేటివ్ సిస్టమ్స్‌లో స్పష్టమైన విభజన ఉంటుంది: \n1. Control Plane: నిర్ణయాలు తీసుకునే మెదడు. Kubernetes లో etcd, API Server, Scheduler; Istio లో Istiod. ఇది ఎక్కడ ఏ పాడ్ రన్ అవ్వాలో, రూటింగ్ రూల్స్ ఏమిటో ప్లాన్ చేస్తుంది. కంట్రోల్ ప్లేన్ తాత్కాలికంగా డౌన్ అయినా ఇప్పటికే నడుస్తున్న అప్లికేషన్లు ఆగవు. \n2. Data Plane: వాస్తవ పని చేసే కండరాలు. Kubelet, Envoy Proxies, Linux Kernel. కస్టమర్ల నుండి వచ్చే అసలైన HTTP రిక్వెస్ట్‌లను, ప్యాకెట్లను గిగాబైట్ల వేగంతో ప్రాసెస్ చేసేది ఇదే.",
        "example": """# Control Plane vs Data Plane పోలిక
#
# Istiod (Control Plane):
# "Envoy, 80% ట్రాఫిక్ ను v1 కి, 20% ట్రాఫిక్ ను v2 కి పంపు" అని కాన్ఫిగ్ పంపుతుంది.
# (ఇది సెకనుకు 1 సారి మాత్రమే జరుగుతుంది).
#
# Envoy Proxy (Data Plane):
# కస్టమర్ల నుండి వచ్చే సెకనుకు 50,000 లైవ్ HTTP రిక్వెస్టులను ఆ రూల్ ప్రకారం మళ్లిస్తుంది!""",
        "mistake": "డేటా ప్లేన్ ప్రాక్సీల ద్వారా కంట్రోల్ ప్లేన్ API సర్వర్‌కు నేరుగా భారీ ట్రాఫిక్ క్వెరీలు పంపడం; API సర్వర్ లోడ్ ఎక్కువై క్లస్టర్ మొత్తం మేనేజ్‌మెంట్ ఫ్రీజ్ అవుతుంది."
    },
    {
        "title": "Reconciliation Loops (Desired vs Actual State)",
        "subtitle": "రికన్సిలియేషన్ లూప్స్ (యూజర్ కోరిన స్థితి మరియు వాస్తవ క్లస్టర్ స్థితి సమానమయ్యే వరకు నిరంతరం సరిచేయడం)",
        "why": "సర్వర్లు క్రాష్ అవ్వడం, నెట్‌వర్క్ డ్రాప్స్ సహజం. సిస్టమ్ ఎప్పటికప్పుడు తనను తాను సరిదిద్దుకునే స్వయం-నియంత్రణ (Self-healing) మెకానిజం కావాలి.",
        "explanation": "కుబెర్‌నెటిస్ వెనుక ఉన్న అత్యంత ముఖ్యమైన ఫిలాసఫీ ఇది. \nఫార్ములా: $Loop: Diff = Desired State - Actual State; If Diff != 0 -> Take Action$. \nయూజర్ కోరిన స్థితి (Desired State): 3 పాడ్స్ రన్ అవ్వాలి. \nవాస్తవ స్థితి (Actual State): ఒక నోడ్ చనిపోయి 2 పాడ్స్ మాత్రమే ఉన్నాయి. \nకంట్రోలర్ ఈ తేడాను ($3 - 2 = 1$) గుర్తించి వెంటనే ఇంకొక కొత్త నోడ్ పై 3వ పాడ్‌ను లాంచ్ చేస్తుంది. ఈ లూప్ నిరంతరం సెకనుకు వందలాది సార్లు బ్యాక్‌గ్రౌండ్ లో రన్ అవుతూ ఉంటుంది.",
        "example": """# Reconciliation Loop సూడోకోడ్
def reconcile(cluster_state):
    desired_replicas = get_spec_replicas()  # YAML లో చెప్పిన 3
    actual_replicas = get_running_pods()    # నిజంగా బతికున్న 2
    
    diff = desired_replicas - actual_replicas
    if diff > 0:
        print(f"🔧 స్వయం-స్వస్థత: {diff} కొత్త పాడ్(లు) సృష్టించబడుతున్నాయి...")
        spawn_pods(count=diff)
    elif diff < 0:
        print(f"🧹 అదనపు పాడ్స్ శుభ్రం చేయబడుతున్నాయి...")
        terminate_pods(count=abs(diff))
    else:
        # అంతా బాగుంది (No Action)
        pass""",
        "mistake": "లెవెల్-ట్రిగ్గర్డ్ (Level-triggered) కాకుండా కేవలం ఈవెంట్-ట్రిగ్గర్డ్ (Edge-triggered) పై మాత్రమే ఆధారపడటం; ఈవెంట్ నెట్‌వర్క్‌లో మిస్ అయితే సిస్టమ్ శాశ్వతంగా అసమాన స్థితిలో ఉండిపోతుంది."
    },
    {
        "title": "eBPF (Extended Berkeley Packet Filter)",
        "subtitle": "eBPF (లైనక్స్ కెర్నల్ సోర్స్ కోడ్ మార్చకుండానే కెర్నల్ లోపల శాండ్‌బాక్స్ ప్రోగ్రామ్స్ రన్ చేయడం)",
        "why": "సాంప్రదాయ అబ్జర్వబిలిటీ లేదా సెక్యూరిటీ కోసం లైనక్స్ కెర్నల్ మాడ్యూల్స్ రాస్తే కెర్నల్ క్రాష్ అయి మొత్తం సర్వర్ కుప్పకూలే ప్రమాదం ఉంది.",
        "explanation": "ఆధునిక క్లౌడ్-నేటివ్ ఇంజనీరింగ్‌లో eBPF ఒక అద్భుతం (Cilium, Falco, Pixie టూల్స్ దీనిపైనే ఆధారపడ్డాయి). ఇది వెబ్ బ్రౌజర్‌లో జావాస్క్రిప్ట్ లాంటిది. లైనక్స్ కెర్నల్ లోపల ఒక చిన్న సురక్షితమైన వర్చువల్ మెషీన్ (eBPF VM) ఉంటుంది. మీరు C లేదా Rust లో రాసిన చిన్న ప్రోగ్రామ్‌ను కెర్నల్ వెరిఫైయర్ క్షుణ్ణంగా తనిఖీ చేసి (ఇది లూప్స్ లో ఆగకుండా, మెమరీ లీక్ లేకుండా ఉంటుందని నిర్ధారించుకుని) కెర్నల్ స్పేస్‌లో లోడ్ చేస్తుంది. ఒక్క నెట్‌వర్క్ ప్యాకెట్ లేదా సిస్టమ్ కాల్ మిస్ కాకుండా అసాధారణ వేగంతో సెక్యూరిటీ, నెట్‌వర్కింగ్, అబ్జర్వబిలిటీ ని అందిస్తుంది.",
        "example": '''# eBPF ప్రోగ్రామ్ కాన్సెప్ట్ (BCC పైథాన్ స్క్రిప్ట్)
from bcc import BPF

# లైనక్స్ కెర్నల్ లో ప్రతిసారి కొత్త ప్రాసెస్ ఓపెన్ అయినప్పుడు (sys_execve) పట్టుకోవడం
bpf_source = """
int trace_exec(void *ctx) {
    bpf_trace_printk("🚨 కొత్త ప్రాసెస్ లాంచ్ అయింది!\\\\n");
    return 0;
}
"""
b = BPF(text=bpf_source)
b.attach_kprobe(event=b.get_syscall_fnname("execve"), fn_name="trace_exec")
print("eBPF కెర్నల్ స్నిఫర్ రన్ అవుతోంది... Ctrl+C తో ఆపండి")
b.trace_print()''',
        "mistake": "పాత లైనక్స్ కెర్నల్ వెర్షన్లలో (Kernel < 4.19) eBPF వాడటానికి ప్రయత్నించడం; ఆధునిక ఫీచర్లకు కనీసం Linux 5.4+ లేదా 6.x అవసరం."
    },
    {
        "title": "Container Runtime Internals (containerd, CRI-O, runc)",
        "subtitle": "కంటైనర్ రన్‌టైమ్ ఇంటర్నల్స్ (డాకర్ కేవలం ఒక పైపై టూల్ మాత్రమే; తెరవెనుక కంటైనర్లను నిజంగా నడిపే ఇంజిన్లు)",
        "why": "'కంటైనర్' అనేది ఒక మ్యాజిక్ కాదు; అది లైనక్స్ లోపల ఎలా పుడుతుందో తెలిస్తేనే కుబెర్‌నెటిస్ OOMKilled మరియు CrashLoopBackOff సమస్యలను లోతుగా డీబగ్ చేయగలం.",
        "explanation": "ఆర్కిటెక్చర్ లేయర్స్: \n1. High-Level Runtime (containerd, CRI-O): ఇవి కుబెర్‌నెటిస్ Kubelet తో CRI (Container Runtime Interface) ద్వారా మాట్లాడతాయి. ఇమేజ్‌లను డౌన్‌లోడ్ చేయడం, అన్‌ప్యాక్ చేయడం, నెట్‌వర్క్ ఇంటర్‌ఫేస్ సెటప్ చేయడం వీటి పని. \n2. Low-Level Runtime (runc): OCI (Open Container Initiative) స్టాండర్డ్ ప్రకారం ఒకే ఒక్క పని చేస్తుంది: లైనక్స్ సిస్టమ్ కాల్స్ చేసి నేమ్‌స్పేస్‌లు, సిగ్రూప్స్ క్రియేట్ చేసి మీ ప్రాసెస్‌ను ఐసోలేట్ చేసి రన్ చేయడం. ప్రాసెస్ రన్ అవ్వగానే `runc` ఎగ్జిట్ అయిపోతుంది.",
        "example": """# Kubelet నుండి కంటైనర్ పుట్టే క్రమం
#
# [Kubernetes Kubelet]
#         | (gRPC CRI Protocol)
#         v
#    [containerd]
#         | (ఇమేజ్ డౌన్‌లోడ్ & రూట్‌ఎఫ్‌ఎస్ అన్‌ప్యాకింగ్)
#         v
#      [runc]
#         | (clone() system call with CLONE_NEWPID, CLONE_NEWNET...)
#         v
#  [My Isolated App Process]""",
        "mistake": "కుబెర్‌నెటిస్ వర్కర్ నోడ్లలో ఇంకా పూర్తి డెస్క్‌టాప్ డాకర్ ఇంజిన్ రన్ అవుతోందని అనుకోవడం; కుబెర్‌నెటిస్ 1.24+ లో డాకర్ షిమ్ తొలగించబడింది, కేవలం తేలికపాటి `containerd` లేదా `cri-o` మాత్రమే వాడతారు."
    },
    {
        "title": "Linux Namespaces (Process Isolation)",
        "subtitle": "లైనక్స్ నేమ్‌స్పేసెస్ (ఒక ప్రాసెస్ కు సర్వర్ లోని ఇతర ప్రాసెస్‌లు కనిపించకుండా కళ్లకు గంతలు కట్టడం)",
        "why": "కంటైనర్లు వర్చువల్ మెషీన్లు కావు. ఒకే ఆపరేటింగ్ సిస్టమ్ కెర్నల్ పై నడుస్తున్న వేర్వేరు కస్టమర్ల ప్రాసెస్‌లు ఒకదానికొకటి చూసుకోకుండా రక్షించాలి.",
        "explanation": "లైనక్స్ నేమ్‌స్పేసెస్ ఒక ప్రాసెస్ చుట్టూ ఒక వర్చువల్ భ్రమను సృష్టిస్తాయి. \nప్రధాన నేమ్‌స్పేస్‌లు: \n- PID Namespace: కంటైనర్ లోపల మీ యాప్ PID 1 లాగా కనిపిస్తుంది; హోస్ట్ సర్వర్ లోని మిగతా ప్రాసెస్‌లు కనిపించవు. \n- NET Namespace: కంటైనర్‌కు ప్రత్యేకమైన IP అడ్రస్, రూటింగ్ టేబుల్, లోకల్‌హోస్ట్ ఉంటాయి. \n- MNT (Mount) Namespace: ప్రత్యేకమైన ఫైల్ సిస్టమ్ రూట్ (`/`). \n- UTS: ప్రత్యేక హోస్ట్‌నేమ్. \n- IPC: షేర్డ్ మెమరీ ఐసోలేషన్. \n- USER: కంటైనర్ లోపల రూట్ యూజర్ అయినా, హోస్ట్ సర్వర్‌లో సాధారణ నాన్-రూట్ యూజర్ గా పరిమితం చేయడం.",
        "example": """# Linux unshare కమాండ్ తో స్వయంగా నేమ్‌స్పేస్ క్రియేట్ చేయడం
'''bash
# కొత్త PID మరియు Mount నేమ్‌స్పేస్ లో ప్రత్యేక షెల్ ఓపెన్ చేయడం
sudo unshare --pid --fork --mount-proc /bin/bash

# ఇప్పుడు 'ps aux' రన్ చేస్తే కేవలం ఈ ఒక్క ప్రాసెస్ మాత్రమే PID 1 గా కనిపిస్తుంది!
ps aux
''' """,
        "mistake": "కంటైనర్లను `--privileged` ఫ్లాగ్ తో లేదా `hostPID: true` తో రన్ చేయడం; ఇలా చేస్తే నేమ్‌స్పేస్ ఐసోలేషన్ బ్రేక్ అయి కంటైనర్ హోస్ట్ సర్వర్ మొత్తాన్ని హ్యాక్ చేయగలదు."
    },
    {
        "title": "Linux Cgroups (Resource Control & CPU Throttling)",
        "subtitle": "లైనక్స్ సిగ్రూప్స్ (ఒక కంటైనర్ ఎంత RAM, ఎంత CPU మాత్రమే వాడాలో విధించే ఉక్కు పరిమితులు)",
        "why": "ఒక చిన్న బగ్ ఉన్న కంటైనర్ అనంతమైన లూప్‌లోకి వెళ్లి సర్వర్‌లోని మొత్తం 64 CPU కోర్లను, 128GB RAM ని తినేసి ఇతర అప్లికేషన్లను చంపేయకుండా అడ్డుకోవాలి.",
        "explanation": "Control Groups (cgroups v1 & modern cgroups v2) రిసోర్స్ అకౌంటింగ్ మరియు లిమిట్స్ ను అమలు చేస్తాయి. \n- Memory Limit: కంటైనర్ కేటాయించిన మెమరీ పరిమితి (ఉదా: 512MB) దాటగానే లైనక్స్ OOM-Killer (Out of Memory Killer) ఆ ప్రాసెస్‌కు `SIGKILL` (Exit Code 137) పంపి వెంటనే చంపేస్తుంది. \n- CPU Limit: CPU ని చంపరు; బదులుగా CFS (Completely Fair Scheduler) క్వోటా ద్వారా ఆ ప్రాసెస్‌కు CPU సమయాన్ని తగ్గించివేస్తారు (CPU Throttling). దీనివల్ల అప్లికేషన్ నిశ్శబ్దంగా నరకం లాగా స్లో అవుతుంది.",
        "example": """# Kubernetes లో Resources Requests & Limits
'''yaml
resources:
  requests:
    memory: "256Mi"
    cpu: "250m"      # కనీస గ్యారెంటీ (0.25 CPU Core)
  limits:
    memory: "512Mi"  # దాటితే -> OOMKilled (Exit Code 137)!
    cpu: "500m"      # దాటితే -> CPU Throttling (యాప్ స్లో అవుతుంది)!
''' """,
        "mistake": "CPU Throttling మెట్రిక్స్ గమనించకుండా ఉండటం; CPU Limits చాలా తక్కువగా పెడితే మీ యాప్ ఎలాంటి ఎర్రర్ లాగ్ లేకుండా విపరీతమైన లాటెన్సీని చూపిస్తుంది."
    },
    {
        "title": "Service Mesh Data Plane (Envoy Proxy Internals)",
        "subtitle": "సర్వీస్ మెష్ డేటా ప్లేన్ (ఎన్వాయ్ ప్రాక్సీ లోపల నెట్‌వర్క్ ఫిల్టర్ చైన్ ఎలా పనిచేస్తుంది?)",
        "why": "Istio లేదా Consul సర్వీస్ మెష్ లో నెట్‌వర్క్ ఎర్రర్స్ వచ్చినప్పుడు, Envoy ప్రాక్సీ లోపల కాన్ఫిగరేషన్ ఎలా ఫ్లో అవుతుందో అర్థం చేసుకోకపోతే సమస్యను పరిష్కరించలేము.",
        "explanation": "Envoy Proxy ఒక హై-పర్ఫార్మెన్స్ C++ నెట్‌వర్క్ ఇంజిన్. దీని నిర్మాణం: \n1. Listeners: నిర్దిష్ట పోర్ట్ (ఉదా: 15001) పై వచ్చే ఇన్‌కమింగ్ కనెక్షన్లను స్వీకరిస్తుంది. \n2. Filter Chains: రిక్వెస్ట్ పై వరుసగా ఫిల్టర్లను అమలు చేస్తుంది (TLS Inspector -> HTTP Connection Manager -> Rate Limiting Filter -> Router Filter). \n3. Clusters: అప్‌స్ట్రీమ్ సర్వీసుల సమూహం (ఉదా: `payment-service-v1`). ఎండ్‌పాయింట్ హెల్త్ చెక్స్, లోడ్ బ్యాలెన్సింగ్ (RoundRobin/LeastRequest) చేస్తుంది. \n4. Routes: URL పాత్ లేదా హెడర్ ఆధారంగా రిక్వెస్ట్‌ను సరైన క్లస్టర్‌కు మళ్లిస్తుంది.",
        "example": """# Envoy కాన్ఫిగరేషన్ ఆర్కిటెక్చర్
# [Downstream Client] 
#         |
#         v
#     [Listener: 0.0.0.0:8080]
#         |
#   [Filter Chain: TLS -> Auth -> Router]
#         |
#      [Route: /api/pay -> Cluster: payment_service]
#         |
#   [Upstream Cluster: Load Balancer (Least Request)]
#         |
#         +---> [Pod 1: 10.244.1.5:80]
#         +---> [Pod 2: 10.244.1.6:80]""",
        "mistake": "Envoy అడ్మిన్ పోర్ట్ (`:15000/stats` లేదా `:15000/clusters`) పరిశీలించకుండా ఊహాగానాలతో నెట్‌వర్క్ డీబగ్గింగ్ చేయడం."
    },
    {
        "title": "GitOps (Declarative Deployment Management with ArgoCD)",
        "subtitle": "గిట్-ఆప్స్ (Git రిపోజిటరీయే ఏకైక పరమ సత్యం; ప్రొడక్షన్ మార్పులన్నీ గిట్ కమిట్స్ ద్వారానే జరగాలి)",
        "why": "ఇంజనీర్లు నేరుగా ప్రొడక్షన్ క్లస్టర్ లోకి వెళ్లి `kubectl edit` లేదా `kubectl apply` చేస్తే ఎవరు ఏమి మార్చారో చరిత్ర ఉండదు, ఆడిట్ దొరకదు, రోల్‌బ్యాక్ అసాధ్యం అవుతుంది.",
        "explanation": "GitOps విధానంలో క్లస్టర్ యొక్క పూర్తి స్థితి (Desired State) ఒక Git రిపోజిటరీలో డిక్లరేటివ్ YAML/Helm/Kustomize ఫైల్స్ రూపంలో ఉంటుంది. ArgoCD లేదా Flux అనే ఏజెంట్ కుబెర్‌నెటిస్ క్లస్టర్ లోపల రన్ అవుతూ ఉంటుంది. ఇది గిట్ రిపోజిటరీని నిరంతరం గమనిస్తుంది (Poll/Webhook). ఎవరైనా గిట్‌లో మార్పు చేయగానే, క్లస్టర్‌ను ఆటోమేటిక్ గా గిట్‌తో సింక్ చేస్తుంది. ఎవరైనా పొరపాటున క్లస్టర్‌లో మాన్యువల్ గా ఏదైనా మార్చినా, ArgoCD దాన్ని వెంటనే గుర్తించి గిట్‌లో ఉన్న అసలైన స్థితికి సరిదిద్దుతుంది (Self-heal / Drift Detection).",
        "example": """# ArgoCD Application డెఫినిషన్
'''yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: billing-service
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/company/k8s-manifests.git'
    targetRevision: HEAD
    path: env/production/billing
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: billing
  syncPolicy:
    automated:
      prune: true     # గిట్ లో డిలీట్ చేస్తే క్లస్టర్ లోనూ డిలీట్ అవుతుంది
      selfHeal: true  # మాన్యువల్ మార్పులను ఆటోమేటిక్ గా సరిచేస్తుంది!
''' """,
        "mistake": "CI పైప్‌లైన్ (GitHub Actions) నుండి ప్రొడక్షన్ కుబెర్‌నెటిస్ క్లస్టర్ లోకి నేరుగా `kubectl apply` పుష్ చేయడం; ఇది సెక్యూరిటీ పరంగా రిస్క్ (Cluster credentials బయట ఉంటాయి). GitOps లో క్లస్టర్ లోపలి నుండే పుల్ (Pull-based) జరుగుతుంది."
    },
    {
        "title": "Progressive Delivery (Canary, Blue-Green, Flagger)",
        "subtitle": "ప్రోగ్రెసివ్ డెలివరీ (కొత్త కోడ్‌ను ఒక్కసారే కాకుండా కొద్ది శాతం కస్టమర్లపై ఆటోమేటిక్ మెట్రిక్స్ చెక్ చేస్తూ రిలీజ్ చేయడం)",
        "why": "కొత్త రిలీజ్ లో దాగివున్న మెమరీ లీక్ లేదా బగ్ వల్ల ఒకేసారి 100% యూజర్లకు సైట్ బ్రేక్ అవ్వకుండా రక్షించాలి.",
        "explanation": "సాంప్రదాయ రోలింగ్ అప్‌డేట్ కేవలం కంటైనర్ రన్ అవుతోందో లేదో మాత్రమే చూస్తుంది (యాప్ 500 ఎర్రర్స్ ఇస్తున్నా తెలియదు). Progressive Delivery లో Argo Rollouts లేదా Flagger టూల్స్ Prometheus మెట్రిక్స్ ను పరిశీలిస్తాయి: \n1. కొత్త వెర్షన్ (v2) కు మొదట కేవలం 5% ట్రాఫిక్ మాత్రమే మళ్లిస్తారు. \n2. తరువాతి 10 నిమిషాలు ఆ 5% ట్రాఫిక్ యొక్క HTTP ఎర్రర్ రేట్ (< 0.5%) మరియు P99 లాటెన్సీని కొలుస్తాయి. \n3. మెట్రిక్స్ అన్నీ ఆరోగ్యంగా ఉంటే, ఆటోమేటిక్ గా 20%, 50%, చివరకు 100% కి పెంచుతాయి. \n4. ఎర్రర్ రేట్ కొద్దిగా పెరిగినా, మనుషుల ప్రమేయం లేకుండా క్షణాల్లో ఆటో-రోల్‌బ్యాక్ (Rollback to v1) చేస్తాయి.",
        "example": """# Argo Rollouts Canary స్పెసిఫికేషన్
'''yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: order-api
spec:
  strategy:
    canary:
      steps:
      - setWeight: 5
      - pause: {duration: 10m} # 10 నిమిషాలు మెట్రిక్స్ అబ్జర్వ్ చేయడం
      - analysis:
          templates:
          - templateName: success-rate-metric-check
      - setWeight: 25
      - pause: {duration: 30m}
      - setWeight: 100
''' """,
        "mistake": "కెనరీ విశ్లేషణలో శాంపిల్ సైజ్ చాలా చిన్నదిగా ఉండటం; కేవలం 10 రిక్వెస్ట్‌లు మాత్రమే వచ్చినప్పుడు ఎర్రర్ రేట్ విశ్లేషణ తప్పుడు ఫలితాలను ఇస్తుంది."
    },
    {
        "title": "Multi-Tenancy Isolation (Resource & Security Boundaries)",
        "subtitle": "మల్టీ-టెనెన్సీ ఐసోలేషన్ (ఒకే కుబెర్‌నెటిస్ క్లస్టర్‌ను వేర్వేరు కస్టమర్లు లేదా టీమ్‌లు సురక్షితంగా పంచుకోవడం)",
        "why": "ప్రతి చిన్న టీమ్ కోసం లేదా ప్రతి క్లయింట్ కోసం ప్రత్యేకంగా వేర్వేరు కుబెర్‌నెటిస్ క్లస్టర్లను కొంటే క్లౌడ్ ఖర్చులు విపరీతంగా పెరిగిపోతాయి.",
        "explanation": "రెండు రకాల టెనెన్సీ ఉంటుంది: \n1. Soft Multi-Tenancy (అంతర్గత టీమ్‌ల కోసం): Kubernetes Namespaces, ResourceQuotas (CPU/RAM పరిమితులు), NetworkPolicies (టీమ్‌ల మధ్య ట్రాఫిక్ బ్లాకింగ్) మరియు RBAC ద్వారా సాధిస్తారు. \n2. Hard Multi-Tenancy (నమ్మకం లేని బాహ్య కస్టమర్ల కోసం): సాధారణ నేమ్‌స్పేస్‌లు కెర్నల్ ను షేర్ చేసుకుంటాయి కాబట్టి సెక్యూరిటీ సరిపోదు. దీనికోసం వర్చువల్ క్లస్టర్లు (vCluster), Kata Containers లేదా gVisor (హార్డ్‌వేర్ ఆధారిత తేలికపాటి మైక్రో-VM శాండ్‌బాక్సింగ్) వాడతారు. ఒక టెనెంట్ హ్యాక్ అయినా హోస్ట్ సర్వర్ కెర్నల్ ముట్టుకోలేరు.",
        "example": """# Kubernetes ResourceQuota టెనెంట్ పరిమితి
'''yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: tenant-team-a-quota
  namespace: team-a
spec:
  hard:
    requests.cpu: "4"
    requests.memory: "8Gi"
    limits.cpu: "8"
    limits.memory: "16Gi"
    pods: "20" # టీమ్-ఎ గరిష్టంగా 20 పాడ్స్ మాత్రమే రన్ చేయగలదు
''' """,
        "mistake": "మల్టీ-టెనెంట్ క్లస్టర్ లో NetworkPolicy కాన్ఫిగర్ చేయకపోవడం; డీఫాల్ట్ గా కుబెర్‌నెటిస్ లో ఒక నేమ్‌స్పేస్ లోని పాడ్ వేరే ఏ నేమ్‌స్పేస్ పాడ్ తోనైనా మాట్లాడగలదు."
    },
    {
        "title": "Platform Engineering (Internal Developer Platforms - IDP)",
        "subtitle": "ప్లాట్‌ఫామ్ ఇంజనీరింగ్ (డెవలపర్లు క్లౌడ్ సంక్లిష్టతలతో కుస్తీ పడకుండా సెల్ఫ్-సర్వీస్ పోర్టల్స్ అందించడం)",
        "why": "డెవలపర్లు కోడ్ రాయడం మానేసి, రోజంతా 500 లైన్ల కుబెర్‌నెటిస్ YAML, IAM రోల్స్, నెట్‌వర్క్ కాన్ఫిగరేషన్లతో కుస్తీ పడుతూ విసుగు చెందుతున్నారు.",
        "explanation": "DevOps తదుపరి పరిణామ క్రమమే Platform Engineering. ఒక ప్రత్యేక ప్లాట్‌ఫామ్ టీమ్ Spotify Backstage, Port లేదా Mia-Platform లాంటి ఒక 'Internal Developer Platform' (IDP) ని నిర్మిస్తుంది. డెవలపర్‌కు ఒక కొత్త సర్వీస్, డేటాబేస్ లేదా టెస్టింగ్ ఎన్విరాన్‌మెంట్ కావాలంటే, డెవొప్స్ ఇంజనీర్‌కు టిక్కెట్ పెట్టాల్సిన పనిలేదు; పోర్టల్‌లో ఒక బటన్ నొక్కితే ఆటోమేటిక్ గా గిట్ రిపోజిటరీ, CI/CD పైప్‌లైన్, కుబెర్‌నెటిస్ ఆర్కిటెక్చర్ క్షణాల్లో సెల్ఫ్-సర్వీస్ గా రెడీ అయిపోతాయి.",
        "example": """# Spotify Backstage సాఫ్ట్‌వేర్ టెంప్లేట్ (IDP) భావన
# డెవలపర్ వెబ్ UI లో వివరాలు ఇస్తాడు:
# Service Name: "payment-gateway"
# Language: "FastAPI / Python"
# Database: "PostgreSQL Aurora"
#
# IDP వెనుక టెర్రాఫార్మ్ మరియు ఆర్గోసీడీ రన్ చేసి 2 నిమిషాల్లో ప్రొడక్షన్-రెడీ 
# రిపోజిటరీని డెవలపర్‌కు అందిస్తుంది!""",
        "mistake": "డెవలపర్ల అభిప్రాయాలు తీసుకోకుండా ప్లాట్‌ఫామ్‌ను వారిపై బలవంతంగా రుద్దడం; ఒక ప్లాట్‌ఫామ్ అంతర్గత ఉత్పత్తిగా (Platform as a Product) విజయవంతం కావాలంటే యూజర్ ఎక్స్‌పీరియన్స్ బాగుండాలి."
    },
    {
        "title": "Golden Paths (Paved Roads for Developer Workflows)",
        "subtitle": "గోల్డెన్ పాత్స్ (కంపెనీలో ఒక కొత్త ఫీచర్ ను సురక్షితంగా ప్రొడక్షన్ కు చేర్చే సుగమమైన రహదారి)",
        "why": "కంపెనీలోని 100 మంది డెవలపర్లు తమకు నచ్చినట్లు 100 రకాల విభిన్న పద్ధతులలో డాకర్ ఫైల్స్, లాగింగ్, డిప్లాయ్‌మెంట్స్ రాస్తే సిస్టమ్ గందరగోళంగా మారుతుంది.",
        "explanation": "నెట్‌ఫ్లిక్స్ ప్రారంభించిన భావన ఇది ('Paved Road' or 'Golden Path'). కంపెనీలో ఒక పనిని పూర్తి చేయడానికి ఉత్తమమైన, సెక్యూరిటీ ఆమోదించిన, అత్యంత వేగవంతమైన ఒక ప్రామాణిక మార్గాన్ని సిద్ధం చేస్తారు. ఉదాహరణకు: 'మీరు ఒక కొత్త మైక్రోసర్వీస్ మొదలుపెట్టాలనుకుంటే, మా అధికారిక Golden Path టెంప్లేట్ వాడితే లాగింగ్, మానిటరింగ్, mTLS, CI/CD ఆటోమేటిక్ గా లభిస్తాయి. మీరు వేరే వింత టెక్నాలజీ వాడాలనుకుంటే మీరే సొంతంగా అన్నీ మేనేజ్ చేసుకోవాలి'. డెవలపర్లు స్వేచ్ఛగా సులభమైన ఈ బంగారు బాటను ఎంచుకుంటారు.",
        "example": """# Golden Path చెక్‌లిస్ట్
# 1. Base Dockerfile (భద్రతా స్కాన్ పూర్తయిన అధికారిక కంపెనీ ఇమేజ్)
# 2. CI/CD Template (ఆటోమేటిక్ SonarQube, Snyk, Trivy స్కానింగ్)
# 3. Observability Standards (OpenTelemetry ట్రేసింగ్ ముందే అమర్చబడి ఉంటుంది)
# 4. Helm Chart / Kustomize బేస్ కాన్ఫిగరేషన్
# డెవలపర్ కేవలం తన వ్యాపార లాజిక్ పై మాత్రమే దృష్టి పెడతాడు!""",
        "mistake": "గోల్డెన్ పాత్‌ను జైలు లాగా మార్చి కఠినమైన ఆంక్షలు విధించడం; ప్రామాణిక మార్గాన్ని సులభతరం చేయాలి కానీ ప్రత్యేక ఆవిష్కరణలను పూర్తిగా అణచివేయకూడదు."
    }
]
