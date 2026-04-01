from __future__ import annotations

from fontTools.ttLib import TTFont
import os
from fontTools.designspaceLib import DesignSpaceDocument as dsp_doc
from fontTools.designspaceLib import DiscreteAxisDescriptor, AxisDescriptor
from fontTools.designspaceLib.split import _extractSubSpace, defaultMakeInstanceFilename, MakeInstanceFilenameCallable, getVFUserRegion
import fontTools.varLib as varLib
from fontTools.misc.fixedTools import otRound, strToFixedToFloat, floatToFixedToFloat
import fnmatch
from typing import Union, Any, Callable, Dict, Iterator, List, Tuple, cast, Optional

import re
import drawBot as bot
import drawBotGrid as grid
from drawBotGrid import textOverflowTestMode as overflow_mode
import more_itertools as mit
from contextlib import contextmanager
from defcon.tools.identifiers import makeRandomIdentifier
from pathlib import Path
import getpass
import datetime
from ufoProcessor.ufoOperator import UFOOperator as uop
import plistlib
import inspect
from random import randint, choice
from collections.abc import MutableSequence
from pprint import pprint
from english_words import get_english_words_set
from itertools import groupby
import uuid
from wordsiv import WordSiv
from iso639 import Lang
from importlib import resources
import sys
from fPDK import fonts

# fPDK, font Proofing Development Kit

USER = getpass.getuser()

FALLBACK = resources.files(fonts).joinpath('AdobeBlank.otf')

CORE         = ()
RUNNING_TEXT = ()
OPENTYPE     = ()
GRADIENT     = ()
INSPECTOR    = ()

VALID_XML_TYPES = ["str", "bool", "int", "float", "dict", "bytes", "datetime.datetime", "tuple", "list"]

SECTION_TYPES = [CORE, RUNNING_TEXT, OPENTYPE, GRADIENT, INSPECTOR]

PROOF_DATA = {

    "core"           : "ABCDEFGHIJKLM\nNOPQRSTUVWXYZ\nabcdefghijklm\nnopqrstuvwxyz\n0123456789ªº\n%*.,:;!¡?¿‽#/\\\n-—_(){}[]‚“”‘’‹›\"\'\n+−×=><@&§®℗|¢$€£¥",
    "spacing"        : "NULL",
    "figures"        : "0123456789 H0H1H2H3H4H5H6H7H8H9"+"\n"+"".join([str((randint(0,9))) for i in range(1000)]),
    "lowercase"      : "Angel Adept Blind Bodice Clique Coast Dunce Docile Enact Eosin Furlong Focal Gnome Gondola Human Hoist Inlet Iodine Justin Jocose Knoll Koala Linden Loads Milliner Modal Number Nodule Onset Oddball Pneumo Poncho Quanta Qophs Rhone Roman Snout Sodium Tundra Tocsin Uncle Udder Vulcan Vocal Whale Woman Xmas Xenon Yunnan Young Zloty Zodiac. Angel angel adept for the nuance loads of the arena cocoa and quaalude. Blind blind bodice for the submit oboe of the club snob and abbot. Clique clique coast for the pouch loco of the franc assoc and accede. Dunce dunce docile for the loudness mastodon of the loud statehood and huddle. Enact enact eosin for the quench coed of the pique canoe and bleep. Furlong furlong focal for the genuflect profound of the motif aloof and offers. Gnome gnome gondola for the impugn logos of the unplug analog and smuggle. Human human hoist for the buddhist alcohol of the riyadh caliph and bathhouse. Inlet inlet iodine for the quince champion of the ennui scampi and shiite. Justin justin jocose for the djibouti sojourn of the oranj raj and hajjis. Knoll knoll koala for the banknote lookout of the dybbuk outlook and trekked. Linden linden loads for the ulna monolog of the consul menthol and shallot. Milliner milliner modal for the alumna solomon of the album custom and summon. Number number nodule for the unmade economic of the shotgun bison and tunnel. Onset onset oddball for the abandon podium of the antiquo tempo and moonlit. Pneumo pneumo poncho for the dauphin opossum of the holdup bishop and supplies. Quanta quanta qophs for the inquest sheqel of the cinq coq and suqqu. Rhone rhone roman for the burnt porous of the lemur clamor and carrot. Snout snout sodium for the ensnare bosom of the genus pathos and missing. Tundra tundra tocsin for the nutmeg isotope of the peasant ingot and ottoman. Uncle uncle udder for the dunes cloud of the hindu thou and continuum. Vulcan vulcan vocal for the alluvial ovoid of the yugoslav chekhov and revved. Whale whale woman for the meanwhile blowout of the forepaw meadow and glowworm. Xmas xmas xenon for the bauxite doxology of the tableaux equinox and exxon. Yunnan yunnan young for the dynamo coyote of the obloquy employ and sayyid. Zloty zloty zodiac for the gizmo ozone of the franz laissez and buzzing.",
    "uppercase"      : "ABIDE ACORN OF THE HABIT DACRON FOR THE BUDDHA GOUDA QUAALUDE. BENCH BOGUS OF THE SCRIBE ROBOT FOR THE APLOMB JACOB RIBBON. CENSUS CORAL OF THE SPICED JOCOSE FOR THE BASIC HAVOC SOCCER. DEMURE DOCILE OF THE TIDBIT LODGER FOR THE CUSPID PERIOD BIDDER. EBBING ECHOING OF THE BUSHED DECAL FOR THE APACHE ANODE NEEDS. FEEDER FOCUS OF THE LIFER BEDFORD FOR THE SERIF PROOF BUFFER. GENDER GOSPEL OF THE PIGEON DOGCART FOR THE SPRIG QUAHOG DIGGER. HERALD HONORS OF THE DIHEDRAL MADHOUSE FOR THE PENH RIYADH BATHHOUSE. IBSEN ICEMAN OF THE APHID NORDIC FOR THE SUSHI SAUDI SHIITE. JENNIES JOGGER OF THE TIJERA ADJOURN FOR THE ORANJ KOWBOJ HAJJIS. KEEPER KOSHER OF THE SHRIKE BOOKCASE FOR THE SHEIK LOGBOOK CHUKKAS. LENDER LOCKER OF THE CHILD GIGOLO FOR THE UNCOIL GAMBOL ENROLLED. MENACE MCCOY OF THE NIMBLE TOMCAT FOR THE DENIM RANDOM SUMMON. NEBULA NOSHED OF THE INBRED BRONCO FOR THE COUSIN CARBON KENNEL. OBSESS OCEAN OF THE PHOBIC DOCKSIDE FOR THE GAUCHO LIBIDO HOODED. PENNIES PODIUM OF THE SNIPER OPCODE FOR THE SCRIP BISHOP HOPPER. QUANTA QOPHS OF THE INQUEST OQOS FOR THE CINQ COQ SUQQU. REDUCE ROGUE OF THE GIRDLE ORCHID FOR THE MEMOIR SENSOR SORREL. SENIOR SCONCE OF THE DISBAR GODSON FOR THE HUBRIS AMENDS LESSEN. TENDON TORQUE OF THE UNITED SCOTCH FOR THE NOUGHT FORGOT BITTERS. UNDER UGLINESS OF THE RHUBARB SEDUCE FOR THE MANCHU HINDU CONTINUUM. VERSED VOUCH OF THE DIVER OVOID FOR THE TELAVIV KARPOV FLIVVER. WENCH WORKER OF THE UNWED SNOWCAP FOR THE ANDREW ESCROW GLOWWORM. XENON XOCHITL OF THE MIXED BOXCAR FOR THE SUFFIX ICEBOX EXXON. YEOMAN YONDER OF THE HYBRID ARROYO FOR THE DINGHY BRANDY SAYYID. ZEBRA ZOMBIE OF THE PRIZED OZONE FOR THE FRANZ ARROZ BUZZING.",
    "paragraph"      : """La noche del 12 de julio de 1954, sufrió de fiebre alta y dolores extremos. Aproximadamente a las seis de la mañana del 13 de julio, su enfermera la encontró muerta en su cama. Kahlo tenía 47 años al morir, y sus causas de muerte oficiales fueron una embolia pulmonar no traumática y una flebitis en un miembro inferior derecho no traumática. No obstante, no se le realizó una autopsia. Ante esto, una versión alterna asegura que en realidad se suicidó. Los puntos que apoyaron dicha hipótesis fueron las declaraciones de su enfermera, quien aseguró que contaba los analgésicos de la artista para poder tenerle un control de los mismos, pero la noche antes de su muerte se provocó una sobredosis. Tenía prescrito una dosis máxima de siete pastillas, pero ingirió once. En adición, esa noche le dio a Rivera un regalo de aniversario de bodas, con más de un mes de antelación. \n\nSu cuerpo fue velado en el Palacio de Bellas Artes y su ataúd fue cubierto con la bandera del Partido Comunista Mexicano, hecho que la prensa nacional criticó profusamente. Concluidas sus ceremonias de despedida, fue cremada en el Panteón Civil de Dolores. Sus cenizas fueron llevadas a descansar a la Casa Azul en Coyoacán, el mismo lugar donde nació y que años más tarde se convirtió en museo. Rivera, quien afirmó que su muerte fue «el día más trágico de su vida», falleció tres años después, en 1957.""",

    "kerning"        : {
        "all pairs"      : "Aardvark Ablution Acrimonious Adventures Aeolian Africa Agamemnon Ahoy Aileron Ajax Akimbo Altruism America Anecdote Aorta Aptitude Aquarium Arcade Aspartame Attrition Aurelius Avuncular Awning Axminster Ayers Azure Banishment Bb Bc Bd Benighted Bf Bg Bhagavad Biblical Bjorn Bk Blancmange Bm Bn Bolton Bp Bq Brusque Bs Bt Burnish Bv Bwana Bx Byzantium Bz Cabbala Cb Cc Cd Cetacean Cf Cg Charlemagne Cicero Cj Ck Clamorous Cm Cnidarian Conifer Cp Cq Crustacean Cs Ctenoid Culled Cv Cw Cx Cynosure Czarina Dalmatian Db Dc Dd Delphi Df Dg Dhurrie Dinner Djinn Dk Dl Dm Dn Document Dp Dq Drill Ds Dt Dunleary Dvorak Dwindle Dx Dynamo Dz Eames Ebullient Echo Edify Eels Eftsoons Egress Ehrlich Eindhoven Eject Ekistics Elzevir Eminence Ennoble Eocene Ephemeral Equator Erstwhile Estienne Etiquette Eucalyptus Everyman Ewen Exeter Eyelet Ezekiel Fanfare Fb Fc Fd Ferocious Ffestiniog Fg Fh Finicky Fjord Fk Flanders Fm Fn Forestry Fp Fq Frills Fs Ft Furniture Fv Fw Fx Fylfot Fz Garrulous Gb Gc Gd Generous Gf Gg Ghastly Gimlet Gj Gk Glorious Gm Gnomon Golfer Gp Gq Grizzled Gs Gt Gumption Gv Gwendolyn Gx Gymkhana Gz Harrow Hb Hc Hd Heifer Hf Hg Hh Hindemith Hj Hk Hl Hm Hn Horace Hp Hq Hr Hsi Ht Hubris Hv Hw Hx Hybrid Hz Iambic Ibarra Ichthyology Identity Ievgeny Ifrit Ignite Ihre Ii Ij Ikon Iliad Imminent Innovation Iolanthe Ipanema Iq Irascible Island Italic Iu Ivory Iwis Ixtapa Iyar Izzard Janacek Jb Jc Jd Jenson Jf Jg Jh Jitter Jj Jk Jl Jm Jn Joinery Jp Jq Jr. Js Jt Jungian Jv Jw Jx Jy Jz Kaiser Kb Kc Kd Kenilworth Kf Kg Khaki Kindred Kj Kk Klondike Km Knowledge Kohlrabi Kp Kq Kraken Ks Kt Kudzu Kvetch Kwacha Kx Kyrie Kz Labrador Lb Lc Ld Lent Lf Lg Lhasa Liniment Lj Lk Llama Lm Ln Longboat Lp Lq Lr Ls Lt Luddite Lv Lw Lx Lyceum Lz Mandarin Mbandaka Mcintyre Mdina Mendacious Mfg. Mg Mh Millinery Mj Mk Mlle. Mme. Mnemonic Moribund Mp Mq Mr. Ms. Mtn. Munitions Mv Mw Mx Myra Mz Narragansett Nb Nc Nd Nefarious Nf Nguyen Nh Nile Nj Nkoso Nl Nm Nnenna Nonsense Np Nq Nr. Ns Nt Nunnery Nv Nw Nx Nyack Nz Oarsman Oblate Ocular Odessa Oedipus Often Ogre Ohms Oilers Oj Okra Olfactory Ominous Onerous Oogamous Opine Oq Ornate Ossified Othello Oubliette Ovens Owlish Oxen Oyster Ozymandias Parisian Pb Pc Pd. Penrose Pfennig Pg. Pharmacy Pirouette Pj Pk Pleistocene Pm Pneumatic Porridge Pp. Pq Principle Psaltery Ptarmigan Pundit Pv Pw Px Pyrrhic Pz Qaid Qb Qc Qd Qed Qf Qg Qh Qibris Qj Qk Ql Qm Qn Qom Qp Qq Qr Qs Qt Quill Qv Qw Qx Qy Qz Ransom Rb. Rc Rd. Renfield Rf Rg Rheumatic Ringlet Rj Rk Rl Rm. Rn Ronsard Rp. Rq Rr Rs Rte. Runcible Rv Rwanda Rx Rye Rz Salacious Sbeitla Scherzo Sd Serpentine Sforza Sg Shackles Sinful Sjoerd Skull Slalom Smelting Snipe Sorbonne Spartan Squire Sri Ss Stultified Summoner Svelte Swarthy Sx Sykes Szentendre Tarragon Tblisi Tcherny Td Tennyson Tf Tg Thaumaturge Tincture Tj Tk Tlaloc Tm Tn Toreador Tp Tq Treacherous Tsunami Tt Turkey Tv Twine Tx Tyrolean Tzara Ua Ubiquitous Ucello Udder Ue Ufology Ugric Uhlan Uitlander Uj Ukulele Ulster Umber Unguent Uomo Uplift Uq Ursine Usurious Utrecht Uu Uvula Uw Uxorious Uy Uzbek Vanished Vb Vc Vd. Venomous Vf Vg Vh Vindicate Vj Vk Vl Vm Vn Voracious Vp Vq Vrillier Vs. Vt. Vulnerable Vv Vw Vx Vying Vz Washington Wb Wc Wd Wendell Wf Wg Wharf Window Wj Wk Wl Wm. Wn Worth Wp Wq Wrung Ws Wt. Wunderman Wv Wx Wy Wyes Wz Xanthan Xb Xc Xd Xenon Xf Xg Xh Xiao Xj Xk Xl Xmas Xn Xo Xp Xq Xray Xs Xt Xuxa Xv Xw Xx Xylem Xz Yarrow Ybarra Ycair Yds. Yellowstone Yf Yggdrasil Yh Yin Yj Yk Ylang Ym Yn Yours Ypsilanti Yquem Yrs. Ys. Ytterbium Yunnan Yvonne Yw Yx Yy Yz Zanzibar Zb Zc Zd Zero Zf Zg Zhora Zinfandel Zj Zk Zl Zm Zn Zone Zp Zq Zr Zs Zt Zuni Zv Zwieback Zx Zygote Zz",
        "lowercase"      : "a b c d e f g h i j k l m n o p q r s t u v w x y z ß æ ð ø þ đ ħ ŋ œ ł ŧ" ,
        "uppercase"      : "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z ẞ Æ Ð Ø Þ Ħ Ł Ŋ Œ Ł Ŧ",
        "mixed"          : "",
        "numr"           : "0001020 0304050 060708090 1011121 1314151 161718191 2021222 2324252 262728292 3031323 3334353 363738393 4041424 4344454 464748494 5051525 5354555 565758595 6061626 6364656 666768696 7071727 7374757 767778797 8081828 8384858 868788898 9091929 9394959 969798999",
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
"lowercase",
"uppercase",
"paragraph",
"kerning"
]

FONT_SIZE_DEFAULT = 28
FONT_SIZE_SMALL   = 9
FONT_SIZE_MED     = 12
FONT_SIZE_LARGE   = 30

# using frederik's window tilling method
TILE_REFERENCE = {
1  : [[1]],
2  : [[1],[1]],
3  : [[1],[1, 1]],
4  : [[1, 1], [1, 1]],
5  : [[1, 1], [1, 1, 1]],
6  : [[1, 1, 1], [1, 1, 1]],
7  : [[1, 1, 1], [1, 1, 1, 1]],
8  : [[1, 1, 1, 1], [1, 1, 1, 1]],
9  : [[1, 1, 1, 1], [1, 1, 1, 1, 1]],
10 : [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],
11 : [[1, 1, 1, 1],[1, 1, 1, 1],[1, 1, 1]],
12 : [[1, 1, 1, 1],[1, 1, 1, 1],[1, 1, 1, 1]],
}

PAGE_SIZES = bot.sizes()
PAGE_SIZE_DEFAULT = "LetterLandscape"


def width_class(wdth_user_value: int) -> int:
    '''
    function taken from fontMake's instancistator
    '''
    WDTH_VALUE_TO_OS2_WIDTH_CLASS = { 50:1, 62.5:2, 75:3, 87.5:4, 100:5, 112.5:6, 125:7, 150:8, 200:9}
    width_user_value = min(max(wdth_user_value, 50), 200)
    width_user_value_mapped = varLib.models.piecewiseLinearMap(
        width_user_value, WDTH_VALUE_TO_OS2_WIDTH_CLASS
    )
    return otRound(width_user_value_mapped)

def weight_class(wght_user_value: int) -> int:
    '''
    function taken from fontMake's instancistator
    '''
    weight_user_value = min(max(wght_user_value, 1), 1000)
    return otRound(weight_user_value)

def italic_value(slnt_user_value: int) -> int | float:
    '''
    function taken from fontMake's instancistator
    '''
    slant_user_value = min(max(slnt_user_value, -90), 90)
    return slant_user_value


class ProofObjectHandler(list):
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
            elif isinstance(initlist, ProofObjectHandler):
                self.data[:] = initlist.data[:]
            else:
                self.data = list(initlist)

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
        if isinstance(other, ProofObjectHandler):
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

    def insert(self, idx: int, value: ProofFont | ProofLocation):
        self.data.insert(idx, value)

    def pop(self, idx: int=-1) -> self.__class__(self):
        return self.data.pop(idx)

    def remove(self, value: ProofFont | ProofLocation):
        self.data.remove(value)

    def clear(self):
        self.data.clear()

    def copy(self) -> self.__class__(self):
        return self.__class__(self)

    def index(self, idx: int, *args: int) -> ProofFont | ProofLocation:
        return self.data.index(idx, *args)

    def reverse(self):
        self.data.reverse()

    def sort(self, /, *args, **kwds):
        # sort a list of instances by locations
        # knows how to sort different subclass types
        test = self.data[0]
        if isinstance(test, ProofLocation):
            self.data.sort(key=lambda d: (-width_class(d.location.get("wdth",0)), -italic_value(d.location.get("slnt",0)), weight_class(d.location.get("wght",0))))
        elif isinstance(test, ProofFont):
            self.data.sort(key=lambda f: (f.font_object["OS/2"].usWeightClass, -f.font_object["post"].italicAngle, -f.font_object["OS/2"].usWidthClass))
        else:
            self.data.sort(*args, **kwds)

    def extend(self, other: self.__class__(self), clear:bool=False):
        if clear:
            self.data.clear()
        if isinstance(other, ProofObjectHandler):
            self.data.extend(other.data)
        else:
            self.data.extend(other)

class ProofLocation:

    def __repr__(self):
        name = ""
        if self.is_source:
            name = "source"
        if self.is_instance:
            name = "instance"
        if self.is_source and self.is_instance:
            name = "both"
        return f"<ProofLocation.{name} @ {self.name}>"

    def __init__(self, location:dict={}):

        self.is_instance = False
        self.is_source = False
        self.data_from = "TTFont" # DesignSpaceDocument or TTFont

        self._in_crop = True
        self._font = None
        self._name = "unnamed location"
        self._location = location


    def _get_in_crop(self) -> bool:
        return self._in_crop

    def _set_in_crop(self, new_in_crop:bool):
        self._in_crop = new_in_crop

    in_crop = property(_get_in_crop, _set_in_crop)

    def _get_origin(self) -> TTFont:
        return self._origin

    def _set_origin(self, new_origin: TTFont):
        self._origin = new_origin

    origin = property(_get_origin, _set_origin)

    def _get_name(self) -> str:
        return self._name

    def _set_name(self, new_name: str):
        self._name = new_name

    name = property(_get_name, _set_name)

    def _get_location(self) -> dict:
        return self._location

    def _set_location(self, new_location: dict):
        self._location = new_location

    location = property(_get_location, _set_location)


    def generate_name(self, font_obj: TTFont) -> str:
        best_name = font_obj["name"].getBestFullName()
        if "fvar" in font_obj:
            for i in font_obj["fvar"].instances:
                l = self._location
                if i.coordinates == l:
                    for name in font_obj["name"].names:
                        if name.nameID == i.subfamilyNameID:
                            best_name = f'{font_obj["name"].getBestFamilyName()} {name}'
        return best_name



class ProofFont:

    def __init__(self, path: str):
        self.path               = path
        self.font_object        = None
        self.load_font()
        self.is_variable        = False
        self.locations          = ProofObjectHandler([])
        self.operator           = dsp_doc
        self._name              = self._compile_name()
        self.features           = {}

    def __repr__(self) -> str:
        return repr(self.path)

    def load_font(self):
        if self.path:
            self.font_object = TTFont(self.path)

    # get font objects best possible name
    def _compile_name(self) -> str:
        f = self.font_object
        try:
            best_name = f["name"].getBestFullName()
        except TypeError:
            best_name = ""

        return best_name

    def _get_name(self) -> str:
        return self._name

    def _set_name(self, new_name:str):
        self._name = new_name

    name = property(_get_name, _set_name)

    # def _sort_locations(self):
    #     return sorted(self.loc, key=lambda d: (-width_class(d.location.get("wdth",0)), -italic_value(d.location.get("slnt",0)), weight_class(d.location.get("wght",0))))

    def _reformat_locations(self, designspace:dsp_doc, instance:dict, axis_map:dict, renamer:dict) -> dict:
        parsed = {}
        instance = designspace.map_backward(instance.location)
        for axis,val in instance.items():
            a = renamer.get(axis)
            parsed[a]=val
        return parsed

    def get_OT(self) -> dict:
        font = self.font_object
        if "GSUB" in font:
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
                    submap = {}
                    for subtable in Lookup.SubTable:

                        if subtable.LookupType == 1:
                            mapping = subtable.mapping
                        elif subtable.LookupType == 6:
                            back = subtable.BacktrackCoverage
                            inp = subtable.InputCoverage
                            ahead = subtable.LookAheadCoverage

                            ind = subtable.SubstLookupRecord[0].LookupListIndex
                            subref = _gsub.table.LookupList.Lookup[ind]
                            sing = subref.SubTable[0].mapping

                            if inp:
                                inp = inp[0].glyphs
                            if back:
                                back = back[0].glyphs
                            if ahead:
                                ahead = ahead[0].glyphs
                            if not back:
                                submap[inp[0]] = (sing[inp[0]], dict(extra=sing.get(ahead[0], ahead[0]), pos="middle"))
                            else:
                                submap[inp[-1]] = (sing[inp[-1]], dict(extra=back[-1], pos="before"))
                            mapping = submap

                    if mapping:
                        _features[tag] = ((desc,LookupID,mapping))

            self.features = _features
            return _features


    """
    I would prefer not to do this but we need
    to keep the old vf paths in order to find the fonts
    accurately so we need to override the
    `keepVFs` attr in the function
    """
    def _splitVariableFonts(
        self,
        doc : dsp_doc,
        makeNames: bool = False,
        expandLocations: bool = False,
        makeInstanceFilename: MakeInstanceFilenameCallable = defaultMakeInstanceFilename,
    ) -> Iterator[Tuple[str, dsp_doc]]:
        """Convert each variable font listed in this document into a standalone
        designspace. This can be used to compile all the variable fonts from a
        format 5 designspace using tools that can only deal with 1 VF at a time.

        Args:
          - ``makeNames``: Whether to compute the instance family and style
            names using the STAT data.
          - ``expandLocations``: Whether to turn all locations into "full"
            locations, including implicit default axis values where missing.
          - ``makeInstanceFilename``: Callable to synthesize an instance filename
            when makeNames=True, for instances that don't specify an instance name
            in the designspace. This part of the name generation can be overridden
            because it's not specified by the STAT table.

        .. versionadded:: 5.0
        """
        # Make one DesignspaceDoc v5 for each variable font

        for vf in self.operator.getVariableFonts():
            vfUserRegion = getVFUserRegion(doc, vf)
            vfDoc = _extractSubSpace(
                doc,
                vfUserRegion,
                keepVFs=True,
                makeNames=makeNames,
                expandLocations=expandLocations,
                makeInstanceFilename=makeInstanceFilename,
            )
            vfDoc.lib = {**vfDoc.lib, **vf.lib}
            yield vf.name, vfDoc


    def build_locations(self, should_sort:bool=True):
        font_obj   = self.font_object
        operator = self.operator

        _instances = {}
        renamer = {a.name:a.tag for a in operator.axes}

        if operator:
            for v in self._splitVariableFonts(operator, expandLocations=True, makeInstanceFilename=True):
                sub_space, split_op = v
                # this is the only way to split the vfs and still keep the paths
                # we can assume that post-split we will only have 1 vf to extract
                extracted_path = split_op.variableFonts[0].filename
                name = sub_space
                if extracted_path:
                    name = os.path.splitext(extracted_path)[0]

                if name == os.path.splitext(os.path.basename(self.path))[0]:
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
                                built = ProofLocation(ii.location)
                            built.name = f"{ii.familyName} {ii.styleName}"
                            built.data_from = "DesignSpaceDocument"
                            setattr(built, f"is_{item}", True)
                            built.origin = font_obj
                            _instances[str(built.location)] = built

        if not _instances:
        # we dont want to rely on the fvar instances because there is no source data to proof
            if "fvar" in font_obj:
                for inst in [instance.coordinates for instance in font_obj["fvar"].instances]:
                    built = ProofLocation(inst)
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
        if should_sort:
            self.locations.sort() # = self._sort_locations(list(_instances.values()))



class ProofDocument:

    def __repr__(self) -> str:
        return f"<ProofDocument @ {self.identifier} : {hash(tuple(self.fonts))}>"

    def __init__(self):

        self._counter = 0
        self._group_count = 0
        self._compiling = False

        self.storage        = []
        self.packaged       = []
        self._now           = datetime.datetime.now()
        self._identifier    = None
        self._operator      = None
        self._crop          = ""
        self._use_instances = False
        self._sort          = True
        self._path          = None
        self._name          = None

        self._custom_text   = ""

        self._scope         = "core"
        self._language      = "english"
        self._lang_tag      = "en"

        self._target_size   = None

        self.fonts          = ProofObjectHandler([])
        self.objects        = []
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

        self._grid = None
        self.instance_color = (0.58, 0.22, 1, 1)
        self.words = []
        self.in_group = 0


    def find_proof_directory(self, root_dir:str, target_filename:str) -> str:
        # I don't think I wrote this function but I can't remember where I got it...
        root_dir = os.path.abspath(root_dir)
        closest_directory = save_path = None
        closest_distance = float('inf')  # Initialize to positive infinity
        current_path = root_dir
        while current_path != os.path.sep:
            for filename in os.listdir(current_path):
                if target_filename in filename:
                    distance = len(os.path.relpath(current_path, root_dir).split(os.path.sep))
                    if distance < closest_distance:
                        closest_directory = current_path
                        closest_distance = distance
                        save_path = os.path.join(closest_directory, filename)
            current_path = os.path.dirname(current_path)
        return save_path

    # do we even need ids??-----------------------
    def _get_identifier(self) -> str:
        if not self._identifier:
            self._identifier = self.generate_identifier()
        return self._identifier

    def _set_identifier(self, new_id: str):
        self._identifier = new_id

    identifier = property(_get_identifier, _set_identifier)

    def generate_identifier(self) -> str:
        return makeRandomIdentifier(existing=[])
    # ----------------------------------------------

    def _get_page_size(self) -> tuple[int,float]:
        if isinstance(self._size, str):
            size = PAGE_SIZES[self._size]
        else:
            size = self._size

        return size

    def _set_page_size(self, new_page_size: Optional[str, tuple]):
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
        self._grid = grid.ColumnGrid(
                                    (
                                        self._margin_left,
                                        self._margin_bottom,
                                        *self._text_box_size
                                    ),
                                    subdivisions=5
                                   )

    size = property(_get_page_size, _set_page_size)

    def _set_caption_font(self, new_font: str):
        import errno
        if new_font in bot.installedFonts():
            self._caption_font = new_font
        else:
            raise FileNotFoundError(
                        errno.ENOENT,
                        os.strerror(errno.ENOENT),
                        new_font
                        )

    def _get_caption_font(self) -> str:
        return self._caption_font

    caption_font = property(_get_caption_font, _set_caption_font)

    def _set_auto_open(self, value: bool):
        self._auto_open = value

    def _get_auto_open(self) -> bool:
        return self._auto_open

    open_automatically = property(_get_auto_open, _set_auto_open) # open pdf immediately after saving to disk


    def _set_custom_text(self, value: str):
        self._custom_text = value

    def _get_custom_text(self) -> str:
        return self._custom_text

    text = property(_get_custom_text, _set_custom_text) # override running text content

    def _set_path(self, new_path: str):
        self._path = new_path

    def _get_path(self) -> str:
        if not self._path:
            self._path = self.generate_path_base()
        return self._path

    path = property(_get_path, _set_path)

    def _set_language(self, new_language: str):

        self._language = new_language
        try:
            self._lang_tag = Lang(new_language.title()).pt1
        except:
            self._lang_tag = ""


    def _get_language(self) -> str:
        return self._language

    language = property(_get_language, _set_language)

    def _set_target_size(self, new_target_size: str):
        self._target_size = new_target_size

    def _get_target_size(self) -> str:
        if not self._target_size:
            self._target_size = False
        return self._target_size

    target_size = property(_get_target_size, _set_target_size)

    def _set_name(self, new_name: str):
        self._name = new_name

    def _get_name(self) -> str:
        if not self._name and self.fonts:
            # return family name for top level font
            self._name = self.fonts[0].font_object["name"].getBestFamilyName().replace(" ","")
        return self._name

    name = property(_get_name, _set_name)

    def _set_scope(self, new_scope: str):
        self._scope = new_scope

    def _get_scope(self) -> str:
        return self._scope

    scope = property(_get_scope, _set_scope)

    # def _set_operator(self, new_operator):
    #     self._operator = new_operator

    # def _get_operator(self):
    #     return self._operator

    # operator = property(_get_operator, _set_operator)

    def _get_margin(self) -> list[int]:
        return (
                self._margin_top,
                self._margin_left,
                self._margin_bottom,
                self._margin_right,
                )

    def _set_margin(self, new_margin: int | tuple[int]):
        # we can accept a tuple of 4 to set individual
        # or 1 value to apply across the board
        if isinstance(new_margin, (tuple, list)):
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

    def _get_use_instances(self) -> bool:
        return self._use_instances

    def _set_use_instances(self, value: bool):
        self._use_instances = value

    use_instances = property(_get_use_instances, _set_use_instances)

    def _get_should_sort(self) -> str:
        return self._sort

    def _set_should_sort(self, value: bool):
        # self._sort = fence
        self._sort = value

    sort = property(_get_should_sort, _set_should_sort)

    def _get_crop(self) -> str:
        return self._crop

    def _set_crop(self, fence: str = ""):
        # self._crop = fence
        self.crop_space(fence, True)

    crop = property(_get_crop, _set_crop)

    def uniquify(self, path: str) -> str:
        # https://stackoverflow.com/a/57896232
        filename, extension = os.path.splitext(path)
        counter = 1
        while os.path.exists(path):
            path = filename + "-" + str(counter) + extension
            counter += 1
        return path

    def generate_path_base(self, suffix: str=".pdf", overwrite: bool=True) -> str:
        cd = os.path.split(self.fonts[0].path)[0]
        directory = self.find_proof_directory(cd, "proofs")
        if not directory:
            directory = cd
        type = "-Proof" if suffix == ".pdf" else ""
        path = f'{directory}/{self._now:%Y-%m%d}-{self.name}{type}{suffix}'

        # make sure file names are unique if have overwrite flag on
        path = self.uniquify(path) if not overwrite else path
        return path


    def load(self, proof_data_path: str):
        with open(proof_data_path, "rb") as proof_settings:
            data = plistlib.load(proof_settings)
            for key, value in data.items():
                if key in ["fonts","objects","crop"]:
                    pass
                else:
                    setattr(self, key, value)

        unpacked = []
        if self.packaged:
            for temp in self.packaged:
                for page in temp:
                    unpacked.append(page)


        self.add_objects(data["objects"])
        self.crop_space(data["crop"])

        # self.crop_space(self.crop)

        self.storage = unpacked
        self.packaged = []

        # call setup directly
        self.setup()


    def write(self, path:Optional[str]=None, overwrite:bool=True):
        if self._compiling:
            pass
        else:
            self.packaged = self._group_data(self.storage, flatten_objects=True)

        _storing = [item[0] for item in inspect.getmembers(self) if not item[0].startswith("_") and not inspect.ismethod(item[1])]
        data = {}

        for item in _storing:
            comp = getattr(self, item)
            if item in ["storage", "fonts"]:
                continue
            data[item] = comp
            if hasattr(comp, "path"):
                data[item] = getattr(self,item).path

            if item == "packaged":
                for group in comp:
                    for page in group:
                        stored = page[-1].get("to_store", {})
                        if "fonts" in stored.keys():
                            del stored["fonts"]

        #pprint(data)
        dump_path = path if path else self.generate_path_base(".proof", overwrite)
        with open(dump_path, "wb") as proof_settings:
            plistlib.dump(data, proof_settings)


    def save(self, path:Optional[str]=None, open="_", overwrite:bool=True):

        _save_path = path if path else self.path
        _auto = open if open != "_" else self.open_automatically

        self._compile_proof()
        self.paginate()

        bot.saveImage(_save_path)
        if _auto:
            os.system(f"open -a Preview '{_save_path}'")


    def get_smallest_core_scaler(self, text:str | bot.FormattedString, fonts:list[ProofFont]) -> float:
        temp_holder = []
        for font in fonts:
            if font.is_variable:
                loc = font.locations.find(in_crop=True) if self.use_instances else font.locations.find(is_source=True, in_crop=True)
                for l in loc:
                    temp_holder.append(
                                        self.draw_core_characters(
                                            txt=text,
                                            font_path=font.path,
                                            variable_location=l.location,
                                            will_draw=False
                                            )
                                      )
            else:
                temp_holder.append(
                                    self.draw_core_characters(
                                        txt=text,
                                        font_path=font.path,
                                        will_draw=False
                                        )
                                  )
        return min(temp_holder)


    def _init_page(self,**kwargs):
        bot.newPage(*self.size)
        self.text_attributes()
        self.draw_header_footer(**kwargs)


    def draw_header_footer(self,**kwargs):
        font       = kwargs.get("font", ProofFont(""))
        proof_type = kwargs.get("proof_type", "")
        location   = kwargs.get("location", ProofLocation())
        cover      = kwargs.get("cover", False)
        features   = kwargs.get("openType", {})

        p = Path(proof_type)
        self.text_attributes()

        header_y_pos = self.size[1]-(self._margin_left/2)

        bot.text(f'Project: {self.name}', (self._grid[0], header_y_pos))
        bot.text(f'Date: {self._now:%Y-%m-%d %H:%M}', (self._grid[1], header_y_pos))
        if not cover:
            if location and not location.is_source:
                bot.fill(*self.instance_color)
                o_s = 8
                bot.oval(self._grid[2]-(o_s + (o_s/2)), header_y_pos-(o_s/4), o_s, o_s)

            bot.fill(0)
            bot.text(f'Style: {location.name if location.name != "unnamed location" else font.name}', (self._grid[2], header_y_pos))

            if True in features.values():
                feature_list = [k for k,v in features.items() if v == True]
                feature_string = ", ".join(feature_list)

                bot.text(f'OT: {feature_string}', (self._grid[3], header_y_pos))

            bot.text(f'Type: {p.stem}', (self.size[0]-self._margin_right, header_y_pos), align="right")
        fw,fh = bot.textSize(f'Style: {font.name}')
        if proof_type != "core" and location:
            bot.linkRect(f"beginPage_{font}{location.location}", (self._margin_left + (self.size[0]/4)*2, self.size[1]-self._margin_left, fw, fh))

        bot.text(f'© {self._now:%Y}' + ' ' + USER, (self._margin_left, self._margin_bottom/2))
        bot.fill(0)
        bot.stroke(None)


    def new_section(self,
                    proof_type:str,
                    point_size:int=FONT_SIZE_MED, # can accept list to generate section at different sizes
                    columns:int=1,
                    sources:bool=True,
                    instances:bool=False,
                    multi_size_page:bool=False,
                    overflow:bool=False, # if set to False the overflow will add new pages
                    openType:dict={}, # the only camel case :) a dict for activating specific OT on this page
                    tracking_values:list=[], # a list of tracking values to test, 0 (current) will always be the first
                    level:str="ascii",
                    ):

        to_store = {
                    item[0]:item[1]
                    for item in inspect.getmembers(self)
                    if not item[0].startswith("_")
                    and not inspect.ismethod(item[1])
                    and item[0] != "storage"
                   }

        cleaned = {k:v for k,v in locals().items() if k != "self"}
        self.move_to_storage(proof_type, cleaned)

        # new_section is just a moving company...
        # build_proofs is the new house but
        # we get our data from the storage

    def _get_working_locations(self, data:list, font) -> List:
        to_process = [ProofLocation()]
        if font.is_variable:
            if data[0] == "core":
                # different structure, fix this??
                to_process = font.locations.find(in_crop=True) if data[-1].get("to_store", {}).get("use_instances") else font.locations.find(is_source=True, in_crop=True)
            else:
                to_process = font.locations.find(in_crop=True) if data[0][-1].get("to_store", {}).get("use_instances") else font.locations.find(is_source=True, in_crop=True)
        return to_process


    def _draw_running_text(self, data=list, fonts:list[ProofFont]=[]):
        for font in fonts:

            to_process = self._get_working_locations(data, font)
            for loca in to_process:
                for sub_sec in data:

                    proof_type, local_data = sub_sec

                    point_size      = local_data.get("point_size", FONT_SIZE_MED)
                    columns         = local_data.get("columns", 1)
                    sources         = local_data.get("sources", True)
                    instances       = local_data.get("instances", False)
                    multi_size_page = local_data.get("multi_size_page", False)
                    overflow        = local_data.get("overflow", False)
                    openType        = local_data.get("openType", {})
                    class_data      = local_data.get("to_store", {})
                    tracking_values = local_data.get("tracking_values", [])
                    point_sizes     = list(mit.always_iterable(point_size))



                    if proof_type == "tracking":

                        num_of_track_vals = len(tracking_values)
                        if num_of_track_vals > 12:
                            raise ValueError

                        columns = len(max(TILE_REFERENCE[num_of_track_vals]))
                        rows = len(TILE_REFERENCE[num_of_track_vals])

                        txt = self.text if self.text else PROOF_DATA.get("paragraph")

                        self._init_page(font=font,proof_type=proof_type,location=loca,openType=openType)
                        txt = self.draw_text_layout(txt=txt,
                                                    font_path=font.path,
                                                    variable_location=loca.location,
                                                    columns=columns,
                                                    rows=rows,
                                                    overflow=False,
                                                    font_size=point_sizes,
                                                    multi_size_page=False,
                                                    openType=openType,
                                                    tracking_values=tracking_values,
                                                    )

                    else:

                        if proof_type == "spacing":
                            txt = self._parse_spacing_strings(
                                font.font_object.getGlyphOrder(),
                                string_data=dict(font=font.path, font_size=point_sizes[0])
                                )
                        elif proof_type == "kerning":
                            temp = PROOF_DATA.get("kerning")
                            def getString(word):
                                return f"nn{word}nn" if len(word) == 2 else word

                            def getKerningPair(pair, case):
                                side = "HO" if case == "uppercase" else "no"
                                l,r = side
                                if case == "mixed":
                                    return f"HH{pair[0]}{pair[1]}nn"
                                else:
                                    return f"{l}{l}{pair[0]}{pair[1]}{l}{r}{pair[0]}{pair[1]}{r}{r}"

                            hold = " ".join([getString(i) for i in temp["all pairs"].split(" ")])
                            temp["all pairs"] = hold

                            hold = " ".join([getKerningPair((ll,rr), "mixed") for ll in temp["uppercase"].split(" ") for rr in temp["lowercase"].split(" ")])
                            temp["mixed"] = hold
                            
                            hold = " ".join([getKerningPair((ll,rr), "lowercase") for ll in temp["lowercase"].split(" ") for rr in temp["lowercase"].split(" ")])
                            temp["lowercase"] = hold

                            hold = " ".join([getKerningPair((ll,rr), "uppercase") for ll in temp["uppercase"].split(" ") for rr in temp["uppercase"].split(" ")])
                            temp["uppercase"] = hold

                            txt = " ".join([t for n,t in temp.items() if "," not in n])
                        else:
                            if proof_type != "figures":
                                txt = self.text if self.text else PROOF_DATA.get("paragraph")
                            else:
                                txt = PROOF_DATA.get(proof_type)

                        if self.scope == "testword":
                            txt = ""
                            for i in range(20):
                                # try and generate words using the declared language
                                tag = self._lang_tag if self._lang_tag in WordSiv().list_vocabs() else "en"
                                wsv = WordSiv(vocab=tag, glyphs="HAMBUGERFONTSIVhambugerfontsiv.,")
                                txt += f"{wsv.sent(rnd=.03)}"
                        while txt:
                            if len(point_sizes) > 1 and multi_size_page:
                                self._init_page(font=font,proof_type=proof_type,location=loca,openType=openType)
                                txt = self.draw_text_layout(txt=txt,
                                                            font_path=font.path,
                                                            variable_location=loca.location,
                                                            columns=len(point_sizes),
                                                            overflow=overflow,
                                                            font_size=point_sizes,
                                                            multi_size_page=multi_size_page,
                                                            openType=openType
                                                            )
                            else:
                                for pt in point_sizes:
                                    self._init_page(font=font,proof_type=proof_type,location=loca,openType=openType)
                                    txt = self.draw_text_layout(txt=txt,
                                                                font_path=font.path,
                                                                variable_location=loca.location,
                                                                columns=columns,
                                                                overflow=overflow,
                                                                font_size=pt,
                                                                multi_size_page=multi_size_page,
                                                                openType=openType
                                                                )


    def _draw_gradient(self, data=list, fonts:list[ProofFont]=[]):
        proof_type,local_data = data
        level = local_data.get("level", "ascii")
        txt = self.get_gradient_strings(level=level)
        while txt:
            self._init_page(font=fonts[0],proof_type="gradient")
            txt = self.draw_text_layout(txt, font_path=fonts[0].path, overflow=True)


    def _parse_spacing_strings(self, characters:list[str,...],string_data:dict):
        from defcon.tools import unicodeTools as uni
        from defcon.objects.uniData import UnicodeData as ud
        from glyphNameFormatter.data import unicodeCategories
        from glyphNameFormatter.reader import n2u

        # characters = characters.replace("\n", "")

        fb = "HO"
        catMap = {"Lu":fb,"Ll":"no","Lt":fb,"Lm":fb,"Lo":"no","Mn":fb,"Mc":fb,"Me":fb,"Nd":"01","Nl":"01","No":"01","Pc":fb,"Pd":fb,"Ps":fb,"Pe":fb,"Pi":fb,"Pf":fb,"Po":fb,"Sm":"01","Sc":"01","Sk":fb,"So":fb,"Zs":fb,"Zl":fb,"Zp":fb,"Cc":fb,"Cf":fb,"Cs":fb,"Co":fb,"Cn":fb}

        #spacingStrings = ""
        spacingStrings = bot.FormattedString()
        for c in characters:
            w = True
            cat = unicodeCategories.get(n2u(c), "Cn")
            cm = catMap[cat]
            oo = ""
            if "P" == cat[0]:
                if cat[1] in ["i","s"]:
                    oo = chr(uni.closeRelative(n2u(c)))
                elif cat[1] in ["e","f"]:
                    oo = chr(uni.openRelative(n2u(c)))
                    w = False
            start,end = cm
            if w: 
                spacingStrings.append(f"{start}{start}", font=string_data.get("font"), fontSize=string_data.get("font_size"))
                spacingStrings.appendGlyph(c)
                spacingStrings.append(f"{start}{oo}{end}{start}{end}")
                spacingStrings.appendGlyph(c)
                spacingStrings.append(f"{end}{end}\n")

                #spacingStrings += f"{start}{start}{c}{start}{oo}{end}{start}{end}{c}{end}{end}\n"
        return spacingStrings
        

    def _draw_core(self, data=list, fonts:list[ProofFont]=[]):
        for font in fonts:
            to_process = self._get_working_locations(data, font)
            for loca in to_process:
                # for sub_sec in data:
                self._init_page(font=font,proof_type="core",location=loca)
                txt = "HAMBURGE\nFONSTIV" if self.scope == "testword" else PROOF_DATA["core"]

                min_size = self.get_smallest_core_scaler(txt, fonts)
                txt = self.draw_core_characters(
                                                txt=txt,
                                                font_path=font.path,
                                                variable_location=loca.location,
                                                will_draw=True,
                                                scale=min_size
                                                )

    def _group_data(self, data=list, flatten_objects:bool=False) -> list:
        # using the context manager we find the grouped sections
        # we need to update this so we can group it only in subsections of clusters
        # grouped = [it for it in storage if it[-1].get("in_group") == True]
        # pprint(grouped)
        result = []
        current = [data[0]]

        for prev, curr in zip(data, data[1:]):

            # if flatten_objects:
            #     curr[-1]["to_store"]["fonts"] = flatten(curr)

            if curr[-1]["to_store"].get("in_group") and (curr[-1]["to_store"].get("in_group") == prev[-1]["to_store"].get("in_group")):
                current.append(curr)
            else:
                result.append(tuple(current))
                current = [curr]
        result.append(tuple(current))

        return result


    def _compile_proof(self):

        self._compiling = True
        fonts = self.fonts
        storage = self.storage

        self.packaged = subs = self._group_data(storage)

        if subs[0][0][0] == "cover":
            """we can safely assume that the
            first item will always be cover because
            it is drawn when we initiate a new proof
            with the setup function
            """
            subs.pop(0)

        for section in subs:

            if len(section) == 1:
                section = section[0]
                name = section[0]
                if name in "paragraph tracking figures spacing kerning".split(" "):
                    self._draw_running_text([section], fonts)
                elif name == "core":
                    self._draw_core(section, fonts) # can not be processed inside a group
                elif name == "gradient":
                    self._draw_gradient(section, fonts) # can not be processed inside a group
                elif name == "features":
                    self._draw_features(section,fonts) # can not be processed inside a group
                else:
                    pass
            else:
                for font in fonts:
                    self._draw_running_text(section,[font])


    def _draw_features(self, data=list, fonts:list[ProofFont]=[]):

        proof_type, local_data = data

        caption_font   = local_data["to_store"].get("caption_font", "SFMono-Regular")
        _margin_left   = local_data["to_store"].get("margin", (50)*4)[1]
        _margin_bottom = local_data["to_store"].get("margin", (50)*4)[2]
        size           = local_data["to_store"].get("size", PAGE_SIZE_DEFAULT)
        if isinstance(size, str):
            size = PAGE_SIZES[size]

        _text_box_size = (
                          (size[0] - (_margin_left * 2 )),
                          (size[1] - (_margin_bottom * 2))
                         )

        for font in fonts:
            _to_use = font.locations.find(in_crop=True)
            if not _to_use:
                if font.locations:
                    _to_use = font.locations[0]
                else:
                    _to_use = None
            else:
                _to_use.sort()
                _to_use = _to_use[0]
            location = _to_use

            font_OT = font.get_OT()
            if not font_OT:
                print(f"""ERROR: {font.name} does not contain a GSUB table, skipping `feature` proof""")
            else:
                # if self.words == []:
                #     self.words = get_english_words_set(['web2'], lower=True)

                for tag, (desc,LookupID,mapping) in font_OT.items():

                    string = bot.FormattedString()
                    if font.is_variable:
                        string.fontVariations(**location.location)
                    cols = 1
                    if desc:
                        string.append(f"{tag} : {desc}\n", font=caption_font, fontSize=12)
                    else:
                        string.append(f"{tag}\n", font=caption_font, fontSize=12)
                    string.append("", font=font.path, fontSize=42)

                    if tag in ["c2sc", "smcp"]:
                        string.append("The Quick Brown Fox Jumps Over The Lazy Dog", font=font.path, fontSize=42, openTypeFeatures={tag:True,})
                    else:
                        # this means that the opentype lookup is complex
                        if isinstance(list(mapping.values())[0], tuple):

                            for fr,_to in mapping.items():
                                to, extra = _to
                                cxt = extra["extra"]
                                pos = extra["pos"]

                                print(fr, to)
                                print(cxt, pos)

                                rd = bot.FormattedString()
                                rd.append("", font=font.path, fontSize=42)
                                rd.append("HH")
                                if pos == "before":
                                    rd.appendGlyph(cxt)
                                    rd.appendGlyph(fr)
                                else:
                                    rd.appendGlyph(fr)
                                    rd.appendGlyph(cxt)
                                rd.append("HH")
                                string.append(rd, openTypeFeatures={tag:False})

                                # for gg in rd:
                                #     if gg in list(mapping.keys())[:2]:
                                #         string.fill(0,0,0,.3)
                                #     else:
                                #         string.fill(0,0,0,1)
                                #     string.append(gg, openTypeFeatures={tag:False})

                                string.append("→", fill=(0,0,0,.2), openTypeFeatures={tag:False})
                                string.fill(0)
                                string.append(rd, fill=(0,0,0,1), openTypeFeatures={tag:True})
                                string.append("\n")
                            cols = 1

                        else:
                            contains_all = lambda word, letters: all(letter in word for letter in letters)
                            #come up with a much faster word finder algo
                            contains = [word for word in self.words if contains_all(word, list(mapping.keys())[:2])]
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
                    grid.columnTextBox(string, (_margin_left, _margin_bottom, *_text_box_size), subdivisions=cols, gutter=15, draw_grid=False)


    def draw_core_characters(self, txt:str | bot.FormattedString, font_path:str, variable_location:dict={}, scale:Optional[float]=None, will_draw:bool=True, openType:dict={}):
        box_w, box_h = self._text_box_size
        box_x, box_y = self._margin_left, self._margin_bottom

        fs = bot.FormattedString()
        fs.fallbackFont(FALLBACK)

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

    def find_common_order(self, lists:list[list[str]]) -> list[str]:
        if len(lists) == 0:
            return []
        common_elements = set(lists[0])
        if len(lists) > 1:
            for lst in lists[1:]:
                common_elements = common_elements.intersection(lst)
        else:
            pass
        return list(common_elements)


    def get_gradient_strings(self, level:Optional[str]="ascii", font_size:int=40) -> str | bot.FormattedString:
        fonts = self.fonts

        if level == "all":
            chars = sorted(
                    self.find_common_order(
                            [ff.font_object.getGlyphOrder() for ff in fonts]
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
                locations = font.locations.find(in_crop=True) if self.use_instances else font.locations.find(is_source=True, in_crop=True) or [ProofLocation()]
                for loca in locations:
                    if loca.location:
                        txt.fontVariations(**loca.location)
                    txt.font(font.path)
                    txt.append("", tracking=(font_size*50/1000), lineHeight=font_size*1.1, fontSize=font_size)
                    txt.appendGlyph(l)
            txt.append("\n")

        return txt


    def draw_text_layout(self, txt:str | bot.FormattedString, font_path:str, variable_location:dict={}, columns:int=1, rows:int=1, overflow:bool=False, font_size:int=FONT_SIZE_MED, multi_size_page:bool=False, openType:dict={}, tracking_values:list[int]=[]) -> str | bot.FormattedString:

        _grid = grid.Grid((self._margin_left, self._margin_bottom, *self._text_box_size),
                               column_subdivisions=columns,
                               row_subdivisions=rows,
                               column_gutter=15,
                               row_gutter=15)

        bot.fallbackFont(FALLBACK)

        bot.fontVariations(**variable_location)
        bot.hyphenation(self.hyphenation)
        bot.openTypeFeatures(**openType)

        tile = TILE_REFERENCE.get(len(tracking_values))

        if tracking_values and tile:
            r_index,c_index = len(tile), 0
            for ti, trk_val in enumerate(tracking_values):
                if ti % len(max(tile)) == 0:
                    # reset line down
                    c_index  = 0
                    r_index -= 1
                else:
                    c_index += 1

                item_size = _grid

                bot.font(font_path, font_size[0])
                bot.tracking(font_size[0]*trk_val/1000)

                x,y = (_grid.columns[c_index], _grid.rows[r_index])
                grid.columnTextBox(txt, (x,y, _grid.columns*1, _grid.rows*1), subdivisions=1, gutter=15, draw_grid=False)

                with bot.savedState():
                    self.text_attributes()
                    bot.fill(*self.instance_color)
                    bot.rotate(90, (x-8, y))
                    bot.text(str(trk_val), (x, y))

            txt = ""
        else:
            if multi_size_page:
                for il, size in enumerate(font_size):
                    bot.font(
                        font_path,
                        size
                    )
                    grid.columnTextBox(txt, (_grid.columns[il], _grid.bottom, _grid.columns*1, _grid.rows * 1), subdivisions=1, gutter=15, draw_grid=False)
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


    def find_close(self, root_dir:str, target_filename:str) -> str:
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


    def get_variable_fonts_from_op(self, designspace:dsp_doc) -> list[ProofFont]:
        var = designspace.variableFonts
        di,fi = os.path.split(os.path.abspath(designspace.path))
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
                            print(f"""ERROR: {file_name} does not exist on disk, cannot load font""")
                            continue
                else:
                    if name:
                        pp = os.path.join(di,"variable_ttf",f"{name}.ttf")
                        if os.path.exists(pp):
                            p = pp
                        else:
                            p = self.find_close(di,f"{name}.ttf")
                if p:
                    te = ProofFont(p)
                    te.is_variable = True
                    te.operator = designspace
                    te.build_locations(should_sort=self.sort)
                    allVFs.append(te)
                else:
                    print(f"""ERROR: cannot find VF for {name}""")
        return allVFs


    def add_object(self, path:str, should_sort:bool=True):
        """Summary
        Args:
            path (str): Path to an OpenType font or designspace
            should_sort (bool, optional): Should sort designspace locations on load
        """
        self.sort = should_sort

        suffixes = ".ttf .otf .woff .woff2"
        suff = os.path.splitext(path)[-1]
        if suff in suffixes.split(" "):
            o = ProofFont(path)
            self.fonts.append(o)
        elif suff == ".designspace":
            operator = dsp_doc.fromfile(path)
            vfs = self.get_variable_fonts_from_op(operator)
            self.fonts.extend(vfs)
        if path not in self.objects:
            self.objects.append(path)


    #convience function to add multiple paths at once
    def add_objects(self, paths:list[str]):
        for path in paths:
            self.add_object(path)


    def _reformat_limits(self, zone_limits:str) -> dict:
        '''
        use fontTools.varLib model for extracting the CLI data into a dictionary item
        taken from the source code ^
        '''
        result = {}
        if zone_limits:
            for limitString in zone_limits.split(" "):
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


    def crop_space(self, _zone:str):
        zone = self._reformat_limits(_zone)
        valid = False

        if self.objects == []:
            pass
        else:
            if zone:
                for font in self.fonts:
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


    def move_to_storage(self, proof_type:str, locals:dict):
        self._counter += 1
        self.storage.append((proof_type,locals))

    def empty_storage(self):
        self._counter = 0
        self.storage = []

    def setup(self, cover_page:bool=True):
        # self.move_to_storage("cover",locals()) # i think we can turn this off for now
        bot.newDrawing()
        if cover_page:
            self._cover_page(self.fonts)

    def text_attributes(self):
        bot.fill(0)
        bot.stroke(None)
        bot.font(self.caption_font, 8)
        bot.fontVariations(None)

    def _cover_page(self, fonts:list[ProofFont]):
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
                        if loc.is_source:
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
        height_ratio = box_h/(FONT_SIZE_DEFAULT * (mu+1) * 1.5)

        sf = min([width_ratio , height_ratio])

        with bot.savedState():
            bot.scale(sf)
            bot.textBox(fs, (box_x/sf, box_y/sf, box_w/sf, box_h/sf))


    @contextmanager
    def grouping(self, group_type="font"):
        self._group_count += 1
        self.in_group = str(uuid.uuid4())
        try:
            yield
        finally:
            self.in_group = 0


if __name__ == "__main__":



    doc = ProofDocument()

    doc.add_object(CurrentDesignspace().path)
    #doc.crop_space("slnt=0")

    doc.size = "LetterLandscape"
    doc.caption_font = "CoreMono-Regular"
    doc.margin = "auto"
    doc.use_instances = False

    doc.setup()
    doc.new_section("core")

    with doc.grouping() as group:
        doc.new_section("paragraph", point_size=[12,20], multi_size_page=True)
        doc.new_section("paragraph", point_size=[24], multi_size_page=False)
        doc.new_section("figures", point_size=[36])



    doc.new_section(
                    "paragraph",
                    point_size=20,
                   )

    doc.use_instances = True

    doc.new_section("gradient")
    #doc.new_section("features")

    doc.save(open=True)
