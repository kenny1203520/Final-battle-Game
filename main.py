import pygame, random, os, pickle, math

# Version
SPECIAL_VERSION = False
VERSION = "Beta 1.2.0"

# 遊戲存檔地址
GAMESAVE_FILE_ADDRESS = 'saves/game_save.gs'

# 設定檔地址
CONFIG_FILE_ADDRESS = 'config.txt'

# Screen_Setting
WIDTH = 1280
HEIGHT = 720
FPS = 60
if not os.path.isfile(CONFIG_FILE_ADDRESS):
    # 建立遊戲設定檔
    with open(CONFIG_FILE_ADDRESS, 'wb') as gameConfigFile:
        gameConfig = {}
        gameConfig['ScreenWidth'] = WIDTH
        gameConfig['ScreenHeight'] = HEIGHT
        gameConfig['FPS'] = FPS
        gameConfig['FullScreen'] = True
        gameConfig['MainVolume'] = 5
        gameConfig['MusicVolume'] = 5
        pickle.dump(gameConfig, gameConfigFile)
else:
    with open(CONFIG_FILE_ADDRESS, 'rb') as gameConfigFile:
        gameConfig = pickle.load(gameConfigFile)
Enable_FullScreen = gameConfig['FullScreen']

# 聲音設定
MainVolume = gameConfig['MainVolume']
MusicVolume = gameConfig['MusicVolume']

# Screen_Display_Tittle
Screen_display_tittle = {}
Screen_display_tittle['main'] = ("最後的戰役")
Screen_display_tittle['tittle'] = [("前進魔王城"), ("銓勇士上阿!"), ("銓進魔王城"), ("最後的戰役"), ("飛彈真的時好時壞"), ("飛彈不一定最強"), ("其實電腦都很弱"), ("如果你覺得自己很強最好去挑戰困難"), ("小孩子才玩簡單模式"), ("Final battle")]

# 遊戲初始化 & 創建視窗
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
if Enable_FullScreen:
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(Screen_display_tittle['main'])
program_running = True
GameSave_content = {}

# 導入字型
text_font = os.path.join("Content", "Font", "font.ttf")

# Screen_Display_Icon
# icon
gameIcon = pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\icon.png")), (32, 32))
pygame.display.set_icon(gameIcon)

# 導入圖片
# 主畫面背景
main_screen_background = {}
main_screen_background['main'] = pygame.image.load(os.path.join("Content/Images/main_screen/main_screen_background0.png")).convert()
main_screen_background['animation'] = []
# 製作主畫面開始動畫
for i in range(12):
    main_screen_background_img = pygame.image.load(os.path.join("Content/Images/main_screen", f"main_screen_background{i}.png")).convert()
    main_screen_background['animation'].append(main_screen_background_img)
for i in range(10, 0, -1):
    main_screen_background_img = pygame.image.load(os.path.join("Content/Images/main_screen", f"main_screen_background{i}.png")).convert()
    main_screen_background['animation'].append(main_screen_background_img)
# 按鈕背景照片
button_background_image_normal = pygame.image.load(os.path.join("Content/Images/button/main_screen_button_image_normal.png"))
button_background_image_move = pygame.image.load(os.path.join("Content/Images/button/main_screen_button_image_onbutton.png"))
button_background_image_down = pygame.image.load(os.path.join("Content/Images/button/main_screen_button_image_click.png"))
button_background_image_arrowButton_normal = pygame.image.load(os.path.join("Content/Images/button/arrowButton_image_normal.png"))
button_background_image_arrowButton_move = pygame.image.load(os.path.join("Content/Images/button/arrowButton_image_onbutton.png"))
button_background_image_arrowButton_down = pygame.image.load(os.path.join("Content/Images/button/arrowButton_image_click.png"))
# 遊戲圖片
image_player_soldier = {}
image_player_soldier['Left'] = []
image_player_soldier['Right'] = []
image_player_soldier['Left'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\player\player_soldier_left_1.png")), (96, 108)))
image_player_soldier['Left'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\player\player_soldier_left_2.png")), (96, 108)))
image_player_soldier['Left'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\player\player_soldier_left_3.png")), (96, 108)))
image_player_soldier['Right'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\player\player_soldier_right_1.png")), (96, 108)))
image_player_soldier['Right'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\player\player_soldier_right_2.png")), (96, 108)))
image_player_soldier['Right'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\player\player_soldier_right_3.png")), (96, 108)))
image_enemy_soldier = {}
image_enemy_soldier['Left'] = []
image_enemy_soldier['Right'] = []
image_enemy_soldier['Up'] = []
image_enemy_soldier['Down'] = []
image_enemy_soldier['Left'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_left_1.png")), (96, 108)))
image_enemy_soldier['Left'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_left_2.png")), (96, 108)))
image_enemy_soldier['Left'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_left_3.png")), (96, 108)))
image_enemy_soldier['Right'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_right_1.png")), (96, 108)))
image_enemy_soldier['Right'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_right_2.png")), (96, 108)))
image_enemy_soldier['Right'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_right_3.png")), (96, 108)))
image_enemy_soldier['Up'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_right_up_1.png")), (96, 108)))
image_enemy_soldier['Up'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_right_up_2.png")), (96, 108)))
image_enemy_soldier['Up'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_right_up_3.png")), (96, 108)))
image_enemy_soldier['Up'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_left_up_1.png")), (96, 108)))
image_enemy_soldier['Up'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_left_up_2.png")), (96, 108)))
image_enemy_soldier['Up'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_left_up_3.png")), (96, 108)))
image_enemy_soldier['Down'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_right_down_1.png")), (96, 108)))
image_enemy_soldier['Down'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_right_down_2.png")), (96, 108)))
image_enemy_soldier['Down'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_right_down_3.png")), (96, 108)))
image_enemy_soldier['Down'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_left_down_1.png")), (96, 108)))
image_enemy_soldier['Down'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_left_down_2.png")), (96, 108)))
image_enemy_soldier['Down'].append(pygame.transform.scale(pygame.image.load(os.path.join("Content\Images\game\enemy\enemy_soldier_left_down_3.png")), (96, 108)))
image_sandBag_front = pygame.image.load(os.path.join("Content/Images/game/sandBag/sandBag-front.png"))
image_sandBag_right = pygame.image.load(os.path.join("Content/Images/game/sandBag/sandBag-right.png"))
image_player_plane = pygame.image.load(os.path.join("Content/Images/game/player/player_plane.png"))
image_enemy_plane = pygame.image.load(os.path.join("Content/Images/game/enemy/enemy_plane.png"))
image_enemy_plane = pygame.transform.rotate(image_enemy_plane, 180)
image_enemy_plane_BOSS = pygame.image.load(os.path.join("Content/Images/game/enemy/enemy_plane_BOSS.png"))
image_enemy_plane_BOSS = pygame.transform.rotate(image_enemy_plane_BOSS, 180)
image_player_livesIcon = pygame.image.load(os.path.join("Content\Images\game\player\heart.png"))
image_bullet_rifle = pygame.image.load(os.path.join("Content/Images/game/bullet/bullet_rifle.png"))
image_bullet_laser = pygame.image.load(os.path.join("Content/Images/game/bullet/bullet_laser.png"))
image_bullet_missile = pygame.image.load(os.path.join("Content/Images/game/bullet/bullet_missile.png"))
image_bullet_missile_small = pygame.transform.scale(image_bullet_missile, (9, 31))
image_rock = pygame.image.load(os.path.join("Content/Images/game/rock/rock.png"))
# image_magazine_rifle = pygame.image.load(os.path.join("Content/Images/game/magazine/magazine_rifle.png"))
image_medkit = pygame.image.load(os.path.join("Content/Images/game/medkit/medkit.png"))
image_repairKit = pygame.image.load(os.path.join("Content/Images/game/repairKit/repairKit.png"))
image_armorpack = pygame.image.load(os.path.join("Content/Images/game/armorpack/armorpack.png"))
image_large_magazine_rifle = pygame.image.load(os.path.join("Content/Images/game/magazine/large_magazine_rifle.png"))
image_highspeed_reload_magazine_rifle = pygame.image.load(os.path.join("Content/Images/game/magazine/highspeed_reload_magazine_rifle.png"))
image_aimPoint = pygame.image.load(os.path.join("Content/Images/game/aimPoint/aim_point.png"))
image_weapon_M4A1 = pygame.image.load(os.path.join("Content/Images/game/weapons/rifle_M4A1.png"))
image_weapon_M4A1 = pygame.transform.scale(image_weapon_M4A1, (94, 34))
image_weapon_M4A1_FlipHorizontally = pygame.image.load(os.path.join("Content/Images/game/weapons/rifle_M4A1 - FlipHorizontally.png"))
image_weapon_M4A1_FlipHorizontally = pygame.transform.scale(image_weapon_M4A1_FlipHorizontally, (94, 34))
image_large_magazine_rifle_status = pygame.image.load(os.path.join("Content/Images/game/magazine/large_magazine_rifle - status.png"))
image_large_magazine_rifle_status = pygame.transform.scale(image_large_magazine_rifle_status, (30, 30))
image_playerInformactionUI_background_singleMode = pygame.image.load(os.path.join("Content/Images/game/bullet/bullet_rifle_singleMode.png"))
image_playerInformactionUI_background_autoMode = pygame.image.load(os.path.join("Content/Images/game/bullet/bullet_rifle_autoMode.png"))
image_turretUpgrade = pygame.image.load(os.path.join("Content/Images/game/battery/battery.png"))
image_turretUpgrade = pygame.transform.scale(image_turretUpgrade, (41, 22))
image_turretUpgrade_status = pygame.image.load(os.path.join("Content/Images/game/battery/turretUpgrade_status.png"))
image_turretUpgrade_status = pygame.transform.scale(image_turretUpgrade_status, (30, 30))
# 背景
image_setting_panel_background = pygame.image.load(os.path.join("Content/Images/game/background/background_SettingPanel.png"))
image_background_passLevelScreen = pygame.image.load(os.path.join("Content/Images/game/background/background_passLevelScreen.png"))
image_playerInformactionUI_background = pygame.image.load(os.path.join("Content/Images/game/background/Player_UI_Panel.png"))
image_background_desert = pygame.image.load(os.path.join("Content/Images/game/background/background_desert.png")).convert()
image_background_space = pygame.image.load(os.path.join("Content/Images/game/background/background_space.png")).convert()
image_background_gameStatistics = pygame.image.load(os.path.join("Content/Images/game/background/background_gameStatistics.png")).convert()
image_background_gameStatistics_special = pygame.image.load(os.path.join("Content/Images/game/background/background_gameStatistics - special.png")).convert()
image_background_gameMarkerScreen = pygame.image.load(os.path.join("Content/Images/game/background/background_gameMarkerScreen.png"))
image_background_level1Trip = pygame.image.load(os.path.join("Content/Images/game/background/background_level1Trip_v2.png"))
image_background_level2Trip = pygame.image.load(os.path.join("Content/Images/game/background/background_level2Trip_v2.png"))

# 導入音檔
sound_rifle_shoot = pygame.mixer.Sound(os.path.join("Content/Sound/game/rifle_fire_effect.mp3"))
sound_rifle_reload = pygame.mixer.Sound(os.path.join("Content/Sound/game/rifle_reload_effect.mp3"))
sound_laser_launcher = pygame.mixer.Sound(os.path.join("Content/Sound/game/laser_launcher_effect.mp3"))
sound_missile_launcher = pygame.mixer.Sound(os.path.join("Content/Sound/game/missile_launcher_effect.mp3"))

def draw_text(location, surf, text, text_color, size, bold, x, y):
    # location =>
    # center = center
    # tl = topleft, tr = topright
    # bl = bottomleft, br = bottomright
    font = pygame.font.Font(text_font, size)
    font.set_bold(bold)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    if location == "center":
        text_rect.centerx = x
        text_rect.centery = y
    elif location == "tl":
        text_rect.left = x
        text_rect.top = y
    elif location == "tr":
        text_rect.right = x
        text_rect.top = y
    elif location == "bl":
        text_rect.left = x
        text_rect.bottom = y
    elif location == "br":
        text_rect.right = x
        text_rect.bottom = y
    surf.blit(text_surface, text_rect)

def draw_Level_1_playerInformactionUI(surf, player, score, LevelStartPlayTime):
    # 現在時間(ticks) 1tick = 1ms
    nowTime = pygame.time.get_ticks()
    PlayTime = int((nowTime - LevelStartPlayTime) / 1000)
    if PlayTime > 60:
        PlayTime_Minute = int(PlayTime / 60) 
        PlayTime_Second = PlayTime - (PlayTime_Minute * 60)
    else:
        PlayTime_Minute = 0
        PlayTime_Second = PlayTime
    # 玩家屬性面板
    # # 外框 300*120, 290*110
    # pygame.draw.polygon(surf, (127, 127, 127), [(0, 600), (300, 600), (300, 720), (0, 720)])
    # pygame.draw.polygon(surf, (200, 200, 200), [(5, 605), (295, 605), (295, 715), (5, 715)])

    # # 血量背景 60*30
    # pygame.draw.polygon(surf, (180, 180, 180), [(72, 610), (132, 610), (132, 640), (72, 640)])

    # # 彈匣背景 86*30
    # pygame.draw.polygon(surf, (180, 180, 180), [(204, 610), (290, 610), (290, 640), (204, 640)])

    # # 分數欄背景 143*30
    # pygame.draw.polygon(surf, (180, 180, 180), [(72, 680), (215, 680), (215, 710), (72, 710)])

    # # 遊玩時間 65*60
    # pygame.draw.polygon(surf, (150, 150, 150), [(225, 650), (290, 650), (290, 710), (225, 710)])

    # # 畫屬性面板背景
    # screen.blit(image_PlayerAttributes_Panel, (0, 600))

    # 血量
    # draw_text("tl", surf, "血量 ", (255, 255, 255), 26, True, 10, 608)
    draw_text("tl", surf, str(int(player.now_health)), (255, 255, 255), 24, True, 64, 681)

    # 護甲
    # draw_text("tl", surf, "護甲 ", (255, 255, 255), 26, True, 10, 643)
    draw_text("tl", surf, str(int(player.now_armor)), (255, 255, 255), 24, True, 234, 681)

    # 彈匣內彈量
    # draw_text("tl", surf, "彈匣 ", (255, 255, 255), 26, True, 142, 608)
    # if player.last_magazine_bullets > 0:
    draw_text("br", surf, str(player.last_magazine_bullets) + " / " + str(player.magazine_bullets), (255, 255, 255), 24, True, 1225, 713)
    # elif player.pressed_reload_key:
    #     draw_text("br", surf, "換彈中", (127, 127, 127), 24, True, 1245, 713)
    # else:
    #     draw_text("br", surf, "換彈中", (127, 127, 127), 24, True, 1245, 713)
    
    # 分數
    # draw_text("bl", surf, "分數 ", (255, 255, 255), 26, True, 10, 712)
    draw_text("tr", surf, str(score), (255, 255, 255), 24, True, 1270, 5)

    # 遊玩時間
    # draw_text("br", surf, "時間", (255, 255, 255), 26, True, 286, 684)
    if PlayTime_Second > 9:
        draw_text("center", surf, str(PlayTime_Minute) + ":" + str(PlayTime_Second), (255, 255, 255), 24, True, WIDTH / 2, 22)
    else:
        draw_text("center", surf, str(PlayTime_Minute) + ":0" + str(PlayTime_Second), (255, 255, 255), 24, True, WIDTH / 2, 22)

def draw_Level_2_playerInformactionUI(surf, player, score, LevelStartPlayTime):
    # 現在時間(ticks) 1tick = 1ms
    nowTime = pygame.time.get_ticks()
    PlayTime = int((nowTime - LevelStartPlayTime) / 1000)
    if PlayTime > 60:
        PlayTime_Minute = int(PlayTime / 60) 
        PlayTime_Second = PlayTime - (PlayTime_Minute * 60)
    else:
        PlayTime_Minute = 0
        PlayTime_Second = PlayTime

    # 血量
    # draw_text("tl", surf, "血量 ", (255, 255, 255), 26, True, 10, 608)
    draw_text("tl", surf, str(int(player.now_health)), (255, 255, 255), 24, True, 64, 681)

    # 護甲
    # draw_text("tl", surf, "護甲 ", (255, 255, 255), 26, True, 10, 643)
    draw_text("tl", surf, str(int(player.now_armor)), (255, 255, 255), 24, True, 234, 681)

    # 飛彈數量
    # draw_text("tl", surf, "彈匣 ", (255, 255, 255), 26, True, 142, 608)
    # if player.last_magazine_bullets > 0:
    draw_text("br", surf, str(player.last_missile_amount) + " / " + str(player.missile_amount_original), (255, 255, 255), 24, True, 1225, 713)
    # elif player.pressed_reload_key:
    #     draw_text("tr", surf, "換彈中", (127, 127, 127), 24, True, 285, 610)
    # else:
    #     draw_text("tr", surf, "換彈中", (127, 127, 127), 24, True, 285, 610)
    
    # 分數
    # draw_text("bl", surf, "分數 ", (255, 255, 255), 26, True, 10, 712)
    draw_text("tr", surf, str(score), (255, 255, 255), 24, True, 1270, 5)

    # 遊玩時間
    # draw_text("br", surf, "時間", (255, 255, 255), 26, True, 286, 684)
    if PlayTime_Second > 9:
        draw_text("center", surf, str(PlayTime_Minute) + ":" + str(PlayTime_Second), (255, 255, 255), 24, True, WIDTH / 2, 22)
    else:
        draw_text("center", surf, str(PlayTime_Minute) + ":0" + str(PlayTime_Second), (255, 255, 255), 24, True, WIDTH / 2, 22)

def draw_lives(surf, lives, image, x, y, spacing):
    for i in range(lives):
        image_rect = image.get_rect()
        image_rect.x = x + spacing * i
        image_rect.y = y
        surf.blit(image, image_rect)

def draw_health(surf, now_health, health, left, top, HealthBar_color, Border_Color):
    if now_health < 0:
        now_health = 0
    BAR_LENGTH = 50
    BAR_HEIGHT = 6
    fill = (now_health / health) * BAR_LENGTH
    outline_rect = pygame.Rect(left, top, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(left, top, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, HealthBar_color, fill_rect)
    pygame.draw.rect(surf, Border_Color, outline_rect, 2)

def draw_spriteStatus(surf, now_armor, armor, now_health, health, left, top, ArmorBar_color, HealthBar_color, Border_Color):
    if now_armor < 0:
        now_armor = 0
    if now_health < 0:
        now_health = 0
    BAR_LENGTH = 50
    BAR_HEIGHT = 6
    fill_health = (now_health / health) * BAR_LENGTH
    fill_armor = (now_armor / armor) * BAR_LENGTH
    outline_rect = pygame.Rect(left, top, BAR_LENGTH, BAR_HEIGHT)
    fill_health_rect = pygame.Rect(left, top, fill_health, BAR_HEIGHT)
    fill_armor_rect = pygame.Rect(left, top, fill_armor, BAR_HEIGHT)
    pygame.draw.rect(surf, HealthBar_color, fill_health_rect)
    pygame.draw.rect(surf, ArmorBar_color, fill_armor_rect)
    pygame.draw.rect(surf, Border_Color, outline_rect, 2)

# 主畫面
def draw_main_screen():
    # Tittle
    draw_text("center", screen, Screen_display_tittle["main"], (250, 250, 250), 64, True, WIDTH / 2, (HEIGHT / 10) + 32)
    # version
    draw_text("bl", screen, VERSION, (180, 180, 180), 18, True, 10, 715)
    # drawBotton
    startPlayGame_Button.draw(screen)
    gameSetting_Button.draw(screen)
    leaveGame_Button.draw(screen)

def draw_Key_escape_screen(surf):
    running = True
    continueGame_Button = SettingPanel_ArrowButton(WIDTH / 2, 200 * (HEIGHT / 720), "繼續", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
    mainMenu_Button = SettingPanel_ArrowButton(WIDTH / 2, 331 * (HEIGHT / 720), "主選單", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
    leaveGame_Button = SettingPanel_ArrowButton(WIDTH / 2, 462 * (HEIGHT / 720), "離開", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
    while running:
        clock.tick(FPS)
        # 獲得滑鼠座標
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    continueGame_Button.bottomMouseUp = True
            # 滑鼠移動事件
            elif event.type == pygame.MOUSEMOTION:
                # 判斷滑鼠是否移動到按鈕範圍內
                continueGame_Button.getFocus(mouse_x, mouse_y)
                mainMenu_Button.getFocus(mouse_x, mouse_y)
                leaveGame_Button.getFocus(mouse_x, mouse_y)
            # 滑鼠按下
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #滑鼠左鍵按下
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    continueGame_Button.mouseDown(mouse_x, mouse_y)
                    mainMenu_Button.mouseDown(mouse_x, mouse_y)
                    leaveGame_Button.mouseDown(mouse_x, mouse_y)
            # 滑鼠彈起
            elif event.type == pygame.MOUSEBUTTONUP:
                continueGame_Button.mouseUp()
                mainMenu_Button.mouseUp()
                leaveGame_Button.mouseUp()
        # surf.blit(image_setting_panel_background, (0, 0))
        mainMenu_Button.draw(surf)
        continueGame_Button.draw(surf)
        leaveGame_Button.draw(surf)
        pygame.display.update()
        if continueGame_Button.bottomMouseUp:
            running = False
        if mainMenu_Button.bottomMouseUp:
            running = False
        if leaveGame_Button.bottomMouseUp:
            running = False
    if continueGame_Button.bottomMouseUp:
        continueGame_Button.bottomMouseUp = False
        return 1
    if mainMenu_Button.bottomMouseUp:
        mainMenu_Button.bottomMouseUp = False
        return 2
    if leaveGame_Button.bottomMouseUp:
        leaveGame_Button.bottomMouseUp = False
        return 3

def draw_passLevelScreen(surf, Level):
    running = True
    nextLevel_Button = SettingPanel_ArrowButton(440 * (WIDTH / 1280), 580 * (HEIGHT / 720), "下一關", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
    mainMenu_Button = SettingPanel_ArrowButton(840 * (WIDTH / 1280), 580 * (HEIGHT / 720), "主選單", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
    while running:
        clock.tick(FPS)
        # 獲得滑鼠座標
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            # 滑鼠移動事件
            elif event.type == pygame.MOUSEMOTION:
                # 判斷滑鼠是否移動到按鈕範圍內
                nextLevel_Button.getFocus(mouse_x, mouse_y)
                mainMenu_Button.getFocus(mouse_x, mouse_y)
            # 滑鼠按下
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #滑鼠左鍵按下
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    nextLevel_Button.mouseDown(mouse_x, mouse_y)
                    mainMenu_Button.mouseDown(mouse_x, mouse_y)
            # 滑鼠彈起
            elif event.type == pygame.MOUSEBUTTONUP:
                nextLevel_Button.mouseUp()
                mainMenu_Button.mouseUp()
        surf.blit(image_background_passLevelScreen, (0, 0))
        mainMenu_Button.draw(surf)
        nextLevel_Button.draw(surf)
        draw_text("center", screen, "勝利", (255, 255, 255), 64, True, WIDTH / 2, 160)
        if Level == 1:
            draw_text("tl", screen, "空軍作戰指揮部派遣空軍戰術戰鬥機聯隊前往前線進行空對地打擊", (255, 255, 255), 24, True, 190, 242)
            draw_text("tl", screen, "此次打擊使敵方勢力攻勢暫緩", (255, 255, 255), 24, True, 190, 271)
        elif Level == 2:
            draw_text("tl", screen, "將敵方轟炸機與協防的戰鬥機剿滅同時", (255, 255, 255), 24, True, 190, 242)
            draw_text("tl", screen, "偵查中隊也偵查到了敵人戰時指揮作戰中心", (255, 255, 255), 24, True, 190, 271)
        pygame.display.update()
        if nextLevel_Button.bottomMouseUp:
            running = False
        if mainMenu_Button.bottomMouseUp:
            running = False
    if nextLevel_Button.bottomMouseUp:
        nextLevel_Button.bottomMouseUp = False
        return True
    if mainMenu_Button.bottomMouseUp:
        mainMenu_Button.bottomMouseUp = False
        return False

def draw_failureLevelScreen(surf):
    running = True
    replayGame_Button = SettingPanel_ArrowButton(440 * (WIDTH / 1280), 580 * (HEIGHT / 720), "重玩本關", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
    mainMenu_Button = SettingPanel_ArrowButton(840 * (WIDTH / 1280), 580 * (HEIGHT / 720), "主選單", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
    while running:
        clock.tick(FPS)
        # 獲得滑鼠座標
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            # 滑鼠移動事件
            elif event.type == pygame.MOUSEMOTION:
                # 判斷滑鼠是否移動到按鈕範圍內
                replayGame_Button.getFocus(mouse_x, mouse_y)
                mainMenu_Button.getFocus(mouse_x, mouse_y)
            # 滑鼠按下
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #滑鼠左鍵按下
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    replayGame_Button.mouseDown(mouse_x, mouse_y)
                    mainMenu_Button.mouseDown(mouse_x, mouse_y)
            # 滑鼠彈起
            elif event.type == pygame.MOUSEBUTTONUP:
                replayGame_Button.mouseUp()
                mainMenu_Button.mouseUp()
        surf.blit(image_background_passLevelScreen, (0, 0))
        mainMenu_Button.draw(surf)
        replayGame_Button.draw(surf)
        draw_text("center", screen, "失敗", (255, 255, 255), 64, True, WIDTH / 2, 160)
        draw_text("tl", screen, "再來一次會更好", (255, 255, 255), 24, True, 190, 242)
        pygame.display.update()
        if replayGame_Button.bottomMouseUp:
            running = False
        if mainMenu_Button.bottomMouseUp:
            running = False
    if replayGame_Button.bottomMouseUp:
        replayGame_Button.bottomMouseUp = False
        return True
    if mainMenu_Button.bottomMouseUp:
        mainMenu_Button.bottomMouseUp = False
        return False

class settingPanel:
    def __init__(self):
        self.surf = screen
        self.settingPanel_gameConfig = gameConfig
        self.ScreenImageResolution_now = {}
        self.ScreenImageResolution_now['Width'] = self.settingPanel_gameConfig['ScreenWidth']
        self.ScreenImageResolution_now['Height'] = self.settingPanel_gameConfig['ScreenHeight']
        self.ScreenFPS = self.settingPanel_gameConfig['FPS']
        self.FullScreen_status = self.settingPanel_gameConfig['FullScreen']
        self.MainVolume_now = self.settingPanel_gameConfig['MainVolume']
        self.MusicVolume_now = self.settingPanel_gameConfig['MusicVolume']
        # 是否完成調整
        self.finishSetting = False
        # 按紐
        self.ScreenMode_nextOne = SettingPanel_ArrowButton(1060, 152, "", 20, (255, 255, 255), False, button_background_image_arrowButton_normal, button_background_image_arrowButton_move, button_background_image_arrowButton_down, text_font)
        self.ScreenMode_lastOne = SettingPanel_ArrowButton(720, 152, "", 20, (255, 255, 255), False, button_background_image_arrowButton_normal, button_background_image_arrowButton_move, button_background_image_arrowButton_down, text_font)
        self.MainVolume_Plus = SettingPanel_ArrowButton(1060, 334, "", 20, (255, 255, 255), False, button_background_image_arrowButton_normal, button_background_image_arrowButton_move, button_background_image_arrowButton_down, text_font)
        self.MainVolume_Subtract = SettingPanel_ArrowButton(720, 334, "", 20, (255, 255, 255), False, button_background_image_arrowButton_normal, button_background_image_arrowButton_move, button_background_image_arrowButton_down, text_font)
        self.MusicVolume_Plus = SettingPanel_ArrowButton(1060, 369, "", 20, (255, 255, 255), False, button_background_image_arrowButton_normal, button_background_image_arrowButton_move, button_background_image_arrowButton_down, text_font)
        self.MusicVolume_Subtract = SettingPanel_ArrowButton(720, 369, "", 20, (255, 255, 255), False, button_background_image_arrowButton_normal, button_background_image_arrowButton_move, button_background_image_arrowButton_down, text_font)
        self.confirm_Buttom = SettingPanel_ArrowButton(1060, 600, "確認", 24, (255, 255, 255), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
        self.apply_Buttom = SettingPanel_ArrowButton(840, 600, "套用", 24, (255, 255, 255), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)

    def updateData(self):
        # 顯示模式切換按鈕
        if self.ScreenMode_nextOne.bottomMouseUp:
            self.ScreenMode_nextOne.bottomMouseUp = False
            self.FullScreen_status = False
        elif self.ScreenMode_lastOne.bottomMouseUp:
            self.ScreenMode_lastOne.bottomMouseUp = False
            self.FullScreen_status = True
        # 主音量加減按鈕
        if self.MainVolume_Plus.bottomMouseUp:
            self.MainVolume_Plus.bottomMouseUp = False
            self.MainVolume_now += 1
        elif self.MainVolume_Subtract.bottomMouseUp:
            self.MainVolume_Subtract.bottomMouseUp = False
            self.MainVolume_now -= 1
        # 音樂音量加減按鈕
        if self.MusicVolume_Plus.bottomMouseUp:
            self.MusicVolume_Plus.bottomMouseUp = False
            self.MusicVolume_now += 1
        elif self.MusicVolume_Subtract.bottomMouseUp:
            self.MusicVolume_Subtract.bottomMouseUp = False
            self.MusicVolume_now -= 1
        # 確認按鈕
        if self.confirm_Buttom.bottomMouseUp:
            self.confirm_Buttom.bottomMouseUp = False
            self.settingPanel_gameConfig['ScreenWidth'] = self.ScreenImageResolution_now['Width']
            self.settingPanel_gameConfig['ScreenHeight'] = self.ScreenImageResolution_now['Height']
            self.settingPanel_gameConfig['FPS'] = self.ScreenFPS
            self.settingPanel_gameConfig['FullScreen'] = self.FullScreen_status
            self.settingPanel_gameConfig['MainVolume'] = self.MainVolume_now
            self.settingPanel_gameConfig['MusicVolume'] = self.MusicVolume_now
            with open(CONFIG_FILE_ADDRESS, 'wb') as gameConfigFile:
                pickle.dump(self.settingPanel_gameConfig, gameConfigFile)
            self.finishSetting = True
        # 套用按鈕
        if self.apply_Buttom.bottomMouseUp:
            self.apply_Buttom.bottomMouseUp = False
            self.settingPanel_gameConfig['ScreenWidth'] = self.ScreenImageResolution_now['Width']
            self.settingPanel_gameConfig['ScreenHeight'] = self.ScreenImageResolution_now['Height']
            self.settingPanel_gameConfig['FPS'] = self.ScreenFPS
            self.settingPanel_gameConfig['FullScreen'] = self.FullScreen_status
            self.settingPanel_gameConfig['MainVolume'] = self.MainVolume_now
            self.settingPanel_gameConfig['MusicVolume'] = self.MusicVolume_now
            with open(CONFIG_FILE_ADDRESS, 'wb') as gameConfigFile:
                pickle.dump(self.settingPanel_gameConfig, gameConfigFile)
    
    def draw(self, surf):
        # 畫面
        draw_text("tl", surf, "顯示", (255, 255, 255), 24, True, 130, 90)
        # 螢幕顯示
        draw_text("tl", surf, "顯示模式", (255, 255, 255), 24, True, 130, 140)
        if self.FullScreen_status:
            draw_text("center", surf, "全螢幕", (255, 255, 255), 24, True, 890, 152)
        else:
            draw_text("center", surf, "視窗化", (255, 255, 255), 24, True, 890, 152)
        # 寫解析度
        draw_text("tl", surf, "解析度", (255, 255, 255), 24, True, 130, 175)
        draw_text("center", surf, str(self.ScreenImageResolution_now['Width']) + "x" + str(self.ScreenImageResolution_now['Height']), (255, 255, 255), 24, True, 890, 187)
        # 幀數
        draw_text("tl", surf, "幀數", (255, 255, 255), 24, True, 130, 210)
        draw_text("center", surf, str(self.ScreenFPS), (255, 255, 255), 24, True, 890, 222)

        # 聲音
        draw_text("tl", surf, "聲音", (255, 255, 255), 24, True, 130, 272)
        # 主音量
        draw_text("tl", surf, "主音量", (255, 255, 255), 24, True, 130, 322)
        draw_text("center", surf, str(self.MainVolume_now), (255, 255, 255), 24, True, 890, 334)
        # 音樂音量
        draw_text("tl", surf, "音樂", (255, 255, 255), 24, True, 130, 357)
        draw_text("center", surf, str(self.MusicVolume_now), (255, 255, 255), 24, True, 890, 369)

        # 按鈕
        # 顯示模式
        if self.FullScreen_status:
            self.ScreenMode_nextOne.draw(surf)
        else:
            self.ScreenMode_lastOne.draw(surf)
        # 主音量
        if 0 < self.MainVolume_now < 10:
            self.MainVolume_Plus.draw(surf)
            self.MainVolume_Subtract.draw(surf)
        elif self.MainVolume_now == 10:
            self.MainVolume_Subtract.draw(surf)
        elif self.MainVolume_now == 0:
            self.MainVolume_Plus.draw(surf)
        # 音樂音量
        if 0 < self.MusicVolume_now < 10:
            self.MusicVolume_Plus.draw(surf)
            self.MusicVolume_Subtract.draw(surf)
        elif self.MusicVolume_now == 10:
            self.MusicVolume_Subtract.draw(surf)
        elif self.MusicVolume_now == 0:
            self.MusicVolume_Plus.draw(surf)
        # 確認
        self.confirm_Buttom.draw(surf)
        # 套用
        self.apply_Buttom.draw(surf)

def draw_gameStatisticsScreen(surf):
    with open(GAMESAVE_FILE_ADDRESS, 'rb') as gamesave:
        gamesave_content = pickle.load(gamesave)
    if not SPECIAL_VERSION:
        screen.blit(image_background_gameStatistics, (0, 0))
        # Tittle
        draw_text("center", surf, Screen_display_tittle["main"], (250, 250, 250), 64, True, WIDTH / 2, (HEIGHT / 10) + 8)
        # version
        draw_text("bl", screen, VERSION, (180, 180, 180), 18, True, 10, 715)
        # scoreList
        draw_text("tl", surf, "遊玩總時長", (250, 250, 250), 26, False, 80, 150)
        draw_text("tl", surf, str(gamesave_content['PlayTime_total']), (250, 250, 250), 24, False, 230, 152)
        draw_text("tl", surf, "遊戲難度", (250, 250, 250), 26, False, 530, 150)
        if gamesave_content['difficult'] == "easy":
            draw_text("tl", surf, "簡單", (250, 250, 250), 24, False, 680, 152)
        if gamesave_content['difficult'] == "normal":
            draw_text("tl", surf, "普通", (250, 250, 250), 24, False, 680, 152)
        if gamesave_content['difficult'] == "hard":
            draw_text("tl", surf, "困難", (250, 250, 250), 24, False, 680, 152)
        draw_text("tl", surf, "遊戲進度", (250, 250, 250), 26, False, 960, 150)
        if gamesave_content['PassGame']:
            draw_text("tl", surf, "通關", (250, 250, 250), 24, False, 1110, 152)
            # 重完選項
            draw_text("tl", surf, "重新挑戰", (250, 250, 250), 26, True, 80, 410)
        else:
            draw_text("tl", surf, "努力中", (250, 250, 250), 24, False, 1110, 152)
        
        # 第一關
        draw_text("tl", surf, "第一關", (250, 250, 250), 26, True, 80, 190)
        draw_text("tl", surf, "遊玩時長", (250, 250, 250), 26, False, 80, 230)
        draw_text("tl", surf, str(gamesave_content['PlayTime_Level_1']), (250, 250, 250), 24, False, 230, 232)
        draw_text("tl", surf, "遊玩總時長", (250, 250, 250), 26, False, 80, 265)
        draw_text("tl", surf, str(gamesave_content['PlayTime_Level_1_total']), (250, 250, 250), 24, False, 230, 267)
        draw_text("tl", surf, "分數", (250, 250, 250), 26, False, 80, 300)
        draw_text("tl", surf, str(gamesave_content['Score_Level_1']), (250, 250, 250), 24, False, 230, 302)
        draw_text("tl", surf, "最高", (250, 250, 250), 26, False, 80, 335)
        draw_text("tl", surf, str(gamesave_content['history_HighestScore_Level_1']), (250, 250, 250), 24, False, 230, 337)
        # 第二關
        draw_text("tl", surf, "第二關", (250, 250, 250), 26, True, 530, 190)
        draw_text("tl", surf, "遊玩時長", (250, 250, 250), 26, False, 530, 230)
        draw_text("tl", surf, str(gamesave_content['PlayTime_Level_2']), (250, 250, 250), 24, False, 680, 232)
        draw_text("tl", surf, "遊玩總時長", (250, 250, 250), 26, False, 530, 265)
        draw_text("tl", surf, str(gamesave_content['PlayTime_Level_2_total']), (250, 250, 250), 24, False, 680, 267)
        draw_text("tl", surf, "分數", (250, 250, 250), 26, False, 530, 300)
        draw_text("tl", surf, str(gamesave_content['Score_Level_2']), (250, 250, 250), 24, False, 680, 302)
        draw_text("tl", surf, "最高", (250, 250, 250), 26, False, 530, 335)
        draw_text("tl", surf, str(gamesave_content['history_HighestScore_Level_2']), (250, 250, 250), 24, False, 680, 337)
        # 第三關
        draw_text("tl", surf, "第三關", (250, 250, 250), 26, True, 960, 190)
        draw_text("tl", surf, "遊玩時長", (250, 250, 250), 26, False, 960, 230)
        draw_text("tl", surf, str(gamesave_content['PlayTime_Level_3']), (250, 250, 250), 24, False, 1110, 232)
        draw_text("tl", surf, "遊玩總時長", (250, 250, 250), 26, False, 960, 265)
        draw_text("tl", surf, str(gamesave_content['PlayTime_Level_3_total']), (250, 250, 250), 24, False, 1110, 267)
        draw_text("tl", surf, "分數", (250, 250, 250), 26, False, 960, 300)
        draw_text("tl", surf, str(gamesave_content['Score_Level_3']), (250, 250, 250), 24, False, 1110, 302)
        draw_text("tl", surf, "最高", (250, 250, 250), 26, False, 960, 335)
        draw_text("tl", surf, str(gamesave_content['history_HighestScore_Level_3']), (250, 250, 250), 24, False, 1110, 337)
    else:
        screen.blit(image_background_gameStatistics_special, (0, 0))
        # Tittle
        draw_text("center", surf, Screen_display_tittle["main"], (250, 250, 250), 64, True, WIDTH / 2, (HEIGHT / 10) + 8)
        # version
        draw_text("bl", screen, VERSION, (180, 180, 180), 18, True, 10, 715)
        # scoreList
        draw_text("tl", surf, "遊玩總時長", (250, 250, 250), 26, False, 80, 150)
        draw_text("tl", surf, str(gamesave_content['PlayTime_total']), (250, 250, 250), 24, False, 230, 152)
        draw_text("tl", surf, "遊戲難度", (250, 250, 250), 26, False, 530, 150)
        if gamesave_content['difficult'] == "easy":
            draw_text("tl", surf, "簡單", (250, 250, 250), 24, False, 680, 152)
        if gamesave_content['difficult'] == "normal":
            draw_text("tl", surf, "普通", (250, 250, 250), 24, False, 680, 152)
        if gamesave_content['difficult'] == "hard":
            draw_text("tl", surf, "困難", (250, 250, 250), 24, False, 680, 152)
        draw_text("tl", surf, "遊戲進度", (250, 250, 250), 26, False, 960, 150)
        if gamesave_content['PassGame']:
            draw_text("tl", surf, "通關", (250, 250, 250), 24, False, 1110, 152)
            # 重完選項
            draw_text("tl", surf, "重新挑戰", (250, 250, 250), 26, True, 80, 410)
        else:
            draw_text("tl", surf, "努力中", (250, 250, 250), 24, False, 1110, 152)
        
        # 第一關
        draw_text("tl", surf, "第一關", (250, 250, 250), 26, True, 80, 190)
        draw_text("tl", surf, "遊玩時長", (250, 250, 250), 26, False, 80, 230)
        draw_text("tl", surf, str(gamesave_content['PlayTime_Level_1']), (250, 250, 250), 24, False, 230, 232)
        draw_text("tl", surf, "遊玩總時長", (250, 250, 250), 26, False, 80, 265)
        draw_text("tl", surf, str(gamesave_content['PlayTime_Level_1_total']), (250, 250, 250), 24, False, 230, 267)
        draw_text("tl", surf, "分數", (250, 250, 250), 26, False, 80, 300)
        draw_text("tl", surf, str(gamesave_content['Score_Level_1']), (250, 250, 250), 24, False, 230, 302)
        draw_text("tl", surf, "最高", (250, 250, 250), 26, False, 80, 335)
        draw_text("tl", surf, str(gamesave_content['history_HighestScore_Level_1']), (250, 250, 250), 24, False, 230, 337)
        # 第二關
        draw_text("tl", surf, "第二關", (250, 250, 250), 26, True, 530, 190)
        draw_text("tl", surf, "遊玩時長", (250, 250, 250), 26, False, 530, 230)
        draw_text("tl", surf, str(gamesave_content['PlayTime_Level_2']), (250, 250, 250), 24, False, 680, 232)
        draw_text("tl", surf, "遊玩總時長", (250, 250, 250), 26, False, 530, 265)
        draw_text("tl", surf, str(gamesave_content['PlayTime_Level_2_total']), (250, 250, 250), 24, False, 680, 267)
        draw_text("tl", surf, "分數", (250, 250, 250), 26, False, 530, 300)
        draw_text("tl", surf, str(gamesave_content['Score_Level_2']), (250, 250, 250), 24, False, 680, 302)
        draw_text("tl", surf, "最高", (250, 250, 250), 26, False, 530, 335)
        draw_text("tl", surf, str(gamesave_content['history_HighestScore_Level_2']), (250, 250, 250), 24, False, 680, 337)
        # 第三關
        draw_text("tl", surf, "第三關", (250, 250, 250), 26, True, 960, 190)
        draw_text("tl", surf, "遊玩時長", (250, 250, 250), 26, False, 960, 230)
        draw_text("tl", surf, str(gamesave_content['PlayTime_Level_3']), (250, 250, 250), 24, False, 1110, 232)
        draw_text("tl", surf, "遊玩總時長", (250, 250, 250), 26, False, 960, 265)
        draw_text("tl", surf, str(gamesave_content['PlayTime_Level_3_total']), (250, 250, 250), 24, False, 1110, 267)
        draw_text("tl", surf, "分數", (250, 250, 250), 26, False, 960, 300)
        draw_text("tl", surf, str(gamesave_content['Score_Level_3']), (250, 250, 250), 24, False, 1110, 302)
        draw_text("tl", surf, "最高", (250, 250, 250), 26, False, 960, 335)
        draw_text("tl", surf, str(gamesave_content['history_HighestScore_Level_3']), (250, 250, 250), 24, False, 1110, 337)

# 按鈕
def startPlayGame_Button_function(surf):
    running = True
    alreadyReadGameSave = False
    exitLoop = False
    while running and not alreadyReadGameSave:
        clock.tick(FPS)
        # 檢查是否有遊戲存檔
        if not os.path.isfile(GAMESAVE_FILE_ADDRESS):
            select_difficult = True
            # 回主選單
            mainMenu_Button = SettingPanel_ArrowButton(WIDTH - 120, HEIGHT - 52, "主選單", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
            # 難度按鈕
            easy_difficult_Button = SettingPanel_ArrowButton(WIDTH / 2, 255, "簡單", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
            normal_difficult_Button = SettingPanel_ArrowButton(WIDTH / 2, 339, "普通", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
            hard_difficult_Button = SettingPanel_ArrowButton(WIDTH / 2, 423, "困難", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
            
            while select_difficult:
                clock.tick(FPS)
                # 獲得滑鼠座標
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # 檢查事件
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        select_difficult = False
                        running = False
                        break
                    # 滑鼠移動事件
                    elif event.type == pygame.MOUSEMOTION:
                        # 判斷滑鼠是否移動到按鈕範圍內
                        easy_difficult_Button.getFocus(mouse_x, mouse_y)
                        normal_difficult_Button.getFocus(mouse_x, mouse_y)
                        hard_difficult_Button.getFocus(mouse_x, mouse_y)
                        mainMenu_Button.getFocus(mouse_x, mouse_y)
                    # 滑鼠按下
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        #滑鼠左鍵按下
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            easy_difficult_Button.mouseDown(mouse_x, mouse_y)
                            normal_difficult_Button.mouseDown(mouse_x, mouse_y)
                            hard_difficult_Button.mouseDown(mouse_x, mouse_y)
                            mainMenu_Button.mouseDown(mouse_x, mouse_y)
                    # 滑鼠彈起
                    elif event.type == pygame.MOUSEBUTTONUP:
                        easy_difficult_Button.mouseUp()
                        normal_difficult_Button.mouseUp()
                        hard_difficult_Button.mouseUp()
                        mainMenu_Button.mouseUp()

                # 難度按鈕
                if easy_difficult_Button.bottomMouseUp:
                    break
                if normal_difficult_Button.bottomMouseUp:
                    break
                if hard_difficult_Button.bottomMouseUp:
                    break
                # 主畫面按鈕
                if mainMenu_Button.bottomMouseUp:
                    break

                # 畫面
                surf.blit(main_screen_background["main"], (0, 0))
                draw_text("center", surf, "選擇存檔難度", (240, 240, 240), 36, False, (WIDTH / 2), 162)
                easy_difficult_Button.draw(surf)
                normal_difficult_Button.draw(surf)
                hard_difficult_Button.draw(surf)
                mainMenu_Button.draw(surf)
                pygame.display.update()
            
            if easy_difficult_Button.bottomMouseUp or normal_difficult_Button.bottomMouseUp or hard_difficult_Button.bottomMouseUp:
                # 建立所有遊戲需儲存參數
                gamesave_content = {}
                gamesave_content['game_checkpoint'] = 0
                gamesave_content['difficult'] = "normal"
                gamesave_content['Score_Level_1'] = 0
                gamesave_content['Score_Level_2'] = 0
                gamesave_content['Score_Level_3'] = 0
                gamesave_content['history_HighestScore_Level_1'] = 0
                gamesave_content['history_HighestScore_Level_2'] = 0
                gamesave_content['history_HighestScore_Level_3'] = 0
                gamesave_content['PlayTime_Level_1'] = 0
                gamesave_content['PlayTime_Level_2'] = 0
                gamesave_content['PlayTime_Level_3'] = 0
                gamesave_content['PlayTime_total'] = 0
                gamesave_content['PlayTime_Level_1_total'] = 0
                gamesave_content['PlayTime_Level_2_total'] = 0
                gamesave_content['PlayTime_Level_3_total'] = 0
                gamesave_content['PassGame'] = False
                # 難度調整
                if easy_difficult_Button.bottomMouseUp:
                    easy_difficult_Button.bottomMouseUp = False
                    gamesave_content['difficult'] = "easy"
                elif normal_difficult_Button.bottomMouseUp:
                    normal_difficult_Button.bottomMouseUp = False
                    gamesave_content['difficult'] = "normal"
                elif hard_difficult_Button.bottomMouseUp:
                    hard_difficult_Button.bottomMouseUp = False
                    gamesave_content['difficult'] = "hard"
                
                # 將參數存到文件中
                with open(GAMESAVE_FILE_ADDRESS, 'wb') as gamesave:
                    pickle.dump(gamesave_content, gamesave)
                select_difficult = False
                running = False
                return gamesave_content

            elif mainMenu_Button.bottomMouseUp:
                select_difficult = False
                mainMenu_Button.bottomMouseUp = False
                break

        elif not alreadyReadGameSave:
            def loadSave_Button_function():
                return True

            def removeSave_Button_function():
                os.remove(GAMESAVE_FILE_ADDRESS)

            # 是否要讀檔
            loadSave_Button = Button((WIDTH / 2), (HEIGHT / 2), ("讀檔"), 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, loadSave_Button_function, text_font)
            removeSave_Button = Button((WIDTH / 2), 260 * (HEIGHT / 720), ("開始新遊戲"), 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, removeSave_Button_function, text_font)
            # 回主選單
            mainMenu_Button = SettingPanel_ArrowButton(WIDTH - 220, HEIGHT - 85, "主選單", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)

            while os.path.isfile(GAMESAVE_FILE_ADDRESS) and not exitLoop:
                clock.tick(FPS)
                # 獲得滑鼠座標
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # 檢查事件
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exitLoop = True
                        running = False
                        break
                    # 滑鼠移動事件
                    elif event.type == pygame.MOUSEMOTION:
                        # 判斷滑鼠是否移動到按鈕範圍內
                        loadSave_Button.getFocus(mouse_x, mouse_y)
                        removeSave_Button.getFocus(mouse_x, mouse_y)
                        mainMenu_Button.getFocus(mouse_x, mouse_y)
                    # 滑鼠按下
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        #滑鼠左鍵按下
                        if pygame.mouse.get_pressed() == (1, 0, 0):
                            loadSave_Button.mouseDown(mouse_x, mouse_y)
                            removeSave_Button.mouseDown(mouse_x, mouse_y)
                            mainMenu_Button.mouseDown(mouse_x, mouse_y)
                    # 滑鼠彈起
                    elif event.type == pygame.MOUSEBUTTONUP:
                        if loadSave_Button.status == Button.DOWN:
                            if loadSave_Button.mouseUp():
                                # 讀取存檔中的參數
                                with open(GAMESAVE_FILE_ADDRESS, 'rb') as gamesave:
                                    gamesave_content = pickle.load(gamesave)
                                alreadyReadGameSave = True
                        removeSave_Button.mouseUp()
                        mainMenu_Button.mouseUp()

                if alreadyReadGameSave:
                    break
                
                if mainMenu_Button.bottomMouseUp:
                    break

                # 畫面
                surf.blit(main_screen_background["main"], (0, 0))
                draw_text("center", surf, "是否要讀取存檔", (240, 240, 240), 36, False, (WIDTH / 2), (HEIGHT / 5) + 18)
                loadSave_Button.draw(surf)
                removeSave_Button.draw(surf)
                mainMenu_Button.draw(surf)
                pygame.display.update()
        if alreadyReadGameSave:
            running = False
            return gamesave_content

        if mainMenu_Button.bottomMouseUp:
            mainMenu_Button.bottomMouseUp = False
            break

def gameSetting_Button_function(surf):
    running = True
    setting_Panel = settingPanel()
    while running:
        clock.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # 檢查事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            # 滑鼠移動事件
            elif event.type == pygame.MOUSEMOTION:
                # 判斷滑鼠是否移動到按鈕範圍內
                # 顯示模式
                if setting_Panel.FullScreen_status:
                    setting_Panel.ScreenMode_nextOne.getFocus(mouse_x, mouse_y)
                else:
                    setting_Panel.ScreenMode_lastOne.getFocus(mouse_x, mouse_y)
                # 主音量
                if 0 < setting_Panel.MainVolume_now < 10:
                    setting_Panel.MainVolume_Plus.getFocus(mouse_x, mouse_y)
                    setting_Panel.MainVolume_Subtract.getFocus(mouse_x, mouse_y)
                elif setting_Panel.MainVolume_now == 10:
                    setting_Panel.MainVolume_Subtract.getFocus(mouse_x, mouse_y)
                elif setting_Panel.MainVolume_now == 0:
                    setting_Panel.MainVolume_Plus.getFocus(mouse_x, mouse_y)
                # 音樂音量
                if 0 < setting_Panel.MusicVolume_now < 10:
                    setting_Panel.MusicVolume_Plus.getFocus(mouse_x, mouse_y)
                    setting_Panel.MusicVolume_Subtract.getFocus(mouse_x, mouse_y)
                elif setting_Panel.MusicVolume_now == 10:
                    setting_Panel.MusicVolume_Subtract.getFocus(mouse_x, mouse_y)
                elif setting_Panel.MusicVolume_now == 0:
                    setting_Panel.MusicVolume_Plus.getFocus(mouse_x, mouse_y)
                # 確認
                    setting_Panel.confirm_Buttom.getFocus(mouse_x, mouse_y)
                    # 套用
                    setting_Panel.apply_Buttom.getFocus(mouse_x, mouse_y)
            
            # 滑鼠按下
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #滑鼠左鍵按下
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    # 顯示模式
                    if setting_Panel.FullScreen_status:
                        setting_Panel.ScreenMode_nextOne.mouseDown(mouse_x, mouse_y)
                    else:
                        setting_Panel.ScreenMode_lastOne.mouseDown(mouse_x, mouse_y)
                    # 主音量
                    if 0 < setting_Panel.MainVolume_now < 10:
                        setting_Panel.MainVolume_Plus.mouseDown(mouse_x, mouse_y)
                        setting_Panel.MainVolume_Subtract.mouseDown(mouse_x, mouse_y)
                    elif setting_Panel.MainVolume_now == 10:
                        setting_Panel.MainVolume_Subtract.mouseDown(mouse_x, mouse_y)
                    elif setting_Panel.MainVolume_now == 0:
                        setting_Panel.MainVolume_Plus.mouseDown(mouse_x, mouse_y)
                    # 音樂音量
                    if 0 < setting_Panel.MusicVolume_now < 10:
                        setting_Panel.MusicVolume_Plus.mouseDown(mouse_x, mouse_y)
                        setting_Panel.MusicVolume_Subtract.mouseDown(mouse_x, mouse_y)
                    elif setting_Panel.MusicVolume_now == 10:
                        setting_Panel.MusicVolume_Subtract.mouseDown(mouse_x, mouse_y)
                    elif setting_Panel.MusicVolume_now == 0:
                        setting_Panel.MusicVolume_Plus.mouseDown(mouse_x, mouse_y)
                    # 確認
                    setting_Panel.confirm_Buttom.mouseDown(mouse_x, mouse_y)
                    # 套用
                    setting_Panel.apply_Buttom.mouseDown(mouse_x, mouse_y)
            
            # 滑鼠彈起
            elif event.type == pygame.MOUSEBUTTONUP:
                setting_Panel.ScreenMode_nextOne.mouseUp()
                setting_Panel.ScreenMode_lastOne.mouseUp()
                setting_Panel.MainVolume_Plus.mouseUp()
                setting_Panel.MainVolume_Subtract.mouseUp()
                setting_Panel.MusicVolume_Plus.mouseUp()
                setting_Panel.MusicVolume_Subtract.mouseUp()
                setting_Panel.confirm_Buttom.mouseUp()
                setting_Panel.apply_Buttom.mouseUp()
                setting_Panel.updateData()
        
        if setting_Panel.finishSetting:
            running = False

        # 畫面
        # 背景
        surf.blit(main_screen_background['main'], (0, 0))
        surf.blit(image_setting_panel_background, (0, 0))
        setting_Panel.draw(surf)
        pygame.display.update()
    if setting_Panel.finishSetting:
        setting_Panel.finishSetting = False
        return True

def leaveGame_Button_function():
    return True

class Button:
    NORMAL = 0
    MOVE = 1
    DOWN = 2
    def __init__(self, center_x, center_y, text, text_size ,text_color, text_bold, imageNormal, imageMove = None, imageDown = None, callBackFunction = None, font = None):
        self.button_images = []
        if not imageNormal:
            raise Exception("請設定普通狀態的圖片")
        self.button_images.append(imageNormal)
        self.button_images.append(imageMove)
        self.button_images.append(imageDown)
        for i in range(2, 0, -1):
            if not self.button_images[i]:
                self.button_images[i] = self.button_images[i - 1]
        self.callBackFunction = callBackFunction
        self.status = Button.NORMAL
        self.button_image_width = imageNormal.get_width()
        self.button_image_height = imageNormal.get_height()
        self.center_x = center_x
        self.center_y = center_y
        self.x = self.center_x - (self.button_image_width / 2)
        self.y = self.center_y - (self.button_image_height / 2)
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.text_bold = text_bold
        self.font = font

    def draw(self, surf):
        # 畫按鈕背景
        if self.button_images[self.status]:
            surf.blit(self.button_images[self.status], (self.x, self.y))
        # 畫文字
        draw_text("center", surf, self.text, self.text_color, self.text_size, self.text_bold, self.center_x, self.center_y)

    def colli(self, x, y):
        # 碰撞檢測
        if self.x < x < self.x + self.button_image_width and self.y < y < self.y + self.button_image_height:
            return True
        else:
            return False

    def getFocus(self, x, y):
        # 按鈕獲得焦點時
        if self.status == Button.DOWN:
            return
        if self.colli(x, y):
            self.status = Button.MOVE
        else:
            self.status = Button.NORMAL

    def mouseDown(self, x, y):
        if self.colli(x, y):
            self.status = Button.DOWN

    def mouseUp(self):
        # 如果按鈕彈起則還原成普通狀態
        if self.status == Button.DOWN:
            self.status = Button.NORMAL
            if self.callBackFunction:
                return self.callBackFunction()

class startPlayGameButton:
    NORMAL = 0
    MOVE = 1
    DOWN = 2
    game_save = {}
    def __init__(self, center_x, center_y, text, text_size ,text_color, text_bold, imageNormal, imageMove = None, imageDown = None, font = None):
        self.button_images = []
        if not imageNormal:
            raise Exception("請設定普通狀態的圖片")
        self.button_images.append(imageNormal)
        self.button_images.append(imageMove)
        self.button_images.append(imageDown)
        for i in range(2, 0, -1):
            if not self.button_images[i]:
                self.button_images[i] = self.button_images[i - 1]
        self.status = Button.NORMAL
        self.button_image_width = imageNormal.get_width()
        self.button_image_height = imageNormal.get_height()
        self.center_x = center_x
        self.center_y = center_y
        self.x = self.center_x - (self.button_image_width / 2)
        self.y = self.center_y - (self.button_image_height / 2)
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.text_bold = text_bold
        self.font = font

    def draw(self, surf):
        # 畫按鈕背景
        if self.button_images[self.status]:
            surf.blit(self.button_images[self.status], (self.x, self.y))
        # 畫文字
        draw_text("center", surf, self.text, self.text_color, self.text_size, self.text_bold, self.center_x, self.center_y)

    def colli(self, x, y):
        # 碰撞檢測
        if self.x < x < self.x + self.button_image_width and self.y < y < self.y + self.button_image_height:
            return True
        else:
            return False

    def getFocus(self, x, y):
        # 按鈕獲得焦點時
        if self.status == Button.DOWN:
            return
        if self.colli(x, y):
            self.status = Button.MOVE
        else:
            self.status = Button.NORMAL

    def mouseDown(self, x, y):
        if self.colli(x, y):
            self.status = Button.DOWN

    def mouseUp(self, surf):
        # 如果按鈕彈起則還原成普通狀態
        if self.status == Button.DOWN:
            self.status = Button.NORMAL
            self.game_save = startPlayGame_Button_function(surf)
            if self.game_save:
                return True

class gameSettingButton:
    NORMAL = 0
    MOVE = 1
    DOWN = 2
    def __init__(self, surf, center_x, center_y, text, text_size ,text_color, text_bold, imageNormal, imageMove = None, imageDown = None, font = None):
        self.button_images = []
        if not imageNormal:
            raise Exception("請設定普通狀態的圖片")
        self.button_images.append(imageNormal)
        self.button_images.append(imageMove)
        self.button_images.append(imageDown)
        for i in range(2, 0, -1):
            if not self.button_images[i]:
                self.button_images[i] = self.button_images[i - 1]
        self.status = Button.NORMAL
        self.surf = surf
        self.button_image_width = imageNormal.get_width()
        self.button_image_height = imageNormal.get_height()
        self.center_x = center_x
        self.center_y = center_y
        self.x = self.center_x - (self.button_image_width / 2)
        self.y = self.center_y - (self.button_image_height / 2)
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.text_bold = text_bold
        self.font = font

    def draw(self, surf):
        # 畫按鈕背景
        if self.button_images[self.status]:
            surf.blit(self.button_images[self.status], (self.x, self.y))
        # 畫文字
        draw_text("center", surf, self.text, self.text_color, self.text_size, self.text_bold, self.center_x, self.center_y)

    def colli(self, x, y):
        # 碰撞檢測
        if self.x < x < self.x + self.button_image_width and self.y < y < self.y + self.button_image_height:
            return True
        else:
            return False

    def getFocus(self, x, y):
        # 按鈕獲得焦點時
        if self.status == Button.DOWN:
            return
        if self.colli(x, y):
            self.status = Button.MOVE
        else:
            self.status = Button.NORMAL

    def mouseDown(self, x, y):
        if self.colli(x, y):
            self.status = Button.DOWN

    def mouseUp(self):
        # 如果按鈕彈起則還原成普通狀態
        if self.status == Button.DOWN:
            self.status = Button.NORMAL
            result = gameSetting_Button_function(self.surf)
            if result:
                return True

class SettingPanel_ArrowButton:
    NORMAL = 0
    MOVE = 1
    DOWN = 2
    def __init__(self, center_x, center_y, text, text_size ,text_color, text_bold, imageNormal, imageMove = None, imageDown = None, font = None):
        self.button_images = []
        if not imageNormal:
            raise Exception("請設定普通狀態的圖片")
        self.button_images.append(imageNormal)
        self.button_images.append(imageMove)
        self.button_images.append(imageDown)
        for i in range(2, 0, -1):
            if not self.button_images[i]:
                self.button_images[i] = self.button_images[i - 1]
        self.status = Button.NORMAL
        self.button_image_width = imageNormal.get_width()
        self.button_image_height = imageNormal.get_height()
        self.center_x = center_x
        self.center_y = center_y
        self.x = self.center_x - (self.button_image_width / 2)
        self.y = self.center_y - (self.button_image_height / 2)
        self.text = text
        self.text_size = text_size
        self.text_color = text_color
        self.text_bold = text_bold
        self.font = font
        self.bottomMouseUp = False

    def draw(self, surf):
        # 畫按鈕背景
        if self.button_images[self.status]:
            surf.blit(self.button_images[self.status], (self.x, self.y))
        # 畫文字
        draw_text("center", surf, self.text, self.text_color, self.text_size, self.text_bold, self.center_x, self.center_y)

    def colli(self, x, y):
        # 碰撞檢測
        if self.x < x < self.x + self.button_image_width and self.y < y < self.y + self.button_image_height:
            return True
        else:
            return False

    def getFocus(self, x, y):
        # 按鈕獲得焦點時
        if self.status == Button.DOWN:
            return
        if self.colli(x, y):
            self.status = Button.MOVE
        else:
            self.status = Button.NORMAL

    def mouseDown(self, x, y):
        if self.colli(x, y):
            self.status = Button.DOWN

    def mouseUp(self):
        # 如果按鈕彈起則還原成普通狀態
        if self.status == Button.DOWN:
            self.status = Button.NORMAL
            self.bottomMouseUp = True

# 第一關
def Level_1_draw_levelTrip():
    screen.blit(image_background_level1Trip, (0, 0))
    draw_text("tl", screen, '鎮守前線', (255, 255, 255), 48, True, 40 * (WIDTH / 1280), 46 * (HEIGHT / 720))
    draw_text("tl", screen, '2087年在地球發生了一場全球性的襲擊', (255, 255, 255), 22, False, 45 * (WIDTH / 1280), 136 * (HEIGHT / 720))
    draw_text("tl", screen, '戰場遍佈在地球的各個角落', (255, 255, 255), 22, False, 45 * (WIDTH / 1280), 168 * (HEIGHT / 720))
    draw_text("tl", screen, '臺灣', (255, 255, 255), 32, True, 45 * (WIDTH / 1280), 218 * (HEIGHT / 720))
    draw_text("tl", screen, '指揮部派遣ASSC前往受到襲擊的現場進行偵查行動', (255, 255, 255), 22, False, 45 * (WIDTH / 1280), 264 * (HEIGHT / 720))
    draw_text("tl", screen, 'ASSC到達現場後發現在前線鎮守的部隊僅剩下一個連隊', (255, 255, 255), 22, False, 45 * (WIDTH / 1280), 296 * (HEIGHT / 720))
    draw_text("tl", screen, '指揮部命令ASSC協助當地部隊鎮守前線等待支援', (255, 255, 255), 22, False, 45 * (WIDTH / 1280), 328 * (HEIGHT / 720))
    draw_text("center", screen, 'WASD 或 ↑←↓→ 操控方向', (255, 255, 255), 16, False, WIDTH / 2, (580 * (HEIGHT / 720)) + 8)
    draw_text("center", screen, '左鍵 進行射擊 R鍵 換彈 B鍵 切換射擊模式', (255, 255, 255), 16, False, WIDTH / 2, (610 * (HEIGHT / 720)) + 8)
    draw_text("center", screen, '按任意鍵開始', (255, 255, 255), 16, False, WIDTH / 2, (640 * (HEIGHT / 720)) + 8)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

def Level_1_choice_spawnArea():
    # 左上 => spawnArea = 1
    # 左中 => spawnArea = 2
    # 左下 => spawnArea = 3
    # 右上 => spawnArea = 4
    # 右中 => spawnArea = 5
    # 右下 => spawnArea = 6
    spawnArea = random.randint(1, 6)
    if spawnArea == 1:
        return (random.randrange(0, 640), random.randrange(0, 240))
    elif spawnArea == 2:
        return (random.randrange(0, 520), random.randrange(240, 480))
    elif spawnArea == 3:
        return (random.randrange(0, 640), random.randrange(480, 720))
    elif spawnArea == 4:
        return (random.randrange(640, 1280), random.randrange(0, 240))
    elif spawnArea == 5:
        return (random.randrange(760, 1280), random.randrange(240, 480))
    elif spawnArea == 6:
        return (random.randrange(640, 1280), random.randrange(480, 720))

class Level_1_Player_soldier(pygame.sprite.Sprite):
    def __init__(self, surf):
        pygame.sprite.Sprite.__init__(self)
        self.surf = surf
        self.image_original = image_player_soldier['Right'][0]
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        # self.radius = 15
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        # 移動速度
        self.speed = 3
        self.speed_oblique = ((self.speed** 2) / 2)** 0.5
        # 血量
        self.health = 100
        self.now_health = self.health
        # 護甲
        self.armor = 100
        self.now_armor = self.armor
        # 生命數
        self.lives = 0
        # 傷害百分比
        self.damageMagnification = 1
        # 彈匣彈量
        self.magazine_bullets_original = 30
        self.magazine_bullets = self.magazine_bullets_original
        self.last_magazine_bullets = self.magazine_bullets
        # 射擊模式: auto, single
        self.shoot_mode = "auto"
        # auto模式下射擊速度
        self.shooting_interval = 300
        # reload所需時間
        self.reloadtime = 2800
        # 上次射擊時間
        self.last_shoot_time = 0
        # 上次重新裝填時間
        self.last_reloadtime = 0
        self.hidden = False
        self.hide_time = 0
        # 方向
        self.direction = "Right"
        self.last_direction = self.direction
        self.image_frame = 0
        self.changeImageTime = 100
        self.lastChangeImageTime = pygame.time.get_ticks()
        self.pressed_reload_key = False
        self.startReloadBullet = False
        self.play_reload_sound = False
        if GameSave_content['difficult'] == "easy":
            self.health *= 1.2
            self.now_health = self.health
            self.lives = 2
            self.damageMagnification = self.damageMagnification * 1.2
        elif GameSave_content['difficult'] == "normal":
            self.health *= 1
            self.now_health = self.health
            self.lives = 1
            self.damageMagnification = self.damageMagnification * 1
        elif GameSave_content['difficult'] == "hard":
            self.health *= 1
            self.now_health = self.health
            self.lives = 0
            self.damageMagnification = self.damageMagnification * 0.8
    
    def update(self):
        now = pygame.time.get_ticks()

        # 取得鍵盤輸入
        key_pressed = pygame.key.get_pressed()
        # # 左上
        # if key_pressed[pygame.K_w] and key_pressed[pygame.K_a]:
        #     self.direction = "Left"
        #     self.rotate()
        #     self.rect.x -= self.speed_oblique
        #     self.rect.y -= self.speed_oblique
        # # 右上
        # elif key_pressed[pygame.K_w] and key_pressed[pygame.K_d]:
        #     self.direction = "Right"
        #     self.rotate()
        #     self.rect.x += self.speed_oblique
        #     self.rect.y -= self.speed_oblique
        # # 左下
        # elif key_pressed[pygame.K_s] and key_pressed[pygame.K_a]:
        #     self.direction = "Left"
        #     self.rotate()
        #     self.rect.x -= self.speed_oblique
        #     self.rect.y += self.speed_oblique
        # # 右下
        # elif key_pressed[pygame.K_s] and key_pressed[pygame.K_d]:
        #     self.direction = "Right"
        #     self.rotate()
        #     self.rect.x += self.speed_oblique
        #     self.rect.y += self.speed_oblique
        # 上
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            self.rotate()
            self.rect.y -= self.speed
        # 左
        elif key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            # if self.direction != "Right":
            #     self.direction = "Left"
            self.rotate()
            self.rect.x -= self.speed
        # 下
        elif key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
            self.rotate()
            self.rect.y += self.speed
        # 右
        elif key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            # if self.direction != "Right":
            #     self.direction = "Right"
            self.rotate()
            self.rect.x += self.speed
        # if key_pressed[pygame.K_SPACE]:
        #     if now - self.last_shoot_time >= self.shooting_interval and self.shoot_mode == "auto":
        #         self.shoot()
        if key_pressed[pygame.K_r] and not self.pressed_reload_key:
            self.pressed_reload_key = True
            self.reload()

        # 取得滑鼠位置
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.difference_x = self.mouse_x - self.rect.centerx
        self.difference_y = self.mouse_y - self.rect.centery
        # 角色方向
        # 第一象限
        if self.difference_x > 0 and self.difference_y < 0:
            if self.direction != "Right":
                self.direction = "Right"
        # 第二象限
        elif self.difference_x < 0 and self.difference_y < 0:
            if self.direction != "Left":
                self.direction = "Left"
        # 第三象限
        elif self.difference_x < 0 and self.difference_y > 0:
            if self.direction != "Left":
                self.direction = "Left"
        # 第四象限
        elif self.difference_x > 0 and self.difference_y > 0:
            if self.direction != "Right":
                self.direction = "Right"
        
        # 重生前的隱身
        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.center = (WIDTH / 2, HEIGHT / 2)

        # 將角色控制在邊界
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT and not self.hidden:
            self.rect.bottom = HEIGHT
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        # 重新裝填彈藥
        self.reload()

    def rotate(self):
        now = pygame.time.get_ticks()
        if self.last_direction == self.direction and now - self.lastChangeImageTime > self.changeImageTime:
            if self.direction == "Left":
                centery = self.rect.centery
                left = self.rect.left
                self.image = image_player_soldier[self.direction][self.image_frame]
                self.rect = self.image.get_rect()
                self.rect.centery = centery
                self.rect.left = left
                self.last_direction = self.direction
                if self.image_frame == 2:
                    self.image_frame = 0
                else:
                    self.image_frame += 1
                self.lastChangeImageTime = now
            elif self.direction == "Right":
                centery = self.rect.centery
                right = self.rect.right
                self.image = image_player_soldier[self.direction][self.image_frame]
                self.rect = self.image.get_rect()
                self.rect.centery = centery
                self.rect.right = right
                self.last_direction = self.direction
                if self.image_frame == 2:
                    self.image_frame = 0
                else:
                    self.image_frame += 1
                self.lastChangeImageTime = now
        elif self.last_direction != self.direction:
            center = self.rect.center
            self.image = image_player_soldier[self.direction][0]
            self.image_frame = 1
            self.rect = self.image.get_rect()
            self.rect.center = center
            self.lastChangeImageTime = now
            self.last_direction = self.direction

    def reload(self):
        now = pygame.time.get_ticks()
        if self.last_magazine_bullets == 0 and not self.startReloadBullet:
            self.last_reloadtime = now
            self.startReloadBullet = True
            self.play_reload_sound = True
        elif self.pressed_reload_key and self.last_magazine_bullets < self.magazine_bullets and not self.startReloadBullet:
            self.last_reloadtime = now
            self.startReloadBullet = True
            self.last_magazine_bullets = 0
            self.pressed_reload_key = True
            self.play_reload_sound = True
        elif self.pressed_reload_key and self.last_magazine_bullets >= self.magazine_bullets and not self.startReloadBullet:
            self.pressed_reload_key = False
        if self.last_magazine_bullets == 0 and now - self.last_reloadtime >= self.reloadtime - 550 and self.play_reload_sound:
            sound_rifle_reload.play()
            self.play_reload_sound = False
        if self.last_magazine_bullets == 0 and now - self.last_reloadtime >= self.reloadtime:
            self.last_magazine_bullets = self.magazine_bullets
            self.startReloadBullet = False
            if self.pressed_reload_key:
                self.pressed_reload_key = False
            if self.play_reload_sound:
                self.play_reload_sound = False

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + HEIGHT)

class Level_1_enemy_soldier(pygame.sprite.Sprite):
    def __init__(self, surf, enemy_centerx, enemy_centery, spawn_center):
        pygame.sprite.Sprite.__init__(self)
        self.surf = surf
        self.enemy_centerx = enemy_centerx
        self.enemy_centery = enemy_centery
        # self.image_original = pygame.Surface((45, 45))
        # self.image_original.fill((255, 0, 0))
        self.image_original = image_enemy_soldier['Right'][0]
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        # self.radius = 15
        self.direction = "Right"
        self.choice_move_direction = 1
        self.last_shoot_time = 0
        self.startReloadBullet = False
        self.last_reloadtime = 0
        self.hitted = False
        # 敵人生成點
        self.rect.centerx , self.rect.centery = spawn_center
        # 移動速度
        self.speedx = 2
        self.speedy = 2
        # 視野距離
        self.frontView = 250
        # 預設屬性
        # 血量
        self.health = 80
        # 傷害百分比
        self.damageMagnification = 1
        # 剩餘子彈
        self.last_moveAmount = 0
        # 彈匣彈量
        self.magazine_bullets_original = 30
        # 射擊速度
        self.shooting_interval = 450
        # reload 速度
        self.reloadtime = 5000
        self.magazine_bullets = self.magazine_bullets_original
        self.last_magazine_bullets = self.magazine_bullets
        # 動畫設定
        self.last_direction = self.direction
        self.image_frame = 0
        self.changeImageTime = 100
        self.lastChangeImageTime = pygame.time.get_ticks()
        # 難度
        if GameSave_content['difficult'] == "easy":
            self.health *= 1
            self.now_health = self.health
            self.damageMagnification *= 0.8
        elif GameSave_content['difficult'] == "normal":
            self.health *= 1
            self.now_health = self.health
            self.damageMagnification *= 1
        elif GameSave_content['difficult'] == "hard":
            self.health *= 1.5
            self.now_health = self.health
            self.damageMagnification *= 1.2
            self.magazine_bullets_original = 45
            self.magazine_bullets = self.magazine_bullets_original

    def update(self):
        now = pygame.time.get_ticks()
        
        # 將角色控制在邊界
        if self.rect.top < 0:
            self.rect.top = 0
            self.last_moveAmount = 0
        if self.rect.left < 0:
            self.rect.left = 0
            self.last_moveAmount = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.last_moveAmount = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.last_moveAmount = 0

        self.move()

        if self.detect_enemy() and (now - self.last_shoot_time) >= self.shooting_interval:
            sound_rifle_shoot.play()
            self.shoot()
        else:
            self.shooting = False

        # 重新裝填彈藥
        self.reload()

    def move(self):
        # 上 => spawnArea = 1
        # 左 => spawnArea = 2
        # 下 => spawnArea = 3
        # 右 => spawnArea = 4
        if self.last_moveAmount == 0:
            self.choice_move_direction = random.randint(1, 4)
            self.last_moveAmount += random.randint(1, 150)
        if self.choice_move_direction == 1:
            self.direction = "Up"
            self.rotate()
            self.rect.centery -= self.speedy
            self.last_moveAmount -= 1
        elif self.choice_move_direction == 2:
            self.direction = "Left"
            self.rotate()
            self.rect.centerx -= self.speedx
            self.last_moveAmount -= 1
        elif self.choice_move_direction == 3:
            self.direction = "Down"
            self.rotate()
            self.rect.centery += self.speedy
            self.last_moveAmount -= 1
        elif self.choice_move_direction == 4:
            self.direction = "Right"
            self.rotate()
            self.rect.centerx += self.speedx
            self.last_moveAmount -= 1

    def rotate(self):
        now = pygame.time.get_ticks()
        if self.last_direction == self.direction and now - self.lastChangeImageTime > self.changeImageTime:
            if self.direction == "Left":
                if self.image_frame >= 3:
                    self.image_frame = 0
                center = self.rect.center
                self.image = image_enemy_soldier[self.direction][self.image_frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.last_direction = self.direction
                if self.image_frame == 2:
                    self.image_frame = 0
                else:
                    self.image_frame += 1
                self.lastChangeImageTime = now
            elif self.direction == "Right":
                center = self.rect.center
                self.image = image_enemy_soldier[self.direction][self.image_frame]
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.last_direction = self.direction
                if self.image_frame == 2:
                    self.image_frame = 0
                else:
                    self.image_frame += 1
                self.lastChangeImageTime = now
        elif self.direction == "Up":
            if now - self.lastChangeImageTime > self.changeImageTime:
                if self.last_direction == "Right":
                    center = self.rect.center
                    self.image = image_enemy_soldier[self.direction][self.image_frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    self.last_direction = "Right"
                    if self.image_frame == 2:
                        self.image_frame = 0
                    else:
                        self.image_frame += 1
                    self.lastChangeImageTime = now
                elif self.last_direction == "Left":
                    center = self.rect.center
                    self.image = image_enemy_soldier[self.direction][self.image_frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    self.last_direction = "Left"
                    if self.image_frame == 5:
                        self.image_frame = 3
                    else:
                        self.image_frame += 1
                    self.lastChangeImageTime = now
        elif self.direction == "Down":
            if now - self.lastChangeImageTime > self.changeImageTime:
                if self.last_direction == "Right":
                    center = self.rect.center
                    self.image = image_enemy_soldier[self.direction][self.image_frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    self.last_direction = "Right"
                    if self.image_frame == 2:
                        self.image_frame = 0
                    else:
                        self.image_frame += 1
                    self.lastChangeImageTime = now
                elif self.last_direction == "Left":
                    center = self.rect.center
                    self.image = image_enemy_soldier[self.direction][self.image_frame]
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    self.last_direction = "Left"
                    if self.image_frame == 5:
                        self.image_frame = 3
                    else:
                        self.image_frame += 1
                    self.lastChangeImageTime = now
        elif self.last_direction != self.direction:
            if self.direction == "Right" or self.direction == "Left":
                center = self.rect.center
                self.image = image_enemy_soldier[self.direction][0]
                self.image_frame = 1
                self.rect = self.image.get_rect()
                self.rect.center = center
                self.lastChangeImageTime = now
                self.last_direction = self.direction
            elif self.direction == "Up":
                if self.last_direction == "Right":
                    center = self.rect.center
                    self.image = image_enemy_soldier[self.direction][0]
                    self.image_frame = 1
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    self.lastChangeImageTime = now
                elif self.last_direction == "Left":
                    center = self.rect.center
                    self.image = image_enemy_soldier[self.direction][3]
                    self.image_frame = 4
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    self.lastChangeImageTime = now
            elif self.direction == "Down":
                if self.last_direction == "Right":
                    center = self.rect.center
                    self.image = image_enemy_soldier[self.direction][0]
                    self.image_frame = 1
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    self.lastChangeImageTime = now
                elif self.last_direction == "Left":
                    center = self.rect.center
                    self.image = image_enemy_soldier[self.direction][3]
                    self.image_frame = 4
                    self.rect = self.image.get_rect()
                    self.rect.center = center
                    self.lastChangeImageTime = now

    def shoot(self):
        now = pygame.time.get_ticks()
        if self.last_magazine_bullets > 0:
            self.shooting = True
            self.last_shoot_time = now
            bullet = Bullet_rifle_enemy(self.rect.centerx, self.rect.centery, self.direction)
            Level_1_all_sprites.add(bullet)
            Level_1_bullets.add(bullet)
            Level_1_enemy_bullets.add(bullet)
            self.last_magazine_bullets -= 1

    def reload(self):
        now = pygame.time.get_ticks()
        # 重新裝填彈藥
        if self.last_magazine_bullets == 0 and not self.startReloadBullet:
            self.last_reloadtime = now
            self.startReloadBullet = True
        elif self.last_magazine_bullets <= 10 and not self.startReloadBullet and not self.shooting:
            self.last_reloadtime = now
            self.startReloadBullet = True
        if self.last_magazine_bullets == 0 and now - self.last_reloadtime >= self.reloadtime:
            self.last_magazine_bullets = self.magazine_bullets
            self.startReloadBullet = False

    def detect_enemy(self):
        self.topright_x, self.topright_y = self.rect.topright
        self.bottomleft_x, self.bottomleft_y = self.rect.bottomleft
        self.bottomright_x, self.bottomright_y = self.rect.bottomright
        # 在上方
        if self.direction == "Up" and (self.rect.x - 20) < self.enemy_centerx < (self.topright_x + 20) and (self.rect.top - self.frontView) < self.enemy_centery < self.rect.top:
            return True
        # 在左方
        elif self.direction == "Left" and (self.rect.left - self.frontView) < self.enemy_centerx < self.rect.left and (self.rect.y - 20) < self.enemy_centery < (self.bottomleft_y + 20):
            return True
        # 在下方
        elif self.direction == "Down" and (self.bottomleft_x - 20) < self.enemy_centerx < (self.bottomright_x + 20) and self.rect.bottom < self.enemy_centery < (self.rect.bottom + self.frontView):
            return True
        # 在右方
        elif self.direction == "Right" and (self.rect.right) < self.enemy_centerx < (self.rect.right + self.frontView) and (self.topright_y - 20) < self.enemy_centery < (self.bottomright_y + 20):
            return True
        else:
            return False

class SandBag(pygame.sprite.Sprite):
    def __init__(self, surf, center_x, center_y, rotate):
        pygame.sprite.Sprite.__init__(self)
        self.surf = surf
        self.center_x = center_x
        self.center_y = center_y
        self.rotate = rotate
        self.image_original = image_sandBag_front
        self.chooseImageAndRotate()
        self.image = self.image_original
        # self.image_original = pygame.Surface((90, 30))
        # self.image_original.fill((255, 255, 0))
        # self.image = pygame.transform.rotate(self.image_original, self.rotate)
        self.rect = self.image.get_rect()
        self.rect.centerx , self.rect.centery = self.center_x, self.center_y
        self.hitted = False
        # 屬性
        self.health = 300
        # 難度
        if GameSave_content['difficult'] == "easy":
            self.health *= 2
            self.now_health = self.health
        elif GameSave_content['difficult'] == "normal":
            self.health *= 1
            self.now_health = self.health
        elif GameSave_content['difficult'] == "hard":
            self.health *= 0.75
            self.now_health = self.health
    
    def chooseImageAndRotate(self):
        # if 0 <= self.rotate < 90 or -90 < self.rotate <= 0:
        #     self.image_original = image_sandBag_front
        # elif 90 <= self.rotate < 180 or -270 <= self.rotate < -180:
        #     self.image_original = image_sandBag_front
        # elif 180 <= self.rotate < 270:
        #     self.image_original = image_sandBag_front
        # elif 270 <= self.rotate < 360 or 0 -180 < self.rotate <= -90:
        #     self.image_original = image_sandBag_front
        if self.rotate == 0:
            self.image_original = image_sandBag_front
        elif self.rotate == 90:
            self.image_original = image_sandBag_right
        elif self.rotate == 180:
            self.image_original = image_sandBag_front
        elif self.rotate == 270:
            self.image_original = image_sandBag_right

class Level_1_rifle(pygame.sprite.Sprite):
    def __init__(self, surf, equipment_role):
        pygame.sprite.Sprite.__init__(self)
        self.surf = surf
        self.image_weapons_original = image_weapon_M4A1
        self.image_weapons_FlipHorizontally_original = image_weapon_M4A1_FlipHorizontally
        self.image = self.image_weapons_original.copy()
        self.rect = self.image.get_rect()
        self.equipment_role = equipment_role
        self.rect.centerx = self.equipment_role.rect.centerx
        self.rect.centery = self.equipment_role.rect.centery - 18
    
    def update(self):
        now = pygame.time.get_ticks()
        self.rect.centerx = self.equipment_role.rect.centerx
        self.rect.centery = self.equipment_role.rect.centery - 18
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.weapon_difference_x = self.mouse_x - self.rect.centerx
        self.weapon_difference_y = self.mouse_y - self.rect.centery
        self.weapon_hypotenuse = (((self.weapon_difference_x** 2) + (self.weapon_difference_y** 2))** 0.5)
        # 更新武器方向
        self.rotate()
        # 取得滑鼠輸入
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed == (1, 0, 0):
            if now - self.equipment_role.last_shoot_time >= self.equipment_role.shooting_interval and self.equipment_role.shoot_mode == "auto":
                self.shoot()

    def rotate(self):
        # 第一象限
        if self.weapon_difference_x > 0 and self.weapon_difference_y < 0:
            self.image = pygame.transform.rotate(self.image_weapons_original, (int((math.acos(self.weapon_difference_x / self.weapon_hypotenuse) / math.pi) * 180)))
        # 第二象限
        elif self.weapon_difference_x < 0 and self.weapon_difference_y < 0:
            self.image = pygame.transform.rotate(self.image_weapons_FlipHorizontally_original, (int((math.acos(self.weapon_difference_x / self.weapon_hypotenuse) / math.pi) * 180) - 180))
        # 第三象限
        elif self.weapon_difference_x < 0 and self.weapon_difference_y > 0:
            self.image = pygame.transform.rotate(self.image_weapons_FlipHorizontally_original, -(int((math.acos(self.weapon_difference_x / self.weapon_hypotenuse) / math.pi) * 180) - 180))
        # 第四象限
        elif self.weapon_difference_x > 0 and self.weapon_difference_y > 0:
            self.image = pygame.transform.rotate(self.image_weapons_original, -(int((math.acos(self.weapon_difference_x / self.weapon_hypotenuse) / math.pi) * 180)))
        # if equipment_role.direction == "Right":
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def shoot(self):
        now = pygame.time.get_ticks()
        if not self.equipment_role.hidden:
            if self.equipment_role.last_magazine_bullets > 0:
                bullet = Bullet_rifle_player(self.rect.centerx, self.rect.centery)
                Level_1_all_sprites.add(bullet)
                Level_1_bullets.add(bullet)
                Level_1_friendly_bullets.add(bullet)
                self.equipment_role.last_magazine_bullets -= 1
                self.equipment_role.last_shoot_time = now
                sound_rifle_shoot.play()

class aimPoint(pygame.sprite.Sprite):
    def __init__(self, surf):
        pygame.sprite.Sprite.__init__(self)
        self.surf = surf
        self.image = image_aimPoint
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.rect.centerx = self.mouse_x
        self.rect.centery = self.mouse_y

class Bullet_rifle_player(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = pygame.transform.rotate(image_bullet_rifle, -90)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.centery = center_y
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.difference_x = self.mouse_x - self.rect.centerx
        self.difference_y = self.mouse_y - self.rect.centery
        self.difference_hypotenuse = ((self.difference_x** 2 + self.difference_y** 2)** 0.5)
        # 子彈飛行速度
        self.speed = 12 * (FPS / 60)
        # 子彈x, y飛行值計算
        self.scale = self.speed / self.difference_hypotenuse
        self.fly_speedx = self.difference_x * self.scale
        self.fly_speedy = self.difference_y * self.scale
        # 子彈已飛行距離
        self.flyingDistance = 0
        # 有效射程
        self.maxFlyingDistance = 400
        # 將子彈位置校正
        self.rotate()

    def update(self):
        if self.flyingDistance <= self.maxFlyingDistance:
            self.rect.x += self.fly_speedx
            self.rect.y += self.fly_speedy
            self.flyingDistance += self.speed
        if self.flyingDistance > self.maxFlyingDistance or self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

    def rotate(self):
        # 第一象限
        if self.difference_x > 0 and self.difference_y < 0:
            self.image = pygame.transform.rotate(self.image_original, (int((math.acos(self.difference_x / self.difference_hypotenuse) / math.pi) * 180)))
        # 第二象限
        elif self.difference_x < 0 and self.difference_y < 0:
            self.image = pygame.transform.rotate(self.image_original, (int((math.acos(self.difference_x / self.difference_hypotenuse) / math.pi) * 180)))
        # 第三象限
        elif self.difference_x < 0 and self.difference_y > 0:
            self.image = pygame.transform.rotate(self.image_original, -(int((math.acos(self.difference_x / self.difference_hypotenuse) / math.pi) * 180)))
        # 第四象限
        elif self.difference_x > 0 and self.difference_y > 0:
            self.image = pygame.transform.rotate(self.image_original, -(int((math.acos(self.difference_x / self.difference_hypotenuse) / math.pi) * 180)))
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

class Bullet_rifle_enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = image_bullet_rifle
        self.rect = self.image_original.get_rect()
        self.image = self.image_original.copy()
        self.rect.centerx = x
        self.rect.centery = y
        self.direction = direction
        self.speed = 12 * (FPS / 60)
        self.flyingDistance = 0
        self.maxFlyingDistance = 400

    def update(self):
        if self.direction == "Up" and self.flyingDistance <= self.maxFlyingDistance:
            self.rotate()
            self.rect.y -= self.speed
            self.flyingDistance += self.speed
        elif self.direction == "Left" and self.flyingDistance <= self.maxFlyingDistance:
            self.rotate()
            self.rect.x -= self.speed
            self.flyingDistance += self.speed
        elif self.direction == "Down" and self.flyingDistance <= self.maxFlyingDistance:
            self.rotate()
            self.rect.y += self.speed
            self.flyingDistance += self.speed
        elif self.direction == "Right" and self.flyingDistance <= self.maxFlyingDistance:
            self.rotate()
            self.rect.x += self.speed
            self.flyingDistance += self.speed
        if self.flyingDistance > self.maxFlyingDistance or self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

    def rotate(self):
        if self.direction == "Up":
            self.image = pygame.transform.rotate(self.image_original, 0)
        elif self.direction == "Left":
            self.image = pygame.transform.rotate(self.image_original, 90)
        elif self.direction == "Down":
            self.image = pygame.transform.rotate(self.image_original, 180)
        elif self.direction == "Right":
            self.image = pygame.transform.rotate(self.image_original, 270)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

class Level_1_powerItem(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = {}
        self.image_original['Medkit'] = image_medkit
        self.image_original['ArmorPack'] = image_armorpack
        self.image_original['LargeMagazine'] = image_large_magazine_rifle
        self.image_original['HighSpeedReload'] = image_highspeed_reload_magazine_rifle
        self.powerType = random.choice(['Medkit', 'ArmorPack', 'LargeMagazine', 'HighSpeedReload'])
        self.image = self.image_original[self.powerType].copy()
        self.rect = self.image.get_rect()
        self.rect.center = center

# 第二關
def Level_2_draw_levelTrip():
    screen.blit(image_background_level2Trip, (0, 0))
    draw_text("tl", screen, '鎮守前線', (255, 255, 255), 48, True, 40 * (WIDTH / 1280), 46 * (HEIGHT / 720))
    draw_text("tl", screen, '空軍作戰指揮部收到訊息', (255, 255, 255), 22, False, 45 * (WIDTH / 1280), 136 * (HEIGHT / 720))
    draw_text("tl", screen, '發現有數架敵方高科技轟炸機、戰鬥機正在向領空範圍前進', (255, 255, 255), 22, False, 45 * (WIDTH / 1280), 168 * (HEIGHT / 720))
    draw_text("tl", screen, '作戰指揮部派遣戰術戰鬥機聯隊前往攔截敵方轟炸機', (255, 255, 255), 22, False, 45 * (WIDTH / 1280), 200 * (HEIGHT / 720))
    draw_text("tl", screen, '同時進行敵方基地的偵察任務', (255, 255, 255), 22, False, 45 * (WIDTH / 1280), 264 * (HEIGHT / 720))
    draw_text("center", screen, 'WASD 或 ↑←↓→ 操控方向', (255, 255, 255), 16, False, WIDTH / 2, (580 * (HEIGHT / 720)) + 8)
    draw_text("center", screen, '空白建 進行射擊 B鍵 切換武器', (255, 255, 255), 16, False, WIDTH / 2, (610 * (HEIGHT / 720)) + 8)
    draw_text("center", screen, '按任意鍵開始', (255, 255, 255), 16, False, WIDTH / 2, (640 * (HEIGHT / 720)) + 8)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

def Level_2_new_rocks():
    rock = Rock()
    Level_2_all_sprites.add(rock)
    Level_2_rocks.add(rock)

def Level_2_summon_powerItem(center):
    # 隨機掉落道具
    if GameSave_content['difficult'] == "easy" and random.random() >= 0.65:
        power = Level_2_powerItem(center)
        Level_2_all_sprites.add(power)
        Level_2_powerItems_group.add(power)
    elif GameSave_content['difficult'] == "normal" and random.random() >= 0.8:
        power = Level_2_powerItem(center)
        Level_2_all_sprites.add(power)
        Level_2_powerItems_group.add(power)
    elif GameSave_content['difficult'] == "hard" and random.random() >= 0.9:
        power = Level_2_powerItem(center)
        Level_2_all_sprites.add(power)
        Level_2_powerItems_group.add(power)

class Level_2_Player_plane(pygame.sprite.Sprite):
    def __init__(self, surf):
        pygame.sprite.Sprite.__init__(self)
        self.surf = surf
        self.image_original = pygame.transform.scale(image_player_plane, (178, 128))
        # self.image_original = pygame.Surface((40, 50))
        # self.image_original.fill((0, 255, 0))
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT - 15
        # 移動速度
        self.speed = 4
        # 血量
        self.health = 200
        self.now_health = self.health
        # 機甲
        self.armor = 1300
        self.now_armor = self.armor
        # 生命數
        self.lives = 0
        # 傷害百分比
        self.damageMagnification = 1
        # 飛彈數量
        self.missile_amount_original = 0
        self.last_missile_amount = self.missile_amount_original
        # 武器選擇: auto, missile (激光炮, 飛彈)
        self.shoot_mode = "auto"
        # 激光炮數量
        self.gun = 1
        self.gun_turboTime = 0
        # auto模式下射擊速度
        self.shooting_interval = 300
        # 上次射擊時間
        self.last_shoot_time = 0
        # 飛彈冷卻時間
        self.missile_colddown = 3000
        # 上次發射飛彈時間
        self.last_launchMissile_time = 0
        self.hidden = False
        self.hide_time = 0
        if GameSave_content['difficult'] == "easy":
            # 血量
            self.health *= 1.2
            self.now_health = self.health
            # 機甲
            self.armor *= 1.2
            self.now_armor = self.armor
            # 生命數
            self.lives = 2
            # 傷害百分比
            self.damageMagnification = self.damageMagnification * 1.2
            # 飛彈數量
            self.missile_amount_original = 20
            self.last_missile_amount = self.missile_amount_original
        elif GameSave_content['difficult'] == "normal":
            # 血量
            self.health *= 1
            self.now_health = self.health
            # 機甲
            self.armor *= 1
            self.now_armor = self.armor
            # 生命數
            self.lives = 1
            # 傷害百分比
            self.damageMagnification = self.damageMagnification * 1
            # 飛彈數量
            self.missile_amount_original = 15
            self.last_missile_amount = self.missile_amount_original
        elif GameSave_content['difficult'] == "hard":
            # 血量
            self.health *= 1
            self.now_health = self.health
            # 機甲
            self.armor *= 0.8
            self.now_armor = self.armor
            # 生命數
            self.lives = 0
            # 傷害百分比
            self.damageMagnification = self.damageMagnification * 0.8
            # 飛彈數量
            self.missile_amount_original = 10
            self.last_missile_amount = self.missile_amount_original
    
    def update(self):
        now = pygame.time.get_ticks()

        # 取得鍵盤輸入
        key_pressed = pygame.key.get_pressed()
        # 上
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            self.rect.y -= self.speed
        # 左
        elif key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speed
        # 下
        elif key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
            self.rect.y += self.speed
        # 右
        elif key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if key_pressed[pygame.K_SPACE]:
            self.shoot()

        # 重生前的隱身
        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.center = (WIDTH / 2, HEIGHT / 2)

        # 將角色控制在邊界
        if self.rect.top < 230:
            self.rect.top = 230
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT and not self.hidden:
            self.rect.bottom = HEIGHT
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        now = pygame.time.get_ticks()
        if not self.hidden:
            if self.shoot_mode == "auto":
                if self.gun == 1:
                    if now - self.last_shoot_time > self.shooting_interval:
                        lazer = Bullet_laser_player(self.rect.centerx, self.rect.centery)
                        Level_2_all_sprites.add(lazer)
                        Level_2_lazers.add(lazer)
                        Level_2_friendly_lazers.add(lazer)
                        self.last_shoot_time = now
                        sound_laser_launcher.play()
                elif self.gun == 2:
                    if now - self.last_shoot_time > self.shooting_interval:
                        lazer1 = Bullet_laser_player(self.rect.centerx - 30, self.rect.centery)
                        lazer2 = Bullet_laser_player(self.rect.centerx + 30, self.rect.centery)
                        Level_2_all_sprites.add(lazer1)
                        Level_2_all_sprites.add(lazer2)
                        Level_2_lazers.add(lazer1)
                        Level_2_lazers.add(lazer2)
                        Level_2_friendly_lazers.add(lazer1)
                        Level_2_friendly_lazers.add(lazer2)
                        self.last_shoot_time = now
                        sound_laser_launcher.play()
            if self.shoot_mode == "missile":
                if now - self.last_launchMissile_time > self.missile_colddown and self.last_missile_amount > 0:
                    self.last_missile_amount -= 1
                    missile = Bullet_missile_player(self.rect.centerx, self.rect.centery)
                    Level_2_all_sprites.add(missile)
                    Level_2_missiles.add(missile)
                    Level_2_friendly_missiles.add(missile)
                    self.last_launchMissile_time = now
                    sound_missile_launcher.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + HEIGHT)

class Level_2_enemy_plane(pygame.sprite.Sprite):
    def __init__(self, surf, centerx, centery):
        pygame.sprite.Sprite.__init__(self)
        self.surf = surf
        self.image_original = pygame.transform.scale(image_enemy_plane, (189, 141))
        # self.image_original = pygame.Surface((40, 50))
        # self.image_original.fill((255, 150, 50))
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = centerx
        self.rect.centery = centery
        # 移動速度
        self.speed = 4
        # 血量
        self.health = 400
        self.now_health = self.health
        # 機甲
        self.armor = 500
        self.now_armor = self.armor
        # 傷害百分比
        self.damageMagnification = 1
        # 飛彈數量
        self.missile_amount_original = 0
        self.last_missile_amount = self.missile_amount_original
        # 武器選擇: auto, missile (激光炮, 飛彈)
        self.shoot_mode = "auto"
        # auto模式下射擊速度
        self.shooting_interval = 400
        # 上次射擊時間
        self.last_shoot_time = 0
        # 飛彈冷卻時間
        self.missile_colddown = 3000
        # 上次發射飛彈時間
        self.last_launchMissile_time = 0
        # 是否開火
        self.start_shoot = False
        self.start_shootTime = 0
        # 使用雷射持續
        self.usingLazer_ValidityPeriod = 6000
        # 使用飛彈持續
        self.usingMissile_ValidityPeriod = 10000
        # 武器使用冷卻
        self.shootAction_colddown = False
        self.shootAction_colddownTime = 5000
        self.shootAction_colddownSt = 0
        # 移動冷卻
        self.move_colddown = 1000
        self.last_moveTime = 0
        self.last_moveAmount = 0
        self.hitted = False
        if GameSave_content['difficult'] == "easy":
            # 血量
            self.health *= 0.8
            self.now_health = self.health
            # 機甲
            self.armor *= 0.8
            self.now_armor = self.armor
            # 傷害百分比
            self.damageMagnification = self.damageMagnification * 0.8
            # 飛彈數量
            self.missile_amount_original = 10
            self.last_missile_amount = self.missile_amount_original
        elif GameSave_content['difficult'] == "normal":
            # 血量
            self.health *= 1
            self.now_health = self.health
            # 機甲
            self.armor *= 1
            self.now_armor = self.armor
            # 傷害百分比
            self.damageMagnification = self.damageMagnification * 1
            # 飛彈數量
            self.missile_amount_original = 15
            self.last_missile_amount = self.missile_amount_original
        elif GameSave_content['difficult'] == "hard":
            # 血量
            self.health *= 1.2
            self.now_health = self.health
            # 機甲
            self.armor *= 1.2
            self.now_armor = self.armor
            # 傷害百分比
            self.damageMagnification = self.damageMagnification * 1.2
            # 飛彈數量
            self.missile_amount_original = 20
            self.last_missile_amount = self.missile_amount_original
    
    def update(self):
        now = pygame.time.get_ticks()

        if not self.start_shoot and not self.shootAction_colddown:
            self.choice_shoot_mode = random.randint(1, 3)
            if self.choice_shoot_mode == 1:
                self.shoot_mode = "auto"
                self.start_shootTime = now
                self.start_shoot = True
            elif self.choice_shoot_mode == 2 and self.last_missile_amount > 0:
                self.shoot_mode = "missile"
                self.start_shootTime = now
                self.start_shoot = True
            elif self.choice_shoot_mode == 3:
                self.shootAction_colddown = True
                self.shootAction_colddownSt = now

        if self.start_shoot:
            if now - self.start_shootTime <= self.usingLazer_ValidityPeriod:
                self.shoot()
            else:
                self.start_shoot = False
        elif self.shootAction_colddown:
            if now - self.shootAction_colddownSt > self.shootAction_colddownTime:
                self.shootAction_colddown = False

        self.move()

        # 將角色控制在邊界
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def move(self):
        now = pygame.time.get_ticks()
        # 左 => spawnArea = 1
        # 右 => spawnArea = 2
        if self.last_moveAmount == 0 and now - self.last_moveTime > self.move_colddown:
            self.choice_move_direction = random.randint(1, 2)
            self.last_moveAmount += random.randint(1, 40)
            self.DoneMove = False
        if self.choice_move_direction == 1 and self.last_moveAmount > 0:
            self.rect.centerx -= self.speed
            self.last_moveAmount -= 1
        elif self.choice_move_direction == 2 and self.last_moveAmount > 0:
            self.rect.centerx += self.speed
            self.last_moveAmount -= 1
        if self.last_moveAmount == 0 and not self.DoneMove:
            self.last_moveTime = now
            self.DoneMove = True

    def shoot(self):
        now = pygame.time.get_ticks()
        if self.shoot_mode == "auto":
            if now - self.last_shoot_time > self.shooting_interval:
                lazer = Bullet_laser_enemy(self.rect.centerx, self.rect.centery)
                Level_2_all_sprites.add(lazer)
                Level_2_lazers.add(lazer)
                Level_2_enemy_lazers.add(lazer)
                self.last_shoot_time = now
                sound_laser_launcher.play()
        if self.shoot_mode == "missile":
            if now - self.last_launchMissile_time > self.missile_colddown and self.last_missile_amount > 0:
                self.last_missile_amount -= 1
                missile = Bullet_missile_enemy(self.rect.centerx, self.rect.centery)
                Level_2_all_sprites.add(missile)
                Level_2_missiles.add(missile)
                Level_2_enemy_missiles.add(missile)
                self.last_launchMissile_time = now
                sound_missile_launcher.play()

class Level_2_enemy_BOSS_plane(pygame.sprite.Sprite):
    def __init__(self, surf, centerx, centery):
        pygame.sprite.Sprite.__init__(self)
        self.surf = surf
        self.image_original = pygame.transform.scale(image_enemy_plane_BOSS, (283, 212))
        # self.image_original = pygame.Surface((40, 50))
        # self.image_original.fill((255, 150, 50))
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = centerx
        self.rect.centery = centery
        # 移動速度
        self.speed = 5
        # 血量
        self.health = 1000
        self.now_health = self.health
        # 機甲
        self.armor = 1000
        self.now_armor = self.armor
        # 傷害百分比
        self.damageMagnification = 1
        # 飛彈數量
        self.missile_amount_original = 0
        self.last_missile_amount = self.missile_amount_original
        # 武器選擇: auto, missile (激光炮, 飛彈)
        self.shoot_mode = "auto"
        # auto模式下射擊速度
        self.shooting_interval = 300
        # 上次射擊時間
        self.last_shoot_time = 0
        # 飛彈冷卻時間
        self.missile_colddown = 3000
        # 上次發射飛彈時間
        self.last_launchMissile_time = 0
        # 是否開火
        self.start_shoot = False
        self.start_shootTime = 0
        # 使用雷射持續
        self.usingLazer_ValidityPeriod = 6000
        # 使用飛彈持續
        self.usingMissile_ValidityPeriod = 10000
        # 武器使用冷卻
        self.shootAction_colddown = False
        self.shootAction_colddownTime = 5000
        self.shootAction_colddownSt = 0
        # 移動冷卻
        self.move_colddown = 1000
        self.last_moveTime = 0
        self.last_moveAmount = 0
        self.hitted = False
        if GameSave_content['difficult'] == "easy":
            # 血量
            self.health *= 0.8
            self.now_health = self.health
            # 機甲
            self.armor *= 0.8
            self.now_armor = self.armor
            # 傷害百分比
            self.damageMagnification = self.damageMagnification * 0.8
            # 飛彈數量
            self.missile_amount_original = 9000000
            self.last_missile_amount = self.missile_amount_original
        elif GameSave_content['difficult'] == "normal":
            # 血量
            self.health *= 1
            self.now_health = self.health
            # 機甲
            self.armor *= 1
            self.now_armor = self.armor
            # 傷害百分比
            self.damageMagnification = self.damageMagnification * 1
            # 飛彈數量
            self.missile_amount_original = 9000000
            self.last_missile_amount = self.missile_amount_original
        elif GameSave_content['difficult'] == "hard":
            # 血量
            self.health *= 1.2
            self.now_health = self.health
            # 機甲
            self.armor *= 1.2
            self.now_armor = self.armor
            # 傷害百分比
            self.damageMagnification = self.damageMagnification * 1.2
            # 飛彈數量
            self.missile_amount_original = 9000000
            self.last_missile_amount = self.missile_amount_original
    
    def update(self):
        now = pygame.time.get_ticks()

        if not self.start_shoot and not self.shootAction_colddown:
            self.choice_shoot_mode = random.randint(1, 3)
            if self.choice_shoot_mode == 1:
                self.shoot_mode = "auto"
                self.start_shootTime = now
                self.start_shoot = True
            elif self.choice_shoot_mode == 2 and self.last_missile_amount > 0:
                self.shoot_mode = "missile"
                self.start_shootTime = now
                self.start_shoot = True
            elif self.choice_shoot_mode == 3:
                self.shootAction_colddown = True
                self.shootAction_colddownSt = now

        if self.start_shoot:
            if now - self.start_shootTime <= self.usingLazer_ValidityPeriod:
                self.shoot()
            else:
                self.start_shoot = False
        elif self.shootAction_colddown:
            if now - self.shootAction_colddownSt > self.shootAction_colddownTime:
                self.shootAction_colddown = False

        self.move()

        # 將角色控制在邊界
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def move(self):
        now = pygame.time.get_ticks()
        # 左 => spawnArea = 1
        # 右 => spawnArea = 2
        if self.last_moveAmount == 0 and now - self.last_moveTime > self.move_colddown:
            self.choice_move_direction = random.randint(1, 2)
            self.last_moveAmount += random.randint(1, 50)
            self.DoneMove = False
        if self.choice_move_direction == 1 and self.last_moveAmount > 0:
            self.rect.centerx -= self.speed
            self.last_moveAmount -= 1
        elif self.choice_move_direction == 2 and self.last_moveAmount > 0:
            self.rect.centerx += self.speed
            self.last_moveAmount -= 1
        if self.last_moveAmount == 0 and not self.DoneMove:
            self.last_moveTime = now
            self.DoneMove = True

    def shoot(self):
        now = pygame.time.get_ticks()
        if self.shoot_mode == "auto":
            if now - self.last_shoot_time > self.shooting_interval:
                lazer = Bullet_laser_enemy(self.rect.centerx, self.rect.centery)
                Level_2_all_sprites.add(lazer)
                Level_2_lazers.add(lazer)
                Level_2_enemy_lazers.add(lazer)
                self.last_shoot_time = now
                sound_laser_launcher.play()
        if self.shoot_mode == "missile":
            if now - self.last_launchMissile_time > self.missile_colddown and self.last_missile_amount > 0:
                self.last_missile_amount -= 1
                missile = Bullet_missile_enemy(self.rect.centerx, self.rect.centery)
                Level_2_all_sprites.add(missile)
                Level_2_missiles.add(missile)
                Level_2_enemy_missiles.add(missile)
                self.last_launchMissile_time = now
                sound_missile_launcher.play()
    
    def skill(self, skillNumber):
        lazer = {}
        missile = {}
        if skillNumber == 1:
            for i in range(1, 21):
                lazer[i] = Bullet_laser_enemy(i * (WIDTH / 21), 50)
                Level_2_all_sprites.add(lazer[i])
                Level_2_lazers.add(lazer[i])
                Level_2_enemy_lazers.add(lazer[i])
                sound_laser_launcher.play()
        if skillNumber == 2:
            for i in range(1, 9):
                missile[i] = Bullet_missile_enemy(i * (WIDTH / 9), 50)
                Level_2_all_sprites.add(missile[i])
                Level_2_missiles.add(missile[i])
                Level_2_enemy_missiles.add(missile[i])
            sound_missile_launcher.play()
        if skillNumber == 3:
            for i in range(1, 17):
                missile[i] = Bullet_missile_enemy(i * (WIDTH / 17), 50)
                Level_2_all_sprites.add(missile[i])
                Level_2_missiles.add(missile[i])
                Level_2_enemy_missiles.add(missile[i])
            sound_missile_launcher.play()

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.size = random.randint(20, 45)
        # self.image_original = pygame.Surface((self.size, self.size))
        self.image_original = pygame.transform.scale(image_rock, (self.size, self.size))
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        # pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(2, 8)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedx = random.randrange(-2, 2)
            self.speedy = random.randrange(2, 8)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_original, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

class Bullet_laser_player(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        pygame.sprite.Sprite.__init__(self)
        # self.image_original = pygame.Surface((6, 20))
        # self.image_original.fill((255, 255, 255))
        self.image_original = image_bullet_laser
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.centery = center_y
        # 子彈飛行速度
        self.speed = 10 * (FPS / 60)
        # 子彈已飛行距離
        self.flyingDistance = 0

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Bullet_missile_player(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        pygame.sprite.Sprite.__init__(self)
        # self.image_original = pygame.Surface((12, 30))
        # self.image_original.fill((255, 255, 255))
        self.image_original = image_bullet_missile
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.centery = center_y
        # 子彈飛行速度
        self.speed = 7 * (FPS / 60)
        # 子彈已飛行距離
        self.flyingDistance = 0

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Bullet_laser_enemy(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        pygame.sprite.Sprite.__init__(self)
        # self.image_original = pygame.Surface((6, 20))
        # self.image_original.fill((255, 255, 255))
        self.image_original = image_bullet_laser
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.centery = center_y
        # 子彈飛行速度
        self.speed = 10 * (FPS / 60)
        # 子彈已飛行距離
        self.flyingDistance = 0

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Bullet_missile_enemy(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        pygame.sprite.Sprite.__init__(self)
        # self.image_original = pygame.Surface((12, 30))
        # self.image_original.fill((255, 255, 255))
        self.image_original = pygame.transform.rotate(image_bullet_missile, 180)
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.centery = center_y
        # 子彈飛行速度
        self.speed = 7 * (FPS / 60)
        # 子彈已飛行距離
        self.flyingDistance = 0

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Level_2_powerItem(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image_original = {}
        self.image_original['Medkit'] = image_medkit
        self.image_original['RepairKit'] = image_repairKit
        self.image_original['TurretUpgrade'] = image_turretUpgrade
        self.powerType = random.choice(['Medkit', 'RepairKit', 'TurretUpgrade'])
        self.image = self.image_original[self.powerType].copy()
        self.rect = self.image.get_rect()
        self.rect.center = center
        # 下墜速度
        self.speed = 2
    
    def update(self):
        self.rect.centery += self.speed
        if self.rect.bottom < 0:
            self.kill()

# 第三關
def Level_3_draw_levelTrip():
    screen.blit(main_screen_background["main"], (0, 0))
    draw_text("center", screen, '鎮守前線', (255, 255, 255), 48, True, 135 * (WIDTH / 1280), 68)
    draw_text("center", screen, '前線受到攻擊', (255, 255, 255), 22, False, 120 * (WIDTH / 1280), 112)
    draw_text("center", screen, 'WASD 或 ↑←↓→ 操控方向', (255, 255, 255), 16, False, WIDTH / 2, (580 * (HEIGHT / 720)) + 8)
    draw_text("center", screen, '空白鍵 進行射擊 R鍵 換彈', (255, 255, 255), 16, False, WIDTH / 2, (610 * (HEIGHT / 720)) + 8)
    draw_text("center", screen, '按任意鍵開始', (255, 255, 255), 16, False, WIDTH / 2, (640 * (HEIGHT / 720)) + 8)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

# 遊戲歷程展示廳
def draw_gameMarkerScreen():
    toEndingScreen_Button = SettingPanel_ArrowButton(1024, 600 * (HEIGHT / 720), "返回", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
    screen.blit(image_background_gameMarkerScreen, (0, 0))
    draw_text("center", screen, '遊戲製作', (255, 255, 255), 64, True, WIDTH / 2, 108)
    draw_text("tl", screen, '遊戲製作', (255, 255, 255), 26, True, 160, 176)
    draw_text("tl", screen, 'Kenny', (255, 255, 255), 24, False, 160, 212)
    # draw_text("tl", screen, '遊戲製作2', (255, 255, 255), 24, False, 160, 241)
    # draw_text("tl", screen, '遊戲製作3', (255, 255, 255), 24, False, 160, 270)
    draw_text("tl", screen, '美術製作', (255, 255, 255), 26, True, 160, 304)
    draw_text("tl", screen, 'Kenny', (255, 255, 255), 24, False, 160, 340)
    draw_text("tl", screen, 'BaconKnight', (255, 255, 255), 24, False, 160, 369)
    # draw_text("tl", screen, '美術3', (255, 255, 255), 24, False, 160, 398)
    draw_text("tl", screen, '測試人員', (255, 255, 255), 26, True, 160, 432)
    draw_text("tl", screen, 'BaconKnight', (255, 255, 255), 24, False, 160, 468)
    # draw_text("tl", screen, '測試人員2', (255, 255, 255), 24, False, 160, 499)
    # draw_text("tl", screen, '測試人員3', (255, 255, 255), 24, False, 160, 530)
    draw_text("tl", screen, '音樂素材', (255, 255, 255), 26, True, 500, 176)
    draw_text("tl", screen, 'YT', (255, 255, 255), 24, False, 500, 212)
    draw_text("tl", screen, 'YT音效庫', (255, 255, 255), 24, False, 500, 241)
    draw_text("tl", screen, '小森平的免費音效', (255, 255, 255), 24, False, 500, 270)
    draw_text("tl", screen, 'Terraria', (255, 255, 255), 24, False, 500, 299)
    # draw_text("tl", screen, '', (255, 255, 255), 24, False, 500, 328)
    # draw_text("center", screen, '按任意鍵返回', (255, 255, 255), 16, False, WIDTH / 2, (640 * (HEIGHT / 720)) + 8)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            # elif event.type == pygame.KEYUP:
            #     waiting = False
            #     return False
            # 滑鼠移動事件
            elif event.type == pygame.MOUSEMOTION:
                # 判斷滑鼠是否移動到按鈕範圍內
                toEndingScreen_Button.getFocus(mouse_x, mouse_y)
            # 滑鼠按下
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #滑鼠左鍵按下
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    toEndingScreen_Button.mouseDown(mouse_x, mouse_y)
            # 滑鼠彈起
            elif event.type == pygame.MOUSEBUTTONUP:
                toEndingScreen_Button.mouseUp()

        if toEndingScreen_Button.bottomMouseUp:
            toEndingScreen_Button.bottomMouseUp = False
            waiting = False
            return False
        
        toEndingScreen_Button.draw(screen)
        pygame.display.update()

# 創建按鈕
startPlayGame_Button = startPlayGameButton(WIDTH / 2, 258 * (HEIGHT / 720), "遊玩", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
gameSetting_Button = gameSettingButton(screen, WIDTH / 2, 360 * (HEIGHT / 720), "設定", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
leaveGame_Button = Button(WIDTH / 2, 462 * (HEIGHT / 720), "離開", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, leaveGame_Button_function, text_font)

# 現在時間(ticks) 1tick = 1ms
nowTime = pygame.time.get_ticks()
# 主畫面動畫設定
main_screen_background_image_frame = 0
main_screen_background_image_changeTime = 75
main_screen_background_image_lastChangeTime = 0
# 存檔讀取次數
# 0 未讀擋, 1 完成第一次讀檔
gameSave_readTimes = 0
# 開始遊戲是否被點擊
startPlayGame_Button_clicked = False
# 是否調整過設定
gameSetting_Button_Done = True
leaveGame_Button_Return = False
# 是否按下ESC
Escape_KeyDown = False
# ESC畫面回傳
escape_screen_return = False
# 關卡開頭
show_levelTrip = True

# mainScreen
while program_running:
    clock.tick(FPS)
    if random.random() >= 0.998:
        pygame.display.set_caption(Screen_display_tittle['tittle'][(random.randint(0, len(Screen_display_tittle['tittle'])) - 1)])
    # 獲得滑鼠座標
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            program_running = False
            break
        # 滑鼠移動事件
        elif event.type == pygame.MOUSEMOTION:
            # 判斷滑鼠是否移動到按鈕範圍內
            startPlayGame_Button.getFocus(mouse_x, mouse_y)
            gameSetting_Button.getFocus(mouse_x, mouse_y)
            leaveGame_Button.getFocus(mouse_x, mouse_y)
        # 滑鼠按下
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #滑鼠左鍵按下
            if pygame.mouse.get_pressed() == (1, 0, 0):
                startPlayGame_Button.mouseDown(mouse_x, mouse_y)
                gameSetting_Button.mouseDown(mouse_x, mouse_y)
                leaveGame_Button.mouseDown(mouse_x, mouse_y)
        # 滑鼠彈起
        elif event.type == pygame.MOUSEBUTTONUP:
            startPlayGame_Button_clicked = startPlayGame_Button.mouseUp(screen)
            gameSetting_Button_Done = gameSetting_Button.mouseUp()
            leaveGame_Button_Return = leaveGame_Button.mouseUp()

    if leaveGame_Button_Return:
        leaveGame_Button_Return = False
        program_running = False
        break

    # 是否調整過設定
    if gameSetting_Button_Done:
        gameSetting_Button_Done = False
        with open(CONFIG_FILE_ADDRESS, 'rb') as gameConfigFile:
            gameConfig = pickle.load(gameConfigFile)
        Enable_FullScreen = gameConfig['FullScreen']
        if Enable_FullScreen:
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
        MainVolume = gameConfig['MainVolume']
        MusicVolume = gameConfig['MusicVolume']

        # 調整音量
        sound_rifle_shoot.set_volume((MainVolume / 10) * 0.4)
        sound_rifle_reload.set_volume((MainVolume / 10))
        sound_missile_launcher.set_volume((MainVolume / 10) * 0.3)
        sound_laser_launcher.set_volume((MainVolume / 10))

    # 畫面顯示
    nowTime = pygame.time.get_ticks()
    if nowTime - main_screen_background_image_lastChangeTime >= main_screen_background_image_changeTime:
        main_screen_background_image_lastChangeTime = nowTime
        main_screen_background_image_frame += 1
        if main_screen_background_image_frame == 22:
            main_screen_background_image_frame = 0
    screen.blit(main_screen_background['animation'][main_screen_background_image_frame], (0, 0))
    draw_main_screen()
    pygame.display.update()

    # 按下遊戲開始
    while startPlayGame_Button_clicked:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_running = False
                startPlayGame_Button_clicked = False
                break
        
        # 遊戲存檔讀取
        if gameSave_readTimes == 0:
            GameSave_content = startPlayGame_Button.game_save
            # 檢查是否完成過遊戲
            if GameSave_content['PassGame']:
                GameSave_content["game_checkpoint"] = 4
            gameSave_readTimes = 1
        
        # 畫面顯示
            screen.fill((0, 0, 0))
            pygame.display.update()

        # GameSave_content["game_chesckpoint"] = 4

        # 關卡一
        while GameSave_content["game_checkpoint"] == 0 and startPlayGame_Button_clicked:
            clock.tick(FPS)
            # 現在時間(ticks) 1tick = 1ms
            nowTime = pygame.time.get_ticks()

            # 初始化
            if show_levelTrip:
                close = Level_1_draw_levelTrip()
                if close:
                    program_running = False
                    startPlayGame_Button_clicked = False
                    break
                show_levelTrip = False
                # 隱藏滑鼠
                pygame.mouse.set_visible(False)
                score = 0
                pauseTime = 0
                enemy_totalAmount = 9
                Use_LargeMagazine = False
                StartUse_LargeMagazine_Time = 0
                LargeMagazine_ValidityPeriod = 0
                Level_1_player_bulletDamage = 25
                Level_1_enemy_bulletDamage = 25
                Level_1_startPlayTime = pygame.time.get_ticks()
                if GameSave_content['difficult'] == "easy":
                    # 防禦時間 2min30sec ~ 3min
                    Level_1_remaining_LevelTime = (random.randint(0, 30) + 150) * 1000
                    # 敵人總數量
                    enemy_totalAmount = 7
                elif GameSave_content['difficult'] == "normal":
                    # 防禦時間 2min30sec ~ 3min30sec
                    Level_1_remaining_LevelTime = (random.randint(0, 60) + 150) * 1000
                    # 敵人總數量
                    enemy_totalAmount = 9
                elif GameSave_content['difficult'] == "hard":
                    # 防禦時間 2min30sec ~ 4min30sec
                    Level_1_remaining_LevelTime = (random.randint(0, 120) + 150) * 1000
                    # 敵人總數量
                    enemy_totalAmount = 12
                Level_1_enemy_number = {}
                Level_1_sandBag = {}
                # 所有物件
                Level_1_all_sprites = pygame.sprite.Group()
                # 各項物件分組
                Level_1_bullets = pygame.sprite.Group()
                Level_1_weapons_group = pygame.sprite.Group()
                # 物件分組
                Level_1_friendly_sprites_group = pygame.sprite.Group()
                Level_1_friendly_bullets = pygame.sprite.Group()
                Level_1_enemy_sprites_group = pygame.sprite.Group()
                Level_1_enemy_bullets = pygame.sprite.Group()
                Level_1_powerItems_group = pygame.sprite.Group()

                # 產生掩體
                Level_1_sandBag[1] = SandBag(screen, 535, 315, 270)
                Level_1_sandBag[2] = SandBag(screen, 535, 405, 270)
                Level_1_sandBag[3] = SandBag(screen, 745, 315, 90)
                Level_1_sandBag[4] = SandBag(screen, 745, 405, 90)
                Level_1_sandBag[5] = SandBag(screen, 595, 285, 0)
                Level_1_sandBag[6] = SandBag(screen, 685, 285, 0)
                Level_1_sandBag[7] = SandBag(screen, 685, 435, 180)
                for i in range(1, 8):
                    Level_1_all_sprites.add(Level_1_sandBag[i])
                # 創建玩家
                player = Level_1_Player_soldier(screen)
                player_weapon = Level_1_rifle(screen, player)
                # 添增玩家至群組
                Level_1_all_sprites.add(player_weapon)
                Level_1_all_sprites.add(player)
                Level_1_friendly_sprites_group.add(player)
                # Level_1_all_sprites.add(player_weapon)
                Level_1_weapons_group.add(player_weapon)
                # 產生電腦
                for i in range(0, enemy_totalAmount, 1):
                    Level_1_enemy_number[i] = Level_1_enemy_soldier(screen, player.rect.centerx, player.rect.centery, Level_1_choice_spawnArea())
                    Level_1_all_sprites.add(Level_1_enemy_number[i])
                    Level_1_enemy_sprites_group.add(Level_1_enemy_number[i])
                # 生成準心
                game_aimPoint = aimPoint(screen)
                Level_1_all_sprites.add(game_aimPoint)

            # 取得輸入
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_running = False
                    startPlayGame_Button_clicked = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Escape_KeyDown = True
                    if event.key == pygame.K_b:
                        if player.shoot_mode == "single":
                            player.shoot_mode = "auto"
                        elif player.shoot_mode == "auto":
                            player.shoot_mode = "single"
                    # if event.key == pygame.K_SPACE:
                    #     if player.shoot_mode == "single":
                    #         player.shoot()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if player.shoot_mode == "single":
                        player_weapon.shoot()

            # 更新玩家位置給敵人
            for i in range(0, enemy_totalAmount, 1):
                if Level_1_enemy_number[i]:
                    Level_1_enemy_number[i].enemy_centerx, Level_1_enemy_number[i].enemy_centery = player.rect.centerx, player.rect.centery

            # 更新遊戲
            Level_1_all_sprites.update()
            # 是否使用擴大彈匣道具
            if Use_LargeMagazine:
                if nowTime - StartUse_LargeMagazine_Time > LargeMagazine_ValidityPeriod:
                    player.magazine_bullets //= 2
                    if player.last_magazine_bullets > player.magazine_bullets:
                        player.last_magazine_bullets = player.magazine_bullets
                    LargeMagazine_ValidityPeriod = 0
                    Use_LargeMagazine = False

            # 判斷電腦
            
            for i in range(0, enemy_totalAmount, 1):
                # 判斷電腦 - 玩家
                if Level_1_enemy_number[i]:
                    # 判斷玩家子彈是否擊中電腦
                    hits = pygame.sprite.spritecollide(Level_1_enemy_number[i], Level_1_friendly_bullets, True, pygame.sprite.collide_rect)
                    for hit in hits:
                        Level_1_enemy_number[i].now_health -= Level_1_player_bulletDamage * player.damageMagnification
                        if Level_1_enemy_number[i].hitted == False:
                            Level_1_enemy_number[i].hitted = True
                        if Level_1_enemy_number[i].now_health <= 0:
                            score += 100
                            # 隨機掉落道具
                            if GameSave_content['difficult'] == "easy" and random.random() >= 0.6:
                                power = Level_1_powerItem(hit.rect.center)
                                Level_1_all_sprites.add(power)
                                Level_1_powerItems_group.add(power)
                            elif GameSave_content['difficult'] == "normal" and random.random() >= 0.8:
                                power = Level_1_powerItem(hit.rect.center)
                                Level_1_all_sprites.add(power)
                                Level_1_powerItems_group.add(power)
                            elif GameSave_content['difficult'] == "hard" and random.random() >= 0.9:
                                power = Level_1_powerItem(hit.rect.center)
                                Level_1_all_sprites.add(power)
                                Level_1_powerItems_group.add(power)
                            Level_1_all_sprites.remove(Level_1_enemy_number[i])
                            Level_1_enemy_sprites_group.remove(Level_1_enemy_number[i])
                            Level_1_enemy_number[i] = Level_1_enemy_soldier(screen, player.rect.centerx, player.rect.centery, Level_1_choice_spawnArea())
                            Level_1_all_sprites.add(Level_1_enemy_number[i])
                            Level_1_enemy_sprites_group.add(Level_1_enemy_number[i])

                    # 判斷電腦 - 掩體
                    # 判斷電腦是否與掩體相撞
                    for r in range(1, 8):
                        if Level_1_sandBag[r]:
                            hits = pygame.sprite.collide_rect(Level_1_enemy_number[i], Level_1_sandBag[r])
                            # 左側沙包
                            if r == 1 or r == 2:
                                if hits:
                                    # 掩體上方
                                    if Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom < (Level_1_sandBag[r].rect.top + Level_1_enemy_number[i].speedy + 1) and Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right and Level_1_enemy_number[i].rect.left < Level_1_sandBag[r].rect.right:
                                        Level_1_enemy_number[i].choice_move_direction = 1
                                        Level_1_enemy_number[i].rect.bottom = Level_1_sandBag[r].rect.top
                                    # 掩體左側
                                    if Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right < Level_1_sandBag[r].rect.centerx and Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom and Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom:
                                        Level_1_enemy_number[i].choice_move_direction = 2
                                        Level_1_enemy_number[i].rect.right = Level_1_sandBag[r].rect.left
                                    elif Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.centerx < Level_1_sandBag[r].rect.centerx and Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom and Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom:
                                        Level_1_enemy_number[i].choice_move_direction = 2
                                        Level_1_enemy_number[i].rect.right = Level_1_sandBag[r].rect.left
                                    # 掩體右測
                                    if Level_1_sandBag[r].rect.centerx < Level_1_enemy_number[i].rect.left < Level_1_sandBag[r].rect.right and Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom and Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom:
                                        Level_1_enemy_number[i].choice_move_direction = 4
                                        Level_1_enemy_number[i].rect.left = Level_1_sandBag[r].rect.right
                                    elif Level_1_sandBag[r].rect.centerx < Level_1_enemy_number[i].rect.centerx < Level_1_sandBag[r].rect.right and Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom and Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom:
                                        Level_1_enemy_number[i].choice_move_direction = 4
                                        Level_1_enemy_number[i].rect.left = Level_1_sandBag[r].rect.right
                                    # 掩體下方
                                    if (Level_1_sandBag[r].rect.bottom - Level_1_enemy_number[i].speedy - 1) < Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom and Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right and Level_1_enemy_number[i].rect.left < Level_1_sandBag[r].rect.right:
                                        Level_1_enemy_number[i].choice_move_direction = 3
                                        Level_1_enemy_number[i].rect.top = Level_1_sandBag[r].rect.bottom
                            # 右側沙包
                            if r == 3 or r == 4:
                                if hits:
                                    # 掩體上方
                                    if Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom < (Level_1_sandBag[r].rect.top + Level_1_enemy_number[i].speedy + 1) and Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right and Level_1_enemy_number[i].rect.left < Level_1_sandBag[r].rect.right:
                                        Level_1_enemy_number[i].choice_move_direction = 1
                                        Level_1_enemy_number[i].rect.bottom = Level_1_sandBag[r].rect.top
                                    # 掩體左側
                                    if Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right < Level_1_sandBag[r].rect.centerx and Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom and Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom:
                                        Level_1_enemy_number[i].choice_move_direction = 2
                                        Level_1_enemy_number[i].rect.right = Level_1_sandBag[r].rect.left
                                    elif Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.centerx < Level_1_sandBag[r].rect.centerx and Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom and Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom:
                                        Level_1_enemy_number[i].choice_move_direction = 2
                                        Level_1_enemy_number[i].rect.right = Level_1_sandBag[r].rect.left
                                    # 掩體右測
                                    if Level_1_sandBag[r].rect.centerx < Level_1_enemy_number[i].rect.left < Level_1_sandBag[r].rect.right and Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom and Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom:
                                        Level_1_enemy_number[i].choice_move_direction = 4
                                        Level_1_enemy_number[i].rect.left = Level_1_sandBag[r].rect.right
                                    elif Level_1_sandBag[r].rect.centerx < Level_1_enemy_number[i].rect.centerx < Level_1_sandBag[r].rect.right and Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom and Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom:
                                        Level_1_enemy_number[i].choice_move_direction = 4
                                        Level_1_enemy_number[i].rect.left = Level_1_sandBag[r].rect.right
                                    # 掩體下方
                                    if (Level_1_sandBag[r].rect.bottom - Level_1_enemy_number[i].speedy - 1) < Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom and Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right and Level_1_enemy_number[i].rect.left < Level_1_sandBag[r].rect.right:
                                        Level_1_enemy_number[i].choice_move_direction = 3
                                        Level_1_enemy_number[i].rect.top = Level_1_sandBag[r].rect.bottom
                            # 上方沙包
                            if r == 5 or r == 6:
                                if hits:
                                    # 掩體上方
                                    if Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom < Level_1_sandBag[r].rect.centery and Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right and Level_1_enemy_number[i].rect.left < Level_1_sandBag[r].rect.right:
                                        Level_1_enemy_number[i].choice_move_direction = 1
                                        Level_1_enemy_number[i].rect.bottom = Level_1_sandBag[r].rect.top
                                    # 掩體下方
                                    if Level_1_sandBag[r].rect.centery < Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom and Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right and Level_1_enemy_number[i].rect.left < Level_1_sandBag[r].rect.right:
                                        Level_1_enemy_number[i].choice_move_direction = 3
                                        Level_1_enemy_number[i].rect.top = Level_1_sandBag[r].rect.bottom
                            # 下方沙包
                            if r == 7:
                                if hits:
                                    # 掩體上方
                                    if Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom < Level_1_sandBag[r].rect.centery and Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right and Level_1_enemy_number[i].rect.left < Level_1_sandBag[r].rect.right:
                                        Level_1_enemy_number[i].choice_move_direction = 1
                                        Level_1_enemy_number[i].rect.bottom = Level_1_sandBag[r].rect.top
                                    # 掩體左側
                                    if Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right < (Level_1_sandBag[r].rect.left + Level_1_enemy_number[i].speedx + 1) and Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom and Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom:
                                        Level_1_enemy_number[i].choice_move_direction = 2
                                        Level_1_enemy_number[i].rect.right = Level_1_sandBag[r].rect.left
                                    elif Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.centerx < Level_1_sandBag[r].rect.centerx and Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom and Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom:
                                        Level_1_enemy_number[i].choice_move_direction = 2
                                        Level_1_enemy_number[i].rect.right = Level_1_sandBag[r].rect.left
                                    # 掩體下方
                                    if Level_1_sandBag[r].rect.centery < Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom and Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right and Level_1_enemy_number[i].rect.left < Level_1_sandBag[r].rect.right:
                                        Level_1_enemy_number[i].choice_move_direction = 3
                                        Level_1_enemy_number[i].rect.top = Level_1_sandBag[r].rect.bottom
                
            # 判斷玩家

            # 判斷玩家 - 電腦
            # 判斷子彈是否擊中玩家
            hits = pygame.sprite.spritecollide(player, Level_1_enemy_bullets, True, pygame.sprite.collide_rect)
            for hit in hits:
                if player.now_armor <= 0:
                    player.now_health -= Level_1_enemy_bulletDamage * Level_1_enemy_number[i].damageMagnification
                    if player.now_health <= 0 and player.lives > 0:
                        player.lives -= 1
                        player.now_health = player.health
                        player.now_armor = player.armor
                        player.hide()
                        # 重置彈藥
                        Use_LargeMagazine = False
                        LargeMagazine_ValidityPeriod = 0
                        player.magazine_bullets = player.magazine_bullets_original
                        player.last_magazine_bullets = player.magazine_bullets
                elif player.now_armor - Level_1_enemy_bulletDamage * 0.5 * Level_1_enemy_number[i].damageMagnification >= 0:
                    player.now_armor -= Level_1_enemy_bulletDamage * 0.5 * Level_1_enemy_number[i].damageMagnification
                else:
                    player.now_health -= (Level_1_enemy_bulletDamage * 0.5 * Level_1_enemy_number[i].damageMagnification) - player.now_armor
                    player.now_armor = 0

            # 判斷玩家是否與電腦相撞
            for i in range(0, enemy_totalAmount, 1):
                if Level_1_enemy_number[i]:
                    hits = pygame.sprite.collide_rect(player, Level_1_enemy_number[i])
                    # 處理電腦
                    if hits:
                        if player.rect.top <= Level_1_enemy_number[i].rect.bottom < player.rect.centery:
                            if Level_1_enemy_number[i].choice_move_direction == 3:
                                Level_1_enemy_number[i].choice_move_direction = 1
                            # Level_1_enemy_number[i].rect.bottom = player.rect.top
                        elif player.rect.centerx < Level_1_enemy_number[i].rect.left <= player.rect.right:
                            if Level_1_enemy_number[i].choice_move_direction == 4:
                                Level_1_enemy_number[i].choice_move_direction = 2
                            # Level_1_enemy_number[i].rect.left = player.rect.right
                        elif player.rect.centery < Level_1_enemy_number[i].rect.top <= player.rect.bottom:
                            if Level_1_enemy_number[i].choice_move_direction == 1:
                                Level_1_enemy_number[i].choice_move_direction = 3
                            # Level_1_enemy_number[i].rect.top = player.rect.bottom
                        elif player.rect.left <= Level_1_enemy_number[i].rect.right < player.rect.centerx:
                            if Level_1_enemy_number[i].choice_move_direction == 2:
                                Level_1_enemy_number[i].choice_move_direction = 4
                            # Level_1_enemy_number[i].rect.right = player.rect.left

                    # 處理玩家
                    if hits:
                        if Level_1_enemy_number[i].rect.centery < player.rect.top <= Level_1_enemy_number[i].rect.bottom:
                            player.rect.top = Level_1_enemy_number[i].rect.bottom
                        elif Level_1_enemy_number[i].rect.centerx < player.rect.left <= Level_1_enemy_number[i].rect.right:
                            player.rect.left = Level_1_enemy_number[i].rect.right
                        elif Level_1_enemy_number[i].rect.top <= player.rect.bottom < Level_1_enemy_number[i].rect.centery:
                            player.rect.bottom = Level_1_enemy_number[i].rect.top
                        elif Level_1_enemy_number[i].rect.left <= player.rect.right < Level_1_enemy_number[i].rect.centerx:
                            player.rect.right = Level_1_enemy_number[i].rect.left
            
            # 判斷玩家 - 掩體
            # 判斷玩家是否與掩體相撞
            for i in range(1, 8):
                if Level_1_sandBag[i]:
                    hits = pygame.sprite.collide_rect(player, Level_1_sandBag[i])
                    # 左側沙包
                    if i == 1 or i == 2:
                        if hits:
                            # 掩體上方
                            if Level_1_sandBag[i].rect.top < player.rect.bottom < (Level_1_sandBag[i].rect.top + player.speed + 1) and Level_1_sandBag[i].rect.left < player.rect.right and player.rect.left < Level_1_sandBag[i].rect.right:
                                player.rect.bottom = Level_1_sandBag[i].rect.top
                            # 掩體左側
                            if Level_1_sandBag[i].rect.left < player.rect.right < Level_1_sandBag[i].rect.centerx and Level_1_sandBag[i].rect.top < player.rect.bottom and player.rect.top < Level_1_sandBag[i].rect.bottom:
                                player.rect.right = Level_1_sandBag[i].rect.left
                            elif Level_1_sandBag[i].rect.left < player.rect.centerx < Level_1_sandBag[i].rect.centerx and Level_1_sandBag[i].rect.top < player.rect.bottom and player.rect.top < Level_1_sandBag[i].rect.bottom:
                                player.rect.right = Level_1_sandBag[i].rect.left
                            # 掩體右測
                            if Level_1_sandBag[i].rect.centerx < player.rect.left < Level_1_sandBag[i].rect.right and Level_1_sandBag[i].rect.top < player.rect.bottom and player.rect.top < Level_1_sandBag[i].rect.bottom:
                                player.rect.left = Level_1_sandBag[i].rect.right
                            elif Level_1_sandBag[i].rect.centerx < player.rect.centerx < Level_1_sandBag[i].rect.right and Level_1_sandBag[i].rect.top < player.rect.bottom and player.rect.top < Level_1_sandBag[i].rect.bottom:
                                player.rect.left = Level_1_sandBag[i].rect.right
                            # 掩體下方
                            if (Level_1_sandBag[i].rect.bottom - player.speed - 1) < player.rect.top < Level_1_sandBag[i].rect.bottom and Level_1_sandBag[i].rect.left < player.rect.right and player.rect.left < Level_1_sandBag[i].rect.right:
                                player.rect.top = Level_1_sandBag[i].rect.bottom
                    # 右側沙包
                    if i == 3 or i == 4:
                        if hits:
                            # 掩體上方
                            if Level_1_sandBag[i].rect.top < player.rect.bottom < (Level_1_sandBag[i].rect.top + player.speed + 1) and Level_1_sandBag[i].rect.left < player.rect.right and player.rect.left < Level_1_sandBag[i].rect.right:
                                player.rect.bottom = Level_1_sandBag[i].rect.top
                            # 掩體左側
                            if Level_1_sandBag[i].rect.left < player.rect.right < Level_1_sandBag[i].rect.centerx and Level_1_sandBag[i].rect.top < player.rect.bottom and player.rect.top < Level_1_sandBag[i].rect.bottom:
                                player.rect.right = Level_1_sandBag[i].rect.left
                            elif Level_1_sandBag[i].rect.left < player.rect.centerx < Level_1_sandBag[i].rect.centerx and Level_1_sandBag[i].rect.top < player.rect.bottom and player.rect.top < Level_1_sandBag[i].rect.bottom:
                                player.rect.right = Level_1_sandBag[i].rect.left
                            # 掩體右測
                            if Level_1_sandBag[i].rect.centerx < player.rect.left < Level_1_sandBag[i].rect.right and Level_1_sandBag[i].rect.top < player.rect.bottom and player.rect.top < Level_1_sandBag[i].rect.bottom:
                                player.rect.left = Level_1_sandBag[i].rect.right
                            elif Level_1_sandBag[i].rect.centerx < player.rect.centerx < Level_1_sandBag[i].rect.right and Level_1_sandBag[i].rect.top < player.rect.bottom and player.rect.top < Level_1_sandBag[i].rect.bottom:
                                player.rect.left = Level_1_sandBag[i].rect.right
                            # 掩體下方
                            if (Level_1_sandBag[i].rect.bottom - player.speed - 1) < player.rect.top < Level_1_sandBag[i].rect.bottom and Level_1_sandBag[i].rect.left < player.rect.right and player.rect.left < Level_1_sandBag[i].rect.right:
                                player.rect.top = Level_1_sandBag[i].rect.bottom
                    # 上方沙包
                    if i == 5 or i == 6:
                        if hits:
                            # 掩體上方
                            if Level_1_sandBag[i].rect.top < player.rect.bottom < Level_1_sandBag[i].rect.centery and Level_1_sandBag[i].rect.left < player.rect.right and player.rect.left < Level_1_sandBag[i].rect.right:
                                player.rect.bottom = Level_1_sandBag[i].rect.top
                            # 掩體下方
                            if Level_1_sandBag[i].rect.centery < player.rect.top < Level_1_sandBag[i].rect.bottom and Level_1_sandBag[i].rect.left < player.rect.right and player.rect.left < Level_1_sandBag[i].rect.right:
                                player.rect.top = Level_1_sandBag[i].rect.bottom
                    # # 下方沙包
                    # if i == 7:
                    #     if hits:
                    #         # 掩體上方
                    #         if Level_1_sandBag[i].rect.top < player.rect.bottom < Level_1_sandBag[i].rect.centery and Level_1_sandBag[i].rect.left < player.rect.right and player.rect.left < Level_1_sandBag[i].rect.right:
                    #             player.rect.bottom = Level_1_sandBag[i].rect.top
                    #         # 掩體左側
                    #         if Level_1_sandBag[i].rect.left < player.rect.right < (Level_1_sandBag[i].rect.left + player.speed + 1) and Level_1_sandBag[i].rect.top < player.rect.bottom and player.rect.top < Level_1_sandBag[i].rect.bottom:
                    #             player.rect.right = Level_1_sandBag[i].rect.left
                    #         elif Level_1_sandBag[i].rect.left < player.rect.centerx < Level_1_sandBag[i].rect.centerx and Level_1_sandBag[i].rect.top < player.rect.bottom and player.rect.top < Level_1_sandBag[i].rect.bottom:
                    #             player.rect.right = Level_1_sandBag[i].rect.left
                    #         # 掩體下方
                    #         if Level_1_sandBag[i].rect.centery < player.rect.top < Level_1_sandBag[i].rect.bottom and Level_1_sandBag[i].rect.left < player.rect.right and player.rect.left < Level_1_sandBag[i].rect.right:
                    #             player.rect.top = Level_1_sandBag[i].rect.bottom

            # 判斷玩家是否取得道具
            hits = pygame.sprite.spritecollide(player, Level_1_powerItems_group, True)
            for hit in hits:
                if hit.powerType == 'Medkit':
                    player.now_health += 25
                    if player.now_health > player.health:
                        player.now_health = player.health
                if hit.powerType == 'ArmorPack':
                    player.now_armor += 50
                    if player.now_armor > 200:
                        player.now_armor = 200
                if hit.powerType == 'LargeMagazine':
                    if not Use_LargeMagazine:
                        StartUse_LargeMagazine_Time = nowTime
                    Use_LargeMagazine = True
                    LargeMagazine_ValidityPeriod += 15000
                    if player.magazine_bullets == player.magazine_bullets_original:
                        player.magazine_bullets *= 2
                    if player.last_magazine_bullets < player.magazine_bullets:
                        player.last_magazine_bullets = player.magazine_bullets
                    if player.startReloadBullet:
                        player.startReloadBullet = False
                    if player.pressed_reload_key:
                        player.pressed_reload_key = False
                    if player.play_reload_sound:
                        player.play_reload_sound = False
                if hit.powerType == 'HighSpeedReload':
                    sound_rifle_reload.play()
                    player.last_magazine_bullets = player.magazine_bullets
                    if player.startReloadBullet:
                        player.startReloadBullet = False
                    if player.pressed_reload_key:
                        player.pressed_reload_key = False
                    if player.play_reload_sound:
                        player.play_reload_sound = False

            # 判斷掩體

            # 判斷掩體 - 電腦
            # 判斷電腦子彈是否擊中掩體
            for i in range(1, 8):
                if Level_1_sandBag[i]:
                    hits = pygame.sprite.spritecollide(Level_1_sandBag[i], Level_1_enemy_bullets, True, pygame.sprite.collide_rect)
                    for hit in hits:
                        Level_1_sandBag[i].now_health -= int(Level_1_enemy_bulletDamage * Level_1_enemy_number[0].damageMagnification)
                        if Level_1_sandBag[i].hitted == False:
                            Level_1_sandBag[i].hitted = True
                        if Level_1_sandBag[i].now_health <= 0:
                            Level_1_all_sprites.remove(Level_1_sandBag[i])
                            Level_1_friendly_sprites_group.remove(Level_1_sandBag[i])
                            Level_1_sandBag[i] = None
            
            # 檢查玩家是否失敗
            if player.now_health <= 0 and player.lives <= 0:
                pygame.mouse.set_visible(True)
                # 啟用關卡初始化
                show_levelTrip = True
                # 檢查是否完成過遊戲
                if GameSave_content['PassGame']:
                    GameSave_content["game_checkpoint"] = 4
                    # 更新存檔
                    with open(GAMESAVE_FILE_ADDRESS, 'wb') as gamesave:
                        pickle.dump(GameSave_content, gamesave)
                    break
                else:
                    # 呼叫遊戲失敗畫面
                    failureLevelScreen_return = draw_failureLevelScreen(screen)
                    if failureLevelScreen_return:
                        # 重新遊玩本關

                        # 啟用關卡初始化
                        show_levelTrip = True
                        break
                    else:
                        # 啟用關卡初始化
                        show_levelTrip = True
                        # 回到主畫面
                        startPlayGame_Button_clicked = False
                        gameSave_readTimes = 0
                        break

            # 檢查是否完成通關條件
            if nowTime - Level_1_startPlayTime - pauseTime >= Level_1_remaining_LevelTime:
                pygame.mouse.set_visible(True)
                # 啟用關卡初始化
                show_levelTrip = True
                # 更新記錄點
                GameSave_content["game_checkpoint"] = 1
                # 記錄分數
                GameSave_content['Score_Level_1'] = score
                if GameSave_content['Score_Level_1'] > GameSave_content['history_HighestScore_Level_1']:
                    GameSave_content['history_HighestScore_Level_1'] = GameSave_content['Score_Level_1']
                # 記錄遊玩時間(Sec)
                GameSave_content['PlayTime_Level_1'] = int((nowTime - Level_1_startPlayTime - pauseTime) / 1000)
                GameSave_content['PlayTime_Level_1_total'] += int((nowTime - Level_1_startPlayTime - pauseTime) / 1000)
                GameSave_content['PlayTime_total'] += GameSave_content['PlayTime_Level_1']
                # 檢查是否完成過遊戲
                if GameSave_content['PassGame']:
                    GameSave_content["game_checkpoint"] = 4
                # 更新存檔
                with open(GAMESAVE_FILE_ADDRESS, 'wb') as gamesave:
                    pickle.dump(GameSave_content, gamesave)
                # 呼叫通關畫面
                passLevelScreen_return = draw_passLevelScreen(screen, 1)
                if passLevelScreen_return:
                    # 前往下一關

                    # 啟用下一關關卡初始化
                    show_levelTrip = True
                    break
                else:
                    # 啟用下一關關卡初始化
                    show_levelTrip = True
                    # 回到主畫面
                    startPlayGame_Button_clicked = False
                    gameSave_readTimes = 0
                    break

            # 畫面顯示
            # screen.fill((255, 255, 150))
            screen.blit(image_background_desert, (0, 0))
            Level_1_all_sprites.draw(screen)
            screen.blit(image_playerInformactionUI_background, (0, 0))
            if player.shoot_mode == "auto":
                screen.blit(image_playerInformactionUI_background_autoMode, (1236, 681))
            else:
                screen.blit(image_playerInformactionUI_background_singleMode, (1236, 681))
            # 可視化圓形碰撞箱
            # pygame.draw.circle(screen, (0, 255, 0), player.rect.center, player.radius)
            # for i in range(0, enemy_totalAmount, 1):
            #     if Level_1_enemy_number[i]:
            #         pygame.draw.circle(screen, (0, 255, 0), Level_1_enemy_number[i].rect.center, Level_1_enemy_number[i].radius)
            
            # 繪製血量
            # 敵人
            for i in range(0, enemy_totalAmount, 1):
                if Level_1_enemy_number[i] and Level_1_enemy_number[i].hitted:
                    draw_health(screen, Level_1_enemy_number[i].now_health, Level_1_enemy_number[i].health, (Level_1_enemy_number[i].rect.centerx - 25), (Level_1_enemy_number[i].rect.top - 10), (255, 0, 0), (0, 0, 0))
            for i in range(1, 8):
                if Level_1_sandBag[i] and Level_1_sandBag[i].hitted:
                    draw_health(screen, Level_1_sandBag[i].now_health, Level_1_sandBag[i].health, (Level_1_sandBag[i].rect.centerx - 25), (Level_1_sandBag[i].rect.centery - 3), (0, 255, 0), (0, 0, 0))

            # 畫角色資訊
            draw_lives(screen, player.lives, image_player_livesIcon, 29, 638, 34)
            draw_Level_1_playerInformactionUI(screen, player, score, Level_1_startPlayTime + pauseTime)
            if Use_LargeMagazine:
                if nowTime - StartUse_LargeMagazine_Time < LargeMagazine_ValidityPeriod:
                    screen.blit(image_large_magazine_rifle_status, (1240, 49))
                    draw_text("center", screen, str(int((LargeMagazine_ValidityPeriod - (nowTime - StartUse_LargeMagazine_Time)) / 1000)), (0, 0, 0), 22, False, 1255, 96)
            # 畫ESC選單
            if Escape_KeyDown:
                pauseTimeSt = nowTime
                pygame.mouse.set_visible(True)
                screen.blit(image_setting_panel_background, (0, 0))
                escape_screen_return = draw_Key_escape_screen(screen)
            # 繼續遊戲
            if escape_screen_return == 1:
                nowTime = pygame.time.get_ticks()
                pauseTime += nowTime - pauseTimeSt
                if Use_LargeMagazine:
                    LargeMagazine_ValidityPeriod += nowTime - pauseTimeSt
                escape_screen_return = 0
                Escape_KeyDown = False
                pygame.mouse.set_visible(False)
            # 回到主畫面
            elif escape_screen_return == 2:
                nowTime = pygame.time.get_ticks()
                pauseTime += nowTime - pauseTimeSt
                escape_screen_return = 0
                Escape_KeyDown = False
                pygame.mouse.set_visible(True)
                # 啟用關卡初始化
                show_levelTrip = True
                gameSave_readTimes = 0
                # 結束遊戲
                startPlayGame_Button_clicked = False
            # 離開遊戲
            elif escape_screen_return == 3:
                escape_screen_return = 0
                program_running = False
                startPlayGame_Button_clicked = False
            
            pygame.display.update()

        # 關卡二
        while GameSave_content["game_checkpoint"] == 1 and startPlayGame_Button_clicked:
            clock.tick(FPS)
            # 現在時間(ticks) 1tick = 1ms
            nowTime = pygame.time.get_ticks()

            # 初始化
            if show_levelTrip:
                close = Level_2_draw_levelTrip()
                if close:
                    program_running = False
                    startPlayGame_Button_clicked = False
                    break
                show_levelTrip = False
                # 隱藏滑鼠
                pygame.mouse.set_visible(False)
                score = 0
                pauseTime = 0
                nowRound = 0
                round_colddown = 1000
                totalRocksAmount = 8
                killEnemyAmount = 0
                Use_TurretUpgrade = False
                StartUse_TurretUpgrade_Time = 0
                Level_2_summonBOSS_time = 0
                Level_2_player_lazerDamage = 30
                Level_2_player_missileDamage = 220
                Level_2_enemy_lazerDamage = 20
                Level_2_enemy_missileDamage = 160
                Level_2_enemy_damageMagnification = 0
                Level_2_enemy_damageMagnification_get = Level_2_enemy_plane(screen, -100, -100)
                Level_2_enemy_damageMagnification = Level_2_enemy_damageMagnification_get.damageMagnification
                Level_2_enemy_damageMagnification_get = None
                # 招術紀錄
                Level_2_enemy_BOSS_Skill_1_Done = {}
                Level_2_enemy_BOSS_Skill_1_Done[1] = False
                Level_2_enemy_BOSS_Skill_1_Done[2] = False
                Level_2_enemy_BOSS_Skill_1_Done[3] = False
                Level_2_enemy_BOSS_Skill_2_Done = {}
                Level_2_enemy_BOSS_Skill_2_Done[1] = False
                Level_2_enemy_BOSS_Skill_2_Done[2] = False
                Level_2_enemy_BOSS_Skill_3_Done = {}
                Level_2_enemy_BOSS_Skill_3_Done[1] = False
                Level_2_startPlayTime = pygame.time.get_ticks()
                Level_2_finishRound = False
                Level_2_finishRoundTime = 0
                Level_2_enemy_number = {}
                Level_2_enemy_BOSS = None
                # 所有物件
                Level_2_all_sprites = pygame.sprite.Group()
                # 各項物件分組
                Level_2_lazers = pygame.sprite.Group()
                Level_2_missiles = pygame.sprite.Group()
                Level_2_rocks = pygame.sprite.Group()
                # 物件分組
                Level_2_friendly_sprites_group = pygame.sprite.Group()
                Level_2_friendly_lazers = pygame.sprite.Group()
                Level_2_friendly_missiles = pygame.sprite.Group()
                Level_2_enemy_sprites_group = pygame.sprite.Group()
                Level_2_enemy_lazers = pygame.sprite.Group()
                Level_2_enemy_missiles = pygame.sprite.Group()
                Level_2_powerItems_group = pygame.sprite.Group()

                # 創建玩家
                player = Level_2_Player_plane(screen)
                # 添增玩家至群組
                Level_2_all_sprites.add(player)
                Level_2_friendly_sprites_group.add(player)
                
                # 創造石頭
                for i in range(totalRocksAmount):
                    Level_2_new_rocks()

                # 重置電腦
                for i in range(0, 7, 1):
                    Level_2_enemy_number[i] = None
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_running = False
                    startPlayGame_Button_clicked = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        Escape_KeyDown = True
                    if event.key == pygame.K_b:
                        if player.shoot_mode == "auto":
                            player.shoot_mode = "missile"
                        elif player.shoot_mode == "missile":
                            player.shoot_mode = "auto"

            if nowRound == 0 and nowTime - Level_2_startPlayTime > round_colddown:
                # 生成電腦
                Level_2_enemy_number[1] = Level_2_enemy_plane(screen, 320, 100)
                Level_2_enemy_number[2] = Level_2_enemy_plane(screen, WIDTH / 2, 100)
                Level_2_enemy_number[3] = Level_2_enemy_plane(screen, 960, 100)
                Level_2_enemy_number[4] = Level_2_enemy_plane(screen, 427, 200)
                Level_2_enemy_number[5] = Level_2_enemy_plane(screen, 853, 200)
                for i in range(1, 6):
                    Level_2_all_sprites.add(Level_2_enemy_number[i])
                    Level_2_enemy_sprites_group.add(Level_2_enemy_number[i])
                nowRound = 1
            elif nowRound == 1 and killEnemyAmount == 5 and nowTime - Level_2_finishRoundTime > round_colddown:
                # 生成電腦
                Level_2_enemy_number[1] = Level_2_enemy_plane(screen, 320, 70)
                Level_2_enemy_number[2] = Level_2_enemy_plane(screen, WIDTH / 2, 70)
                Level_2_enemy_number[3] = Level_2_enemy_plane(screen, 960, 70)
                Level_2_enemy_number[4] = Level_2_enemy_plane(screen, 427, 140)
                Level_2_enemy_number[5] = Level_2_enemy_plane(screen, 853, 140)
                Level_2_enemy_number[6] = Level_2_enemy_plane(screen, WIDTH / 2, 200)
                for i in range(1, 7):
                    Level_2_all_sprites.add(Level_2_enemy_number[i])
                    Level_2_enemy_sprites_group.add(Level_2_enemy_number[i])
                Level_2_finishRound = False
                nowRound = 2
            elif nowRound == 2 and killEnemyAmount == 11 and nowTime - Level_2_finishRoundTime > round_colddown:
                # 生成BOSS
                Level_2_enemy_BOSS = Level_2_enemy_BOSS_plane(screen, 320, 70)
                Level_2_all_sprites.add(Level_2_enemy_BOSS)
                Level_2_enemy_sprites_group.add(Level_2_enemy_BOSS)
                Level_2_finishRound = False
                Level_2_summonBOSS_time = nowTime
                nowRound = 3

            # 敵人BOSS全場技能
            if Level_2_enemy_BOSS:
                # 到達指定時間
                if nowTime - Level_2_summonBOSS_time > 45000 and not Level_2_enemy_BOSS_Skill_1_Done[1]:
                    # 施放招式一 (1)
                    Level_2_enemy_BOSS.skill(1)
                    Level_2_enemy_BOSS_Skill_1_Done[1] = True
                if nowTime - Level_2_summonBOSS_time > 130000 and not Level_2_enemy_BOSS_Skill_2_Done[1]:
                    # 施放招式二 (1)
                    Level_2_enemy_BOSS.skill(2)
                    Level_2_enemy_BOSS_Skill_2_Done[1] = True
                # 低於指定狀態
                if (Level_2_enemy_BOSS.now_armor / Level_2_enemy_BOSS.armor) <= 0.5 and not Level_2_enemy_BOSS_Skill_1_Done[2]:
                    # 施放招式一 (2)
                    Level_2_enemy_BOSS.skill(1)
                    Level_2_enemy_BOSS_Skill_1_Done[2] = True
                if (Level_2_enemy_BOSS.now_armor / Level_2_enemy_BOSS.armor) <= 0 and not Level_2_enemy_BOSS_Skill_1_Done[3]:
                    # 施放招式一 (3)
                    Level_2_enemy_BOSS.skill(1)
                    Level_2_enemy_BOSS_Skill_1_Done[3] = True
                if (Level_2_enemy_BOSS.now_health / Level_2_enemy_BOSS.health) <= 0.5 and not Level_2_enemy_BOSS_Skill_2_Done[2]:
                    # 施放招式二 (2)
                    Level_2_enemy_BOSS.skill(2)
                    Level_2_enemy_BOSS_Skill_2_Done[2] = True
                if (Level_2_enemy_BOSS.now_health / Level_2_enemy_BOSS.health) <= 0.2 and not Level_2_enemy_BOSS_Skill_3_Done[1]:
                    # 施放招式三 (1)
                    Level_2_enemy_BOSS.skill(3)
                    Level_2_enemy_BOSS_Skill_3_Done[1] = True
 
            # 更新遊戲
            Level_2_all_sprites.update()
            # 是否使用擴大射擊道具
            if Use_TurretUpgrade:
                if nowTime - StartUse_TurretUpgrade_Time > player.gun_turboTime:
                    player.gun = 1
                    player.gun_turboTime = 0
                    Use_TurretUpgrade = False

            # 玩家

            # 玩家 - 隕石
            # 判斷玩家雷射是否擊中隕石
            hits = pygame.sprite.groupcollide(Level_2_rocks, Level_2_friendly_lazers, True, True)
            for hit in hits:
                score += hit.radius
                Level_2_summon_powerItem(hit.rect.center)
                Level_2_new_rocks()
            # 判斷玩家飛彈是否擊中隕石
            hits = pygame.sprite.groupcollide(Level_2_rocks, Level_2_friendly_missiles, True, True)
            for hit in hits:
                score += hit.radius
                Level_2_summon_powerItem(hit.rect.center)
                Level_2_new_rocks()

            # 玩家 - 敵人
            # 判斷玩家雷射是否擊中敵人
            hits = pygame.sprite.groupcollide(Level_2_enemy_sprites_group, Level_2_friendly_lazers, False, True)
            for hit in hits:
                if hit.hitted == False:
                    hit.hitted = True
                if hit.now_armor <= 0:
                    hit.now_health -= Level_2_player_lazerDamage * player.damageMagnification * 1.2
                    if hit.now_health <= 0:
                        killEnemyAmount += 1
                        score += 500
                        if hit.hitted == True:
                            hit.hitted = False
                        Level_2_all_sprites.remove(hit)
                        Level_2_enemy_sprites_group.remove(hit)
                        Level_2_summon_powerItem(hit.rect.center)
                        hit = None
                elif hit.now_armor - (Level_2_player_lazerDamage * player.damageMagnification) >= 0:
                    hit.now_armor -= Level_2_player_lazerDamage * player.damageMagnification
                else:
                    hit.now_health -= ((Level_2_player_lazerDamage * player.damageMagnification) - hit.now_armor) * 1.2
                    hit.now_armor = 0         
            # 判斷玩家飛彈是否擊中敵人
            hits = pygame.sprite.groupcollide(Level_2_enemy_sprites_group, Level_2_friendly_missiles, False, True)
            for hit in hits:
                if hit.hitted == False:
                    hit.hitted = True
                if hit.now_armor <= 0:
                    hit.now_health -= Level_2_player_missileDamage * player.damageMagnification * 1.5
                    if hit.now_health <= 0:
                        killEnemyAmount += 1
                        score += 500
                        if hit.hitted == True:
                            hit.hitted = False
                        Level_2_all_sprites.remove(hit)
                        Level_2_enemy_sprites_group.remove(hit)
                        Level_2_summon_powerItem(hit.rect.center)
                        hit = None
                elif hit.now_armor - (Level_2_player_missileDamage * player.damageMagnification) >= 0:
                    hit.now_armor -= Level_2_player_missileDamage * player.damageMagnification
                else:
                    hit.now_health -= ((Level_2_player_missileDamage * player.damageMagnification) - hit.now_armor) * 1.5
                    hit.now_armor = 0
            
            # 判斷玩家是否取得道具
            hits = pygame.sprite.spritecollide(player, Level_2_powerItems_group, True)
            for hit in hits:
                if hit.powerType == 'Medkit':
                    player.now_health += player.health * 0.25
                    if player.now_health > player.health:
                        player.now_health = player.health
                if hit.powerType == 'RepairKit':
                    player.now_armor += player.armor * 0.25
                    if player.now_armor > player.armor:
                        player.now_armor = player.armor
                if hit.powerType == 'TurretUpgrade':
                    if not Use_TurretUpgrade:
                        StartUse_TurretUpgrade_Time = nowTime
                    player.gun = 2
                    Use_TurretUpgrade = True
                    player.gun_turboTime += 15000

            # 敵人

            # 敵人 - 玩家
            # 判斷敵人雷射是否擊中玩家
            hits = pygame.sprite.spritecollide(player, Level_2_enemy_lazers, True, pygame.sprite.collide_circle)
            for hit in hits:
                if player.now_armor <= 0:
                    player.now_health -= Level_2_enemy_lazerDamage * Level_2_enemy_damageMagnification * 1.2
                    if player.now_health <= 0 and player.lives > 0:
                        player.lives -= 1
                        player.now_health = player.health
                        player.now_armor = player.armor
                        player.hide()
                elif player.now_armor - (Level_2_enemy_lazerDamage * Level_2_enemy_damageMagnification) >= 0:
                    player.now_armor -= Level_2_enemy_lazerDamage * Level_2_enemy_damageMagnification
                else:
                    player.now_health -= ((Level_2_enemy_lazerDamage * Level_2_enemy_damageMagnification) - player.now_armor) * 1.2
                    player.now_armor = 0
            # 判斷敵人飛彈是否擊中玩家
            hits = pygame.sprite.spritecollide(player, Level_2_enemy_missiles, True, pygame.sprite.collide_circle)
            for hit in hits:
                if player.now_armor <= 0:
                    player.now_health -= Level_2_enemy_missileDamage * Level_2_enemy_damageMagnification * 1.5
                    if player.now_health <= 0 and player.lives > 0:
                        player.lives -= 1
                        player.now_health = player.health
                        player.now_armor = player.armor
                        player.hide()
                elif player.now_armor - (Level_2_enemy_missileDamage * Level_2_enemy_damageMagnification) >= 0:
                    player.now_armor -= Level_2_enemy_missileDamage * Level_2_enemy_damageMagnification
                else:
                    player.now_health -= ((Level_2_enemy_missileDamage * Level_2_enemy_damageMagnification) - player.now_armor) * 1.5
                    player.now_armor = 0
            
            # 隕石

            # 隕石 - 玩家
            # 判斷隕石是否擊中玩家
            hits = pygame.sprite.spritecollide(player, Level_2_rocks, True, pygame.sprite.collide_circle)
            for hit in hits:
                Level_2_new_rocks()
                if player.now_armor <= 0:
                    player.now_health -= hit.radius * 1.2
                    if player.health <= 0 and player.lives > 0:
                        player.lives -= 1
                        player.now_health = player.health
                        player.now_armor = player.armor
                        player.hide()
                elif player.now_armor - hit.radius >= 0:
                    player.now_armor -= hit.radius
                else:
                    player.now_health -= hit.radius - player.now_armor
                    player.now_armor = 0

            # 檢查玩家是否失敗
            if player.now_health <= 0 and player.lives <= 0:
                pygame.mouse.set_visible(True)
                # 啟用關卡初始化
                show_levelTrip = True
                # 檢查是否完成過遊戲
                if GameSave_content['PassGame']:
                    GameSave_content["game_checkpoint"] = 4
                    # 更新存檔
                    with open(GAMESAVE_FILE_ADDRESS, 'wb') as gamesave:
                        pickle.dump(GameSave_content, gamesave)
                    break
                else:
                    # 呼叫遊戲失敗畫面
                    failureLevelScreen_return = draw_failureLevelScreen(screen)
                    if failureLevelScreen_return:
                        # 重新遊玩本關

                        # 啟用關卡初始化
                        show_levelTrip = True
                        break
                    else:
                        # 啟用關卡初始化
                        show_levelTrip = True
                        # 回到主畫面
                        startPlayGame_Button_clicked = False
                        gameSave_readTimes = 0
                        break

            # 檢查是否完成通關條件
            if killEnemyAmount == 12 and Level_2_finishRound:
                pygame.mouse.set_visible(True)
                # 啟用關卡初始化
                show_levelTrip = True
                # 更新記錄點
                # GameSave_content["game_checkpoint"] = 2
                # beta Setting
                GameSave_content['PassGame'] = True
                # 記錄分數
                GameSave_content['Score_Level_2'] = score
                if GameSave_content['Score_Level_2'] > GameSave_content['history_HighestScore_Level_2']:
                    GameSave_content['history_HighestScore_Level_2'] = GameSave_content['Score_Level_2']
                # 記錄遊玩時間(Sec)
                GameSave_content['PlayTime_Level_2'] = int((nowTime - Level_2_startPlayTime - pauseTime) / 1000)
                GameSave_content['PlayTime_Level_2_total'] += int((nowTime - Level_2_startPlayTime - pauseTime) / 1000)
                GameSave_content['PlayTime_total'] += GameSave_content['PlayTime_Level_2']
                # 檢查是否完成過遊戲
                if GameSave_content['PassGame']:
                    GameSave_content["game_checkpoint"] = 4
                # 更新存檔
                with open(GAMESAVE_FILE_ADDRESS, 'wb') as gamesave:
                    pickle.dump(GameSave_content, gamesave)
                # 呼叫通關畫面
                passLevelScreen_return = draw_passLevelScreen(screen, 2)
                if passLevelScreen_return:
                    # 前往下一關

                    # 啟用下一關關卡初始化
                    show_levelTrip = True
                    break
                else:
                    # 啟用下一關關卡初始化
                    show_levelTrip = True
                    # 回到主畫面
                    startPlayGame_Button_clicked = False
                    gameSave_readTimes = 0
                    break

            # 是否完成波數
            if nowRound == 1 and killEnemyAmount == 5 and not Level_2_finishRound:
                Level_2_finishRoundTime = nowTime
                Level_2_finishRound = True
            elif nowRound == 2 and killEnemyAmount == 11 and not Level_2_finishRound:
                Level_2_finishRoundTime = nowTime
                Level_2_finishRound = True
            elif nowRound == 3 and killEnemyAmount == 12 and not Level_2_finishRound:
                Level_2_finishRoundTime = nowTime
                Level_2_finishRound = True

            # 畫面顯示
            # screen.fill((0, 0, 255))
            screen.blit(image_background_space, (0, 0))
            Level_2_all_sprites.draw(screen)
            screen.blit(image_playerInformactionUI_background, (0, 0))
            screen.blit(image_bullet_missile_small, (1248, 682))

            # 繪製血量
            # 敵人
            for i in range(1, 7):
                if Level_2_enemy_number[i] and Level_2_enemy_number[i].hitted:
                    draw_spriteStatus(screen, Level_2_enemy_number[i].now_armor, Level_2_enemy_number[i].armor, Level_2_enemy_number[i].now_health, Level_2_enemy_number[i].health, (Level_2_enemy_number[i].rect.centerx - 25), ((Level_2_enemy_number[i].rect.top - 6) + 5), (101, 216, 255), (255, 0, 0), (0, 0, 0))
            if Level_2_enemy_BOSS and Level_2_enemy_BOSS.hitted:
                draw_spriteStatus(screen, Level_2_enemy_BOSS.now_armor, Level_2_enemy_BOSS.armor, Level_2_enemy_BOSS.now_health, Level_2_enemy_BOSS.health, (Level_2_enemy_BOSS.rect.centerx - 25), ((Level_2_enemy_BOSS.rect.top - 6) + 5), (0, 127, 255), (255, 0, 0), (0, 0, 0))

            # 畫角色資訊
            draw_lives(screen, player.lives, image_player_livesIcon, 29, 638, 34)
            draw_Level_2_playerInformactionUI(screen, player, score, Level_2_startPlayTime + pauseTime)
            if Use_TurretUpgrade:
                if nowTime - StartUse_TurretUpgrade_Time < player.gun_turboTime:
                    screen.blit(image_turretUpgrade_status, (1240, 49))
                    draw_text("center", screen, str(int((player.gun_turboTime - (nowTime - StartUse_TurretUpgrade_Time)) / 1000)), (255, 255, 255), 22, False, 1255, 96)

            # 畫ESC選單
            if Escape_KeyDown:
                pauseTimeSt = nowTime
                pygame.mouse.set_visible(True)
                screen.blit(image_setting_panel_background, (0, 0))
                escape_screen_return = draw_Key_escape_screen(screen)
            # 繼續遊戲
            if escape_screen_return == 1:
                nowTime = pygame.time.get_ticks()
                pauseTime += nowTime - pauseTimeSt
                escape_screen_return = 0
                Escape_KeyDown = False
                pygame.mouse.set_visible(False)
                if Level_2_summonBOSS_time > 0:
                    Level_2_summonBOSS_time -= nowTime - pauseTimeSt
                if Use_TurretUpgrade:
                    player.gun_turboTime += nowTime - pauseTimeSt
            # 回到主畫面
            elif escape_screen_return == 2:
                nowTime = pygame.time.get_ticks()
                pauseTime += nowTime - pauseTimeSt
                escape_screen_return = 0
                Escape_KeyDown = False
                pygame.mouse.set_visible(True)
                # 啟用關卡初始化
                show_levelTrip = True
                gameSave_readTimes = 0
                # 結束遊戲
                startPlayGame_Button_clicked = False
            # 離開遊戲
            elif escape_screen_return == 3:
                escape_screen_return = 0
                program_running = False
                startPlayGame_Button_clicked = False

            pygame.display.update()
        
        # 關卡三
        while GameSave_content["game_checkpoint"] == 2 and startPlayGame_Button_clicked:
            clock.tick(FPS)
            
            # 初始化
            if show_levelTrip:
                close = Level_3_draw_levelTrip()
                if close:
                    program_running = False
                    startPlayGame_Button_clicked = False
                show_levelTrip = False
                score = 0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_running = False
                    startPlayGame_Button_clicked = False
                    pygame.quit()

            # 畫面顯示
            pygame.display.update()
        
        # 結局
        while GameSave_content["game_checkpoint"] == 3 and startPlayGame_Button_clicked:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_running = False
                    startPlayGame_Button_clicked = False

            # 畫面顯示
            pygame.display.update()
        
        # 遊戲歷程展示廳
        while GameSave_content["game_checkpoint"] == 4 and startPlayGame_Button_clicked:
            clock.tick(FPS)
            # 初始化
            if show_levelTrip:
                show_levelTrip = False
                mainScreen_Button = SettingPanel_ArrowButton(940, 677 * (HEIGHT / 720), "主選單", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
                leaveGame_Button_gameStatistics = SettingPanel_ArrowButton(1160, 677 * (HEIGHT / 720), "離開", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
                gameMarker_Button = SettingPanel_ArrowButton(720, 677 * (HEIGHT / 720), "遊戲製作", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
                toLevel_1_Button = SettingPanel_ArrowButton(206, 499 * (HEIGHT / 720), "第一關", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
                toLevel_2_Button = SettingPanel_ArrowButton(472, 499 * (HEIGHT / 720), "第二關", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
                toLevel_3_Button = SettingPanel_ArrowButton(748, 499 * (HEIGHT / 720), "第三關", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
                toLevel_4_Button = SettingPanel_ArrowButton(1024, 499 * (HEIGHT / 720), "結局", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
            # 獲得滑鼠座標
            mouse_x, mouse_y = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_running = False
                    startPlayGame_Button_clicked = False
                # 滑鼠移動事件
                elif event.type == pygame.MOUSEMOTION:
                    # 判斷滑鼠是否移動到按鈕範圍內
                    mainScreen_Button.getFocus(mouse_x, mouse_y)
                    leaveGame_Button_gameStatistics.getFocus(mouse_x, mouse_y)
                    gameMarker_Button.getFocus(mouse_x, mouse_y)
                    if GameSave_content['PassGame']:
                        toLevel_1_Button.getFocus(mouse_x, mouse_y)
                        toLevel_2_Button.getFocus(mouse_x, mouse_y)
                        toLevel_3_Button.getFocus(mouse_x, mouse_y)
                        toLevel_4_Button.getFocus(mouse_x, mouse_y)
                # 滑鼠按下
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    #滑鼠左鍵按下
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        mainScreen_Button.mouseDown(mouse_x, mouse_y)
                        leaveGame_Button_gameStatistics.mouseDown(mouse_x, mouse_y)
                        gameMarker_Button.mouseDown(mouse_x, mouse_y)
                        if GameSave_content['PassGame']:
                            toLevel_1_Button.mouseDown(mouse_x, mouse_y)
                            toLevel_2_Button.mouseDown(mouse_x, mouse_y)
                            toLevel_3_Button.mouseDown(mouse_x, mouse_y)
                            toLevel_4_Button.mouseDown(mouse_x, mouse_y)

                # 滑鼠彈起
                elif event.type == pygame.MOUSEBUTTONUP:
                    mainScreen_Button.mouseUp()
                    leaveGame_Button_gameStatistics.mouseUp()
                    gameMarker_Button.mouseUp()
                    if GameSave_content['PassGame']:
                        toLevel_1_Button.mouseUp()
                        toLevel_2_Button.mouseUp()
                        toLevel_3_Button.mouseUp()
                        toLevel_4_Button.mouseUp()

            if leaveGame_Button_gameStatistics.bottomMouseUp:
                leaveGame_Button_gameStatistics.bottomMouseUp = False
                startPlayGame_Button_clicked = False
                program_running = False
                break
            
            if mainScreen_Button.bottomMouseUp:
                mainScreen_Button.bottomMouseUp = False
                pygame.mouse.set_visible(True)
                # 啟用關卡初始化
                show_levelTrip = True
                gameSave_readTimes = 0
                # 結束遊戲
                startPlayGame_Button_clicked = False

            if gameMarker_Button.bottomMouseUp:
                close = draw_gameMarkerScreen()
                if close:
                    program_running = False
                    startPlayGame_Button_clicked = False
                    break
                gameMarker_Button.bottomMouseUp = False

            if toLevel_1_Button.bottomMouseUp:
                toLevel_1_Button.bottomMouseUp = False
                GameSave_content["game_checkpoint"] = 0
                # 更新存檔
                with open(GAMESAVE_FILE_ADDRESS, 'wb') as gamesave:
                    pickle.dump(GameSave_content, gamesave)
                pygame.mouse.set_visible(True)
                # 啟用關卡初始化
                show_levelTrip = True
                # gameSave_readTimes = 0
                # # 結束遊戲
                # startPlayGame_Button_clicked = False
            if toLevel_2_Button.bottomMouseUp:
                toLevel_2_Button.bottomMouseUp = False
                GameSave_content["game_checkpoint"] = 1
                # 更新存檔
                with open(GAMESAVE_FILE_ADDRESS, 'wb') as gamesave:
                    pickle.dump(GameSave_content, gamesave)
                pygame.mouse.set_visible(True)
                # 啟用關卡初始化
                show_levelTrip = True
            # if toLevel_3_Button.bottomMouseUp:
            #     toLevel_3_Button.bottomMouseUp = False
            #     GameSave_content["game_checkpoint"] = 2
            #     # 更新存檔
            #     with open(GAMESAVE_FILE_ADDRESS, 'wb') as gamesave:
            #         pickle.dump(GameSave_content, gamesave)
            #     pygame.mouse.set_visible(True)
            #     # 啟用關卡初始化
            #     show_levelTrip = True
            # if toLevel_4_Button.bottomMouseUp:
            #     toLevel_4_Button.bottomMouseUp = False
            #     GameSave_content["game_checkpoint"] = 3
            #     # 更新存檔
            #     with open(GAMESAVE_FILE_ADDRESS, 'wb') as gamesave:
            #         pickle.dump(GameSave_content, gamesave)
            #     pygame.mouse.set_visible(True)
            #     # 啟用關卡初始化
            #     show_levelTrip = True

            # 畫面顯示
            draw_gameStatisticsScreen(screen)
            mainScreen_Button.draw(screen)
            leaveGame_Button_gameStatistics.draw(screen)
            gameMarker_Button.draw(screen)
            if GameSave_content['PassGame']:
                toLevel_1_Button.draw(screen)
                toLevel_2_Button.draw(screen)
                toLevel_3_Button.draw(screen)
                toLevel_4_Button.draw(screen)
            pygame.display.update()

pygame.quit()