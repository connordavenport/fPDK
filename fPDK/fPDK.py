from fontTools.ttLib import TTFont
import os
from fontTools.designspaceLib import DesignSpaceDocument as dsp_doc
from fontTools.designspaceLib import DiscreteAxisDescriptor, AxisDescriptor
from fontTools.designspaceLib.split import *
import fontTools.varLib as varLib
from fontTools.misc.fixedTools import otRound, strToFixedToFloat, floatToFixedToFloat
import fnmatch
from typing import Union
import re
import drawBot as bot
import drawBotGrid as grid
from drawBotGrid import textOverflowTestMode as overflow_mode
import more_itertools as mit

from defcon.tools.identifiers import makeRandomIdentifier
from pathlib import Path
import getpass
import datetime
from ufoProcessor.ufoOperator import UFOOperator as uop
import plistlib
import inspect
from random import randint, choice
from collections.abc import MutableSequence

from english_words import get_english_words_set

# fPDK, font Proofing Development Kit

USER = getpass.getuser()

CORE         = ()
RUNNING_TEXT = ()
OPENTYPE     = ()
GRADIENT     = ()
INSPECTOR    = ()

SECTION_TYPES = [CORE, RUNNING_TEXT, OPENTYPE, GRADIENT, INSPECTOR]

PROOF_DATA = {

    "core"           : "ABCDEFGHIJKLM\nNOPQRSTUVWXYZ\nabcdefghijklm\nnopqrstuvwxyz\n0123456789ªº\n%*.,:;!¡?¿‽#/\\\n-—_(){}[]‚“”‘’‹›\"\'\n+−×=><@&§®℗|¢$€£¥",
    "spacing"        : "NULL",
    "figures"        : "0123456789 H0H1H2H3H4H5H6H7H8H9"+"\n"+"".join([str((randint(0,9))) for i in range(1000)]),
    "lowercaseCopy"  : "Angel Adept Blind Bodice Clique Coast Dunce Docile Enact Eosin Furlong Focal Gnome Gondola Human Hoist Inlet Iodine Justin Jocose Knoll Koala Linden Loads Milliner Modal Number Nodule Onset Oddball Pneumo Poncho Quanta Qophs Rhone Roman Snout Sodium Tundra Tocsin Uncle Udder Vulcan Vocal Whale Woman Xmas Xenon Yunnan Young Zloty Zodiac. Angel angel adept for the nuance loads of the arena cocoa and quaalude. Blind blind bodice for the submit oboe of the club snob and abbot. Clique clique coast for the pouch loco of the franc assoc and accede. Dunce dunce docile for the loudness mastodon of the loud statehood and huddle. Enact enact eosin for the quench coed of the pique canoe and bleep. Furlong furlong focal for the genuflect profound of the motif aloof and offers. Gnome gnome gondola for the impugn logos of the unplug analog and smuggle. Human human hoist for the buddhist alcohol of the riyadh caliph and bathhouse. Inlet inlet iodine for the quince champion of the ennui scampi and shiite. Justin justin jocose for the djibouti sojourn of the oranj raj and hajjis. Knoll knoll koala for the banknote lookout of the dybbuk outlook and trekked. Linden linden loads for the ulna monolog of the consul menthol and shallot. Milliner milliner modal for the alumna solomon of the album custom and summon. Number number nodule for the unmade economic of the shotgun bison and tunnel. Onset onset oddball for the abandon podium of the antiquo tempo and moonlit. Pneumo pneumo poncho for the dauphin opossum of the holdup bishop and supplies. Quanta quanta qophs for the inquest sheqel of the cinq coq and suqqu. Rhone rhone roman for the burnt porous of the lemur clamor and carrot. Snout snout sodium for the ensnare bosom of the genus pathos and missing. Tundra tundra tocsin for the nutmeg isotope of the peasant ingot and ottoman. Uncle uncle udder for the dunes cloud of the hindu thou and continuum. Vulcan vulcan vocal for the alluvial ovoid of the yugoslav chekhov and revved. Whale whale woman for the meanwhile blowout of the forepaw meadow and glowworm. Xmas xmas xenon for the bauxite doxology of the tableaux equinox and exxon. Yunnan yunnan young for the dynamo coyote of the obloquy employ and sayyid. Zloty zloty zodiac for the gizmo ozone of the franz laissez and buzzing.",
    "uppercaseCopy"  : "ABIDE ACORN OF THE HABIT DACRON FOR THE BUDDHA GOUDA QUAALUDE. BENCH BOGUS OF THE SCRIBE ROBOT FOR THE APLOMB JACOB RIBBON. CENSUS CORAL OF THE SPICED JOCOSE FOR THE BASIC HAVOC SOCCER. DEMURE DOCILE OF THE TIDBIT LODGER FOR THE CUSPID PERIOD BIDDER. EBBING ECHOING OF THE BUSHED DECAL FOR THE APACHE ANODE NEEDS. FEEDER FOCUS OF THE LIFER BEDFORD FOR THE SERIF PROOF BUFFER. GENDER GOSPEL OF THE PIGEON DOGCART FOR THE SPRIG QUAHOG DIGGER. HERALD HONORS OF THE DIHEDRAL MADHOUSE FOR THE PENH RIYADH BATHHOUSE. IBSEN ICEMAN OF THE APHID NORDIC FOR THE SUSHI SAUDI SHIITE. JENNIES JOGGER OF THE TIJERA ADJOURN FOR THE ORANJ KOWBOJ HAJJIS. KEEPER KOSHER OF THE SHRIKE BOOKCASE FOR THE SHEIK LOGBOOK CHUKKAS. LENDER LOCKER OF THE CHILD GIGOLO FOR THE UNCOIL GAMBOL ENROLLED. MENACE MCCOY OF THE NIMBLE TOMCAT FOR THE DENIM RANDOM SUMMON. NEBULA NOSHED OF THE INBRED BRONCO FOR THE COUSIN CARBON KENNEL. OBSESS OCEAN OF THE PHOBIC DOCKSIDE FOR THE GAUCHO LIBIDO HOODED. PENNIES PODIUM OF THE SNIPER OPCODE FOR THE SCRIP BISHOP HOPPER. QUANTA QOPHS OF THE INQUEST OQOS FOR THE CINQ COQ SUQQU. REDUCE ROGUE OF THE GIRDLE ORCHID FOR THE MEMOIR SENSOR SORREL. SENIOR SCONCE OF THE DISBAR GODSON FOR THE HUBRIS AMENDS LESSEN. TENDON TORQUE OF THE UNITED SCOTCH FOR THE NOUGHT FORGOT BITTERS. UNDER UGLINESS OF THE RHUBARB SEDUCE FOR THE MANCHU HINDU CONTINUUM. VERSED VOUCH OF THE DIVER OVOID FOR THE TELAVIV KARPOV FLIVVER. WENCH WORKER OF THE UNWED SNOWCAP FOR THE ANDREW ESCROW GLOWWORM. XENON XOCHITL OF THE MIXED BOXCAR FOR THE SUFFIX ICEBOX EXXON. YEOMAN YONDER OF THE HYBRID ARROYO FOR THE DINGHY BRANDY SAYYID. ZEBRA ZOMBIE OF THE PRIZED OZONE FOR THE FRANZ ARROZ BUZZING.",
    "paragraph"      : """Tetrahydrobiopterin (BH4, THB), also known as sapropterin (INN), is a cofactor of the three aromatic amino acid hydroxylase enzymes, used in the degradation of amino acid phenylalanine and in the biosynthesis of the neurotransmitters serotonin (5-hydroxytryptamine, 5-HT), melatonin, dopamine, norepinephrine (noradrenaline), epinephrine (adrenaline), and is a cofactor for the production of nitric oxide (NO) by the nitric oxide synthases. Chemically, its structure is that of a (dihydropteridine reductase) reduced pteridine derivative (quinonoid dihydrobiopterin). Tetrahydrobiopterin is available as a tablet for oral administration in the form of sapropterin dihydrochloride (BH4*2HCL). It was approved for use in the United States as a tablet in December 2007 and as a powder in December 2013. It was approved for use in the European Union in December 2008, Canada in April 2010, and Japan in July 2008. It is sold under the brand names Kuvan and Biopten. The typical cost of treating a patient with Kuvan is US$100,000 per year. BioMarin holds the patent for Kuvan until at least 2024, but Par Pharmaceutical has a right to produce a generic version by 2020. Sapropterin is indicated in tetrahydrobiopterin deficiency caused by GTP cyclohydrolase I (GTPCH) deficiency, or 6-pyruvoyltetrahydropterin synthase (PTPS) deficiency. Also, BH4*2HCL is FDA approved for use in phenylketonuria (PKU), along with dietary measures. However, most people with PKU have little or no benefit from BH4*2HCL. The most common adverse effects, observed in more than 10% of people, include headache and a running or obstructed nose. Diarrhea and vomiting are also relatively common, seen in at least 1% of people. No interaction studies have been conducted. Because of its mechanism, tetrahydrobiopterin might interact with dihydrofolate reductase inhibitors like methotrexate and trimethoprim, and NO-enhancing drugs like nitroglycerin, molsidomine, minoxidil, and PDE5 inhibitors. Combination of tetrahydrobiopterin with levodopa can lead to increased excitability. Tetrahydrobiopterin has multiple roles in human biochemistry. The major one is to convert amino acids such as phenylalanine, tyrosine, and tryptophan to precursors of dopamine and serotonin, major monoamine neurotransmitters. It works as a cofactor, being required for an enzyme's activity as a catalyst, mainly hydroxylases. Tetrahydrobiopterin is a cofactor for tryptophan hydroxylase (TPH) for the conversion of L-tryptophan (TRP) to 5-hydroxytryptophan (5-HTP). Phenylalanine hydroxylase (PAH) catalyses the conversion of L-phenylalanine (PHE) to L-tyrosine (TYR). Therefore, a deficiency in tetrahydrobiopterin can cause a toxic buildup of L-phenylalanine, which manifests as the severe neurological issues seen in phenylketonuria. Tyrosine hydroxylase (TH) catalyses the conversion of L-tyrosine to L-DOPA (DOPA), which is the precursor for dopamine. Dopamine is a vital neurotransmitter, and is the precursor of norepinephrine and epinephrine. Thus, a deficiency of BH4 can lead to systemic deficiencies of dopamine, norepinephrine, and epinephrine. In fact, one of the primary conditions that can result from GTPCH-related BH4 deficiency is dopamine-responsive dystonia; currently, this condition is typically treated with carbidopa/levodopa, which directly restores dopamine levels within the brain. Nitric oxide synthase (NOS) catalyses the conversion of a guanidino nitrogen of L-arginine (L-Arg) to nitric oxide (NO). Among other things, nitric oxide is involved in vasodilation, which improves systematic blood flow. The role of BH4 in this enzymatic process is so critical that some research points to a deficiency of BH4 – and thus, of nitric oxide – as being a core cause of the neurovascular dysfunction that is the hallmark of circulation-related diseases such as diabetes. Ether lipid oxidase (alkylglycerol monooxygenase, AGMO) catalyses the conversion of 1-alkyl-sn-glycerol to 1-hydroxyalkyl-sn-glycerol. Tetrahydrobiopterin was discovered to play a role as an enzymatic cofactor. The first enzyme found to use tetrahydrobiopterin is phenylalanine hydroxylase (PAH). Tetrahydrobiopterin is biosynthesized from guanosine triphosphate (GTP) by three chemical reactions mediated by the enzymes GTP cyclohydrolase I (GTPCH), 6-pyruvoyltetrahydropterin synthase (PTPS), and sepiapterin reductase (SR). BH4 can be oxidized by one or two electron reactions, to generate BH4 or BH3 radical and BH2, respectively. Research shows that ascorbic acid (also known as ascorbate or vitamin C) can reduce BH3 radical into BH4, preventing the BH3 radical from reacting with other free radicals (superoxide and peroxynitrite specifically). Without this recycling process, uncoupling of the endothelial nitric oxide synthase (eNOS) enzyme and reduced bioavailability of the vasodilator nitric oxide occur, creating a form of endothelial dysfunction. Ascorbic acid is oxidized to dehydroascorbic acid during this process, although it can be recycled back to ascorbic acid. Folic acid and its metabolites seem to be particularly important in the recycling of BH4 and NOS coupling. Other than PKU studies, tetrahydrobiopterin has participated in clinical trials studying other approaches to solving conditions resultant from a deficiency of tetrahydrobiopterin. These include autism, depression, ADHD, hypertension, endothelial dysfunction, and chronic kidney disease. Experimental studies suggest that tetrahydrobiopterin regulates deficient production of nitric oxide in cardiovascular disease states, and contributes to the response to inflammation and injury, for example in pain due to nerve injury. A 2015 BioMarin-funded study of PKU patients found that those who responded to tetrahydrobiopterin also showed a reduction of ADHD symptoms. In psychiatry, tetrahydrobiopterin has been hypothesized to be involved in the pathophysiology of depression, although evidence is inconclusive to date. In 1997, a small pilot study was published on the efficacy of tetrahydrobiopterin (BH4) on relieving the symptoms of autism, which concluded that it "might be useful for a subgroup of children with autism" and that double-blind trials are needed, as are trials which measure outcomes over a longer period of time. In 2010, Frye et al. published a paper which concluded that it was safe, and also noted that "several clinical trials have suggested that treatment with BH4 improves ASD symptomatology in some individuals." Since nitric oxide production is important in regulation of blood pressure and blood flow, thereby playing a significant role in cardiovascular diseases, tetrahydrobiopterin is a potential therapeutic target. In the endothelial cell lining of blood vessels, endothelial nitric oxide synthase is dependent on tetrahydrobiopterin availability. Increasing tetrahydrobiopterin in endothelial cells by augmenting the levels of the biosynthetic enzyme GTPCH can maintain endothelial nitric oxide synthase function in experimental models of disease states such as diabetes, atherosclerosis, and hypoxic pulmonary hypertension. However, treatment of people with existing coronary artery disease with oral tetrahydrobiopterin is limited by oxidation of tetrahydrobiopterin to the inactive form, dihydrobiopterin, with little benefit on vascular function. Depletion of tetrahydrobiopterin occurs in the hypoxic brain and leads to toxin production. Preclinical studies in mice reveal that treatment with oral tetrahydrobiopterin therapy mitigates the toxic effects of hypoxia on the developing brain, specifically improving white matter development in hypoxic animals. GTPCH (GCH1) and tetrahydrobiopterin were found to have a secondary role protecting against cell death by ferroptosis in cellular models by limiting the formation of toxic lipid peroxides. Tetrahydrobiopterin acts as a potent, diffusable antioxidant that resists oxidative stress and enables cancer cell survival via promotion of angiogenesis.""",

    "kerning"        : {
        "frequent"       : "the be to of and a in that have I it for not on with he as you do at this but his by from they we say her she or an will my one all would there their what so up out if about who get which go me when make can like time no just him know take people into year your good some could them see other than then now look only come its over think also back after use two how our work first well way even new want because any these give day most us el de que y a en un ser se no haber por con su para como estar tener le lo todo pero más hacer o poder decir este ir otro ese la si me ya ver porque dar cuando él muy sin vez mucho saber qué sobre mi alguno mismo yo también hasta año dos querer entre así primero desde grande eso ni nos llegar pasar tiempo ella sí día uno bien poco deber entonces poner cosa tanto hombre parecer nuestro tan donde ahora parte después vida quedar siempre creer hablar llevar dejar nada cada seguir menos nuevo encontrar como I seu que ele foi para em são com eles ser em uma tem este a por quente palavra mas o alguns é ele você ou teve o de a e uma em nós lata fora outro foram que fazer seu tempo se vontade como disse uma cada dizer faz conjunto três quer ar bem também jogar pequeno fim colocar casa ler mão port grande soletrar adicionar mesmo terra aqui necessário grande tais siga ato por perguntar homens mudança fui luz tipo off precisa casa imagem tentar nós novamente animais ponto mãe mundo perto construir auto terra pai le de un à être et en avoir que pour dans ce il qui ne sur se pas plus pouvoir par je avec tout faire son mettre autre on mais nous comme ou si leur y dire elle devoir avant deux même prendre aussi celui donner bien où fois vous encore nouveau aller cela entre premier vouloir déjà grand mon me moins aucun lui temps très savoir falloir voir quelque sans raison notre dont non an monde jour monsieur demander alors après trouver personne rendre part dernier venir pendant passer peu lequel suite bon comprendre depuis point ainsi heure rester der die das und sein in ein zu haben ich werden sie von nicht mit es sich auch auf für an er so dass können dies als ihr ja wie bei oder wir aber dann man da sein noch nach was also aus all wenn nur müssen sagen um über machen kein Jahr du mein schon vor durch geben mehr andere viel kommen jetzt sollen mir wollen ganz mich immer gehen sehr hier doch bis groß wieder Mal zwei gut wissen neu sehen lassen uns weil unter denn stehen jede Beispiel Zeit erste ihm ihn wo lang eigentlich damit selbst",
        "kern king"      : "lynx tuft frogs, dolphins abduct by proxy the ever awkward klutz, dud, dummkopf, jinx snubnose filmgoer, orphan sgt. renfruw grudgek reyfus, md. sikh psych if halt tympany jewelry sri heh! twyer vs jojo pneu fylfot alcaaba son of nonplussed halfbreed bubbly playboy guggenheim daddy coccyx sgraffito effect, vacuum dirndle impossible attempt to disvalue, muzzle the afghan czech czar and exninja, bob bixby dvorak wood dhurrie savvy, dizzy eye aeon circumcision uvula scrungy picnic luxurious special type carbohydrate ovoid adzuki kumquat bomb? afterglows gold girl pygmy gnome lb. ankhs acme aggroupment akmed brouhha tv wt. ujjain ms. oz abacus mnemonics bhikku khaki bwana aorta embolism vivid owls often kvetch otherwise, wysiwyg densfort wright you’ve absorbed rhythm, put obstacle kyaks krieg kern wurst subject enmity equity coquet quorum pique tzetse hepzibah sulfhydryl briefcase ajax ehler kafka fjord elfship halfdressed jugful eggcup hummingbirds swingdevil bagpipe legwork reproachful hunchback archknave baghdad wejh rijswijk rajbansi rajput ajdir okay weekday obfuscate subpoena liebknecht marcgravia ecbolic arcticward dickcissel pincpinc boldface maidkin adjective adcraft adman dwarfness applejack darkbrown kiln palzy always farmland flimflam unbossy nonlineal stepbrother lapdog stopgap sx countdown basketball beaujolais vb. flowchart aztec lazy bozo syrup tarzan annoying dyke yucky hawg gagzhukz cuzco squire when hiho mayhem nietzsche szasz gumdrop milk emplotment ambidextrously lacquer byway ecclesiastes stubchen hobgoblins crabmill aqua hawaii blvd. subquality byzantine empire debt obvious cervantes jekabzeel anecdote flicflac mechanicville bedbug couldn’t i’ve it’s they’ll they’d dpt. headquarter burkhardt xerxes atkins govt. ebenezer lg. lhama amtrak amway fixity axmen quumbabda upjohn hrumpf",
        "diacritic cntx" : "Zsittnik Sinn Féin Oötooid Echinococcose Ovoviviparous Tqibuli Ñacuñán Üüdipä Annuis Cœptis Sígarettumunn Skoðaðu Stuöðugri Eðlisfræði syvyys Pääsymaksut Þórarinsson Næstvæd Åsså Åbenrå Fæøerne Føroyar Nöje Pinggera Egger Schifffahrt Greüzi Nööd Türkçe Şiir ürünü výročné súţže zeeëgel Koffie IJsbrand Ÿsbrand Meeùs Wisła Łódź łódź Michał Złoty złoty",
        "ruder 1"        : "bibel malhabile modo biegen peuple punibile blind qualifier quindi damals quelle dinamica china quelque analiso schaden salomon macchina schein sellier secondo lager sommier singolo legion unique possibile mime unanime unico mohn usuel legge nagel abonner unione puder agir punizione quälen aiglon dunque huldigen allégir quando geduld alliance uomini",
        "ruder 2"        : "vertrag crainte screw verwalter croyant science verzicht fratricide sketchy vorrede frivolité story yankee instruction take zwetschge lyre treaty zypresse navette tricycle fraktur nocturne typograph kraft pervertir vanity raffeln presto victory reaktion prévoyant vivacity rekord priorité wayward revolte proscrire efficiency tritt raviver without trotzkopf tactilité through tyrann arrêt known",
        "all pairs"      : "Aardvark Ablution Acrimonious Adventures Aeolian Africa Agamemnon Ahoy Aileron Ajax Akimbo Altruism America Anecdote Aorta Aptitude Aquarium Arcade Aspartame Attrition Aurelius Avuncular Awning Axminster Ayers Azure Banishment Bb Bc Bd Benighted Bf Bg Bhagavad Biblical Bjorn Bk Blancmange Bm Bn Bolton Bp Bq Brusque Bs Bt Burnish Bv Bwana Bx Byzantium Bz Cabbala Cb Cc Cd Cetacean Cf Cg Charlemagne Cicero Cj Ck Clamorous Cm Cnidarian Conifer Cp Cq Crustacean Cs Ctenoid Culled Cv Cw Cx Cynosure Czarina Dalmatian Db Dc Dd Delphi Df Dg Dhurrie Dinner Djinn Dk Dl Dm Dn Document Dp Dq Drill Ds Dt Dunleary Dvorak Dwindle Dx Dynamo Dz Eames Ebullient Echo Edify Eels Eftsoons Egress Ehrlich Eindhoven Eject Ekistics Elzevir Eminence Ennoble Eocene Ephemeral Equator Erstwhile Estienne Etiquette Eucalyptus Everyman Ewen Exeter Eyelet Ezekiel Fanfare Fb Fc Fd Ferocious Ffestiniog Fg Fh Finicky Fjord Fk Flanders Fm Fn Forestry Fp Fq Frills Fs Ft Furniture Fv Fw Fx Fylfot Fz Garrulous Gb Gc Gd Generous Gf Gg Ghastly Gimlet Gj Gk Glorious Gm Gnomon Golfer Gp Gq Grizzled Gs Gt Gumption Gv Gwendolyn Gx Gymkhana Gz Harrow Hb Hc Hd Heifer Hf Hg Hh Hindemith Hj Hk Hl Hm Hn Horace Hp Hq Hr Hsi Ht Hubris Hv Hw Hx Hybrid Hz Iambic Ibarra Ichthyology Identity Ievgeny Ifrit Ignite Ihre Ii Ij Ikon Iliad Imminent Innovation Iolanthe Ipanema Iq Irascible Island Italic Iu Ivory Iwis Ixtapa Iyar Izzard Janacek Jb Jc Jd Jenson Jf Jg Jh Jitter Jj Jk Jl Jm Jn Joinery Jp Jq Jr. Js Jt Jungian Jv Jw Jx Jy Jz Kaiser Kb Kc Kd Kenilworth Kf Kg Khaki Kindred Kj Kk Klondike Km Knowledge Kohlrabi Kp Kq Kraken Ks Kt Kudzu Kvetch Kwacha Kx Kyrie Kz Labrador Lb Lc Ld Lent Lf Lg Lhasa Liniment Lj Lk Llama Lm Ln Longboat Lp Lq Lr Ls Lt Luddite Lv Lw Lx Lyceum Lz Mandarin Mbandaka Mcintyre Mdina Mendacious Mfg. Mg Mh Millinery Mj Mk Mlle. Mme. Mnemonic Moribund Mp Mq Mr. Ms. Mtn. Munitions Mv Mw Mx Myra Mz Narragansett Nb Nc Nd Nefarious Nf Nguyen Nh Nile Nj Nkoso Nl Nm Nnenna Nonsense Np Nq Nr. Ns Nt Nunnery Nv Nw Nx Nyack Nz Oarsman Oblate Ocular Odessa Oedipus Often Ogre Ohms Oilers Oj Okra Olfactory Ominous Onerous Oogamous Opine Oq Ornate Ossified Othello Oubliette Ovens Owlish Oxen Oyster Ozymandias Parisian Pb Pc Pd. Penrose Pfennig Pg. Pharmacy Pirouette Pj Pk Pleistocene Pm Pneumatic Porridge Pp. Pq Principle Psaltery Ptarmigan Pundit Pv Pw Px Pyrrhic Pz Qaid Qb Qc Qd Qed Qf Qg Qh Qibris Qj Qk Ql Qm Qn Qom Qp Qq Qr Qs Qt Quill Qv Qw Qx Qy Qz Ransom Rb. Rc Rd. Renfield Rf Rg Rheumatic Ringlet Rj Rk Rl Rm. Rn Ronsard Rp. Rq Rr Rs Rte. Runcible Rv Rwanda Rx Rye Rz Salacious Sbeitla Scherzo Sd Serpentine Sforza Sg Shackles Sinful Sjoerd Skull Slalom Smelting Snipe Sorbonne Spartan Squire Sri Ss Stultified Summoner Svelte Swarthy Sx Sykes Szentendre Tarragon Tblisi Tcherny Td Tennyson Tf Tg Thaumaturge Tincture Tj Tk Tlaloc Tm Tn Toreador Tp Tq Treacherous Tsunami Tt Turkey Tv Twine Tx Tyrolean Tzara Ua Ubiquitous Ucello Udder Ue Ufology Ugric Uhlan Uitlander Uj Ukulele Ulster Umber Unguent Uomo Uplift Uq Ursine Usurious Utrecht Uu Uvula Uw Uxorious Uy Uzbek Vanished Vb Vc Vd. Venomous Vf Vg Vh Vindicate Vj Vk Vl Vm Vn Voracious Vp Vq Vrillier Vs. Vt. Vulnerable Vv Vw Vx Vying Vz Washington Wb Wc Wd Wendell Wf Wg Wharf Window Wj Wk Wl Wm. Wn Worth Wp Wq Wrung Ws Wt. Wunderman Wv Wx Wy Wyes Wz Xanthan Xb Xc Xd Xenon Xf Xg Xh Xiao Xj Xk Xl Xmas Xn Xo Xp Xq Xray Xs Xt Xuxa Xv Xw Xx Xylem Xz Yarrow Ybarra Ycair Yds. Yellowstone Yf Yggdrasil Yh Yin Yj Yk Ylang Ym Yn Yours Ypsilanti Yquem Yrs. Ys. Ytterbium Yunnan Yvonne Yw Yx Yy Yz Zanzibar Zb Zc Zd Zero Zf Zg Zhora Zinfandel Zj Zk Zl Zm Zn Zone Zp Zq Zr Zs Zt Zuni Zv Zwieback Zx Zygote Zz",
        "lowercase"      : "aaabacadaeafagahaiajakala amanaoapaqarasatauavawaxa ayazaðađałaøaħaŧaþaæaœaßaıa babbbcbdbebfbgbhbibjbkblb bmbnbobpbqbrbsbtbubvbwbxb bybzbðbđbłbøbħbŧbþbæbœbßbıb cacbcccdcecfcgchcicjckclc cmcncocpcqcrcsctcucvcwcxc cyczcðcđcłcøcħcŧcþcæcœcßcıc dadbdcdddedfdgdhdidjdkdld dmdndodpdqdrdsdtdudvdwdxd dydzdðdđdłdødħdŧdþdædœdßdıd eaebecedeeefegeheiejekele emeneoepeqereseteuevewexe eyezeðeđełeøeħeŧeþeæeœeßeıe fafbfcfdfefffgfhfifjfkflf fmfnfofpfqfrfsftfufvfwfxf fyfzfðfđfłføfħfŧfþfæfœfßfıf gagbgcgdgegfggghgigjgkglg gmgngogpgqgrgsgtgugvgwgxg gygzgðgđgłgøgħgŧgþgægœgßgıg hahbhchdhehfhghhhihjhkhlh hmhnhohphqhrhshthuhvhwhxh hyhzhðhđhłhøhħhŧhþhæhœhßhıh iaibicidieifigihiiijikili iminioipiqirisitiuiviwixi iyiziðiđiłiøiħiŧiþiæiœißiıi jajbjcjdjejfjgjhjijjjkjlj jmjnjojpjqjrjsjtjujvjwjxj jyjzjðjđjłjøjħjŧjþjæjœjßjıj kakbkckdkekfkgkhkikjkkklk kmknkokpkqkrksktkukvkwkxk kykzkðkđkłkøkħkŧkþkækœkßkık lalblcldlelflglhliljlklll lmlnlolplqlrlsltlulvlwlxl lylzlðlđlłlølħlŧlþlælœlßlıl mambmcmdmemfmgmhmimjmkmlm mmmnmompmqmrmsmtmumvmwmxm mymzmðmđmłmømħmŧmþmæmœmßmım nanbncndnenfngnhninjnknln nmnnnonpnqnrnsntnunvnwnxn nynznðnđnłnønħnŧnþnænœnßnın oaobocodoeofogohoiojokolo omonooopoqorosotouovowoxo oyozoðođołoøoħoŧoþoæoœoßoıo papbpcpdpepfpgphpipjpkplp pmpnpopppqprpsptpupvpwpxp pypzpðpđpłpøpħpŧpþpæpœpßpıp qaqbqcqdqeqfqgqhqiqjqkqlq qmqnqoqpqqqrqsqtquqvqwqxq qyqzqðqđqłqøqħqŧqþqæqœqßqıq rarbrcrdrerfrgrhrirjrkrlr rmrnrorprqrrrsrtrurvrwrxr ryrzrðrđrłrørħrŧrþrærœrßrır sasbscsdsesfsgshsisjsksls smsnsospsqsrssstsusvswsxs syszsðsđsłsøsħsŧsþsæsœsßsıs tatbtctdtetftgthtitjtktlt tmtntotptqtrtstttutvtwtxt tytztðtđtłtøtħtŧtþtætœtßtıt uaubucudueufuguhuiujukulu umunuoupuqurusutuuuvuwuxu uyuzuðuđułuøuħuŧuþuæuœußuıu vavbvcvdvevfvgvhvivjvkvlv vmvnvovpvqvrvsvtvuvvvwvxv vyvzvðvđvłvøvħvŧvþvævœvßvıv wawbwcwdwewfwgwhwiwjwkwlw wmwnwowpwqwrwswtwuwvwwwxw wywzwðwđwłwøwħwŧwþwæwœwßwıw xaxbxcxdxexfxgxhxixjxkxlx xmxnxoxpxqxrxsxtxuxvxwxxx xyxzxðxđxłxøxħxŧxþxæxœxßxıx yaybycydyeyfygyhyiyjykyly ymynyoypyqyrysytyuyvywyxy yyyzyðyđyłyøyħyŧyþyæyœyßyıy zazbzczdzezfzgzhzizjzkzlz zmznzozpzqzrzsztzuzvzwzxz zyzzzðzđzłzøzħzŧzþzæzœzßzız ðaðbðcðdðeðfðgðhðiðjðkðlð ðmðnðoðpðqðrðsðtðuðvðwðxð ðyðzðððđðłðøðħðŧðþðæðœðßðıð đađbđcđdđeđfđgđhđiđjđkđlđ đmđnđođpđqđrđsđtđuđvđwđxđ đyđzđðđđđłđøđħđŧđþđæđœđßđıđ łałbłcłdłełfłgłhłiłjłkłlł łmłnłołpłqłrłsłtłułvłwłxł łyłzłðłđłłłøłħłŧłþłæłœłßłıł øaøbøcødøeøføgøhøiøjøkølø ømønøoøpøqørøsøtøuøvøwøxø øyøzøðøđøłøøøħøŧøþøæøœøßøıø ħaħbħcħdħeħfħgħhħiħjħkħlħ ħmħnħoħpħqħrħsħtħuħvħwħxħ ħyħzħðħđħłħøħħħŧħþħæħœħßħıħ ŧaŧbŧcŧdŧeŧfŧgŧhŧiŧjŧkŧlŧ ŧmŧnŧoŧpŧqŧrŧsŧtŧuŧvŧwŧxŧ ŧyŧzŧðŧđŧłŧøŧħŧŧŧþŧæŧœŧßŧıŧ þaþbþcþdþeþfþgþhþiþjþkþlþ þmþnþoþpþqþrþsþtþuþvþwþxþ þyþzþðþđþłþøþħþŧþþþæþœþßþıþ æaæbæcædæeæfægæhæiæjækælæ æmænæoæpæqæræsætæuævæwæxæ æyæzæðæđæłæøæħæŧæþæææœæßæıæ œaœbœcœdœeœfœgœhœiœjœkœlœ œmœnœoœpœqœrœsœtœuœvœwœxœ œyœzœðœđœłœøœħœŧœþœæœœœßœıœ ßaßbßcßdßeßfßgßhßißjßkßlß ßmßnßoßpßqßrßsßtßußvßwßxß ßyßzßðßđßłßøßħßŧßþßæßœßßßıß ıaıbıcıdıeıfıgıhıiıjıkılı ımınıoıpıqırısıtıuıvıwıxı ıyızıðıđıłıøıħıŧıþıæıœıßııı",
        "uppercase"      : "aAaBaCaDaEaFaGaHaIaJaKa aLaMaNaOaPaQaRaSaTaUaVa aWaXaYaZaÐaŁaØaĦaŦaÞaÆaŒa bAbBbCbDbEbFbGbHbIbJbKb bLbMbNbObPbQbRbSbTbUbVb bWbXbYbZbÐbŁbØbĦbŦbÞbÆbŒb cAcBcCcDcEcFcGcHcIcJcKc cLcMcNcOcPcQcRcScTcUcVc cWcXcYcZcÐcŁcØcĦcŦcÞcÆcŒc dAdBdCdDdEdFdGdHdIdJdKd dLdMdNdOdPdQdRdSdTdUdVd dWdXdYdZdÐdŁdØdĦdŦdÞdÆdŒd eAeBeCeDeEeFeGeHeIeJeKe eLeMeNeOePeQeReSeTeUeVe eWeXeYeZeÐeŁeØeĦeŦeÞeÆeŒe fAfBfCfDfEfFfGfHfIfJfKf fLfMfNfOfPfQfRfSfTfUfVf fWfXfYfZfÐfŁfØfĦfŦfÞfÆfŒf gAgBgCgDgEgFgGgHgIgJgKg gLgMgNgOgPgQgRgSgTgUgVg gWgXgYgZgÐgŁgØgĦgŦgÞgÆgŒg hAhBhChDhEhFhGhHhIhJhKh hLhMhNhOhPhQhRhShThUhVh hWhXhYhZhÐhŁhØhĦhŦhÞhÆhŒh iAiBiCiDiEiFiGiHiIiJiKi iLiMiNiOiPiQiRiSiTiUiVi iWiXiYiZiÐiŁiØiĦiŦiÞiÆiŒi jAjBjCjDjEjFjGjHjIjJjKj jLjMjNjOjPjQjRjSjTjUjVj jWjXjYjZjÐjŁjØjĦjŦjÞjÆjŒj kAkBkCkDkEkFkGkHkIkJkKk kLkMkNkOkPkQkRkSkTkUkVk kWkXkYkZkÐkŁkØkĦkŦkÞkÆkŒk lAlBlClDlElFlGlHlIlJlKl lLlMlNlOlPlQlRlSlTlUlVl lWlXlYlZlÐlŁlØlĦlŦlÞlÆlŒl mAmBmCmDmEmFmGmHmImJmKm mLmMmNmOmPmQmRmSmTmUmVm mWmXmYmZmÐmŁmØmĦmŦmÞmÆmŒm nAnBnCnDnEnFnGnHnInJnKn nLnMnNnOnPnQnRnSnTnUnVn nWnXnYnZnÐnŁnØnĦnŦnÞnÆnŒn oAoBoCoDoEoFoGoHoIoJoKo oLoMoNoOoPoQoRoSoToUoVo oWoXoYoZoÐoŁoØoĦoŦoÞoÆoŒo pApBpCpDpEpFpGpHpIpJpKp pLpMpNpOpPpQpRpSpTpUpVp pWpXpYpZpÐpŁpØpĦpŦpÞpÆpŒp qAqBqCqDqEqFqGqHqIqJqKq qLqMqNqOqPqQqRqSqTqUqVq qWqXqYqZqÐqŁqØqĦqŦqÞqÆqŒq rArBrCrDrErFrGrHrIrJrKr rLrMrNrOrPrQrRrSrTrUrVr rWrXrYrZrÐrŁrØrĦrŦrÞrÆrŒr sAsBsCsDsEsFsGsHsIsJsKs sLsMsNsOsPsQsRsSsTsUsVs sWsXsYsZsÐsŁsØsĦsŦsÞsÆsŒs tAtBtCtDtEtFtGtHtItJtKt tLtMtNtOtPtQtRtStTtUtVt tWtXtYtZtÐtŁtØtĦtŦtÞtÆtŒt uAuBuCuDuEuFuGuHuIuJuKu uLuMuNuOuPuQuRuSuTuUuVu uWuXuYuZuÐuŁuØuĦuŦuÞuÆuŒu vAvBvCvDvEvFvGvHvIvJvKv vLvMvNvOvPvQvRvSvTvUvVv vWvXvYvZvÐvŁvØvĦvŦvÞvÆvŒv wAwBwCwDwEwFwGwHwIwJwKw wLwMwNwOwPwQwRwSwTwUwVw wWwXwYwZwÐwŁwØwĦwŦwÞwÆwŒw xAxBxCxDxExFxGxHxIxJxKx xLxMxNxOxPxQxRxSxTxUxVx xWxXxYxZxÐxŁxØxĦxŦxÞxÆxŒx yAyByCyDyEyFyGyHyIyJyKy yLyMyNyOyPyQyRySyTyUyVy yWyXyYyZyÐyŁyØyĦyŦyÞyÆyŒy zAzBzCzDzEzFzGzHzIzJzKz zLzMzNzOzPzQzRzSzTzUzVz zWzXzYzZzÐzŁzØzĦzŦzÞzÆzŒz ðAðBðCðDðEðFðGðHðIðJðKð ðLðMðNðOðPðQðRðSðTðUðVð ðWðXðYðZðÐðŁðØðĦðŦðÞðÆðŒð đAđBđCđDđEđFđGđHđIđJđKđ đLđMđNđOđPđQđRđSđTđUđVđ đWđXđYđZđÐđŁđØđĦđŦđÞđÆđŒđ łAłBłCłDłEłFłGłHłIłJłKł łLłMłNłOłPłQłRłSłTłUłVł łWłXłYłZłÐłŁłØłĦłŦłÞłÆłŒł øAøBøCøDøEøFøGøHøIøJøKø øLøMøNøOøPøQøRøSøTøUøVø øWøXøYøZøÐøŁøØøĦøŦøÞøÆøŒø ħAħBħCħDħEħFħGħHħIħJħKħ ħLħMħNħOħPħQħRħSħTħUħVħ ħWħXħYħZħÐħŁħØħĦħŦħÞħÆħŒħ ŧAŧBŧCŧDŧEŧFŧGŧHŧIŧJŧKŧ ŧLŧMŧNŧOŧPŧQŧRŧSŧTŧUŧVŧ ŧWŧXŧYŧZŧÐŧŁŧØŧĦŧŦŧÞŧÆŧŒŧ þAþBþCþDþEþFþGþHþIþJþKþ þLþMþNþOþPþQþRþSþTþUþVþ þWþXþYþZþÐþŁþØþĦþŦþÞþÆþŒþ æAæBæCæDæEæFæGæHæIæJæKæ æLæMæNæOæPæQæRæSæTæUæVæ æWæXæYæZæÐæŁæØæĦæŦæÞæÆæŒæ œAœBœCœDœEœFœGœHœIœJœKœ œLœMœNœOœPœQœRœSœTœUœVœ œWœXœYœZœÐœŁœØœĦœŦœÞœÆœŒœ ßAßBßCßDßEßFßGßHßIßJßKß ßLßMßNßOßPßQßRßSßTßUßVß ßWßXßYßZßÐßŁßØßĦßŦßÞßÆßŒß ıAıBıCıDıEıFıGıHıIıJıKı ıLıMıNıOıPıQıRıSıTıUıVı ıWıXıYıZıÐıŁıØıĦıŦıÞıÆıŒı AAABACADAEAFAGAHAIAJAKA ALAMANAOAPAQARASATAUAVA AWAXAYAZAÐAŁAØAĦAŦAÞAÆAŒA BABBBCBDBEBFBGBHBIBJBKB BLBMBNBOBPBQBRBSBTBUBVB BWBXBYBZBÐBŁBØBĦBŦBÞBÆBŒB CACBCCCDCECFCGCHCICJCKC CLCMCNCOCPCQCRCSCTCUCVC CWCXCYCZCÐCŁCØCĦCŦCÞCÆCŒC DADBDCDDDEDFDGDHDIDJDKD DLDMDNDODPDQDRDSDTDUDVD DWDXDYDZDÐDŁDØDĦDŦDÞDÆDŒD EAEBECEDEEEFEGEHEIEJEKE ELEMENEOEPEQERESETEUEVE EWEXEYEZEÐEŁEØEĦEŦEÞEÆEŒE FAFBFCFDFEFFFGFHFIFJFKF FLFMFNFOFPFQFRFSFTFUFVF FWFXFYFZFÐFŁFØFĦFŦFÞFÆFŒF GAGBGCGDGEGFGGGHGIGJGKG GLGMGNGOGPGQGRGSGTGUGVG GWGXGYGZGÐGŁGØGĦGŦGÞGÆGŒG HAHBHCHDHEHFHGHHHIHJHKH HLHMHNHOHPHQHRHSHTHUHVH HWHXHYHZHÐHŁHØHĦHŦHÞHÆHŒH IAIBICIDIEIFIGIHIIIJIKI ILIMINIOIPIQIRISITIUIVI IWIXIYIZIÐIŁIØIĦIŦIÞIÆIŒI JAJBJCJDJEJFJGJHJIJJJKJ JLJMJNJOJPJQJRJSJTJUJVJ JWJXJYJZJÐJŁJØJĦJŦJÞJÆJŒJ KAKBKCKDKEKFKGKHKIKJKKK KLKMKNKOKPKQKRKSKTKUKVK KWKXKYKZKÐKŁKØKĦKŦKÞKÆKŒK LALBLCLDLELFLGLHLILJLKL LLLMLNLOLPLQLRLSLTLULVL LWLXLYLZLÐLŁLØLĦLŦLÞLÆLŒL MAMBMCMDMEMFMGMHMIMJMKM MLMMMNMOMPMQMRMSMTMUMVM MWMXMYMZMÐMŁMØMĦMŦMÞMÆMŒM NANBNCNDNENFNGNHNINJNKN NLNMNNNONPNQNRNSNTNUNVN NWNXNYNZNÐNŁNØNĦNŦNÞNÆNŒN OAOBOCODOEOFOGOHOIOJOKO OLOMONOOOPOQOROSOTOUOVO OWOXOYOZOÐOŁOØOĦOŦOÞOÆOŒO PAPBPCPDPEPFPGPHPIPJPKP PLPMPNPOPPPQPRPSPTPUPVP PWPXPYPZPÐPŁPØPĦPŦPÞPÆPŒP QAQBQCQDQEQFQGQHQIQJQKQ QLQMQNQOQPQQQRQSQTQUQVQ QWQXQYQZQÐQŁQØQĦQŦQÞQÆQŒQ RARBRCRDRERFRGRHRIRJRKR RLRMRNRORPRQRRRSRTRURVR RWRXRYRZRÐRŁRØRĦRŦRÞRÆRŒR SASBSCSDSESFSGSHSISJSKS SLSMSNSOSPSQSRSSSTSUSVS SWSXSYSZSÐSŁSØSĦSŦSÞSÆSŒS TATBTCTDTETFTGTHTITJTKT TLTMTNTOTPTQTRTSTTTUTVT TWTXTYTZTÐTŁTØTĦTŦTÞTÆTŒT UAUBUCUDUEUFUGUHUIUJUKU ULUMUNUOUPUQURUSUTUUUVU UWUXUYUZUÐUŁUØUĦUŦUÞUÆUŒU VAVBVCVDVEVFVGVHVIVJVKV VLVMVNVOVPVQVRVSVTVUVVV VWVXVYVZVÐVŁVØVĦVŦVÞVÆVŒV WAWBWCWDWEWFWGWHWIWJWKW WLWMWNWOWPWQWRWSWTWUWVW WWWXWYWZWÐWŁWØWĦWŦWÞWÆWŒW XAXBXCXDXEXFXGXHXIXJXKX XLXMXNXOXPXQXRXSXTXUXVX XWXXXYXZXÐXŁXØXĦXŦXÞXÆXŒX YAYBYCYDYEYFYGYHYIYJYKY YLYMYNYOYPYQYRYSYTYUYVY YWYXYYYZYÐYŁYØYĦYŦYÞYÆYŒY ZAZBZCZDZEZFZGZHZIZJZKZ ZLZMZNZOZPZQZRZSZTZUZVZ ZWZXZYZZZÐZŁZØZĦZŦZÞZÆZŒZ ÐAÐBÐCÐDÐEÐFÐGÐHÐIÐJÐKÐ ÐLÐMÐNÐOÐPÐQÐRÐSÐTÐUÐVÐ ÐWÐXÐYÐZÐÐÐŁÐØÐĦÐŦÐÞÐÆÐŒÐ ŁAŁBŁCŁDŁEŁFŁGŁHŁIŁJŁKŁ ŁLŁMŁNŁOŁPŁQŁRŁSŁTŁUŁVŁ ŁWŁXŁYŁZŁÐŁŁŁØŁĦŁŦŁÞŁÆŁŒŁ ØAØBØCØDØEØFØGØHØIØJØKØ ØLØMØNØOØPØQØRØSØTØUØVØ ØWØXØYØZØÐØŁØØØĦØŦØÞØÆØŒØ ĦAĦBĦCĦDĦEĦFĦGĦHĦIĦJĦKĦ ĦLĦMĦNĦOĦPĦQĦRĦSĦTĦUĦVĦ ĦWĦXĦYĦZĦÐĦŁĦØĦĦĦŦĦÞĦÆĦŒĦ ŦAŦBŦCŦDŦEŦFŦGŦHŦIŦJŦKŦ ŦLŦMŦNŦOŦPŦQŦRŦSŦTŦUŦVŦ ŦWŦXŦYŦZŦÐŦŁŦØŦĦŦŦŦÞŦÆŦŒŦ ÞAÞBÞCÞDÞEÞFÞGÞHÞIÞJÞKÞ ÞLÞMÞNÞOÞPÞQÞRÞSÞTÞUÞVÞ ÞWÞXÞYÞZÞÐÞŁÞØÞĦÞŦÞÞÞÆÞŒÞ ÆAÆBÆCÆDÆEÆFÆGÆHÆIÆJÆKÆ ÆLÆMÆNÆOÆPÆQÆRÆSÆTÆUÆVÆ ÆWÆXÆYÆZÆÐÆŁÆØÆĦÆŦÆÞÆÆÆŒÆ ŒAŒBŒCŒDŒEŒFŒGŒHŒIŒJŒKŒ ŒLŒMŒNŒOŒPŒQŒRŒSŒTŒUŒVŒ ŒWŒXŒYŒZŒÐŒŁŒØŒĦŒŦŒÞŒÆŒŒŒ",
        "lnum,pnum"      : "0001020 0304050 060708090 1011121 1314151 161718191 2021222 2324252 262728292 3031323 3334353 363738393 4041424 4344454 464748494 5051525 5354555 565758595 6061626 6364656 666768696 7071727 7374757 767778797 8081828 8384858 868788898 9091929 9394959 969798999",
        "onum,pnum"      : "0001020 0304050 060708090 1011121 1314151 161718191 2021222 2324252 262728292 3031323 3334353 363738393 4041424 4344454 464748494 5051525 5354555 565758595 6061626 6364656 666768696 7071727 7374757 767778797 8081828 8384858 868788898 9091929 9394959 969798999",
        "lnum,tnum"      : "0001020 0304050 060708090 1011121 1314151 161718191 2021222 2324252 262728292 3031323 3334353 363738393 4041424 4344454 464748494 5051525 5354555 565758595 6061626 6364656 666768696 7071727 7374757 767778797 8081828 8384858 868788898 9091929 9394959 969798999",
        "onum,tnum"      : "0001020 0304050 060708090 1011121 1314151 161718191 2021222 2324252 262728292 3031323 3334353 363738393 4041424 4344454 464748494 5051525 5354555 565758595 6061626 6364656 666768696 7071727 7374757 767778797 8081828 8384858 868788898 9091929 9394959 969798999",
        "numr"           : "0001020 0304050 060708090 1011121 1314151 161718191 2021222 2324252 262728292 3031323 3334353 363738393 4041424 4344454 464748494 5051525 5354555 565758595 6061626 6364656 666768696 7071727 7374757 767778797 8081828 8384858 868788898 9091929 9394959 969798999",
        "frac"           : "000 0/0 101 1/1 202 2/2 303 3/3 404 4/4 505 5/5 606 6/6 707 7/7 808 8/8 909 9/9",
        "lower punx"     : "‘a’ ‘b’ ‘c’ ‘d’ ‘e’ ‘f’ ‘g’ ‘h’ ‘i’ ‘j’ ‘k’ ‘l’ ‘m’ ‘n’ ‘o’ ‘p’ ‘q’ ‘r’ ‘s’ ‘t’ ‘u’ ‘v’ ‘w’ ‘x’ ‘y’ ‘z’ ‘ð’ ‘đ’ ‘ł’ ‘ø’ ‘ħ’ ‘ŧ’ ‘þ’ ‘æ’ ‘œ’ ‘ß’ ‘ı’ ’a‘ ’b‘ ’c‘ ’d‘ ’e‘ ’f‘ ’g‘ ’h‘ ’i‘ ’j‘ ’k‘ ’l‘ ’m‘ ’n‘ ’o‘ ’p‘ ’q‘ ’r‘ ’s‘ ’t‘ ’u‘ ’v‘ ’w‘ ’x‘ ’y‘ ’z‘ ’ð‘ ’đ‘ ’ł‘ ’ø‘ ’ħ‘ ’ŧ‘ ’þ‘ ’æ‘ ’œ‘ ’ß‘ ’ı‘ ”a”b”c”d”e”f”g”h”i”j”k”l”m”n”o”p”q”r” ”s”t”u”v”w”x”y”z”ð”đ”ł”ø”ħ”ŧ”þ”æ”œ”ß”ı” “a“b“c“d“e“f“g“h“i“j“k“l“m“n“o“p“q“r“ “s“t“u“v“w“x“y“z“ð“đ“ł“ø“ħ“ŧ“þ“æ“œ“ß“ı“ .a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r. .s.t.u.v.w.x.y.z.ð.đ.ł.ø.ħ.ŧ.þ.æ.œ.ß.ı. ,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r, ,s,t,u,v,w,x,y,z,ð,đ,ł,ø,ħ,ŧ,þ,æ,œ,ß,ı, :a:b:c:d:e:f:g:h:i:j:k:l:m:n:o:p:q:r: :s:t:u:v:w:x:y:z:ð:đ:ł:ø:ħ:ŧ:þ:æ:œ:ß:ı: ;a;b;c;d;e;f;g;h;i;j;k;l;m;n;o;p;q;r; ;s;t;u;v;w;x;y;z;ð;đ;ł;ø;ħ;ŧ;þ;æ;œ;ß;ı; ‹a› ‹b› ‹c› ‹d› ‹e› ‹f› ‹g› ‹h› ‹i› ‹j› ‹k› ‹l› ‹m› ‹n› ‹o› ‹p› ‹q› ‹r› ‹s› ‹t› ‹u› ‹v› ‹w› ‹x› ‹y› ‹z› ‹ð› ‹đ› ‹ł› ‹ø› ‹ħ› ‹ŧ› ‹þ› ‹æ› ‹œ› ‹ß› ‹ı› ›a‹ ›b‹ ›c‹ ›d‹ ›e‹ ›f‹ ›g‹ ›h‹ ›i‹ ›j‹ ›k‹ ›l‹ ›m‹ ›n‹ ›o‹ ›p‹ ›q‹ ›r‹ ›s‹ ›t‹ ›u‹ ›v‹ ›w‹ ›x‹ ›y‹ ›z‹ ›ð‹ ›đ‹ ›ł‹ ›ø‹ ›ħ‹ ›ŧ‹ ›þ‹ ›æ‹ ›œ‹ ›ß‹ ›ı‹ «a«b«c«d«e«f«g«h«i«j«k«l«m«n«o«p«q«r« «s«t«u«v«w«x«y«z«ð«đ«ł«ø«ħ«ŧ«þ«æ«œ«ß«ı« »a»b»c»d»e»f»g»h»i»j»k»l»m»n»o»p»q»r» »s»t»u»v»w»x»y»z»ð»đ»ł»ø»ħ»ŧ»þ»æ»œ»ß»ı» -a-b-c-d-e-f-g-h-i-j-k-l-m-n-o-p-q-r- -s-t-u-v-w-x-y-z-ð-đ-ł-ø-ħ-ŧ-þ-æ-œ-ß-ı- –a–b–c–d–e–f–g–h–i–j–k–l–m–n–o–p–q–r– –s–t–u–v–w–x–y–z–ð–đ–ł–ø–ħ–ŧ–þ–æ–œ–ß–ı– ·a·b·c·d·e·f·g·h·i·j·k·l·m·n·o·p·q·r· ·s·t·u·v·w·x·y·z·ð·đ·ł·ø·ħ·ŧ·þ·æ·œ·ß·ı· •a•b•c•d•e•f•g•h•i•j•k•l•m•n•o•p•q•r• •s•t•u•v•w•x•y•z•ð•đ•ł•ø•ħ•ŧ•þ•æ•œ•ß•ı• +a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+ +s+t+u+v+w+x+y+z+ð+đ+ł+ø+ħ+ŧ+þ+æ+œ+ß+ı+ (a) (b) (c) (d) (e) (f) (g) (h)(i)(j)(k)(l)(m)(n)(o)(p)(q)(r)(s)(t)(u)(v)(w)(x)(y)(z)(ð)(đ)(ł)(ø)(ħ)(ŧ)(þ)(æ)(œ)(ß)(ı)[a][b][c][d] [e][f][g][h][i][j][k][l][m][n][o][p][q][r][s][t][u][v][w][x][y][z][ð][đ][ł][ø][ħ][ŧ][þ][æ][œ][ß][ı]{a}{b} {c}{d}{e}{f}{g}{h}{i}{j}{k}{l}{m}{n}{o}{p}{q}{r}{s}{t}{u}{v}{w}{x}{y}{z}{ð}{đ}{ł}{ø}{ħ}{ŧ}{þ}{æ}{œ}{ß} {ı}¡a!¡b!¡c!¡d!¡e!¡f!¡g!¡h!¡i!¡j!¡k!¡l!¡m!¡n!¡o!¡p!¡q!¡r!¡s!¡t!¡u!¡v!¡w!¡x!¡y!¡z!¡ð!¡đ!¡ł!¡ø!¡ħ!¡ŧ!¡þ!¡æ!¡œ!¡ß!¡ı!¿a? ¿b?¿c?¿d?¿e?¿f?¿g?¿h?¿i?¿j?¿k?¿l?¿m?¿n?¿o?¿p?¿q?¿r?¿s?¿t?¿u?¿v?¿w?¿x?¿y?¿z?¿ð?¿đ?¿ł?¿ø?¿ħ?¿ŧ?¿þ?¿æ? ¿œ? ¿ß? ¿ı? &a&b&c&d&e&f&g&h&i&j&k&l&m&n&o&p&q&r& &s&t&u&v&w&x&y&z&ð&đ&ł&ø&ħ&ŧ&þ&æ&œ&ß&ı& *a*b*c*d*e*f*g*h*i*j*k*l*m*n*o*p*q*r* *s*t*u*v*w*x*y*z*ð*đ*ł*ø*ħ*ŧ*þ*æ*œ*ß*ı* a® b® c® d® e® f® g® h® i® j® k® l® m® n® o® p® q® r® s®t®u®v®w®x®y®z®ð®đ®ł®ø®ħ®ŧ®þ®æ®œ®ß®ı®a™b™c™d™e™f™g™h™i™j™k™l™m™n™o™p™q™r™s™t™u™v™ w™x™y™z™ð™đ™ł™ø™ħ™ŧ™þ™æ™œ™ß™ı™a℠b℠c℠d℠e℠f℠g℠h℠i℠j℠k℠l℠m℠n℠o℠p℠q℠r℠s℠t℠u℠v℠ w℠ x℠ y℠ z℠ ð℠ đ℠ ł℠ ø℠ ħ℠ ŧ℠ þ℠ æ℠ œ℠ ß℠ ı℠ †a†b†c†d†e†f†g†h†i†j†k†l†m†n†o†p†q†r† †s†t†u†v†w†x†y†z†ð†đ†ł†ø†ħ†ŧ†þ†æ†œ†ß†ı† ‡a‡b‡c‡d‡e‡f‡g‡h‡i‡j‡k‡l‡m‡n‡o‡p‡q‡r‡ ‡s‡t‡u‡v‡w‡x‡y‡z‡ð‡đ‡ł‡ø‡ħ‡ŧ‡þ‡æ‡œ‡ß‡ı‡ @a@b@c@d@e@f@g@h@i@j@k@l@m@n@o@p@q@r@s@t@u@v@w@x@y@z@ð@đ@ł@ø@ħ@ŧ@þ@æ@œ@ß@ı@ #a#b#c#d#e#f#g#h#i#j#k#l#m#n#o#p#q#r# #s#t#u#v#w#x#y#z#ð#đ#ł#ø#ħ#ŧ#þ#æ#œ#ß#ı# /a/b/c/d/e/f/g/h/i/j/k/l/m/n/ o/p/q/r/ /s/t/u/v/w/x/y/z/ð/đ/ł/ø/ħ/ŧ/þ/æ/œ/ß/ı/",
        "upper punx"     : "‘A’ ‘B’ ‘C’ ‘D’ ‘E’ ‘F’ ‘G’ ‘H’ ‘I’ ‘J’ ‘K’ ‘L’ ‘M’ ‘N’ ‘O’ ‘P’ ‘Q’ ‘R’ ‘S’ ‘T’ ‘U’ ‘V’ ‘W’ ‘X’ ‘Y’ ‘Z’ ‘Ð’ ‘Ł’ ‘Ø’ ‘Ħ’ ‘Ŧ’ ‘Þ’ ‘Æ’ ‘Œ’ ’A‘ ’B‘ ’C‘ ’D‘ ’E‘ ’F‘ ’G‘ ’H‘ ’I‘ ’J‘ ’K‘ ’L‘ ’M‘ ’N‘ ’O‘ ’P‘ ’Q‘ ’R‘ ’S‘ ’T‘ ’U‘ ’V‘ ’W‘ ’X‘ ’Y‘ ’Z‘ ’Ð‘ ’Ł‘ ’Ø‘ ’Ħ‘ ’Ŧ‘ ’Þ‘ ’Æ‘ ’Œ‘ ”A”B”C”D”E”F”G”H”I”J”K”L”M”N”O”P”Q”R” ”S”T”U”V”W”X”Y”Z”Ð”Ł”Ø”Ħ”Ŧ”Þ”Æ”Œ” “A“B“C“D“E“F“G“H“I“J“K“L“M“N“O“P“Q“R“ “S“T“U“V“W“X“Y“Z“Ð“Ł“Ø“Ħ“Ŧ“Þ“Æ“Œ“ .A.B.C.D.E.F.G.H.I.J.K.L.M. N.O.P.Q.R. .S.T.U.V.W.X.Y.Z.Ð.Ł.Ø.Ħ.Ŧ.Þ.Æ.Œ. ,A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R, ,S,T,U,V,W,X,Y,Z,Ð,Ł,Ø,Ħ,Ŧ,Þ,Æ,Œ, :A:B:C:D:E:F:G:H:I:J:K:L:M:N:O:P:Q:R: :S:T:U:V:W:X:Y:Z:Ð:Ł:Ø:Ħ:Ŧ:Þ:Æ:Œ: ;A;B;C;D;E;F;G;H;I;J;K;L;M;N;O;P;Q;R; ;S;T;U;V;W;X;Y;Z;Ð;Ł;Ø;Ħ;Ŧ;Þ;Æ;Œ; ‹A› ‹B› ‹C› ‹D› ‹E› ‹F› ‹G› ‹H› ‹I› ‹J› ‹K› ‹L› ‹M› ‹N› ‹O› ‹P› ‹Q› ‹R› ‹S› ‹T› ‹U› ‹V› ‹W› ‹X› ‹Y› ‹Z› ‹Ð› ‹Ł› ‹Ø› ‹Ħ› ‹Ŧ› ‹Þ› ‹Æ› ‹Œ› ›A‹ ›B‹ ›C‹ ›D‹ ›E‹ ›F‹ ›G‹ ›H‹ ›I‹ ›J‹ ›K‹ ›L‹ ›M‹ ›N‹ ›O‹ ›P‹ ›Q‹ ›R‹ ›S‹ ›T‹ ›U‹ ›V‹ ›W‹ ›X‹ ›Y‹ ›Z‹ ›Ð‹ ›Ł‹ ›Ø‹ ›Ħ‹ ›Ŧ‹ ›Þ‹ ›Æ‹ ›Œ‹ «A«B«C«D«E«F«G«H«I«J«K«L«M«N«O«P«Q«R« «S«T«U«V«W«X«Y«Z«Ð«Ł«Ø«Ħ«Ŧ«Þ«Æ«Œ« »A»B»C»D»E»F»G»H»I»J»K»L»M»N»O»P»Q»R» »S»T»U»V»W»X»Y»Z»Ð»Ł»Ø»Ħ»Ŧ»Þ»Æ»Œ» -A-B-C- D-E-F-G-H-I-J-K-L-M-N-O-P-Q-R- -S-T-U-V-W-X-Y-Z-Ð-Ł-Ø-Ħ-Ŧ-Þ-Æ-Œ- –A–B–C–D–E–F–G–H–I–J–K–L–M–N–O–P–Q–R– –S–T–U–V–W–X–Y–Z–Ð–Ł–Ø–Ħ–Ŧ–Þ–Æ–Œ– ·A·B·C·D·E·F·G·H·I·J·K·L·M·N·O·P·Q·R· ·S·T·U·V·W·X·Y·Z·Ð·Ł·Ø·Ħ·Ŧ·Þ·Æ·Œ· •A•B•C•D•E•F•G•H•I•J•K•L•M•N•O•P•Q•R• •S•T•U•V•W•X•Y•Z•Ð•Ł•Ø•Ħ•Ŧ•Þ•Æ•Œ• +A+B+C+D+E+F+G+H+I+J+K+L+M+N+O+P+Q+R+ +S+T+U+V+W+X+Y+Z+Ð+Ł+Ø+Ħ+Ŧ+Þ+Æ+Œ+ (A) (B) (C) (D) (E) (F) (G) (H) (I) (J) (K) (L) (M) (N) (O) (P) (Q) (R) (S) (T) (U) (V) (W) (X) (Y) (Z) (Ð) (Ł) (Ø) (Ħ) (Ŧ) (Þ) (Æ) (Œ) [A] [B] [C] [D] [E] [F] [G] [H] [I] [J] [K] [L] [M] [N] [O] [P] [Q] [R] [S] [T] [U] [V] [W] [X] [Y] [Z] [Ð] [Ł] [Ø] [Ħ] [Ŧ] [Þ] [Æ] [Œ] {A} {B} {C} {D} {E} {F} {G} {H} {I} {J} {K} {L} {M} {N} {O} {P} {Q} {R} {S} {T} {U} {V} {W} {X} {Y} {Z} {Ð} {Ł} {Ø} {Ħ} {Ŧ} {Þ} {Æ} {Œ}¡A!¡B!¡C!¡D!¡E!¡F!¡G!¡H!¡I!¡J!¡K!¡L!¡M!¡N!¡O!¡P!¡Q!¡R!¡S!¡T!¡U!¡V!¡W!¡X!¡Y!¡Z!¡Ð!¡Ł!¡Ø!¡Ħ!¡Ŧ!¡Þ!¡Æ!¡Œ!¿A? ¿B? ¿C? ¿D? ¿E? ¿F? ¿G? ¿H? ¿I? ¿J? ¿K? ¿L? ¿M? ¿N? ¿O? ¿P? ¿Q? ¿R? ¿S? ¿T? ¿U? ¿V? ¿W? ¿X? ¿Y? ¿Z? ¿Ð? ¿Ł? ¿Ø? ¿Ħ? ¿Ŧ? ¿Þ? ¿Æ? ¿Œ? &A&B&C&D&E&F&G&H&I&J&K&L&M&N&O&P&Q&R& &S&T&U&V&W&X&Y&Z&Ð&Ł&Ø&Ħ&Ŧ&Þ&Æ&Œ& *A*B*C*D*E*F*G*H*I*J*K*L*M*N*O*P*Q*R* *S*T*U*V*W*X*Y*Z*Ð*Ł*Ø*Ħ*Ŧ*Þ*Æ*Œ* A® B® C® D® E® F® G® H® I® J® K® L® M® N®O®P®Q®R®S®T®U®V®W®X®Y®Z®Ð®Ł®Ø®Ħ®Ŧ®Þ®Æ®Œ®A™B™C™D™E™F™G™H™I™J™K™L™M™N™O™ P™Q™R™S™T™U™V™W™X™Y™Z™Ð™Ł™Ø™Ħ™Ŧ™Þ™Æ™Œ™A℠B℠C℠D℠E℠F℠G℠H℠I℠J℠K℠L℠M℠ N℠ O℠ P℠ Q℠ R℠ S℠ T℠ U℠ V℠ W℠ X℠ Y℠ Z℠ Ð℠ Ł℠ Ø℠ Ħ℠ Ŧ℠ Þ℠ Æ℠ Œ℠ †A†B†C†D†E†F†G†H†I†J†K†L†M†N†O†P†Q†R† †S†T†U†V†W†X†Y†Z†Ð†Ł†Ø†Ħ†Ŧ†Þ†Æ†Œ† ‡A‡B‡C‡D‡E‡F‡G‡H‡I‡J‡K‡L‡M‡N‡O‡P‡Q‡R‡ ‡S‡T‡U‡V‡W‡X‡Y‡Z‡Ð‡Ł‡Ø‡Ħ‡Ŧ‡Þ‡Æ‡Œ‡ @A@B@C@D@E@F@G@H@I@ @J@K@L@M@N@O@P@Q@ @R@S@T@U@V@W@X@Y@Z@ @Ð@Ł@Ø@Ħ@Ŧ@Þ@Æ@Œ@ #A#B#C#D#E#F#G#H#I# #J#K#L#M#N#O#P#Q# #R#S#T#U#V#W#X#Y#Z# #Ð#Ł#Ø#Ħ#Ŧ#Þ#Æ#Œ# /A/B/C/D/E/F/G/H/I/J/K/L/M/N/O/P/Q/R/ /S/T/U/V/W/X/Y/Z/Ð/Ł/Ø/Ħ/Ŧ/Þ/Æ/Œ/ ‘0’ ‘1’ ‘2’ ‘3’ ‘4’ ‘5’ ‘6’ ‘7’ ‘8’ ‘9’ ’0‘ ’1‘ ’2‘ ’3‘ ’4‘ ’5‘ ’6‘ ’7‘ ’8‘ ’9‘ ”0”1”2”3”4”5”6”7”8”9” “0“1“2“3“4“5“6“7“8“9“ .0.1.2.3.4.5.6.7.8.9. ,0,1,2,3,4,5,6,7,8,9, :0:1:2:3:4:5:6:7:8:9: ;0;1;2;3;4;5;6;7;8;9; ‹0› ‹1› ‹2› ‹3› ‹4› ‹5› ‹6› ‹7› ‹8› ‹9› ›0‹ ›1‹ ›2‹ ›3‹ ›4‹ ›5‹ ›6‹ ›7‹ ›8‹ ›9‹ «0«1«2«3«4«5«6«7«8«9« »0»1»2»3»4»5»6»7»8»9» -0-1-2-3-4-5-6-7-8-9- –0–1–2–3–4–5–6–7–8–9– ·0·1·2·3·4·5·6·7·8·9· •0•1•2•3•4•5•6•7•8•9• +0+1+2+3+4+5+6+7+8+9+ −0−1−2−3−4−5−6−7−8−9− ×0×1×2×3×4×5×6×7×8×9× ÷0÷1÷2÷3÷4÷5÷6÷7÷8÷9÷ <0<1<2<3<4<5<6<7<8<9< >0>1>2>3>4>5>6>7>8>9> =0=1=2=3=4=5=6=7=8=9= ~0~1~2~3~4~5~6~7~8~9~ (0) (1) (2) (3) (4) (5)(6)(7)(8)(9)[0][1][2][3][4][5][6][7][8][9]{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}¡0!¡1!¡2!¡3!¡4!¡5!¡6!¡7!¡8!¡9!¿0? ¿1? ¿2? ¿3? ¿4? ¿5? ¿6? ¿7? ¿8? ¿9? &0&1&2&3&4&5&6&7&8&9& *0*1*2*3*4*5*6*7*8*9* 0® 1® 2® 3® 4® 5® 6® 7® 8® 9® 0™ 1™ 2™ 3™ 4™ 5™ 6™ 7™ 8™ 9™ 0℠ 1℠ 2℠ 3℠ 4℠ 5℠ 6℠ 7℠ 8℠ 9℠ †0†1†2†3†4†5†6†7†8†9† ‡0‡1‡2‡3‡4‡5‡6‡7‡8‡9‡ $0$1$2$3$4$5$6$7$8$9$ ¢0¢1¢2¢3¢4¢5¢6¢7¢8¢9¢ £0£1£2£3£4£5£6£7£8£9£ ¥0¥1¥2¥3¥4¥5¥6¥7¥8¥9¥ ƒ0ƒ1ƒ2ƒ3ƒ4ƒ5ƒ6ƒ7ƒ8ƒ9ƒ €0€1€2€3€4€5€6€7€8€9€ ₹0₹1₹2₹3₹4₹5₹6₹7₹8₹9₹ ₺0₺1₺2₺3₺4₺5₺6₺7₺8₺9₺ ₽0₽1₽2₽3₽4₽5₽6₽7₽8₽9₽ ₿0₿1₿2₿3₿4₿5₿6₿7₿8₿9₿ №0№1№2№3№4№5№6№7№8№9№ ©0©1©2©3©4©5©6©7©8©9© §0§1§2§3§4§5§6§7§8§9§ ¶0¶1¶2¶3¶4¶5¶6¶7¶8¶9¶ %0%1%2%3%4%5%6%7%8%9% a0a1a2a3a4a5a6a7a8a9a o0o1o2o3o4o5o6o7o8o9o @0@1@2@3@4@5@6@7@8@9@ #0#1#2#3#4#5#6#7#8#9# /0/1/2/3/4/5/6/7/8/9/ ‘0’ ‘1’ ‘2’ ‘3’ ‘4’ ‘5’ ‘6’ ‘7’ ‘8’ ‘9’ ’0‘ ’1‘ ’2‘ ’3‘ ’4‘ ’5‘ ’6‘ ’7‘ ’8‘ ’9‘ ”0”1”2”3”4”5”6”7”8”9” “0“1“2“3“4“5“6“7“8“9“ .0.1.2.3.4.5.6.7.8.9. ,0,1,2,3,4,5,6,7,8,9, :0:1:2:3:4:5:6:7:8:9: ;0;1;2;3;4;5;6;7;8;9; ‹0› ‹1› ‹2› ‹3› ‹4› ‹5› ‹6› ‹7› ‹8› ‹9› ›0‹ ›1‹ ›2‹ ›3‹ ›4‹ ›5‹ ›6‹ ›7‹ ›8‹ ›9‹ «0«1«2«3«4«5«6«7«8«9« »0»1»2»3»4»5»6»7»8»9» -0-1-2-3-4-5-6-7-8-9- –0–1–2–3–4–5–6–7–8–9– ·0·1·2·3·4·5·6·7·8·9· •0•1•2•3•4•5•6•7•8•9• +0+1+2+3+4+5+6+7+8+9+ −0−1−2−3−4−5−6−7−8−9− ×0×1×2×3×4×5×6×7×8×9× ÷0÷1÷2÷3÷4÷5÷6÷7÷8÷9÷ <0<1<2<3<4<5<6<7<8<9< >0>1>2>3>4>5>6>7>8>9> =0=1=2=3=4=5=6=7=8=9= ~0~1~2~3~4~5~6~7~8~9~ (0) (1) (2) (3) (4) (5) (6) (7) (8) (9) [0] [1] [2] [3] [4] [5] [6] [7] [8] [9] {0} {1} {2} {3} {4} {5} {6} {7} {8} {9} ¡0! ¡1! ¡2! ¡3! ¡4! ¡5! ¡6! ¡7! ¡8! ¡9! ¿0? ¿1? ¿2? ¿3? ¿4? ¿5? ¿6? ¿7? ¿8? ¿9? &0&1&2&3&4&5&6&7&8&9& *0*1*2*3*4*5*6*7*8*9* 0®1®2®3®4®5®6®7®8®9®0™1™2™3™4™5™6™7™8™9™0℠1℠2℠3℠4℠5℠6℠7℠8℠9℠†0†1†2†3†4†5†6†7†8†9† ‡0‡1‡2‡3‡4‡5‡6‡7‡8‡9‡ $0$1$2$3$4$5$6$7$8$9$ ¢0¢1¢2¢3¢4¢5¢6¢7¢8¢9¢ £0£1£2£3£4£5£6£7£8£9£ ¥0¥1¥2¥3¥4¥5¥6¥7¥8¥9¥ ƒ0ƒ1ƒ2ƒ3ƒ4ƒ5ƒ6ƒ7ƒ8ƒ9ƒ €0€1€2€3€4€5€6€7€8€9€ ₹0₹1₹2₹3₹4₹5₹6₹7₹8₹9₹ ₺0₺1₺2₺3₺4₺5₺6₺7₺8₺9₺ ₽0₽1₽2₽3₽4₽5₽6₽7₽8₽9₽ ₿0₿1₿2₿3₿4₿5₿6₿7₿8₿9₿ №0№1№2№3№4№5№6№7№8№9№ ©0©1©2©3©4©5©6©7©8©9© §0§1§2§3§4§5§6§7§8§9§ ¶0¶1¶2¶3¶4¶5¶6¶7¶8¶9¶ %0%1%2%3%4%5%6%7%8%9% a0a1a2a3a4a5a6a7a8a9a o0o1o2o3o4o5o6o7o8o9o @0@1@2@3@4@5@6@7@8@9@ #0#1#2#3#4#5#6#7#8#9# /0/1/2/3/4/5/6/7/8/9/",
        "case punx"      : "‹A› ‹B› ‹C› ‹D› ‹E› ‹F› ‹G› ‹H› ‹I› ‹J› ‹K› ‹L› ‹M› ‹N› ‹O› ‹P› ‹Q› ‹R› ‹S› ‹T› ‹U› ‹V› ‹W› ‹X› ‹Y› ‹Z› ‹Ð› ‹Ł› ‹Ø›‹Ħ›‹Ŧ›‹Þ›‹Æ›‹Œ››A‹›B‹›C‹›D‹›E‹›F‹›G‹›H‹›I‹›J‹›K‹›L‹›M‹›N‹›O‹›P‹›Q‹›R‹›S‹›T‹›U‹›V‹›W‹›X‹›Y‹›Z‹›Ð‹›Ł‹ ›Ø‹ ›Ħ‹ ›Ŧ‹ ›Þ‹ ›Æ‹ ›Œ‹ «A«B«C«D«E«F«G«H«I«J«K«L«M«N«O«P«Q«R« «S«T«U«V«W«X«Y«Z«Ð«Ł«Ø«Ħ«Ŧ«Þ«Æ«Œ« »A»B»C»D»E»F»G»H»I»J»K»L»M»N»O»P»Q»R» »S»T»U»V»W»X»Y»Z»Ð»Ł»Ø»Ħ»Ŧ»Þ»Æ»Œ» -A-B-C-D-E-F-G-H-I-J-K-L-M- N-O-P-Q-R- -S-T-U-V-W-X-Y-Z-Ð-Ł-Ø-Ħ-Ŧ-Þ-Æ-Œ- –A–B–C–D–E–F–G–H–I–J–K–L–M–N–O–P–Q–R– –S–T–U–V–W–X–Y–Z– Ð–Ł–Ø–Ħ–Ŧ–Þ–Æ–Œ– (A) (B) (C) (D) (E) (F) (G) (H) (I) (J) (K) (L) (M) (N) (O) (P) (Q) (R) (S) (T) (U) (V) (W) (X) (Y) (Z) (Ð) (Ł)(Ø)(Ħ)(Ŧ)(Þ)(Æ)(Œ)[A][B][C][D][E][F][G][H][I][J][K][L][M][N][O][P][Q][R][S][T][U][V][W][X][Y][Z][Ð] [Ł][Ø][Ħ][Ŧ][Þ][Æ][Œ]{A}{B}{C}{D}{E}{F}{G}{H}{I}{J}{K}{L}{M}{N}{O}{P}{Q}{R}{S}{T}{U}{V}{W}{X}{Y}{Z} {Ð}{Ł}{Ø}{Ħ}{Ŧ}{Þ}{Æ}{Œ}¡A!¡B!¡C!¡D!¡E!¡F!¡G!¡H!¡I!¡J!¡K!¡L!¡M!¡N!¡O!¡P!¡Q!¡R!¡S!¡T!¡U!¡V!¡W!¡X!¡Y!¡Z!¡Ð! ¡Ł! ¡Ø! ¡Ħ! ¡Ŧ! ¡Þ! ¡Æ! ¡Œ! ¿A? ¿B? ¿C? ¿D? ¿E? ¿F? ¿G? ¿H? ¿I? ¿J? ¿K? ¿L? ¿M? ¿N? ¿O? ¿P? ¿Q? ¿R? ¿S? ¿T? ¿U? ¿V? ¿W? ¿X? ¿Y? ¿Z? ¿Ð? ¿Ł? ¿Ø? ¿Ħ? ¿Ŧ? ¿Þ? ¿Æ? ¿Œ? ‹0› ‹1› ‹2› ‹3› ‹4› ‹5› ‹6› ‹7› ‹8› ‹9› ›0‹ ›1‹ ›2‹ ›3‹ ›4‹ ›5‹ ›6‹ ›7‹ ›8‹ ›9‹ «0«1«2«3«4«5«6«7«8«9« »0»1»2»3»4»5»6»7»8»9» -0-1-2-3-4-5-6-7-8-9- –0–1–2–3–4–5–6–7–8–9–(0) (1) (2) (3) (4) (5) (6) (7) (8) (9) [0] [1] [2] [3] [4] [5] [6][7][8][9]{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}¡0!¡1!¡2!¡3!¡4!¡5!¡6!¡7!¡8!¡9!¿0?¿1?¿2?¿3?¿4?¿5?¿6?¿7?¿8?¿9?",
        "diacritics"     : "ďďaďbďcďdďeďfď ďgďhďiďjďkďlďmď ďnďoďpďqďrďsď ďtďuďvďwďxďyďzďžďáď ľľaľbľcľdľeľfľ ľgľhľiľjľkľlľmľ ľnľoľpľqľrľsľ ľtľuľvľwľxľyľzľčľňľšľžľúľ ťťaťbťcťdťeťfť ťgťhťiťjťkťlťmť ťnťoťpťqťrťsť ťtťuťvťwťxťyťzťčťšťůťáť ĽĽaĽbĽcĽdĽeĽfĽ ĽgĽhĽiĽjĽkĽlĽmĽ ĽnĽoĽpĽqĽrĽsĽ ĽtĽuĽvĽwĽxĽyĽzĽ ĽĽAĽBĽCĽDĽEĽFĽ ĽGĽHĽIĽJĽKĽLĽMĽ ĽNĽOĽPĽQĽRĽSĽ ĽTĽUĽVĽWĽXĽYĽZĽ AíAĭAîAïAìAīA AĩAĵAóAŏAôAöA AòAőAōAõAŕAřA BíBĭBîBïBìBīB BĩBĵBóBŏBôBöB BòBőBōBõBŕBřB CíCĭCîCïCìCīC CĩCĵCóCŏCôCöC CòCőCōCõCŕCřC DíDĭDîDïDìDīD DĩDĵDóDŏDôDöD DòDőDōDõDŕDřD EíEĭEîEïEìEīE EĩEĵEóEŏEôEöE EòEőEōEõEŕEřE FíFĭFîFïFìFīF FĩFĵFóFŏFôFöF FòFőFōFõFŕFřF GíGĭGîGïGìGīG GĩGĵGóGŏGôGöG GòGőGōGõGŕGřG HíHĭHîHïHìHīH HĩHĵHóHŏHôHöH HòHőHōHõHŕHřH JíJĭJîJïJìJīJ JĩJĵJóJŏJôJöJ JòJőJōJõJŕJřJ KíKĭKîKïKìKīK KĩKĵKóKŏKôKöK KòKőKōKõKŕKřK NíNĭNîNïNìNīN NĩNĵNóNŏNôNöN NòNőNōNõNŕNřN OíOĭOîOïOìOīO OĩOĵOóOŏOôOöO OòOőOōOõOŕOřO PíPĭPîPïPìPīP PĩPĵPóPŏPôPöP PòPőPōPõPŕPřP QíQĭQîQïQìQīQ QĩQĵQóQŏQôQöQ QòQőQōQõQŕQřQ RíRĭRîRïRìRīR RĩRĵRóRŏRôRöR RòRőRōRõRŕRřR SíSĭSîSïSìSīS SĩSĵSóSŏSôSöS SòSőSōSõSŕSřS TíTĭTîTïTìTīT TĩTĵTóTŏTôTöT TòTőTōTõTŕTřT UíUĭUîUïUìUīU UĩUĵUóUŏUôUöU UòUőUōUõUŕUřU VíVĭVîVïVìVīV VĩVĵVóVŏVôVöV VòVőVōVõVŕVřV WíWĭWîWïWìWīW WĩWĵWóWŏWôWöW WòWőWōWõWŕWřW XíXĭXîXïXìXīX XĩXĵXóXŏXôXöX XòXőXōXõXŕXřX YíYĭYîYïYìYīY YĩYĵYóYŏYôYöY YòYőYōYõYŕYřY ZíZĭZîZïZìZīZ ZĩZĵZóZŏZôZöZ ZòZőZōZõZŕZřZ fífĭfîfïfìfīf fĩfĵfófŏfôföf fòfőfōfõfŕfřf ‘í‘ĭ‘î‘ï‘ì‘ī‘ĩ‘ĵ‘ŕ‘ř‘ ’í’ĭ’î’ï’ì’ī’ĩ’ĵ’ŕ’ř’ 'í'ĭ'î'ï'ì'ī'ĩ'ĵ'ŕ'ř' /í/ĭ/î/ï/ì/ī/ĩ/ĵ/ŕ/ř/ *í*ĭ*î*ï*ì*ī*ĩ*ĵ*ŕ*ř* †í†ĭ†î†ï†ì†ī†ĩ†ĵ†ŕ†ř† ‡í‡ĭ‡î‡ï‡ì‡ī‡ĩ‡ĵ‡ŕ‡ř‡ í™ ĭ™ î™ ï™ ì™ ī™ĩ™ĵ™ŕ™ř™í℠ĭ℠î℠ï℠ì℠ī℠ĩ℠ĵ℠ŕ℠ř℠í®ĭ®î®ï®ì®ī®ĩ®ĵ®ŕ®ř®@í@ĭ@î@ï@ì@ī@ĩ@ĵ@ŕ@ř@(í)(ĭ)(î)(ï)(ì)(ī)(ĩ)(ĵ)(ŕ) (ř) [í] [ĭ] [î] [ï] [ì] [ī] [ĩ] [ĵ] [ŕ] [ř] {í} {ĭ} {î} {ï} {ì} {ī} {ĩ} {ĵ} {ŕ} {ř} í! ĭ! î! ï! ì! ī! ĩ! ĵ! ŕ! ř! í? ĭ? î? ï? ì? ī? ĩ? ĵ? ŕ? ř? yąyęyįyųyțyţyĄyĘyĮy pąpępįpųpțpţpĄpĘpĮp ,ą,ę,į,ų,ț,ţ,Ą,Ę,Į, ;ą;ę;į;ų;ț;ţ;Ą;Ę;Į; /ą/ę/į/ų/ț/ţ/Ą/Ę/Į/ (ą) (ę) (į) (ų) (ț) (ţ) (Ą) (Ę) (Į) [ą] [ę] [į] [ų] [ț] [ţ] [Ą] [Ę] [Į] {ą} {ę} {į} {ų} {ț} {ţ} {Ą} {Ę} {Į} AíAĭAîAïAìAīA AĩAĵ BíBĭBîBïBìBīB BĩBĵ CíCĭCîCïCìCīC CĩCĵ DíDĭDîDïDìDīD DĩDĵ EíEĭEîEïEìEīE EĩEĵ FíFĭFîFïFìFīF FĩFĵ GíGĭGîGïGìGīG GĩGĵ HíHĭHîHïHìHīH HĩHĵ JíJĭJîJïJìJīJ JĩJĵ KíKĭKîKïKìKīK KĩKĵ NíNĭNîNïNìNīN NĩNĵ PíPĭPîPïPìPīP PĩPĵ RíRĭRîRïRìRīR RĩRĵ SíSĭSîSïSìSīS SĩSĵ TíTĭTîTïTìTīT TĩTĵ UíUĭUîUïUìUīU UĩUĵ VíVĭVîVïVìVīV VĩVĵ WíWĭWîWïWìWīW WĩWĵ XíXĭXîXïXìXīX XĩXĵ YíYĭYîYïYìYīY YĩYĵ ZíZĭZîZïZìZīZ ZĩZĵ ‘í‘ĭ‘î‘ï‘ì‘ī‘ĩ‘ĵ‘ ’í’ĭ’î’ï’ì’ī’ĩ’ĵ’ 'í'ĭ'î'ï'ì'ī'ĩ'ĵ' /í/ĭ/î/ï/ì/ī/ĩ/ĵ/ *í*ĭ*î*ï*ì*ī*ĩ*ĵ* †í†ĭ†î†ï†ì†ī†ĩ†ĵ† ‡í‡ĭ‡î‡ï‡ì‡ī‡ĩ‡ĵ‡ í™ ĭ™ î™ ï™ ì™ ī™ ĩ™ ĵ™ í℠ ĭ℠ î℠ ï℠ ì℠ ī℠ ĩ℠ ĵ℠ í® ĭ® î® ï® ì® ī® ĩ® ĵ® @í@ĭ@î@ï@ì@ī@ĩ@ĵ@ (í) (ĭ) (î) (ï) (ì) (ī) (ĩ) (ĵ) [í] [ĭ] [î] [ï] [ì] [ī] [ĩ] [ĵ] {í} {ĭ} {î} {ï} {ì} {ī} {ĩ} {ĵ} í! ĭ! î! ï! ì! ī! ĩ! ĵ! í? ĭ? î? ï? ì? ī? ĩ? ĵ?",
        "puncuation"     : "—¿Hn —¡Hn ‘¿Hn ‘¡Hn nn.” nn,” nn”. nn”, nn.’ nn,’ nn’. nn’,",
    }
}

RUNNING_TEXT_TYPES = [
"spacing",
"figures",
"lowercaseCopy",
"uppercaseCopy",
"paragraph",
"kerning"
]

FONT_SIZE_DEFAULT = 28
FONT_SIZE_SMALL   = 9
FONT_SIZE_MED     = 12
FONT_SIZE_LARGE   = 30

PAGE_SIZES = bot.sizes()
PAGE_SIZE_DEFAULT = "LetterLandscape"


def find_proof_directory(start_location, target):
    # I don't think I wrote this function but I can't remember where I got it...
    start_location = os.path.abspath(start_location)
    closest_directory = save_path = None
    closest_distance = float('inf')  # Initialize to positive infinity
    current_path = start_location
    while current_path != os.path.sep:
        for filename in os.listdir(current_path):
            if target in filename:
                distance = len(os.path.relpath(current_path, start_location).split(os.path.sep))
                if distance < closest_distance:
                    closest_directory = current_path
                    closest_distance = distance
                    save_path = os.path.join(closest_directory, filename)
        current_path = os.path.dirname(current_path)
    return save_path


def width_class(wdth_user_value) -> int:
    '''
    function taken from fontMake's instancistator
    '''
    WDTH_VALUE_TO_OS2_WIDTH_CLASS = { 50:1, 62.5:2, 75:3, 87.5:4, 100:5, 112.5:6, 125:7, 150:8, 200:9}
    width_user_value = min(max(wdth_user_value, 50), 200)
    width_user_value_mapped = varLib.models.piecewiseLinearMap(
        width_user_value, WDTH_VALUE_TO_OS2_WIDTH_CLASS
    )
    return otRound(width_user_value_mapped)

def weight_class(wght_user_value) -> int:
    '''
    function taken from fontMake's instancistator
    '''
    weight_user_value = min(max(wght_user_value, 1), 1000)
    return otRound(weight_user_value)

def italic_value(slnt_user_value) -> Union[int, float]:
    '''
    function taken from fontMake's instancistator
    '''
    slant_user_value = min(max(slnt_user_value, -90), 90)
    return slant_user_value


class proofObjectHandler(List):
    """
    https://stackoverflow.com/questions/6560354/how-would-i-create-a-custom-list-class-in-python
    An extensive user-defined wrapper around list objects.
    """

    def __init__(self, initlist=None):
        super().__init__()
        self.data = []
        if initlist is not None:
            if isinstance(initlist, list):
                self.data[:] = initlist
            elif isinstance(initlist, proofObjectHandler):
                self.data[:] = initlist.data[:]
            else:
                self.data = list(initlist)

    def __repr__(self):
        return f"""<{self.__class__.__name__} @ {hash(tuple(self.data))}>"""

    def __contains__(self, value):
        return value in self.data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        if isinstance(idx, slice):
            return self.__class__(self.data[idx])
        else:
            return self.data[idx]

    def __setitem__(self, idx, value):
        # optional: self._acl_check(val)
        self.data[idx] = value

    def __delitem__(self, idx):
        del self.data[idx]

    def __iter__(self):
        for item in self.data:
            yield item

    def __add__(self, other):
        if isinstance(other, proofObjectHandler):
            return self.__class__(self.data + other.data)
        elif isinstance(other, type(self.data)):
            return self.__class__(self.data + other)
        return self.__class__(self.data + list(other))

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)

        # Create a copy and avoid triggering descriptors
        inst.__dict__["data"] = self.__dict__["data"][:]

        return inst
        
    def find(self, **kwargs):
        # getter that finds items in object that have the given attributes
        # this *must* pass all the kwarg values to be valid item
        found = self.__class__()    
        for item in self.data:
            test = []
            for attr, value in kwargs.items():
                if getattr(item, attr, None) == value:
                    test.append(True)
                else:
                    test.append(False)
            if False not in test: found.append(item)
        return found
        
    def append(self, value):
        self.data.append(value)

    def insert(self, idx, value):
        self.data.insert(idx, value)

    def pop(self, idx=-1):
        return self.data.pop(idx)

    def remove(self, value):
        self.data.remove(value)

    def clear(self):
        self.data.clear()

    def copy(self):
        return self.__class__(self)

    def index(self, idx, *args):
        return self.data.index(idx, *args)

    def reverse(self):
        self.data.reverse()

    def sort(self, /, *args, **kwds):
        # sort a list of instances by locations
        # knows how to sort different subclass types
        test = self.data[0]
        if isinstance(test, proofLocation):
            self.data.sort(key=lambda d: (-width_class(d.location.get("wdth",0)), -italic_value(d.location.get("slnt",0)), weight_class(d.location.get("wght",0))))
        elif isinstance(test, proofFont):
            self.data.sort(key=lambda d: (-f.font_object["OS_2"].usWidthClass, -f.font_object["post"].italicAngle, f.font_object["OS_2"].usWeightClass))
        else:
            self.data.sort(*args, **kwds)

    def extend(self, other, clear=False):
        if clear:
            self.data.clear()
        if isinstance(other, proofObjectHandler):
            self.data.extend(other.data)
        else:
            self.data.extend(other)

class proofLocation:

    def __repr__(self):
        name = ""
        if self.is_source:
            name = "source"
        if self.is_instance:
            name = "instance"
        if self.is_source and self.is_instance:
            name = "both"
        return f"<proofLocation.{name} @ {self.name}>"

    def __init__(self, location):

        self.type = None
        self.is_instance = False
        self.is_source = False
        self.tag_location = None
        self.data_from = "TTFont" # DesignSpaceDocument or TTFont

        self._in_crop = True
        self._font = None
        self._name = "unnamed location"
        self._location = location


    def _get_in_crop(self):
        return self._in_crop

    def _set_in_crop(self, new_in_crop):
        self._in_crop = new_in_crop

    in_crop = property(_get_in_crop, _set_in_crop)

    def _get_origin(self):
        return self._origin

    def _set_origin(self, new_origin):
        self._origin = new_origin

    origin = property(_get_origin, _set_origin)

    def _get_name(self):
        return self._name

    def _set_name(self, new_name):
        self._name = new_name

    name = property(_get_name, _set_name)

    def _get_location(self):
        return self._location

    def _set_location(self, new_location):
        self._location = new_location

    location = property(_get_location, _set_location)


    def generate_name(self, TTFont):
        f = TTFont
        best_name = f["name"].getBestFullName()
        if "fvar" in f:
            for i in f["fvar"].instances: 
                l = self._location
                # print(l)
                #l = {a:v for a,v in self._location.items() if a in [a.axisTag for a in f["fvar"].axes]}
                if i.coordinates == l:   
                    for name in f["name"].names:
                        if name.nameID == i.subfamilyNameID:
                            best_name = f'{f["name"].getBestFamilyName()} {name}'
        return best_name



class proofFont:

    def __repr__(self):
        return f"<proofFont @ {self.name}>"

    def __init__(self, path):

        self.path               = path
        self.font_object        = None
        self.load_font()
        self.is_variable        = False
        self.locations          = proofObjectHandler([])
        self.operator           = None
        self._name              = self._compile_name()
        self.features           = {}

    def load_font(self):
        if self.path:
            self.font_object = TTFont(self.path)

    # get font objects best possible name
    def _compile_name(self):
        f = self.font_object
        try:
            best_name = f["name"].getBestFullName()
        except TypeError:
            best_name = ""

        return best_name

    def _get_name(self):
        return self._name

    def _set_name(self, new_name=None):
        self._name = new_name

    name = property(_get_name, _set_name)

    # def _sort_locations(self):
    #     return sorted(self.loc, key=lambda d: (-width_class(d.location.get("wdth",0)), -italic_value(d.location.get("slnt",0)), weight_class(d.location.get("wght",0))))

    def _reformat_locations(self,designspace,instance,axis_map,renamer):
        parsed = {}
        instance = designspace.map_backward(instance.location)
        for axis,val in instance.items():
            a = renamer.get(axis)
            parsed[a]=val
        return parsed


    def get_OT(self):

        font = self.font_object
        _gsub = font["GSUB"]
        i = []

        for r in _gsub.table.FeatureList.FeatureRecord:
            name = ""
            fp = r.Feature.FeatureParams
            if fp:
                name = font["name"].getName(fp.UINameID,1,0,0)
                if not name:
                    name = font["name"].getName(fp.UINameID,3,1,0x409)
            if r.Feature.LookupListIndex:
                i.append((r.FeatureTag, name, r.Feature.LookupListIndex[0]))

        i = sorted(list(set(i)), key=lambda x: x[0])
        _features = {}

        if i:
            for _temp in i:
                tag, desc, LookupID = _temp
                Lookup = _gsub.table.LookupList.Lookup[LookupID]
                mapping = None
                for subtable in Lookup.SubTable:
                    if subtable.LookupType == 1:
                        mapping = subtable.mapping
                _features[tag] = ((desc,LookupID,mapping))

        self.features = _features
        return _features


    def build_locations(self):
        font_obj   = self.font_object
        operator = self.operator

        _instances = {}
        renamer = {a.name:a.tag for a in operator.axes}

        if operator:
            for v in splitVariableFonts(operator, expandLocations=True):
                sub_space, split_op = v
                if sub_space == os.path.splitext(os.path.basename(self.path))[0]:
                    self.operator = split_op
                    for item in ["source", "instance"]:
                        i = getattr(split_op, f"{item}s")
                        for ii in i:

                            re = [ir for ir in getattr(operator, f"{item}s") if ir.filename == ii.filename][0]
                            # normalize order and formatting
                            ii.location = {renamer.get(k,k):float(v) for k,v in sorted(operator.map_backward(re.location).items(), key=lambda item: item[0])}

                            temp = _instances.get(str(ii.location))
                            if temp:
                                built = temp
                            else:
                                built = proofLocation(ii.location)
                            built.name = f"{ii.familyName} {ii.styleName}"
                            built.data_from = "DesignSpaceDocument"
                            setattr(built, f"is_{item}", True)
                            built.origin = font_obj
                            _instances[str(built.location)] = built

                
                        #print(built.location, built.is_instance, built.is_source)
        if not _instances:
        # we dont want to rely on the fvar instances because there is no source data to proof
            if "fvar" in font_obj:
                for inst in [instance.coordinates for instance in font_obj["fvar"].instances]:
                    built = proofLocation(inst)
                    n = built.generate_name(font_obj)
                    built.name = n
                    built.data_from = "TTFont"
                    built.is_instance = True
                    built.is_source = False
                    built.origin = font_obj
                    _instances[str(built.location)] = built
            else:
                _instances = {}

        self.locations.extend(list(_instances.values()), clear=True)
        self.locations.sort() # = self._sort_locations(list(_instances.values()))



class proofDocument:

    def __repr__(self):
        return f"<proofDocument @ {self.identifier} : {hash(tuple(self._fonts))}>"

    def __init__(self):

        self.storage = []
        self._now = datetime.datetime.now()
        self._identifier = None
        self._fonts = proofObjectHandler([])
        self._operator = None
        self._crop = ""
        self._use_instances = False
        self._path = None
        self._name = None

        # proof UI settings
        # size can either be a tuple of ints or a DrawBot
        # compatible paper size name string

        self._size = "LetterLandscape"
        self._margin = 50
        self._margin_left   = self._margin
        self._margin_right  = self._margin
        self._margin_top    = self._margin
        self._margin_bottom = self._margin
        self._text_box_size = (
                               (self.size[0] - (self._margin_left + self._margin_right )),
                               (self.size[1] - (self._margin_top  + self._margin_bottom))
                              )

        self._auto_open = False
        self._caption_font = "SFMono-Regular"
        self.hyphenation = True

        self.grid = None
        self.instance_color = (0.58, 0.22, 1, 1)
        self.WORDS = []




    # do we even need ids??-----------------------
    def _get_identifier(self):
        if not self._identifier:
            self._identifier = self.generate_identifier()
        return self._identifier

    def _set_identifier(self, new_id):
        self._identifier = new_id

    identifier = property(_get_identifier, _set_identifier)

    def generate_identifier(self):
        return makeRandomIdentifier(existing=[])
    # ----------------------------------------------

    def _get_page_size(self):
        if isinstance(self._size, str):
            size = PAGE_SIZES[self._size]
        else:
            size = self._size

        return size

    def _set_page_size(self, new_page_size):
        if isinstance(new_page_size, str):
            if new_page_size in list(PAGE_SIZES.keys()):
                self._size = new_page_size
            else:
                self._size = PAGE_SIZE_DEFAULT
                print(f"""ERROR: {new_page_size} is not a valid page size, defaulting to {PAGE_SIZE_DEFAULT}""")
        if isinstance(new_page_size, tuple):
            ll = len(new_page_size)
            if ll == 2:
                self._size = new_page_size
            elif ll == 1:
                self._size = (new_page_size, new_page_size)
            else:
                self._size = PAGE_SIZE_DEFAULT
                print(f"""ERROR: {new_page_size} is not a valid page size, defaulting to {PAGE_SIZES[PAGE_SIZE_DEFAULT]}""")

        if self._margin == "auto":
            self.margin = "auto"

        self._text_box_size = (
                               (self.size[0] - (self._margin_left + self._margin_right )),
                               (self.size[1] - (self._margin_top  + self._margin_bottom))
                              )

        # keep a stored grid for reference
        self.grid = grid.ColumnGrid(
                                    (   
                                        self._margin_left,
                                        self._margin_bottom,
                                        *self._text_box_size
                                    ),
                                    subdivisions=5
                                   )

    size = property(_get_page_size, _set_page_size)

    def _set_caption_font(self, new_font):
        import errno
        if new_font in bot.installedFonts():
            self._caption_font = new_font
        else:
            raise FileNotFoundError(
                        errno.ENOENT,
                        os.strerror(errno.ENOENT),
                        new_font
                        )

    def _get_caption_font(self):
        return self._caption_font

    caption_font = property(_get_caption_font, _set_caption_font)

    def _set_auto_open(self, bool):
        self._auto_open = bool

    def _get_auto_open(self):
        return self._auto_open

    open_automatically = property(_get_auto_open, _set_auto_open) # open pdf immediately after saving to disk

    def _set_path(self, new_path):
        self._path = new_path

    def _get_path(self):
        if not self._path:
            self._path = self.generate_path_base()
        return self._path

    path = property(_get_path, _set_path)

    def _set_name(self, new_name):
        self._name = new_name

    def _get_name(self):
        if not self._name and self._fonts:
            # return family name for top level font
            self._name = self._fonts[0].font_object["name"].getBestFamilyName().replace(" ","")
        return self._name

    name = property(_get_name, _set_name)

    def _set_operator(self, new_operator):
        self._operator = new_operator

    def _get_operator(self):
        return self._operator

    operator = property(_get_operator, _set_operator)

    def _get_margin(self):
        return (
                self._margin_top,
                self._margin_left, 
                self._margin_bottom,
                self._margin_right,
                )

    def _set_margin(self, new_margin):
        # we can accept a tuple of 4 to set individual 
        # or 1 value to apply across the board
        if isinstance(new_margin, tuple):
            if len(new_margin) == 4:
                # counter clockwise from top
                T,L,B,R = new_margin
            else:
                # if length isnt 4 we just use the first value
                T = L = B = R = new_margin[0]
        elif str(new_margin).lower() == "auto":
            # this is a biased margin spacing based on page size
            w,h = self.size
            T = int(h * 0.09)
            L = R = int(w * 0.085)
            B = int(h * 0.12)

        else:
            # if we set the main margin, we also reset all margins and text box size
            T = L = B = R = new_margin
        self._margin        = new_margin
        self._margin_left   = L
        self._margin_right  = R
        self._margin_top    = T
        self._margin_bottom = B
        self._text_box_size = (
                               (self.size[0] - (self._margin_left + self._margin_right )),
                               (self.size[1] - (self._margin_top  + self._margin_bottom))
                              )

    margin = property(_get_margin, _set_margin)

    def _get_use_instances(self):
        return self._use_instances

    def _set_use_instances(self, bool):
        self._use_instances = bool

    use_instances = property(_get_use_instances, _set_use_instances)

    def _get_crop(self):
        return self._crop

    def _set_crop(self, fence=""):
        # self._crop = fence
        self.crop_space(fence, True)

    crop = property(_get_crop, _set_crop)

    def uniquify(self, path):
        # https://stackoverflow.com/a/57896232
        filename, extension = os.path.splitext(path)
        counter = 1
        while os.path.exists(path):
            path = filename + "-" + str(counter) + extension
            counter += 1
        return path

    def generate_path_base(self, suffix=".pdf", overwrite=True):
        cd = os.path.split(self._fonts[0].path)[0]
        directory = find_proof_directory(cd, "proofs") 
        if not directory:
            directory = cd
        type = "-Proof" if suffix == ".pdf" else ""
        path = f'{directory}/{self._now:%Y-%m%d}-{self.name}{type}{suffix}'

        # make sure file names are unique if have overwrite flag on
        path = self.uniquify(path) if not overwrite else path

        return path

    def load(self, proof_data_path):
        with open(proof_data_path, "rb") as proof_settings:
            data = plistlib.load(proof_settings)
            for name, val in data.items():
                if val:
                    attr = setattr(self, name, val)

    def write(self, path=None, overwrite=True):
        to_store = [item[0] for item in inspect.getmembers(self) if not item[0].startswith("_") and not inspect.ismethod(item[1])]
        data = {}
        for item in to_store:
            comp = getattr(self, item)
            data[item] = comp
            if hasattr(comp, "path"):
                data[item] = getattr(self,item).path

        dump_path = path if path else self.generate_path_base(".proof", overwrite)
        with open(dump_path, "wb") as proof_settings:
            plistlib.dump(data, proof_settings)
        # pass

    def save(self, path=None, open="_", overwrite=True):

        _save_path = path if path else self.path
        _auto = open if open != "_" else self.open_automatically

        self.paginate()
        bot.saveImage(_save_path)
        if _auto:
            os.system(f"open -a Preview '{_save_path}'")


    def get_smallest_core_scaler(self, text):
        temp_holder = []
        for font in self._fonts:

            loc = font.locations.find(in_crop=True) if self.use_instances else font.locations.find(is_source=True, in_crop=True)
            for l in loc:
                temp_holder.append(
                                    self.draw_core_characters(
                                        text,
                                        font.path,
                                        l.location,
                                        False
                                        )
                                  )
        return min(temp_holder)

    def _init_page(self,**kwargs):
        bot.newPage(*self.size)
        self.text_attributes()
        self.draw_header_footer(**kwargs)


    def draw_header_footer(self,**kwargs):
        font       = kwargs.get("font", proofFont(""))
        proof_type = kwargs.get("proof_type", "")
        location   = kwargs.get("location", proofLocation({}))
        cover      = kwargs.get("cover", False)


        self.move_to_storage(locals())
        p = Path(proof_type)
        self.text_attributes()

        header_y_pos = self.size[1]-(self._margin_left/2)

        bot.text(f'Project: {self.name}', (self.grid[0], header_y_pos))
        bot.text(f'Date: {self._now:%Y-%m-%d %H:%M}', (self.grid[1], header_y_pos))
        if not cover:
            if location and not location.is_source:
                bot.fill(*self.instance_color)
                o_s = 8
                bot.oval(self.grid[2]-(o_s + (o_s/2)), header_y_pos-(o_s/4), o_s, o_s)

            bot.fill(0)
            bot.text(f'Style: {location.name if location else font.name}', (self.grid[2], header_y_pos))
            bot.text(f'Type: {p.stem}', (self.size[0]-self._margin_right, header_y_pos), align="right")
        fw,fh = bot.textSize(f'Style: {font.name}')
        if proof_type != "core" and location:
            bot.linkRect(f"beginPage_{font}{location.location}", (self._margin_left + (self.size[0]/4)*2, self.size[1]-self._margin_left, fw, fh))

        bot.text(f'© {self._now:%Y}' + ' ' + USER, (self._margin_left, self._margin_bottom/2))
        bot.fill(0)
        bot.stroke(None)


    def new_section(self,
                    proof_type=None,
                    point_size=FONT_SIZE_MED, # can accept list to generate section at different sizes
                    columns=1,
                    sources=True,
                    instances=False,
                    multi_size_page=False,
                    restrict_page=True, # if set to False the overflow will add new pages
                    openType={}, # the only snake case :) a dict for activating specific OT on this page
                    ):

        # accept a list of point sizes or a single point size
        point_sizes = list(mit.always_iterable(point_size))

        if proof_type == "gradient":
            txt = self.get_gradient_strings()
            while txt:
                self._init_page(font=self._fonts[0],proof_type=proof_type)
                txt = self.draw_text_layout(txt)

        elif proof_type == "features":
            for font in self._fonts:

                # get the front most location if it is in the crop
                # otherwise just get the first locaiton in a sorted stack

                front_most = font.locations.find(in_crop=True)
                if not front_most:
                    front_most = font.locations[0]
                else:
                    front_most.sort()
                    front_most = front_most[0]
                self.draw_feature_proofs(font=font, location=front_most)

        else:
            for font in self._fonts:
                to_process = font.locations.find(in_crop=True) if self.use_instances else font.locations.find(is_source=True, in_crop=True)
                for loca in to_process:
                    txt = PROOF_DATA[proof_type]

                    while txt:
                        if proof_type == "core":
                            self._init_page(font=font,proof_type=proof_type,location=loca)
                            min_size = self.get_smallest_core_scaler(txt)
                            txt = self.draw_core_characters(txt,
                                                 font.path,
                                                 loca.location,
                                                 True,
                                                 min_size
                                                )
                        else:
                            if len(point_sizes) > 1 and multi_size_page:
                                self._init_page(font=font,proof_type=proof_type,location=loca)
                                txt = self.draw_text_layout(txt,
                                                            font.path,
                                                            loca.location,
                                                            len(point_sizes),
                                                            restrict_page,
                                                            point_sizes,
                                                            True,
                                                            openType
                                                            )
                            else:
                                for pt in point_sizes:
                                    self._init_page(font=font,proof_type=proof_type,location=loca)
                                    txt = self.draw_text_layout(txt,
                                                                font.path,
                                                                loca.location,
                                                                columns,
                                                                restrict_page,
                                                                pt,
                                                                False,
                                                                openType
                                                                )



    def draw_feature_proofs(self, font=None, location=None):
        font_OT = font.get_OT()

        if self.WORDS == []:
            self.WORDS = get_english_words_set(['web2'], lower=True)

        if font_OT:
            for tag, (desc,LookupID,mapping) in font_OT.items():
                
                string = bot.FormattedString()
                string.fontVariations(**location.location)
                cols = 1
                if desc:
                    string.append(f"{tag} : {desc}\n", font=self.caption_font, fontSize=12)
                else:
                    string.append(f"{tag}\n", font=self.caption_font, fontSize=12)
                string.append("", font=font.path, fontSize=42)
                
                if tag in ["c2sc", "smcp"]:
                    string.append("The Quick Brown Fox Jumps Over The Lazy Dog", font=font.path, fontSize=42, openTypeFeatures={tag:True,})            
                else:

                    """
                    come up with a much faster word finder algo
                    """
                    
                    contains_all = lambda word, letters: all(letter in word for letter in letters)
                    contains = [word for word in self.WORDS if contains_all(word, list(mapping.keys())[:2])]
                    if contains:
                        if tag.startswith("ss"):
                            rd = choice(contains)
                            for gg in rd:
                                if gg in list(mapping.keys())[:2]:
                                    string.fill(0,0,0,.3)
                                else:
                                    string.fill(0,0,0,1)
                                string.append(gg, openTypeFeatures={tag:False})
                
                            string.append("→", fill=(0,0,0,.2), openTypeFeatures={tag:False})
                            string.fill(0)
                            string.append(rd, fill=(0,0,0,1), openTypeFeatures={tag:True})
                            string.append("\n")
                            cols = 1
                    else:
                        for fr,to in mapping.items():
                            string.fill(0,0,0,.3)            
                            string.appendGlyph(fr)
                            string.append("→", fill=(0,0,0,.2))
                            string.fill(0)
                            string.appendGlyph(to)
                            string.append("\n")
                        cols = 3
                    # string = Grid.columnTextBox(string, (10, 10, width()-20, height()-20), subdivisions=3, gutter=15, draw_grid=False)


                self._init_page(font=font,proof_type="features",location=location)
                grid.columnTextBox(string, (self._margin_left, self._margin_bottom, *self._text_box_size), subdivisions=cols, gutter=15, draw_grid=False)


    def draw_core_characters(self, txt, font_path, variable_location={}, will_draw=True, scale=None, openType={"resetFeatures":True}):
        box_w, box_h = self._text_box_size
        box_x, box_y = self._margin_left, self._margin_bottom

        fs = bot.FormattedString()

        fs.font(
                font_path,
                FONT_SIZE_LARGE,
               )

        fs.fontVariations(**variable_location)
        fs.tracking(FONT_SIZE_LARGE*50/1000)
        fs.align("center")
        fs.append(txt)

        txt_w = bot.textSize(fs)[0]
        txt_h = bot.textSize(fs)[1]
        width_ratio = box_w/txt_w 
        height_ratio = box_h/(FONT_SIZE_LARGE * txt.count("\n") * 1.5)

        sf = min([width_ratio , height_ratio]) if not scale else scale

        if will_draw:
            with bot.savedState():
                # fs.fontSize(FONT_SIZE_LARGE*sf)
                bot.scale(sf)
                w,h = self._text_box_size
                grid.columnTextBox(fs, (self._margin_left/sf, self._margin_bottom/sf, w/sf, h/sf), subdivisions=1, gutter=15, draw_grid=False)
                return ""
        else:
            return sf


    def get_gradient_strings(self, level="ascii", font_size=40):
        fonts = self._fonts

        if level == "all":
            chars = sorted(
                    self.find_common_elements(
                            [ff.getGlyphOrder() for ff in fonts]
                        )
                    )
        elif level == "ascii":
            _unis = [65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 32, 46, 44, 58, 59, 33, 63, 42, 35, 47, 92, 45, 95, 40, 41, 123, 125, 91, 93, 34, 39, 64, 38, 124, 36, 43, 61, 62, 60, 94, 37, 96]
            names = [table.cmap.get(cs) for cs in _unis for table in fonts[0].font_object["cmap"].tables]
            chars = []
            for n in names:
                if n not in chars:
                    chars.append(n)
            # chars=" ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz&`.,:;!?/\\|-()[]{}*^~_'\"@$#0123456789%+=<>"
        elif level in [None, "none", "None"]:
            chars = ""
        else:
            _unis = [ord(a) for a in level]
            names = [table.cmap.get(cs) for cs in _unis for table in fonts[0].font_object["cmap"].tables]
            chars = []
            for n in names:
                if n not in chars:
                    chars.append(n)    

        txt = bot.FormattedString()

        for l in chars:
            for font in fonts:
                for loca in font.locations:
                    if loca.location:
                        txt.fontVariations(**loca.location)
                    txt.font(font.path)
                    txt.append("", tracking=(font_size*20/1000), lineHeight=font_size*1.1, fontSize=font_size)
                    txt.appendGlyph(l)
            txt.append("\n")

        # txt = grid.columnTextBox(txt, (self._margin_left, self._margin_bottom, *self._text_box_size), subdivisions=1, gutter=15, draw_grid=False)
        return txt



    def draw_text_layout(self, txt="", font_path="", variable_location={}, columns=1, overflow=True, font_size=FONT_SIZE_MED, multi_size_page=False, openType={"resetFeatures":True}):
        sub_columns = grid.ColumnGrid((self._margin_left, self._margin_bottom, *self._text_box_size), subdivisions=columns)
        bot.fontVariations(**variable_location)
        bot.hyphenation(self.hyphenation)
        bot.openTypeFeatures(**openType)

        if multi_size_page:
            for il, size in enumerate(font_size):
                bot.font(
                    font_path,
                    size
                )
                grid.columnTextBox(txt, (sub_columns[il], sub_columns.bottom, sub_columns*1, self._text_box_size[1]), subdivisions=1, gutter=15, draw_grid=False)
            txt = ""
        else:
            bot.font(
                font_path,
                font_size
                )
            txt = grid.columnTextBox(txt, (self._margin_left, self._margin_bottom, *self._text_box_size), subdivisions=columns, gutter=15, draw_grid=False)
            txt = txt if overflow else ""
        return txt


    def paginate(self):
        allPages = bot.pages()
        totalPages = len(allPages)

        self.text_attributes()
        tw,th = bot.textSize(f'Page {totalPages}/{totalPages}') 

        for pp, page in enumerate(allPages):
            with page:
                self.text_attributes()
                page_string = f'Page {str(pp+1).zfill(len(str(totalPages)))}/{totalPages}'
                bot.text(page_string, ((self.size[0] - self._margin_left)-tw, self._margin_bottom/2))


    def find_close(self, root_dir, target_filename):
        closest_file = None
        closest_mtime = float('inf')

        for foldername, subfolders, filenames in os.walk(root_dir):
            for filename in fnmatch.filter(filenames, target_filename):
                file_path = os.path.join(foldername, filename)
                mtime = os.path.getmtime(file_path)
                
                if mtime < closest_mtime:
                    closest_mtime = mtime
                    closest_file = file_path

        return closest_file


    def get_variable_fonts_from_op(self):
        d = self.operator
        var = d.variableFonts
        di,fi = os.path.split(os.path.abspath(d.path))
        allVFs = []
        if var:
            for vf in var:
                name = vf.name
                file_name = vf.filename
                if file_name:
                    if os.path.isabs(file_name):
                        p = file_name
                    else:
                        if "variable_ttf/" in file_name:
                            pass
                        else:
                            file_name = f"variable_ttf/{file_name}"
                        p = os.path.join(di,file_name)
                        if not os.path.exists(p):
                            continue 
                else:
                    if name:
                        p = self.find_close(di,f"{name}.ttf")

                te = proofFont(p)
                te.is_variable = True
                te.operator = self.operator

                te.build_locations()

                allVFs.append(te)


        return allVFs


    def add_object(self, path=None):
        suffixes = ".ttf .otf .woff .woff2"
        suff = os.path.splitext(path)[-1]
        if suff in suffixes.split(" "):
            o = proofFont(path)        
            self._fonts.append(o)
        elif suff == ".designspace":
            self.operator = dsp_doc.fromfile(path)
            vfs = self.get_variable_fonts_from_op()
            self._fonts.extend(vfs)


    #convience function to add multiple paths at once
    def add_objects(self, paths=[]):
        for path in paths:
            self.add_object(path)


    def reformat_limits(self, limits):
        '''
        use fontTools.varLib model for extracting the CLI data into a dictionary item
        taken from the source code ^
        '''
        result = {}
        if limits:
            for limitString in limits.split(" "):
                match = re.match(r"^(\w{1,4})=(?:(drop)|(?:([^:]+)(?:[:](.+))?))$", limitString)
                if not match:
                    # raise ValueError("invalid location format: %r" % limitString)
                    # sys.exit()
                    return {}
                tag = match.group(1).ljust(4)
                if match.group(2):  # 'drop'
                    lbound = None
                else:
                    lbound = strToFixedToFloat(match.group(3), precisionBits=16)
                ubound = lbound
                if match.group(4):
                    ubound = []
                    for v in match.group(4).split(":"):
                        ubound.append(strToFixedToFloat(v, precisionBits=16))
                if lbound != ubound:
                    result[tag] = tuple((lbound, *ubound))
                else:
                    result[tag] = lbound
            return result
        else:
            return {}


    def crop_space(self, _zone="",inf_loop=False):
        zone = self.reformat_limits(_zone)
        valid = False
        if zone:
            for font in self._fonts:
                cropped = []
                if isinstance(zone, dict):
                    for inst in font.locations:
                        check = []
                        for axis,value in zone.items():
                            a = inst.location.get(axis)
                            if a != None:
                                valid = True
                                if isinstance(value, float):
                                    if a == value:
                                        check.append(1)
                                    else:
                                        check.append(0)
                                if isinstance(value, tuple):
                                    mn,mx = value[0],value[-1]
                                    if a:
                                        if mn <= a <= mx:
                                            check.append(1)
                                        else:
                                            check.append(0)
                            else:
                                valid = False

                        if 0 not in check:
                            inst.in_crop = True
                        else:
                            inst.in_crop = False
        if valid:
            self._crop = _zone


    def move_to_storage(self, locals):
        self.storage.append(locals)

    def setup_proof(self, cover_page=True):
        self.move_to_storage(locals())
        bot.newDrawing()
        if cover_page:
            self._cover_page(self._fonts)

    def text_attributes(self):
        bot.fill(0)
        bot.stroke(None)
        bot.font(self.caption_font, 8)


    def _cover_page(self, fonts):
        # this function is biased and draws a custom cover page of all
        # locations / fonts and scales to fit them all

        self._init_page(font=fonts[0],cover=True)

        _fonts = {}
        for font in fonts:
            if font.is_variable:
                locs = font.locations.find(in_crop=True) if self.use_instances else font.locations.find(is_source=True, in_crop=True)
                if locs:
                    _fonts[font] = locs
            else:
                _fonts[font] = ""


        box_w, box_h = self.size[0]-100, self.size[1]-150
        box_x, box_y = 50, 50

        fs = bot.FormattedString()

        for proof_font,locations in _fonts.items():
            if locations:
                for loc in locations:
                    fs.fontVariations(**loc.location)
                    fs.fontSize(FONT_SIZE_DEFAULT)
                    fs.font(proof_font.path)
                    fs.align("center")

                    _faded = (0,0,0,.15)

                    if self.use_instances == False:
                        fs.fill(0)
                        fs.append(f"{loc.name}")
                    else:
                        if loc.type == "source":
                            fs.fill(*_faded)
                            fs.append("〖")
                            fs.fill(0)
                            fs.append(f"{loc.name}")
                            fs.fill(*_faded)
                            fs.append("〗")
                        else:
                            fs.fill(0)
                            fs.append(f"{loc.name}")

                    fs.append("\n")
            else:
                fs.fontSize(FONT_SIZE_DEFAULT)
                fs.font(proof_font.path)
                fs.align("center")
                fs.append(f"{proof_font.name}")
                if proof_font != fonts[-1]:
                    fs.append("\n")    
                
        txt_w = bot.textSize(fs)[0]
        txt_h = bot.textSize(fs)[1]

        try:
            width_ratio = box_w/txt_w 
        except ZeroDivisionError:
            width_ratio = 1
        mu = str(fs).count("\n") or 1
        height_ratio = box_h/(FONT_SIZE_DEFAULT * mu * 1.5)

        sf = min([width_ratio , height_ratio])

        with bot.savedState():
            bot.scale(sf)
            bot.textBox(fs, (box_x/sf, box_y/sf, box_w/sf, box_h/sf))   


if __name__ == "__main__":

    doc = proofDocument()

    """load old settings"""
    # doc.load("/Users/connordavenport/Dropbox/Clients/Dinamo/03_DifferentTimes/Sources/variable_ttf/2025-0526-ABCDifferentTimes.proof")

    """
    add a font or designspace, only accepts path strings
        should it accept designspace objects? ufos?
    """
    doc.add_object("/Users/connordavenport/Dropbox/Clients/Dinamo/03_DifferentTimes/Sources/Different-Times-v10.designspace")

    doc.crop_space("wght=500:900 slnt=1")
    doc.size = "LetterLandscape"
    doc.caption_font = "CoreMono-Regular"
    doc.margin = "auto"
    doc.use_instances = False

    doc.setup_proof()
    # doc.new_section(
    #                 "core",
    #                )
    # doc.new_section(
    #                 "paragraph",
    #                 point_size=[12,20],
    #                 multi_size_page=True, # if True and multi point sizes, adds multi-column page with no overflow
    #                )
    doc.new_section(
                    "features",
                   )

    """
    proofml is an experimental proofing language
    that is inspried by Tal Leming's ezui.
    """
    proofml_data = '''
    * proof
    [][][] @top
    [ ][ ] @middle
    '''

    # doc.new_section(
    #                 "proofml",
    #                 data=proofml_data
    #                )


    # doc.open_automatically = False
    """
    kwargs inside of save overwrite whatever the doc says.
    path, compiles name for current proof, will override with given if used
    open, by default is `False`, open in Preview
    overwrite, save over older proofs, default is `True`. `False` will append + "1" until path is unique
    write to disk
    """
    doc.save(open=True)

    """
    write to custom file format to save exact proof settings for later
    doc and save both allow for overwriting the previous file on disk
    overwrite is set to True by default
    """
    # doc.write(overwrite=True)




