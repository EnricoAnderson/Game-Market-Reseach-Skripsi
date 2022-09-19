import collections
import math
import operator


def hitungFO(parameter):
    i = 0
    j = 0
    temp = []

    for x in parameter:
        for y in parameter[i]:
            temp.append(y)
            j += 1
        i += 1

    n = givecode(temp)
    # print(n)
    counter = collections.Counter(n)
    print(counter)
    hasil = beriprioritas(counter.most_common())
    hasil = preeliminasi(hasil, i)

    print("Jumlah data " + str(i))
    print("Jumlah tag " + str(j))

    # print(hasil)
    return hasil



def preeliminasi(FO, jumlahdata):
    mcs = math.ceil(0.2 * jumlahdata)

    mcs += 1
    print('minimum support count: ',mcs)
    i = 0
    # print(mcs)
    # print(FO)
    hasil = []

    for x in FO:
        if FO[i][1] >= mcs:
            # print(FO[i])
            hasil.append(FO[i])
            i += 1

    return hasil


def beriprioritas(FO):
    i = 0
    hasil = []
    for x in FO:
        temp = []
        temp.append(FO[i][0])
        temp.append(FO[i][1])
        hasil.append(temp)
        i += 1

    # hasil.sort(key= lambda x: (x[1], x[0]), reverse=True)
    hasil = sorted(hasil, key= operator.itemgetter(0))
    hasil = sorted(hasil, key=operator.itemgetter(1), reverse=True)

    i = 0
    priority = 1
    for x in hasil:
        hasil[i].append(priority)
        i += 1
        priority += 1

    return hasil


def urutkan(parameter, FO):
    temp = []
    for x in parameter:
        temp.append(givecode(x))

    # how tf
    # print(FO)
    # print(temp)
    i = 0
    hasil = []
    for x in temp:
        temp2 = []
        for y in FO:
            for z in x:
                if y[0] == z:
                    temp2.append(y[0])

        hasil.append(temp2)

    # print(hasil)
    return hasil


def givecode(tags):
    isi =   "Indie,Action,Adventure,Casual,Simulation,RPG,Strategy,Singleplayer,Early Access,Free to Play,2D," \
            "Atmospheric,3D,Massively Multiplayer,Multiplayer,Story Rich,Sports,Violent,Puzzle,Fantasy,Colorful," \
            "Pixel Graphics,Exploration,Racing,Cute,Nudity,First-Person,Sexual Content,Anime,Gore,Funny,Sci-fi," \
            "Arcade,Shooter,Action-Adventure,Family Friendly,Horror,Relaxing,Combat,Retro,Open World,Platformer," \
            "Co-op,Female Protagonist,Third Person,Survival,Great Soundtrack,Stylized,Comedy,Difficult,PvP," \
            "Controller,VR,Choices Matter,Old School,Visual Novel,FPS,Realistic,Top-Down,Physics,Online Co-Op,Dark," \
            "Character Customization,Mystery,Cartoony,Sandbox,Multiple Endings,2D Platformer,PvE,Psychological " \
            "Horror,Linear,Tactical,Minimalist,Medieval,Space,Shoot 'Em Up,Magic,Design & Illustration,Building," \
            "Action RPG,Futuristic,Point & Click,Management,Local Multiplayer,Utilities,Hand-drawn,Crafting," \
            "Side Scroller,1980s,Education,Cartoon,Procedural Generation,Resource Management,Puzzle-Platformer," \
            "Mature,Survival Horror,Logic,Drama,Turn-Based,Rogue-like,Replay Value,Turn-Based Combat,Dark Fantasy,War," \
            "3D Platformer,Turn-Based Strategy,Zombies,Tabletop,Romance,Hack and Slash,Choose Your Own Adventure," \
            "Local Co-Op,Rogue-lite,Post-apocalyptic,JRPG,Turn-Based Tactics,Base-Building,Interactive Fiction," \
            "Historical,Dating Sim,Party-Based RPG,Emotional,Hidden Object,Surreal,Stealth,Narration," \
            "Walking Simulator,Dungeon Crawler,Memes,Hentai,Nature,Immersive Sim,1990's,Web Publishing,Score Attack," \
            "Bullet Hell,Military,Third-Person Shooter,Fast-Paced,Classic,Robots,Team-Based,Top-Down Shooter," \
            "Isometric,Conversation,2.5D,Cyberpunk,Short,Aliens,Text-Based,RTS,Cinematic,Dark Humor,Action Roguelike," \
            "Animation & Modeling,LGBTQ+,Software,Investigation,Movie,Nonlinear,Card Game,Inventory Management," \
            "Tutorial,Economy,Driving,Abstract,NSFW,Artificial Intelligence,Beautiful,Music,RPGMaker,Perma Death," \
            "Board Game,4 Player Local,Demons,Strategy RPG,Clicker,Life Sim,Lore-Rich,Real Time Tactics,Experimental," \
            "Psychological,Thriller,Detective,Flight,Arena Shooter,Modern,Fighting,Soundtrack,Dystopian," \
            "Tower Defense,City Builder,Time Management,Precision Platformer,Moddable,Audio Production,Loot," \
            "Psychedelic,Destruction,Supernatural,Tactical RPG,Beat 'em up,Metroidvania,Video Production," \
            "Alternate History,Competitive,Wargame,Level Editor,Comic Book,Souls-like,Mythology,MMORPG,Crime," \
            "Game Development,Parkour,Grid-Based Movement,Runner,2D Fighter,Dark Comedy,World War II,CRPG," \
            "Philosophical,Collectathon,Class-Based,Science,Co-op Campaign,Automobile Sim,Character Action Game," \
            "Idler,Twin Stick Shooter,Gun Customization,Grand Strategy,Software Training,Rhythm,Space Sim,Swordplay," \
            "Deckbuilding,Cats,Dragons,Blood,Lovecraftian,Battle Royale,Addictive,Vehicular Combat,Card Battler,6DOF," \
            "e-Sports,America,3D Vision,Match 3,Split Screen,Noir,3D Fighter,Parody,Capitalism,Illuminati,Conspiracy," \
            "Open World Survival Craft,Satire,Bullet Time,Automation,Trading,Voxel,Political,Colony Sim,Steampunk," \
            "Mystery Dungeon,Time Manipulation,Gothic,Dynamic Narration,Photo Editing,Mechs,Quick-Time Events," \
            "Agriculture,Underground,Mouse only,Real-Time,Time Travel,Hero Shooter,Farming Sim,Mining,Hunting," \
            "Episodic,Cult Classic,Word Game,Epic,Martial Arts,MOBA,Otome,Tanks,Creature Collector,Spectacle fighter," \
            "Pirates,Politics,Ninja,Dog,Looter Shooter,Hacking,God Game,Combat Racing,Solitaire,Remake,Cold War," \
            "Hex Grid,Asynchronous Multiplayer,FMV,Trading Card Game,Superhero,Assassin,Fishing,4X,Cooking," \
            "Underwater,Programming,Vampire,Dinosaurs,Narrative,Faith,Immersive,Trains,Western,Naval,Real-Time with " \
            "Pause,Heist,Sokoban,Political Sim,Party,Minigames,Auto Battler,Party Game,Archery,Kickstarter,Diplomacy," \
            "Foreign,Action RTS,Transportation,Snow,GameMaker,Naval Combat,Touch-Friendly,Mod,Dungeons & Dragons," \
            "Experience,Sequel,Sniper,Music-Based Procedural Generation,Gambling,Sailing,Transhumanism,Mars,Typing," \
            "Villain Protagonist,On-Rails Shooter,Time Attack,Offroad,Soccer,World War I,Documentary,Games Workshop," \
            "Football,Horses,Werewolves,Trivia,Gaming,Traditional Roguelike,Silent Protagonist,360 Video," \
            "Roguelike Deckbuilder,Boxing,Farming,Nostalgia,Chess,Crowdfunded,Unforgiving,Jet,LEGO,Outbreak Sim," \
            "Spaceships,Rome,Asymmetric VR,Escape Room,TrackIR,Spelling,Motorbike,Medical Sim,Golf,Pinball," \
            "Electronic Music,Ambient,Submarine,Bikes,Roguevania,Warhammer 40K,Basketball,Social Deduction," \
            "Based On A Novel,Skateboarding,Mini Golf,Wrestling,Intentionally Awkward Controls,Instrumental Music," \
            "Pool,Vikings,Tennis,Baseball,Benchmark,Lemmings,Skating,Motocross,Cycling,Hockey,Hardware,Steam Machine," \
            "Bowling,Rock Music,8-bit Music,Electronic,ATV,Voice Control,BMX,Boss Rush,Well-Written,Snowboarding," \
            "Feature Film,Skiing,Reboot,VR Only,Masterpiece"

    taglist = isi.split(",")
    taglistLower = []
    for x in taglist:
        x = x.lower().replace(" ", "").replace("-", "")
        taglistLower.append(x)


    hasil = []
    i = 0

    for x in tags:
        berhasil = False
        kode = 1
        j = 0
        for y in taglistLower:
            if tags[i].strip().lower() == taglistLower[j].lower():
                hasil.append(kode)
                berhasil = True
                break
            j += 1
            kode += 1

        if berhasil == False:
            hasil.append(tags[i])


        i += 1

    return hasil
    # print(hasil)