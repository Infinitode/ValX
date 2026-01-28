import os
import re

# New version, that includes AI detection
import pickle
from sklearn import __version__ as sklearnversion
from sklearn.tree import DecisionTreeClassifier  # Import the DecisionTreeClassifier class
from sklearn.feature_extraction.text import CountVectorizer  # Import the CountVectorizer class

'''
ValX uses data from this GitHub repository:
https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/
© 2012-2020 Shutterstock, Inc.

Creative Commons Attribution 4.0 International License:
https://github.com/LDNOOBW/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words/blob/master/LICENSE
'''

def load_profanity_words(language='English', custom_words_list: list[str] = None):
    """
    Load profanity words for the specified language, optionally including a custom list.

    Args:
        language (str, optional): The language for which to load profanity words.
                                  Defaults to 'English'. Can be None to use only custom_words_list.
        custom_words_list (list[str], optional): A list of custom profanity words. Defaults to None.

    Returns:
        list: A list of profanity words.

    Raises:
        ValueError: If language is None and custom_words_list is None or empty.
    """
    # Profanity words as a string
    PROFANITY_WORDS = """
    $Arabic|AR$
    سكس
    طيز
    شرج
    لعق
    لحس
    مص
    تمص
    بيضان
    ثدي
    بز
    بزاز
    حلمة
    مفلقسة
    بظر
    كس
    فرج
    شهوة
    شاذ
    مبادل
    عاهرة
    جماع
    قضيب
    زب
    لوطي
    لواط
    سحاق
    سحاقية
    اغتصاب
    خنثي
    احتلام
    نيك
    متناك
    متناكة
    شرموطة
    عرص
    خول
    قحبة
    لبوة
    $Czech|CS$
    bordel
    buzna
    čumět
    čurák
    debil
    do piče
    do prdele
    dršťka
    držka
    flundra
    hajzl
    hovno
    chcanky
    chuj
    jebat
    kokot
    kokotina
    koňomrd
    kunda
    kurva
    mamrd
    mrdat
    mrdka
    mrdník
    oslošoust
    piča
    píčus
    píchat
    pizda
    prcat
    prdel
    prdelka
    sračka
    srát
    šoustat
    šulin
    vypíčenec
    zkurvit
    zkurvysyn
    zmrd
    žrát
    $Danish|DA$
    anus
    bøsserøv
    cock
    fisse
    fissehår
    fuck
    hestepik
    kussekryller
    lort
    luder
    pik
    pikhår
    pikslugeri
    piksutteri
    pis
    røv
    røvhul
    røvskæg
    røvspræke
    shit
    $German|DE$
    analritter
    arsch
    arschficker
    arschlecker
    arschloch
    bimbo
    bratze
    bumsen
    bonze
    dödel
    fick
    ficken
    flittchen
    fotze
    fratze
    hackfresse
    hure
    hurensohn
    ische
    kackbratze
    kacke
    kacken
    kackwurst
    kampflesbe
    kanake
    kimme
    lümmel
    MILF
    möpse
    morgenlatte
    möse
    mufti
    muschi
    nackt
    neger
    nigger
    nippel
    nutte
    onanieren
    orgasmus
    penis
    pimmel
    pimpern
    pinkeln
    pissen
    pisser
    popel
    poppen
    porno
    reudig
    rosette
    schabracke
    schlampe
    scheiße
    scheisser
    schiesser
    schnackeln
    schwanzlutscher
    schwuchtel
    tittchen
    titten
    vögeln
    vollpfosten
    wichse
    wichsen
    wichser
    $Hindi|HI$
    aand
    aandu
    balatkar
    balatkari
    behen chod
    beti chod
    bhadva
    bhadve
    bhandve
    bhangi
    bhootni ke
    bhosad
    bhosadi ke
    boobe
    chakke
    chinaal
    chinki
    chod
    chodu
    chodu bhagat
    chooche
    choochi
    choope
    choot
    choot ke baal
    chootia
    chootiya
    chuche
    chuchi
    chudaap
    chudai khanaa
    chudam chudai
    chude
    chut
    chut ka chuha
    chut ka churan
    chut ka mail
    chut ke baal
    chut ke dhakkan
    chut maarli
    chutad
    chutadd
    chutan
    chutia
    chutiya
    gaand
    gaandfat
    gaandmasti
    gaandufad
    gandfattu
    gandu
    gashti
    gasti
    ghassa
    ghasti
    gucchi
    gucchu
    harami
    haramzade
    hawas
    hawas ke pujari
    hijda
    hijra
    jhant
    jhant chaatu
    jhant ka keeda
    jhant ke baal
    jhant ke pissu
    jhantu
    kamine
    kaminey
    kanjar
    kutta
    kutta kamina
    kutte ki aulad
    kutte ki jat
    kuttiya
    loda
    lodu
    lund
    lund choos
    lund ka bakkal
    lund khajoor
    lundtopi
    lundure
    maa ki chut
    maal
    madar chod
    madarchod
    madhavchod
    mooh mein le
    mutth
    mutthal
    najayaz
    najayaz aulaad
    najayaz paidaish
    paki
    pataka
    patakha
    raand
    randaap
    randi
    randi rona
    saala
    saala kutta
    saali kutti
    saali randi
    suar
    suar ke lund
    suar ki aulad
    tatte
    tatti
    teri maa ka bhosada
    teri maa ka boba chusu
    teri maa ki behenchod 
    teri maa ki chut
    tharak
    tharki
    tu chuda
    $English|EN$
    2g1c
    2 girls 1 cup
    acrotomophilia
    alabama hot pocket
    alaskan pipeline
    anal
    anilingus
    anus
    apeshit
    arsehole
    ass
    asshole
    assmunch
    auto erotic
    autoerotic
    babeland
    baby batter
    baby juice
    ball gag
    ball gravy
    ball kicking
    ball licking
    ball sack
    ball sucking
    bangbros
    bangbus
    bareback
    barely legal
    barenaked
    bastard
    bastardo
    bastinado
    bbw
    bdsm
    beaner
    beaners
    beaver cleaver
    beaver lips
    beastiality
    bestiality
    big black
    big breasts
    big knockers
    big tits
    bimbos
    birdlock
    bitch
    bitches
    black cock
    blonde action
    blonde on blonde action
    blowjob
    blow job
    blow your load
    blue waffle
    blumpkin
    bollocks
    bondage
    boner
    boob
    boobs
    booty call
    brown showers
    brunette action
    bukkake
    bulldyke
    bullet vibe
    bullshit
    bung hole
    bunghole
    busty
    butt
    buttcheeks
    butthole
    camel toe
    camgirl
    camslut
    camwhore
    carpet muncher
    carpetmuncher
    chocolate rosebuds
    cialis
    circlejerk
    cleveland steamer
    clit
    clitoris
    clover clamps
    clusterfuck
    cock
    cocks
    coprolagnia
    coprophilia
    cornhole
    coon
    coons
    creampie
    cum
    cumming
    cumshot
    cumshots
    cunnilingus
    cunt
    darkie
    date rape
    daterape
    deep throat
    deepthroat
    dendrophilia
    dick
    dildo
    dingleberry
    dingleberries
    dirty pillows
    dirty sanchez
    doggie style
    doggiestyle
    doggy style
    doggystyle
    dog style
    dolcett
    domination
    dominatrix
    dommes
    donkey punch
    double dong
    double penetration
    dp action
    dry hump
    dvda
    eat my ass
    ecchi
    ejaculation
    erotic
    erotism
    escort
    eunuch
    fag
    faggot
    fecal
    felch
    fellatio
    feltch
    female squirting
    femdom
    figging
    fingerbang
    fingering
    fisting
    foot fetish
    footjob
    frotting
    fuck
    fuck buttons
    fuckin
    fucking
    fucktards
    fudge packer
    fudgepacker
    futanari
    gangbang
    gang bang
    gay sex
    genitals
    giant cock
    girl on
    girl on top
    girls gone wild
    goatcx
    goatse
    god damn
    gokkun
    golden shower
    goodpoop
    goo girl
    goregasm
    grope
    group sex
    g-spot
    guro
    hand job
    handjob
    hard core
    hardcore
    hentai
    homoerotic
    honkey
    hooker
    horny
    hot carl
    hot chick
    how to kill
    how to murder
    huge fat
    humping
    incest
    intercourse
    jack off
    jail bait
    jailbait
    jelly donut
    jerk off
    jigaboo
    jiggaboo
    jiggerboo
    jizz
    juggs
    kike
    kinbaku
    kinkster
    kinky
    knobbing
    leather restraint
    leather straight jacket
    lemon party
    livesex
    lolita
    lovemaking
    make me come
    male squirting
    masturbate
    masturbating
    masturbation
    menage a trois
    milf
    missionary position
    mong
    motherfucker
    mound of venus
    mr hands
    muff diver
    muffdiving
    nambla
    nawashi
    negro
    neonazi
    nigga
    nigger
    nig nog
    nimphomania
    nipple
    nipples
    nsfw
    nsfw images
    nude
    nudity
    nutten
    nympho
    nymphomania
    octopussy
    omorashi
    one cup two girls
    one guy one jar
    orgasm
    orgy
    paedophile
    paki
    panties
    panty
    pedobear
    pedophile
    pegging
    penis
    phone sex
    piece of shit
    pikey
    pissing
    piss pig
    pisspig
    playboy
    pleasure chest
    pole smoker
    ponyplay
    poof
    poon
    poontang
    punany
    poop chute
    poopchute
    porn
    porno
    pornography
    prince albert piercing
    pthc
    pubes
    pussy
    queaf
    queef
    quim
    raghead
    raging boner
    rape
    raping
    rapist
    rectum
    reverse cowgirl
    rimjob
    rimming
    rosy palm
    rosy palm and her 5 sisters
    rusty trombone
    sadism
    santorum
    scat
    schlong
    scissoring
    semen
    sex
    sexcam
    sexo
    sexy
    sexual
    sexually
    sexuality
    shaved beaver
    shaved pussy
    shemale
    shibari
    shit
    shitblimp
    shitty
    shota
    shrimping
    skeet
    slanteye
    slut
    s&m
    smut
    snatch
    snowballing
    sodomize
    sodomy
    spastic
    spic
    splooge
    splooge moose
    spooge
    spread legs
    spunk
    strap on
    strapon
    strappado
    strip club
    style doggy
    suck
    sucks
    suicide girls
    sultry women
    swastika
    swinger
    tainted love
    taste my
    tea bagging
    threesome
    throating
    thumbzilla
    tied up
    tight white
    tit
    tits
    titties
    titty
    tongue in a
    topless
    tosser
    towelhead
    tranny
    tribadism
    tub girl
    tubgirl
    tushy
    twat
    twink
    twinkie
    two girls one cup
    undressing
    upskirt
    urethra play
    urophilia
    vagina
    venus mound
    viagra
    vibrator
    violet wand
    vorarephilia
    voyeur
    voyeurweb
    voyuer
    vulva
    wank
    wetback
    wet dream
    white power
    whore
    worldsex
    wrapping men
    wrinkled starfish
    xx
    xxx
    yaoi
    yellow showers
    yiffy
    zoophilia
    🖕
    $Esperanto|EO$
    bugren
    bugri
    bugru
    ĉiesulino
    ĉiesulo
    diofek
    diofeka
    fek
    feken
    fekfikanto
    feklekulo
    fekulo
    fik
    fikado
    fikema
    fikfek
    fiki
    fikiĝi
    fikiĝu
    fikilo
    fikklaŭno
    fikota
    fiku
    forfiki
    forfikiĝu
    forfiku
    forfurzu
    forpisi
    forpisu
    furzulo
    kacen
    kaco
    kacsuĉulo
    kojono
    piĉen
    piĉo
    zamenfek
    $Persian|FA$
    آب کیر
    ارگاسم
    برهنه
    پورن
    پورنو
    تجاوز
    تخمی
    جق
    جقی
    جلق
    جنده
    چوچول
    حشر
    حشری
    داف
    دودول
    ساک زدن
    سکس
    سکس کردن
    سکسی
    سوپر
    شق کردن
    شهوت
    شهوتی
    شونبول
    فیلم سوپر
    کس
    کس دادن
    کس کردن
    کسکش
    کوس
    کون
    کون دادن
    کون کردن
    کونکش
    کونی
    کیر
    کیری
    لاپا
    لاپایی
    لاشی
    لخت
    لش
    منی
    هرزه
    $Finnish$
    alfred nussi
    bylsiä
    haahka
    haista paska
    haista vittu
    hatullinen
    helvetisti
    hevonkuusi
    hevonpaska
    hevonperse
    hevonvittu
    hevonvitunperse
    hitosti
    hitto
    huorata
    hässiä
    juosten kustu
    jutku
    jutsku
    jätkä
    kananpaska
    koiranpaska
    kuin esterin perseestä
    kulli
    kullinluikaus
    kuppainen
    kusaista
    kuseksia
    kusettaa
    kusi
    kusipää
    kusta
    kyrpiintynyt
    kyrpiintyä
    kyrpiä
    kyrpä
    kyrpänaama
    kyrvitys
    lahtari
    lutka
    molo
    molopää
    mulkero
    mulkku
    mulkvisti
    muna
    munapää
    munaton
    mutakuono
    mutiainen
    naida
    nainti
    narttu
    neekeri
    nekru
    nuolla persettä
    nussia
    nussija
    nussinta
    paljaalla
    palli
    pallit
    paneskella
    panettaa
    panna
    pano
    pantava
    paska
    paskainen
    paskamainen
    paskanmarjat
    paskantaa
    paskapuhe
    paskapää
    paskattaa
    paskiainen
    paskoa
    pehko
    pentele
    perkele
    perkeleesti
    persaukinen
    perse
    perseennuolija
    perseet olalla
    persereikä
    perseääliö
    persläpi
    perspano
    persvako
    pilkunnussija
    pillu
    pillut
    pipari
    piru
    pistää
    pyllyvako
    reikä
    reva
    ripsipiirakka
    runkata
    runkkari
    runkkaus
    runkku
    ryssä
    rättipää
    saatanasti
    suklaaosasto
    tavara
    toosa
    tuhkaluukku
    tumputtaa
    turpasauna
    tussu
    tussukka
    tussut
    vakipano
    vetää käteen
    viiksi
    vittu
    vittuilla
    vittuilu
    vittumainen
    vittuuntua
    vittuuntunut
    vitun
    vitusti
    vituttaa
    vitutus
    äpärä
    $Filipino|FIL$
    puta ka
    putang ina
    tang ina
    tangina
    burat
    bayag
    bobo
    nognog
    tanga
    ulol
    kantot
    anak ka ng puta
    ulol
    jakol
    $French|FR$
    baiser
    bander
    bigornette
    bite
    bitte
    bloblos
    bordel
    bourré
    bourrée
    brackmard
    branlage
    branler
    branlette
    branleur
    branleuse
    brouter le cresson
    caca
    chatte
    chiasse
    chier
    chiottes
    clito
    clitoris
    con
    connard
    connasse
    conne
    couilles
    cramouille
    cul
    déconne
    déconner
    emmerdant
    emmerder
    emmerdeur
    emmerdeuse
    enculé
    enculée
    enculeur
    enculeurs
    enfoiré
    enfoirée
    étron
    fille de pute
    fils de pute
    folle
    foutre
    gerbe
    gerber
    gouine
    grande folle
    grogniasse
    gueule
    jouir
    la putain de ta mère
    MALPT
    ménage à trois
    merde
    merdeuse
    merdeux
    meuf
    nègre
    negro
    nique ta mère
    nique ta race
    palucher
    pédale
    pédé
    péter
    pipi
    pisser
    pouffiasse
    pousse-crotte
    putain
    pute
    ramoner
    sac à foutre
    sac à merde
    salaud
    salope
    suce
    tapette
    tanche
    teuch
    tringler
    trique
    troncher
    trou du cul
    turlute
    zigounette
    zizi
    $French (CA)|FR-CA-U-SD-CAQC$
    noune
    osti
    criss
    crisse
    calice
    tabarnak
    viarge
    $Hungarian|HU$
    balfasz
    balfaszok
    balfaszokat
    balfaszt
    barmok
    barmokat
    barmot
    barom
    baszik
    bazmeg
    buksza
    bukszák
    bukszákat
    bukszát
    búr
    búrok
    csöcs
    csöcsök
    csöcsöket
    csöcsöt
    fasz
    faszfej
    faszfejek
    faszfejeket
    faszfejet
    faszok
    faszokat
    faszt
    fing
    fingok
    fingokat
    fingot
    franc
    francok
    francokat
    francot
    geci
    gecibb
    gecik
    geciket
    gecit
    kibaszott
    kibaszottabb
    kúr
    kurafi
    kurafik
    kurafikat
    kurafit
    kurva
    kurvák
    kurvákat
    kurvát
    leggecibb
    legkibaszottabb
    legszarabb
    marha
    marhák
    marhákat
    marhát
    megdöglik
    pele
    pelék
    picsa
    picsákat
    picsát
    pina
    pinák
    pinákat
    pinát
    pofa
    pofákat
    pofát
    pöcs
    pöcsök
    pöcsöket
    pöcsöt
    punci
    puncik
    segg
    seggek
    seggeket
    segget
    seggfej
    seggfejek
    seggfejeket
    seggfejet
    szajha
    szajhák
    szajhákat
    szajhát
    szar
    szarabb
    szarik
    szarok
    szarokat
    szart
    $Italian|IT$
    allupato
    ammucchiata
    anale
    arrapato
    arrusa
    arruso
    assatanato
    bagascia
    bagassa
    bagnarsi
    baldracca
    balle
    battere
    battona
    belino
    biga
    bocchinara
    bocchino
    bofilo
    boiata
    bordello
    brinca
    bucaiolo
    budiùlo
    busone
    cacca
    caciocappella
    cadavere
    cagare
    cagata
    cagna
    casci
    cazzata
    cazzimma
    cazzo
    cesso
    cazzone
    checca
    chiappa
    chiavare
    chiavata
    ciospo
    ciucciami il cazzo
    coglione
    coglioni
    cornuto
    cozza
    culattina
    culattone
    culo
    ditalino
    fava
    femminuccia
    fica
    figa
    figlio di buona donna
    figlio di puttana
    figone
    finocchio
    fottere
    fottersi
    fracicone
    fregna
    frocio
    froscio
    goldone
    guardone
    imbecille
    incazzarsi
    incoglionirsi
    ingoio
    leccaculo
    lecchino
    lofare
    loffa
    loffare
    mannaggia
    merda
    merdata
    merdoso
    mignotta
    minchia
    minchione
    mona
    monta
    montare
    mussa
    nave scuola
    nerchia
    padulo
    palle
    palloso
    patacca
    patonza
    pecorina
    pesce
    picio
    pincare
    pippa
    pinnolone
    pipì
    pippone
    pirla
    pisciare
    piscio
    pisello
    pistolotto
    pomiciare
    pompa
    pompino
    porca
    porca madonna
    porca miseria
    porca puttana
    porco
    porco due
    porco zio
    potta
    puppami
    puttana
    quaglia
    recchione
    regina
    rincoglionire
    rizzarsi
    rompiballe
    rompipalle
    ruffiano
    sbattere
    sbattersi
    sborra
    sborrata
    sborrone
    sbrodolata
    scopare
    scopata
    scorreggiare
    sega
    slinguare
    slinguata
    smandrappata
    soccia
    socmel
    sorca
    spagnola
    spompinare
    sticchio
    stronza
    stronzata
    stronzo
    succhiami
    succhione
    sveltina
    sverginare
    tarzanello
    terrone
    testa di cazzo
    tette
    tirare
    topa
    troia
    trombare
    vacca
    vaffanculo
    vangare
    zinne
    zio cantante
    zoccola
    $Japanese|JA$
    3p
    g スポット
    s ＆ m
    sm
    sm女王
    xx
    アジアのかわいい女の子
    アスホール
    アナリングス
    アナル
    いたずら
    イラマチオ
    エクスタシー
    エスコート
    エッチ
    エロティズム
    エロティック
    オーガズム
    オカマ
    おしっこ
    おしり
    オシリ
    おしりのあな
    おっぱい
    オッパイ
    オナニー
    オマンコ
    おもらし
    お尻
    カーマスートラ
    カント
    クリトリス
    グループ・セックス
    グロ
    クンニリングス
    ゲイ・セックス
    ゲイボーイ
    ゴールデンシャワー
    コカイン
    ゴックン
    サディズム
    しばり
    スウィンガー
    スカートの中
    スカトロ
    ストラップオン
    ストリップ劇場
    スラット
    スリット
    セクシーな
    セクシーな 10 代
    セックス
    ソドミー
    ちんこ
    ディープ・スロート
    ディック
    ディルド
    デートレイプ
    デブ
    テレフォンセックス
    ドッグスタイル
    トップレス
    なめ
    ニガー
    ヌード
    ネオ・ナチ
    ハードコア
    パイパン
    バイブレーター
    バック・スタイル
    パンティー
    ビッチ
    ファック
    ファンタジー
    フィスト
    フェティッシュ
    フェラチオ
    ふたなり
    ぶっかけ
    フック
    プリンス アルバート ピアス
    プレイボーイ
    ベアバック
    ペニス
    ペニスバンド
    ボーイズラブ
    ボールギャグ
    ぽっちゃり
    ホモ
    ポルノ
    ポルノグラフィー
    ボンテージ
    マザー・ファッカー
    マスターベーション
    まんこ
    やおい
    やりまん
    ラティーナ
    ラバー
    ランジェリー
    レイプ
    レズビアン
    ローター
    ロリータ
    淫乱
    陰毛
    革抑制
    騎上位
    巨根
    巨乳
    強姦犯
    玉なめ
    玉舐め
    緊縛
    近親相姦
    嫌い
    後背位
    合意の性交
    拷問
    殺し方
    殺人事件
    殺人方法
    支配
    児童性虐待
    自己愛性
    射精
    手コキ
    獣姦
    女の子
    女王様
    女子高生
    女装
    新しいポルノ
    人妻
    人種
    性交
    正常位
    生殖器
    精液
    挿入
    足フェチ
    足を広げる
    大陰唇
    脱衣
    茶色のシャワー
    中出し
    潮吹き女
    潮吹き男性
    直腸
    剃毛
    貞操帯
    奴隷
    二穴
    乳首
    尿道プレイ
    覗き
    売春婦
    縛り
    噴出
    糞
    糞尿愛好症
    糞便
    平手打ち
    変態
    勃起する
    夢精
    毛深い
    誘惑
    幼児性愛者
    裸
    裸の女性
    乱交
    両性
    両性具有
    両刀
    輪姦
    卍
    宦官
    肛門
    膣
    $Kabyle|KAB$
    abbuc
    aεeṭṭuḍ
    aḥeččun
    taḥeččunt
    axuzziḍ
    asxuẓeḍ
    qqu
    qquɣ
    qqiɣ
    qqan
    qqant
    tteqqun
    tteqqunt
    tteqqun
    aqerqur
    ajeḥniḍ
    awellaq
    iwellaqen
    iḥeččan
    iḥeččunen
    uqan
    taxna
    $Korean|KO$
    강간
    개새끼
    개자식
    개좆
    개차반
    거유
    계집년
    고자
    근친
    노모
    니기미
    뒤질래
    딸딸이
    때씹
    또라이
    뙤놈
    로리타
    망가
    몰카
    미친
    미친새끼
    바바리맨
    변태
    병신
    보지
    불알
    빠구리
    사까시
    섹스
    스와핑
    쌍놈
    씨발
    씨발놈
    씨팔
    씹
    씹물
    씹빨
    씹새끼
    씹알
    씹창
    씹팔
    암캐
    애자
    야동
    야사
    야애니
    엄창
    에로
    염병
    옘병
    유모
    육갑
    은꼴
    자위
    자지
    잡년
    종간나
    좆
    좆만
    죽일년
    쥐좆
    직촬
    짱깨
    쪽바리
    창녀
    포르노
    하드코어
    호로
    화냥년
    후레아들
    후장
    희쭈그리
    $Dutch|NL$
    aardappels afgieten
    achter het raam zitten
    afberen
    aflebberen
    afrossen
    afrukken
    aftrekken
    afwerkplaats
    afzeiken
    afzuigen
    een halve man en een paardekop
    anita
    asbak
    aso
    bagger schijten
    balen
    bedonderen
    befborstel
    beffen
    bekken
    belazeren
    besodemieterd zijn
    besodemieteren
    beurt
    boemelen
    boerelul
    boerenpummel
    bokkelul
    botergeil
    broekhoesten
    brugpieper
    buffelen
    buiten de pot piesen
    da's kloten van de bok
    de ballen
    de hoer spelen
    de hond uitlaten
    de koffer induiken
    del
    de pijp uitgaan
    dombo
    draaikont
    driehoog achter wonen
    drol
    drooggeiler
    droogkloot
    een beurt geven
    een nummertje maken
    een wip maken
    eikel
    engerd
    flamoes
    flikken
    flikker
    gadverdamme
    galbak
    gat
    gedoogzone
    geilneef
    gesodemieter
    godverdomme
    graftak
    gras maaien
    gratenkut
    greppeldel
    griet
    hoempert
    hoer
    hoerenbuurt
    hoerenloper
    hoerig
    hol
    hufter
    huisdealer
    johny
    kanen
    kettingzeug
    klaarkomen
    klerebeer
    klojo
    klooien
    klootjesvolk
    klootoog
    klootzak
    kloten
    knor
    kont
    kontneuken
    krentekakker
    kut
    kuttelikkertje
    kwakkie
    liefdesgrot
    lul
    lul-de-behanger
    lulhannes
    lummel
    mafketel
    matennaaier
    matje
    mof
    muts
    naaien
    naakt
    neuken
    neukstier
    nicht
    oetlul
    opgeilen
    opkankeren
    oprotten
    opsodemieteren
    op z'n hondjes
    op z'n sodemieter geven
    opzouten
    ouwehoer
    ouwehoeren
    ouwe rukker
    paal
    paardelul
    palen
    penoze
    piesen
    pijpbekkieg
    pijpen
    pik
    pleurislaaier
    poep
    poepen
    poot
    portiekslet
    pot
    potverdorie
    publiciteitsgeil
    raaskallen
    reet
    reetridder
    reet trappen, voor zijn
    remsporen
    reutelen
    rothoer
    rotzak
    rukhond
    rukken
    schatje
    schijt
    schijten
    schoft
    schuinsmarcheerder
    shit
    slempen
    slet
    sletterig
    slik mijn zaad
    snol
    spuiten
    standje
    standje-69
    stoephoer
    stootje
    stront
    sufferd
    tapijtnek
    teef
    temeier
    teringlijer
    toeter
    tongzoeng
    triootjeg
    trottoir prostituée
    trottoirteef
    vergallen
    verkloten
    verneuken
    viespeuk
    vingeren
    vleesroos
    voor jan lul
    voor jan-met-de-korte-achternaam
    watje
    welzijnsmafia
    wijf
    wippen
    wuftje
    zaadje
    zakkenwasser
    zeiken
    zeiker
    zuigen
    zuiplap
    $Norwegian|NO$
    asshole
    dritt
    drittsekk
    faen
    faen i helvete
    fan
    fanken
    fitte
    forbanna
    forbannet
    forjævlig
    fuck
    fy faen
    føkk
    føkka
    føkkings
    jævla
    jævlig
    helvete
    helvetet
    kuk
    kukene
    kuker
    morraknuller
    morrapuler
    nigger
    pakkis
    pikk
    pokker
    ræva
    ræven
    satan
    shit
    sinnsykt
    skitt
    sotrør
    ståpikk
    ståpikkene
    ståpikker
    svartheiteste
    $Polish|PL$
    burdel
    burdelmama
    chuj
    chujnia
    ciota
    cipa
    cyc
    debil
    dmuchać
    do kurwy nędzy
    dupa
    dupek
    duperele
    dziwka
    fiut
    gówno
    gówno prawda
    huj
    huj ci w dupę
    jajco
    jajko
    ja pierdolę
    jebać
    jebany
    kurwa
    kurwy
    kutafon
    kutas
    lizać pałę
    obciągać chuja
    obciągać fiuta
    obciągać loda
    pieprzyć
    pierdolec
    pierdolić
    pierdolnąć
    pierdolnięty
    pierdoła
    pierdzieć
    pizda
    pojeb
    pojebany
    popierdolony
    robic loda
    robić loda
    ruchać
    rzygać
    skurwysyn
    sraczka
    srać
    suka
    syf
    wkurwiać
    zajebisty
    $Portuguese|PT$
    aborto
    amador
    ânus
    aranha
    ariano
    balalao
    bastardo
    bicha
    biscate
    bissexual
    boceta
    boob
    bosta
    braulio de borracha
    bumbum
    burro
    cabrao
    cacete
    cagar
    camisinha
    caralho
    cerveja
    chochota
    chupar
    clitoris
    cocaína
    coito
    colhoes
    comer
    cona
    consolo
    corno
    cu
    dar o rabo
    dum raio
    esporra
    fecal
    filho da puta
    foda
    foda-se
    foder
    frango assado
    gozar
    grelho
    heroína
    heterosexual
    homem gay
    homoerótico
    homosexual
    inferno
    lésbica
    lolita
    mama
    merda
    paneleiro
    passar um cheque
    pau
    peidar
    pênis
    pinto
    porra
    puta
    puta que pariu
    puta que te pariu
    queca
    sacanagem
    saco
    torneira
    transar
    vadia
    vai-te foder
    vai tomar no cu
    veado
    vibrador
    xana
    xochota
    $Russian|RU$
    bychara
    byk
    chernozhopyi
    dolboy'eb
    ebalnik
    ebalo
    ebalom sch'elkat
    gol
    mudack
    opizdenet
    osto'eblo
    ostokhuitel'no
    ot'ebis
    otmudohat
    otpizdit
    otsosi
    padlo
    pedik
    perdet
    petuh
    pidar gnoinyj
    pizda
    pizdato
    pizdatyi
    piz'det
    pizdetc
    pizdoi nakryt'sja
    pizd'uk
    piz`dyulina
    podi ku'evo
    poeben
    po'imat' na konchik
    po'iti posrat
    po khuy
    poluchit pizdy
    pososi moyu konfetku
    prissat
    proebat
    promudobl'adsksya pizdopro'ebina
    propezdoloch
    prosrat
    raspeezdeyi
    raspizdatyi
    raz'yebuy
    raz'yoba
    s'ebat'sya
    shalava
    styervo
    sukin syn
    svodit posrat
    svoloch
    trakhat'sya
    trimandoblydskiy pizdoproyob
    ubl'yudok
    uboy
    u'ebitsche
    vafl'a
    vafli lovit
    v pizdu
    vyperdysh
    vzdrochennyi
    yeb vas
    za'ebat
    zaebis
    zalupa
    zalupat
    zasranetc
    zassat
    zlo'ebuchy
    бздёнок
    блядки
    блядовать
    блядство
    блядь
    бугор
    во пизду
    встать раком
    выёбываться
    гандон
    говно
    говнюк
    голый
    дать пизды
    дерьмо
    дрочить
    другой дразнится
    ёбарь
    ебать
    ебать-копать
    ебло
    ебнуть
    ёб твою мать
    жопа
    жополиз
    играть на кожаной флейте
    измудохать
    каждый дрочит как он хочет
    какая разница
    как два пальца обоссать
    курите мою трубку
    лысого в кулаке гонять
    малофья
    манда
    мандавошка
    мент
    муда
    мудило
    мудозвон
    наебать
    наебениться
    наебнуться
    на фиг
    на хуй
    на хую вертеть
    на хуя
    нахуячиться
    невебенный
    не ебет
    ни за хуй собачу
    ни хуя
    обнаженный
    обоссаться можно
    один ебётся
    опесдол
    офигеть
    охуеть
    охуительно
    половое сношение
    секс
    сиськи
    спиздить
    срать
    ссать
    траxать
    ты мне ваньку не валяй
    фига
    хапать
    хер с ней
    хер с ним
    хохол
    хрен
    хуёво
    хуёвый
    хуем груши околачивать
    хуеплет
    хуило
    хуиней страдать
    хуиня
    хуй
    хуйнуть
    хуй пинать
    $Spanish|ES$
    Asesinato
    asno
    bastardo
    Bollera
    Cabrón
    Caca
    Chupada
    Chupapollas
    Chupetón
    concha
    Concha de tu madre
    Coño
    Coprofagía
    Culo
    Drogas
    Esperma
    Fiesta de salchichas
    Follador
    Follar
    Gilipichis
    Gilipollas
    Hacer una paja
    Haciendo el amor
    Heroína
    Hija de puta
    Hijaputa
    Hijo de puta
    Hijoputa
    Idiota
    Imbécil
    infierno
    Jilipollas
    Kapullo
    Lameculos
    Maciza
    Macizorra
    maldito
    Mamada
    Marica
    Maricón
    Mariconazo
    martillo
    Mierda
    Nazi
    Orina
    Pedo
    Pendejo
    Pervertido
    Pezón
    Pinche
    Pis
    Prostituta
    Puta
    Racista
    Ramera
    Sádico
    Semen
    Sexo
    Sexo oral
    Soplagaitas
    Soplapollas
    Tetas grandes
    Tía buena
    Travesti
    Trio
    Verga
    vete a la mierda
    Vulva
    $Swedish|SV$
    arsle
    brutta
    discofitta
    dra åt helvete
    fan
    fitta
    fittig
    för helvete
    helvete
    hård
    jävlar
    knulla
    kuk
    kuksås
    kötthuvud
    köttnacke
    moona
    moonade
    moonar
    moonat
    mutta
    nigger
    neger
    olla
    pippa
    pitt
    prutt
    pök
    runka
    röv
    rövhål
    rövknulla
    satan
    skita
    skit ner dig
    skäggbiff
    snedfitta
    snefitta
    stake
    subba
    sås
    sätta på
    tusan
    $Thai|TH$
    กระดอ
    กระเด้า
    กระหรี่
    กะปิ
    กู
    ขี้
    ควย
    จิ๋ม
    จู๋
    เจ๊ก
    เจี๊ยว
    ดอกทอง
    ตอแหล
    ตูด
    น้ําแตก
    มึง
    แม่ง
    เย็ด
    รูตูด
    ล้างตู้เย็น
    ส้นตีน
    สัด
    เสือก
    หญิงชาติชั่ว
    หลั่ง
    ห่า
    หํา
    หี
    เหี้ย
    อมนกเขา
    ไอ้ควาย
    $Turkish|TR$
    am
    amcığa
    amcığı
    amcığın
    amcık
    amcıklar
    amcıklara
    amcıklarda
    amcıklardan
    amcıkları
    amcıkların
    amcıkta
    amcıktan
    amı
    amlar
    çingene
    Çingenede
    Çingeneden
    Çingeneler
    Çingenelerde
    Çingenelerden
    Çingenelere
    Çingeneleri
    Çingenelerin
    Çingenenin
    Çingeneye
    Çingeneyi
    göt
    göte
    götler
    götlerde
    götlerden
    götlere
    götleri
    götlerin
    götte
    götten
    götü
    götün
    götveren
    götverende
    götverenden
    götverene
    götvereni
    götverenin
    götverenler
    götverenlerde
    götverenlerden
    götverenlere
    götverenleri
    götverenlerin
    kaltağa
    kaltağı
    kaltağın
    kaltak
    kaltaklar
    kaltaklara
    kaltaklarda
    kaltaklardan
    kaltakları
    kaltakların
    kaltakta
    kaltaktan
    orospu
    orospuda
    orospudan
    orospular
    orospulara
    orospularda
    orospulardan
    orospuları
    orospuların
    orospunun
    orospuya
    orospuyu
    otuz birci
    otuz bircide
    otuz birciden
    otuz birciler
    otuz bircilerde
    otuz bircilerden
    otuz bircilere
    otuz bircileri
    otuz bircilerin
    otuz bircinin
    otuz birciye
    otuz birciyi
    saksocu
    saksocuda
    saksocudan
    saksocular
    saksoculara
    saksocularda
    saksoculardan
    saksocuları
    saksocuların
    saksocunun
    saksocuya
    saksocuyu
    sıçmak
    sik
    sike
    siker sikmez
    siki
    sikilir sikilmez
    sikin
    sikler
    siklerde
    siklerden
    siklere
    sikleri
    siklerin
    sikmek
    sikmemek
    sikte
    sikten
    siktir
    siktirir siktirmez
    taşağa
    taşağı
    taşağın
    taşak
    taşaklar
    taşaklara
    taşaklarda
    taşaklardan
    taşakları
    taşakların
    taşakta
    taşaktan
    yarağa
    yarağı
    yarağın
    yarak
    yaraklar
    yaraklara
    yaraklarda
    yaraklardan
    yarakları
    yarakların
    yarakta
    yaraktan
    $Klingon|TLH$
    ghuy'cha'
    QI'yaH
    Qu'vatlh
    $Chinese|ZH$
    13.
    13点
    三级片
    下三烂
    下贱
    个老子的
    九游
    乳
    乳交
    乳头
    乳房
    乳波臀浪
    交配
    仆街
    他奶奶
    他奶奶的
    他奶娘的
    他妈
    他妈ㄉ王八蛋
    他妈地
    他妈的
    他娘
    他马的
    你个傻比
    你他马的
    你全家
    你奶奶的
    你她马的
    你妈
    你妈的
    你娘
    你娘卡好
    你娘咧
    你它妈的
    你它马的
    你是鸡
    你是鸭
    你马的
    做爱
    傻比
    傻逼
    册那
    军妓
    几八
    几叭
    几巴
    几芭
    刚度
    刚瘪三
    包皮
    十三点
    卖B
    卖比
    卖淫
    卵
    卵子
    双峰微颤
    口交
    口肯
    叫床
    吃屎
    后庭
    吹箫
    塞你公
    塞你娘
    塞你母
    塞你爸
    塞你老师
    塞你老母
    处女
    外阴
    大卵子
    大卵泡
    大鸡巴
    奶
    奶奶的熊
    奶子
    奸
    奸你
    她妈地
    她妈的
    她马的
    妈B
    妈个B
    妈个比
    妈个老比
    妈妈的
    妈比
    妈的
    妈的B
    妈逼
    妓
    妓女
    妓院
    妳她妈的
    妳妈的
    妳娘的
    妳老母的
    妳马的
    姘头
    姣西
    姦
    娘个比
    娘的
    婊子
    婊子养的
    嫖娼
    嫖客
    它妈地
    它妈的
    密洞
    射你
    射精
    小乳头
    小卵子
    小卵泡
    小瘪三
    小肉粒
    小骚比
    小骚货
    小鸡巴
    小鸡鸡
    屁眼
    屁股
    屄
    屌
    巨乳
    干x娘
    干七八
    干你
    干你妈
    干你娘
    干你老母
    干你良
    干妳妈
    干妳娘
    干妳老母
    干妳马
    干您娘
    干机掰
    干死CS
    干死GM
    干死你
    干死客服
    幹
    强奸
    强奸你
    性
    性交
    性器
    性无能
    性爱
    情色
    想上你
    懆您妈
    懆您娘
    懒8
    懒八
    懒叫
    懒教
    成人
    我操你祖宗十八代
    扒光
    打炮
    打飞机
    抽插
    招妓
    插你
    插死你
    撒尿
    操你
    操你全家
    操你奶奶
    操你妈
    操你娘
    操你祖宗
    操你老妈
    操你老母
    操妳
    操妳全家
    操妳妈
    操妳娘
    操妳祖宗
    操机掰
    操比
    操逼
    放荡
    日他娘
    日你
    日你妈
    日你老娘
    日你老母
    日批
    月经
    机八
    机巴
    机机歪歪
    杂种
    浪叫
    淫
    淫乱
    淫妇
    淫棍
    淫水
    淫秽
    淫荡
    淫西
    湿透的内裤
    激情
    灨你娘
    烂货
    烂逼
    爛
    狗屁
    狗日
    狗狼养的
    玉杵
    王八蛋
    瓜娃子
    瓜婆娘
    瓜批
    瘪三
    白烂
    白痴
    白癡
    祖宗
    私服
    笨蛋
    精子
    老二
    老味
    老母
    老瘪三
    老骚比
    老骚货
    肉壁
    肉棍子
    肉棒
    肉缝
    肏
    肛交
    肥西
    色情
    花柳
    荡妇
    賤
    贝肉
    贱B
    贱人
    贱货
    贼你妈
    赛你老母
    赛妳阿母
    赣您娘
    轮奸
    迷药
    逼
    逼样
    野鸡
    阳具
    阳萎
    阴唇
    阴户
    阴核
    阴毛
    阴茎
    阴道
    阴部
    雞巴
    靠北
    靠母
    靠爸
    靠背
    靠腰
    驶你公
    驶你娘
    驶你母
    驶你爸
    驶你老师
    驶你老母
    骚比
    骚货
    骚逼
    鬼公
    鸡8
    鸡八
    鸡叭
    鸡吧
    鸡奸
    鸡巴
    鸡芭
    鸡鸡
    龟儿子
    龟头
    𨳒
    陰莖
    㞗
    尻
    𨳊
    鳩
    𡳞
    𨶙
    撚
    𨳍
    柒
    閪
    仆街
    咸家鏟
    冚家鏟
    咸家伶
    冚家拎
    笨實
    粉腸
    屎忽
    躝癱
    你老闆
    你老味
    你老母
    硬膠
    """

    profanity_lists = {}
    current_language = None
    current_words = []
    
    for line in PROFANITY_WORDS.split('\n'):
        line = line.strip()
        if line.startswith("$") and line.endswith("$"):
            if current_language:
                for lang in current_language.split('|'):
                    profanity_lists[lang.strip().lower()] = current_words
                current_words = []
            current_language = line.strip("$")
        elif line:
            current_words.append(line)

    if current_language:
        for lang in current_language.split('|'):
            profanity_lists[lang.strip().lower()] = current_words

    loaded_words = []
    if language is None:
        if not custom_words_list:
            raise ValueError("If language is None, custom_words_list must be provided and non-empty.")
        loaded_words = list(custom_words_list) # Use a copy
    elif language.lower() == "all":
        for words in profanity_lists.values():
            loaded_words.extend(words)
        if custom_words_list:
            loaded_words.extend(w for w in custom_words_list if w not in loaded_words)
    else:
        loaded_words = list(profanity_lists.get(language.lower(), [])) # Use a copy
        if custom_words_list:
            loaded_words.extend(w for w in custom_words_list if w not in loaded_words)

    return list(set(loaded_words)) # Return unique words


def load_custom_profanity_from_file(filepath: str) -> list[str]:
    """
    Loads a custom list of profanity words from a file.

    The file should contain one word per line. Lines starting with '#' will be ignored as comments.
    Empty lines or lines with only whitespace will also be ignored.

    Args:
        filepath (str): The path to the file containing custom profanity words.

    Returns:
        list[str]: A list of words loaded from the file.

    Raises:
        FileNotFoundError: If the specified filepath does not exist.
        IOError: For other file reading issues.
    """
    custom_words = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word and not word.startswith('#'):
                    custom_words.append(word)
    except FileNotFoundError:
        # Re-raise FileNotFoundError to be explicit, or handle as per specific project policy
        # For example, could log a warning and return empty list:
        # print(f"Warning: File not found at {filepath}. Returning empty custom word list.")
        # return []
        raise
    except IOError as e:
        # Handle other IO errors, perhaps log them or raise a more generic error
        # print(f"Warning: Error reading file {filepath}: {e}. Returning empty custom word list.")
        # return []
        raise IOError(f"Error reading custom profanity file {filepath}: {e}")
    return custom_words


def detect_profanity(text_data, language='English', custom_words_list: list[str] = None):
    """
    Detect profanity in text data using regex.

    Args:
        text_data (list): A list of strings representing the text data to analyze.
        language (str, optional): The language used to detect profanity. Defaults to 'English'.
                                  Can be None if custom_words_list is provided.
                                  Available languages include: All, Arabic, AR, Czech, CS, Danish, DA, German, DE,
                                  English, EN, Esperanto, EO, Persian, Finnish, FI, Filipino, FIL, French, FR,
                                  French (CA), FR-CA-U-SD-CAQC, Hindi, HI, Hungarian, HU, Italian, IT, Japanese, JA, Kabyle, KAB, 
                                  Korean, KO, Dutch, NL, Norwegian, NO, Polish, PL, Portuguese, PT, Russian, RU, Spanish, ES, 
                                  Swedish, SV, Thai, TH, Klingon, TLH, Turkish, TR, Chinese, ZH.
        custom_words_list (list[str], optional): A list of custom profanity words. Defaults to None.
    Returns:
        list: A list of dictionaries where each dictionary represents a detected instance of profanity.
            Each dictionary contains the following keys:
            - "Line" (int): The line number where the profanity was detected.
            - "Column" (int): The column number (position in the line) where the profanity starts.
            - "Word" (str): The detected profanity word.
            - "Language" (str): The language string indicating the source of the profanity list.
    """
    profanity_keywords = load_profanity_words(language, custom_words_list)
    detected = set()  # Use a set to store unique occurrences

    display_language = "Custom"
    if language:
        if custom_words_list:
            display_language = f"Custom + {language}"
        else:
            display_language = language
    elif not custom_words_list:
        # This case should ideally be prevented by load_profanity_words raising an error,
        # but as a fallback, if somehow load_profanity_words returns empty and language is None
        # and no custom_words_list, we avoid error here.
        return []


    for i, line in enumerate(text_data):
        # Skip lines with language markers (though less relevant if custom lists are primary)
        if line.startswith("$") and line.endswith("$"):
            continue

        # Detect profanity
        for profanity in profanity_keywords:
            matches = re.finditer(r'\b{}\b'.format(re.escape(profanity)), line, flags=re.IGNORECASE)
            for match in matches:
                # Store with display_language, not the input `language` parameter
                detected.add((i + 1, match.start() + 1, display_language, profanity))

    detections = []  # Initialize detections as a list

    if detected:
        for line_num, col_num, lang_display_name, word in detected:
            detection_info = {
                "Line": line_num,
                "Column": col_num,
                "Word": word,
                "Language": lang_display_name
            }
            detections.append(detection_info)

    return detections


def remove_profanity(text_data, output_file=None, language='English', custom_words_list: list[str] = None):
    """
    Remove profanity from text data.

    Args:
        text_data (list): A list of strings representing the text data to clean.
        output_file (str, optional): The file path to write the cleaned data. If None, cleaned data is not written to a file.
        language (str, optional): The language for which to remove profanity. Defaults to 'English'.
                                  Can be None if custom_words_list is provided.
        custom_words_list (list[str], optional): A list of custom profanity words. Defaults to None.

    Returns:
        list: A list of strings representing the cleaned text data.
    """
    profanity_keywords = load_profanity_words(language, custom_words_list)
    cleaned_data = []

    for line in text_data:
        # Skip lines with language markers
        if line.startswith("$") and line.endswith("$"):
            continue

        # Remove profanity
        cleaned_line = line
        for profanity in profanity_keywords:
            cleaned_line = re.sub(r'\b{}\b'.format(re.escape(profanity)), 'bad word', cleaned_line, flags=re.IGNORECASE)
        cleaned_data.append(cleaned_line)

    # Write cleaned data to output file if provided
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(cleaned_data))

    return cleaned_data

def detect_sensitive_information(text_data, info_type=["email", "phone", "credit_card", "ssn", "id", "address", "ip", "iban", "mrn", "icd10", "geo_coords", "username", "file_path", "bitcoin_wallet", "ethereum_wallet"]):
    """
    Detect sensitive information patterns in the provided text data.

    Args:
        text_data (list of str): A list of strings representing the text data to be analyzed.
        info_type (str or list of str, optional): One or more types of sensitive info to detect. Available types are: "email", "phone", "credit_card", "ssn", "id", "address", "ip", "iban", "mrn", "icd10", "geo_coords", "username", "file_path", "bitcoin_wallet", "ethereum_wallet". Uses all info types by default.

    Returns:
        list of tuple: A list of tuples containing detected sensitive information, each tuple
            representing (line number, column index, type, value).
    """
    if isinstance(info_type, str):
        info_type = [info_type]  # Convert single string to list for consistent handling

    # Dictionary to map info_type to regex patterns
    regex_patterns = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b(?:\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\d{3}[-.\s]??\d{4})\b',
        "credit_card": r'\b(?:\d[ -]*?){13,16}\b',
        "ssn": r'\b\d{3}[-]?\d{2}[-]?\d{4}\b',
        "id": r'\b[A-Za-z]{1,2}\d{6,9}\b',
        "address": r'\b\d+\s\w+\s\w+,\s\w+,\s\w+\b',
        "ip": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
        "iban": r'\b[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}\b',
        "mrn": r'\b\d{5,10}\b',
        "icd10": r'\b[A-TV-Z][0-9]{2}(?:\.[0-9A-TV-Z]{1,4})?\b',
        "geo_coords": r'\b[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)\b',
        "username": r'@\w+',
        "file_path": r'([A-Za-z]:\\|/)?([-\w\s]+\\|/)*[-\w\s]+\.\w+',
        "bitcoin_wallet": r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',
        "ethereum_wallet": r'\b0x[a-fA-F0-9]{40}\b'
    }

    sensitive_info = []
    
    # Loop through each line and check for sensitive info types based on specified `info_type`
    for i, line in enumerate(text_data):
        for type_ in info_type:
            pattern = regex_patterns.get(type_)
            if pattern:
                matches = re.finditer(pattern, line)
                for match in matches:
                    sensitive_info.append((i + 1, match.start(), type_.capitalize(), match.group()))

    return sensitive_info

def remove_sensitive_information(text_data, output_file=None, info_type=["email", "phone", "credit_card", "ssn", "id", "address", "ip", "iban", "mrn", "icd10", "geo_coords", "username", "file_path", "bitcoin_wallet", "ethereum_wallet"]):
    """
    Remove sensitive information patterns from the provided text data.

    Args:
        text_data (list of str): A list of strings representing the text data to be cleaned.
        output_file (str, optional): Path to the output file where cleaned data will be saved.
        info_type (str or list of str, optional): One or more types of sensitive info to detect and remove. Available types are: "email", "phone", "credit_card", "ssn", "id", "address", "ip", "iban", "mrn", "icd10", "geo_coords", "username", "file_path", "bitcoin_wallet", "ethereum_wallet". Uses all info types by default.

    Returns:
        list of str: A list of strings representing the cleaned text data.
    """
    # Detect sensitive information
    sensitive_info = detect_sensitive_information(text_data, info_type=info_type)

    cleaned_data = []
    for line in text_data:
        cleaned_line = line
        for _, _, _, info in sensitive_info:
            cleaned_line = cleaned_line.replace(info, '[SENSITIVE]')
        cleaned_data.append(cleaned_line)

    # Write cleaned data to output file if provided
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write('\n'.join(cleaned_data))
    return cleaned_data

# New version
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
COUNT_VECTORIZER_PATH = os.path.join(MODEL_DIR, 'count_vectorizer.sav')
DEFAULT_MODEL_FILENAME = "decision_tree_model.sav"
UPGRADED_MODEL_FILENAME = "classifier_upgraded.pkl"

# Check scikit-learn version
SKLEARN_VERSION = tuple(map(int, sklearnversion.split(".")))

# Set the model path based on the version
if SKLEARN_VERSION >= (1, 3, 0):
    DECISION_TREE_MODEL_PATH = os.path.join(MODEL_DIR, UPGRADED_MODEL_FILENAME)
else:
    DECISION_TREE_MODEL_PATH = os.path.join(MODEL_DIR, DEFAULT_MODEL_FILENAME)

# Load the saved models
model = pickle.load(open(DECISION_TREE_MODEL_PATH, 'rb'))
cv = pickle.load(open(COUNT_VECTORIZER_PATH, 'rb'))

def detect_hate_speech(text):
    """
    Detect offensive language or hate speech in the provided text string, using an AI model.

    Args:
        text_data (list of str): A list of strings representing the text data to be cleaned.

    Returns:
        list of str: A list of strings representing the outcome of the detection.
    """
    text = cv.transform([text]).toarray()
    return model.predict((text))

def remove_hate_speech(text_data):
    """
    Remove offensive language or hate speech in the provided text data array, using an AI model.

    Args:
        text (str): A string representing the text data to be used for hate speech detection and offensive language detection.

    Returns:
        list of str: A list of strings representing the cleaned text data.
    """
    cleaned_data = []
    for sentence in text_data:
        outcome = detect_hate_speech(sentence)
        if outcome != ['Hate Speech'] and outcome != ['Offensive Speech'] and outcome == ['No Hate and Offensive Speech']:
            cleaned_data.append(sentence)
    
    return cleaned_data