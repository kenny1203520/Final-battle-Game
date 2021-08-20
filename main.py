import pygame, random, os, pickle, math

# Version
SPECIAL_VERSION = False
VERSION = "beta0.1.1"

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
        gameConfig['MainVulume'] = 50
        gameConfig['EffectVolume'] = 50
        pickle.dump(gameConfig, gameConfigFile)
else:
    with open(CONFIG_FILE_ADDRESS, 'rb') as gameConfigFile:
        gameConfig = pickle.load(gameConfigFile)
Enable_FullScreen = gameConfig['FullScreen']

# 聲音設定
MainVulume = gameConfig['MainVulume']
EffectVulume = gameConfig['EffectVolume']

# Screen_Display_Tittle
Screen_display_tittle = {}
Screen_display_tittle['main'] = ("前進魔王城")
# Screen_display_tittle['tittle'] = [("前進魔王城"), ("銓勇士上阿!"), ("銓進魔王城"), ("")]

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

# 導入圖片
# 主畫面背景
main_screen_background = {}
main_screen_background['main'] = pygame.image.load(os.path.join("Content/Images/main_screen/main_screen_background0.png")).convert()
main_screen_background['animation'] = []
# 製作主畫面開始動畫
for i in range(12):
    main_screen_background_img = pygame.image.load(os.path.join("Content/Images/main_screen", f"main_screen_background{i}.png")).convert()
    main_screen_background['animation'].append(main_screen_background_img)
# 按鈕背景照片
button_background_image_normal = pygame.image.load(os.path.join("Content/Images/button/main_screen_button_image_normal.png")).convert()
button_background_image_normal.set_colorkey((0, 0, 0))
button_background_image_move = pygame.image.load(os.path.join("Content/Images/button/main_screen_button_image_onbutton.png")).convert()
button_background_image_move.set_colorkey((0, 0, 0))
button_background_image_down = pygame.image.load(os.path.join("Content/Images/button/main_screen_button_image_click.png")).convert()
button_background_image_down.set_colorkey((0, 0, 0))
# 遊戲圖片
image_bullet_rifle = pygame.image.load(os.path.join("Content/Images/game/bullet/bullet_rifle.png")).convert()
image_bullet_rifle.set_colorkey((0, 0, 0))
image_magazine_rifle = pygame.image.load(os.path.join("Content/Images/game/magazine/magazine_rifle.png")).convert()
image_magazine_rifle.set_colorkey((0, 255, 0))
image_medkit = pygame.image.load(os.path.join("Content/Images/game/medkit/medkit.png")).convert()
image_medkit.set_colorkey((0, 255, 0))
image_armorpack = pygame.image.load(os.path.join("Content/Images/game/armorpack/armorpack.png")).convert()
image_large_magazine_rifle = pygame.image.load(os.path.join("Content/Images/game/magazine/large_magazine_rifle.png")).convert()
image_large_magazine_rifle.set_colorkey((0, 255, 0))
image_highspeed_reload_magazine_rifle = pygame.image.load(os.path.join("Content/Images/game/magazine/highspeed_reload_magazine_rifle.png")).convert()
image_highspeed_reload_magazine_rifle.set_colorkey((0, 255, 0))
image_aimPoint = pygame.image.load(os.path.join("Content/Images/game/aimPoint/aim_point.png"))
image_aimPoint.set_colorkey((0, 255, 0))
# 背景
image_PlayerAttributes_Panel = pygame.image.load(os.path.join("Content/Images/game/background/PlayerAttributes_Panel.png")).convert()
image_setting_panel_background = pygame.image.load(os.path.join("Content/Images/game/background/background_SettingPanel.png"))
image_setting_panel_background.set_colorkey((255, 255, 255))

# 導入音檔

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

def draw_playerInformactionUI(surf, player, score, LevelStartPlayTime):
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

    # 畫屬性面板背景
    screen.blit(image_PlayerAttributes_Panel, (0, 600))

    # 血量
    draw_text("tl", surf, "血量 ", (255, 255, 255), 26, True, 10, 608)
    draw_text("tr", surf, str(player.now_health), (255, 0, 0), 24, True, 127, 610)

    # 護甲
    draw_text("tl", surf, "護甲 ", (255, 255, 255), 26, True, 10, 643)
    draw_text("tr", surf, str(player.now_armor), (25, 150, 255), 24, True, 127, 645)

    # 彈匣內彈量
    draw_text("tl", surf, "彈匣 ", (255, 255, 255), 26, True, 142, 608)
    if player.last_magazine_bullets > 0:
        draw_text("tr", surf, str(player.last_magazine_bullets) + "/" + str(player.magazine_bullets), (226, 127, 28), 24, True, 285, 610)
    elif player.pressed_reload_key:
        draw_text("tr", surf, "換彈中", (127, 127, 127), 24, True, 285, 610)
    else:
        draw_text("tr", surf, "換彈中", (127, 127, 127), 24, True, 285, 610)
    
    # 分數
    draw_text("bl", surf, "分數 ", (255, 255, 255), 26, True, 10, 712)
    draw_text("br", surf, str(score), (255, 255, 255), 24, True, 210, 710)

    # 遊玩時間
    draw_text("br", surf, "時間", (255, 255, 255), 26, True, 286, 684)
    if PlayTime_Second > 9:
        draw_text("br", surf, str(PlayTime_Minute) + ":" + str(PlayTime_Second), (255, 255, 255), 20, True, 290, 706)
    else:
        draw_text("br", surf, str(PlayTime_Minute) + ":0" + str(PlayTime_Second), (255, 255, 255), 20, True, 290, 706)

# 主畫面
def draw_main_screen():
    screen.blit(main_screen_background['main'], (0, 0))
    # Tittle
    draw_text("center", screen, Screen_display_tittle["main"], (250, 250, 250), 64, False, WIDTH / 2, (HEIGHT / 10) + 32)
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
    leaveGame_Button = Button(WIDTH / 2, 462 * (HEIGHT / 720), "離開", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, leaveGame_Button_function, text_font)
    while running:
        clock.tick(FPS)
        # 獲得滑鼠座標
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
        surf.blit(image_setting_panel_background, (0, 0))
        mainMenu_Button.draw(surf)
        continueGame_Button.draw(surf)
        leaveGame_Button.draw(surf)
        pygame.display.update()
        if continueGame_Button.bottomMouseUp:
            running = False
        if mainMenu_Button.bottomMouseUp:
            running = False
    if continueGame_Button.bottomMouseUp:
        continueGame_Button.bottomMouseUp = False
        return 1
    if mainMenu_Button.bottomMouseUp:
        mainMenu_Button.bottomMouseUp = False
        return 2

def draw_passLevelScreen(surf):
    running = True
    nextLevel_Button = SettingPanel_ArrowButton(WIDTH / 2, 200 * (HEIGHT / 720), "下一關", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
    mainMenu_Button = SettingPanel_ArrowButton(WIDTH / 2, 331 * (HEIGHT / 720), "主選單", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
    while running:
        clock.tick(FPS)
        # 獲得滑鼠座標
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
        surf.blit(image_setting_panel_background, (0, 0))
        mainMenu_Button.draw(surf)
        nextLevel_Button.draw(surf)
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
    print("game_win")

def draw_failureLevelScreen(surf):
    running = True
    replayGame_Button = SettingPanel_ArrowButton(WIDTH / 2, 200 * (HEIGHT / 720), "重玩本關", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
    mainMenu_Button = SettingPanel_ArrowButton(WIDTH / 2, 331 * (HEIGHT / 720), "主選單", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
    while running:
        clock.tick(FPS)
        # 獲得滑鼠座標
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
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
        surf.blit(image_setting_panel_background, (0, 0))
        mainMenu_Button.draw(surf)
        replayGame_Button.draw(surf)
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
    print("game_lose")

class settingPanel:
    def __init__(self):
        self.surf = screen
        self.settingPanel_gameConfig = gameConfig
        self.ScreenImageResolution_now = {}
        self.ScreenImageResolution_now['Width'] = self.settingPanel_gameConfig['ScreenWidth']
        self.ScreenImageResolution_now['Height'] = self.settingPanel_gameConfig['ScreenHeight']
        self.ScreenFPS = self.settingPanel_gameConfig['FPS']
        self.FullScreen_status = self.settingPanel_gameConfig['FullScreen']
        self.MainVulume_now = self.settingPanel_gameConfig['MainVulume']
        self.EffectVolume_now = self.settingPanel_gameConfig['EffectVolume']
        # 是否完成調整
        self.finishSetting = False
        # 按紐
        self.ScreenMode_nextOne = SettingPanel_ArrowButton(720, 30, "", 24, (255, 255, 255), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
        self.ScreenMode_lastOne = SettingPanel_ArrowButton(900, 30, "", 24, (255, 255, 255), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
        self.MainVulume_Plus = SettingPanel_ArrowButton(900, 165, "", 24, (255, 255, 255), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
        self.MainVulume_Subtract = SettingPanel_ArrowButton(720, 165, "", 24, (255, 255, 255), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
        self.EffectVolume_Plus = SettingPanel_ArrowButton(900, 195, "", 24, (255, 255, 255), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
        self.EffectVolume_Subtract = SettingPanel_ArrowButton(720, 195, "", 24, (255, 255, 255), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
        self.confirm_Buttom = SettingPanel_ArrowButton(1000, 600, "確認", 24, (255, 255, 255), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
        self.apply_Buttom = SettingPanel_ArrowButton(850, 600, "套用", 24, (255, 255, 255), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)

    def updateData(self):
        # 顯示模式切換按鈕
        if self.ScreenMode_nextOne.bottomMouseUp:
            self.ScreenMode_nextOne.bottomMouseUp = False
            self.FullScreen_status = False
        elif self.ScreenMode_lastOne.bottomMouseUp:
            self.ScreenMode_lastOne.bottomMouseUp = False
            self.FullScreen_status = True
        # 主音量加減按鈕
        if self.MainVulume_Plus.bottomMouseUp:
            self.MainVulume_Plus.bottomMouseUp = False
            self.MainVulume_now += 1
        elif self.MainVulume_Subtract.bottomMouseUp:
            self.MainVulume_Subtract.bottomMouseUp = False
            self.MainVulume_now -= 1
        # 音效音量加減按鈕
        if self.EffectVolume_Plus.bottomMouseUp:
            self.EffectVolume_Plus.bottomMouseUp = False
            self.EffectVolume_now += 1
        elif self.EffectVolume_Subtract.bottomMouseUp:
            self.EffectVolume_Subtract.bottomMouseUp = False
            self.EffectVolume_now -= 1
        # 確認按鈕
        if self.confirm_Buttom.bottomMouseUp:
            self.confirm_Buttom.bottomMouseUp = False
            self.settingPanel_gameConfig['ScreenWidth'] = self.ScreenImageResolution_now['Width']
            self.settingPanel_gameConfig['ScreenHeight'] = self.ScreenImageResolution_now['Height']
            self.settingPanel_gameConfig['FPS'] = self.ScreenFPS
            self.settingPanel_gameConfig['FullScreen'] = self.FullScreen_status
            self.settingPanel_gameConfig['MainVulume'] = self.MainVulume_now
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
            self.settingPanel_gameConfig['MainVulume'] = self.MainVulume_now
            self.settingPanel_gameConfig['EffectVolume'] = self.EffectVolume_now
            with open(CONFIG_FILE_ADDRESS, 'wb') as gameConfigFile:
                pickle.dump(self.settingPanel_gameConfig, gameConfigFile)
    
    def draw(self, surf):
        # 畫面
        draw_text("tl", surf, "顯示", (255, 255, 255), 24, True, 0, 0)
        # 螢幕顯示
        draw_text("tl", surf, "顯示模式", (255, 255, 255), 24, True, 0, 30)
        if self.FullScreen_status:
            draw_text("tl", surf, "全螢幕", (255, 255, 255), 24, True, 500, 30)
        else:
            draw_text("tl", surf, "視窗化", (255, 255, 255), 24, True, 500, 30)
        # 寫解析度
        draw_text("tl", surf, "解析度", (255, 255, 255), 24, True, 0, 60)
        draw_text("tl", surf, str(self.ScreenImageResolution_now['Width']) + "x" + str(self.ScreenImageResolution_now['Height']), (255, 255, 255), 24, True, 500, 60)
        # 幀數
        draw_text("tl", surf, "幀數", (255, 255, 255), 24, True, 0, 90)
        draw_text("tl", surf, str(self.ScreenFPS), (255, 255, 255), 24, True, 500, 90)

        # 聲音
        draw_text("tl", surf, "聲音", (255, 255, 255), 24, True, 0, 135)
        # 主音量
        draw_text("tl", surf, "主音量", (255, 255, 255), 24, True, 0, 165)
        draw_text("tl", surf, str(self.MainVulume_now), (255, 255, 255), 24, True, 500, 165)
        # 音效音量
        draw_text("tl", surf, "音效", (255, 255, 255), 24, True, 0, 195)
        draw_text("tl", surf, str(self.EffectVolume_now), (255, 255, 255), 24, True, 500, 195)

        # 按鈕
        # 顯示模式
        if self.FullScreen_status:
            self.ScreenMode_nextOne.draw(surf)
        else:
            self.ScreenMode_lastOne.draw(surf)
        # 主音量
        if 0 < self.MainVulume_now < 100:
            self.MainVulume_Plus.draw(surf)
            self.MainVulume_Subtract.draw(surf)
        elif self.MainVulume_now == 100:
            self.MainVulume_Subtract.draw(surf)
        elif self.MainVulume_now == 0:
            self.MainVulume_Plus.draw(surf)
        # 音效音量
        if 0 < self.EffectVolume_now < 100:
            self.EffectVolume_Plus.draw(surf)
            self.EffectVolume_Subtract.draw(surf)
        elif self.EffectVolume_now == 100:
            self.EffectVolume_Subtract.draw(surf)
        elif self.EffectVolume_now == 0:
            self.EffectVolume_Plus.draw(surf)
        # 確認
        self.confirm_Buttom.draw(surf)
        # 套用
        self.apply_Buttom.draw(surf)

# 按鈕

def startPlayGame_Button_function(surf):
    running = True
    alreadyReadGameSave = False
    while running and not alreadyReadGameSave:
        clock.tick(FPS)
        # 檢查是否有遊戲存檔
        if not os.path.isfile(GAMESAVE_FILE_ADDRESS):
            select_difficult = True
            # 回主選單
            mainMenu_Button = SettingPanel_ArrowButton(WIDTH - 120, HEIGHT - 52, "主選單", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
            # 難度按鈕
            easy_difficult_Button = SettingPanel_ArrowButton(WIDTH / 2, HEIGHT - 275, "簡單", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
            normal_difficult_Button = SettingPanel_ArrowButton(WIDTH / 2, HEIGHT - 180, "普通", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
            hard_difficult_Button = SettingPanel_ArrowButton(WIDTH / 2, HEIGHT - 85, "困難", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
            
            while select_difficult:
                clock.tick(FPS)
                # 獲得滑鼠座標
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # 檢查事件
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
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
                draw_text("center", surf, "選擇存檔難度", (240, 240, 240), 36, False, (WIDTH / 2), (HEIGHT / 5) + 18)
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
                print("已創建新存檔")
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
                print("已刪除存檔")

            # 是否要讀檔
            loadSave_Button = Button((WIDTH / 2), (HEIGHT / 2), ("讀檔"), 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, loadSave_Button_function, text_font)
            removeSave_Button = Button((WIDTH / 2), 260 * (HEIGHT / 720), ("開始新遊戲"), 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, removeSave_Button_function, text_font)
            # 回主選單
            mainMenu_Button = SettingPanel_ArrowButton(WIDTH - 220, HEIGHT - 85, "主選單", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)

            while os.path.isfile(GAMESAVE_FILE_ADDRESS):
                clock.tick(FPS)
                # 獲得滑鼠座標
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # 檢查事件
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
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
                                print("完成讀檔")
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
                pygame.quit()
            # 滑鼠移動事件
            elif event.type == pygame.MOUSEMOTION:
                # 判斷滑鼠是否移動到按鈕範圍內
                # 顯示模式
                if setting_Panel.FullScreen_status:
                    setting_Panel.ScreenMode_nextOne.getFocus(mouse_x, mouse_y)
                else:
                    setting_Panel.ScreenMode_lastOne.getFocus(mouse_x, mouse_y)
                # 主音量
                if 0 < setting_Panel.MainVulume_now < 100:
                    setting_Panel.MainVulume_Plus.getFocus(mouse_x, mouse_y)
                    setting_Panel.MainVulume_Subtract.getFocus(mouse_x, mouse_y)
                elif setting_Panel.MainVulume_now == 100:
                    setting_Panel.MainVulume_Subtract.getFocus(mouse_x, mouse_y)
                elif setting_Panel.MainVulume_now == 0:
                    setting_Panel.MainVulume_Plus.getFocus(mouse_x, mouse_y)
                # 音效音量
                if 0 < setting_Panel.EffectVolume_now < 100:
                    setting_Panel.EffectVolume_Plus.getFocus(mouse_x, mouse_y)
                    setting_Panel.EffectVolume_Subtract.getFocus(mouse_x, mouse_y)
                elif setting_Panel.EffectVolume_now == 100:
                    setting_Panel.EffectVolume_Subtract.getFocus(mouse_x, mouse_y)
                elif setting_Panel.EffectVolume_now == 0:
                    setting_Panel.EffectVolume_Plus.getFocus(mouse_x, mouse_y)
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
                    if 0 < setting_Panel.MainVulume_now < 100:
                        setting_Panel.MainVulume_Plus.mouseDown(mouse_x, mouse_y)
                        setting_Panel.MainVulume_Subtract.mouseDown(mouse_x, mouse_y)
                    elif setting_Panel.MainVulume_now == 100:
                        setting_Panel.MainVulume_Subtract.mouseDown(mouse_x, mouse_y)
                    elif setting_Panel.MainVulume_now == 0:
                        setting_Panel.MainVulume_Plus.mouseDown(mouse_x, mouse_y)
                    # 音效音量
                    if 0 < setting_Panel.EffectVolume_now < 100:
                        setting_Panel.EffectVolume_Plus.mouseDown(mouse_x, mouse_y)
                        setting_Panel.EffectVolume_Subtract.mouseDown(mouse_x, mouse_y)
                    elif setting_Panel.EffectVolume_now == 100:
                        setting_Panel.EffectVolume_Subtract.mouseDown(mouse_x, mouse_y)
                    elif setting_Panel.EffectVolume_now == 0:
                        setting_Panel.EffectVolume_Plus.mouseDown(mouse_x, mouse_y)
                    # 確認
                    setting_Panel.confirm_Buttom.mouseDown(mouse_x, mouse_y)
                    # 套用
                    setting_Panel.apply_Buttom.mouseDown(mouse_x, mouse_y)
            
            # 滑鼠彈起
            elif event.type == pygame.MOUSEBUTTONUP:
                setting_Panel.ScreenMode_nextOne.mouseUp()
                setting_Panel.ScreenMode_lastOne.mouseUp()
                setting_Panel.MainVulume_Plus.mouseUp()
                setting_Panel.MainVulume_Subtract.mouseUp()
                setting_Panel.EffectVolume_Plus.mouseUp()
                setting_Panel.EffectVolume_Subtract.mouseUp()
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
    pygame.quit()
    exit()

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
            startPlayGameButton.game_save = startPlayGame_Button_function(surf)
            if startPlayGameButton.game_save:
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
        self.image_original = image_medkit
        # self.image_original.fill((0, 0, 255))
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = 15
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2
        self.speed = 3
        self.health = 100
        self.now_health = self.health
        self.armor = 100
        self.now_armor = self.armor
        self.lives = 0
        self.damageMagnification = 1
        self.hidden = False
        self.hide_time = 0
        self.direction = "Up"
        self.magazine_bullets_original = 30
        # 上次射擊時間
        self.last_shoot_time = 0
        # 彈匣內子彈數量
        self.magazine_bullets = self.magazine_bullets_original
        self.last_magazine_bullets = self.magazine_bullets
        # 射擊模式: auto, single
        self.shoot_mode = "auto"
        # auto模式下射擊速度
        self.shooting_interval = 450
        # reload所需時間
        self.reloadtime = 2800
        self.last_reloadtime = 0
        self.pressed_reload_key = False
        self.startReloadBullet = False
        if GameSave_content['difficult'] == "easy":
            self.health =  int(self.health * 1.2)
            self.now_health = self.health
            self.lives = 2
            self.damageMagnification = int(self.damageMagnification * 1.2)
        elif GameSave_content['difficult'] == "normal":
            self.health = int(self.health * 1)
            self.now_health = self.health
            self.lives = 1
            self.damageMagnification = int(self.damageMagnification * 1)
        elif GameSave_content['difficult'] == "hard":
            self.health = int(self.health * 1)
            self.now_health = self.health
            self.lives = 0
            self.damageMagnification = int(self.damageMagnification * 0.8)
    
    def update(self):
        now = pygame.time.get_ticks()
        self.bottomleft_x, self.bottomleft_y = self.rect.bottomleft

        # 取得鍵盤輸入
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w] or key_pressed[pygame.K_UP]:
            self.direction = "Up"
            self.rotate()
            self.rect.y -= self.speed
        elif key_pressed[pygame.K_a] or key_pressed[pygame.K_LEFT]:
            self.direction = "Left"
            self.rotate()
            self.rect.x -= self.speed
        elif key_pressed[pygame.K_s] or key_pressed[pygame.K_DOWN]:
            self.direction = "Down"
            self.rotate()
            self.rect.y += self.speed
        elif key_pressed[pygame.K_d] or key_pressed[pygame.K_RIGHT]:
            self.direction = "Right"
            self.rotate()
            self.rect.x += self.speed
        # if key_pressed[pygame.K_SPACE]:
        #     if now - self.last_shoot_time >= self.shooting_interval and self.shoot_mode == "auto":
        #         self.shoot()
        if key_pressed[pygame.K_r] and not self.pressed_reload_key:
            self.pressed_reload_key = True
            self.reload()
        
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
        if self.bottomleft_x < 300 and 600 < self.bottomleft_y:
            self.rect.bottomleft = (self.bottomleft_x + 1, self.bottomleft_y - 1)

        # 重新裝填彈藥
        self.reload()

    def rotate(self):
        if self.direction == "Up":
            self.image = pygame.transform.rotate(self.image_original, 0)
        elif self.direction == "Left":
            self.image = pygame.transform.rotate(self.image_original, 90)
        elif self.direction == "Down":
            self.image = pygame.transform.rotate(self.image_original, 0)
        elif self.direction == "Right":
            self.image = pygame.transform.rotate(self.image_original, 270)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def reload(self):
        now = pygame.time.get_ticks()
        if self.last_magazine_bullets == 0 and not self.startReloadBullet:
            self.last_reloadtime = now
            self.startReloadBullet = True
        elif self.pressed_reload_key and self.last_magazine_bullets < self.magazine_bullets and not self.startReloadBullet:
            self.last_reloadtime = now
            self.startReloadBullet = True
            self.last_magazine_bullets = 0
            self.pressed_reload_key = True
        elif self.pressed_reload_key and self.last_magazine_bullets >= self.magazine_bullets and not self.startReloadBullet:
            self.pressed_reload_key = False
        if self.last_magazine_bullets == 0 and now - self.last_reloadtime >= self.reloadtime:
            self.last_magazine_bullets = self.magazine_bullets
            self.startReloadBullet = False
            if self.pressed_reload_key:
                self.pressed_reload_key = False

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
        self.image_original = pygame.Surface((45, 30))
        self.image_original.fill((255, 0, 0))
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.radius = 15
        self.frontView = 250
        self.direction = "Up"
        # 敵人生成點
        self.rect.centerx , self.rect.centery = spawn_center
        # 移動速度
        self.speedx = 2
        self.speedy = 2
        # 預設屬性
        self.health = 80
        self.damageMagnification = 1
        self.choice_move_direction = 1
        self.last_moveAmount = 0
        self.magazine_bullets = 30
        self.shooting_interval = 500
        self.last_shoot_time = 0
        self.magazine_bullets_original = 30
        self.magazine_bullets = self.magazine_bullets_original
        self.last_magazine_bullets = self.magazine_bullets
        self.startReloadBullet = False
        self.reloadtime = 5000
        self.last_reloadtime = 0
        # 難度
        if GameSave_content['difficult'] == "easy":
            self.health *= 1
            self.damageMagnification *= 0.8
        elif GameSave_content['difficult'] == "normal":
            self.health *= 1
            self.damageMagnification *= 1
        elif GameSave_content['difficult'] == "hard":
            self.health *= 1.5
            self.damageMagnification *= 1.2
            self.magazine_bullets_original = 45
            self.magazine_bullets = self.magazine_bullets_original

    def update(self):
        now = pygame.time.get_ticks()
        self.bottomleft_x, self.bottomleft_y = self.rect.bottomleft
        
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
        if self.bottomleft_x < 300 and 600 < self.bottomleft_y:
            self.last_moveAmount = 0
            self.rect.bottomleft = (self.bottomleft_x + 1, self.bottomleft_y - 1)

        self.move()

        if self.detect_enemy() and (now - self.last_shoot_time) >= self.shooting_interval:
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
        self.image_original = pygame.Surface((90, 30))
        self.image_original.fill((255, 255, 0))
        self.image = pygame.transform.rotate(self.image_original, self.rotate)
        self.rect = self.image.get_rect()
        self.rect.centerx , self.rect.centery = self.center_x, self.center_y
        # 屬性
        self.health = 300
        # 難度
        if GameSave_content['difficult'] == "easy":
            self.health *= 2
        elif GameSave_content['difficult'] == "normal":
            self.health *= 1
        elif GameSave_content['difficult'] == "hard":
            self.health *= 0.75

class Level_1_rifle(pygame.sprite.Sprite):
    def __init__(self, surf, equipment_role):
        pygame.sprite.Sprite.__init__(self)
        self.surf = surf
        self.image_weapons_original = image_magazine_rifle
        self.image = self.image_weapons_original.copy()
        self.rect = self.image.get_rect()
        self.equipment_role = equipment_role
        self.rect.centerx = self.equipment_role.rect.centerx
        self.rect.centery = self.equipment_role.rect.centery
    
    def update(self):
        now = pygame.time.get_ticks()
        self.rect.centerx = self.equipment_role.rect.centerx
        self.rect.centery = self.equipment_role.rect.centery
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
        if self.weapon_difference_x > 0 and self.weapon_difference_y > 0:
            self.image = pygame.transform.rotate(self.image_weapons_original, -(int((math.acos(self.weapon_difference_x / self.weapon_hypotenuse) / math.pi) * 180 - 90)))
        elif self.weapon_difference_x < 0 and self.weapon_difference_y > 0:
            self.image = pygame.transform.rotate(self.image_weapons_original, (270 - int((math.acos(self.weapon_difference_x / self.weapon_hypotenuse) / math.pi) * 180)))
        elif self.weapon_difference_x < 0 and self.weapon_difference_y < 0:
            self.image = pygame.transform.rotate(self.image_weapons_original, (90 + int((math.acos(self.weapon_difference_x / self.weapon_hypotenuse) / math.pi) * 180)))
        elif self.weapon_difference_x > 0 and self.weapon_difference_y < 0:
            self.image = pygame.transform.rotate(self.image_weapons_original, (90 + int((math.acos(self.weapon_difference_x / self.weapon_hypotenuse) / math.pi) * 180)))
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def shoot(self):
        now = pygame.time.get_ticks()
        if self.equipment_role.last_magazine_bullets > 0:
            bullet = Bullet_rifle_player(self.rect.centerx, self.rect.centery)
            Level_1_all_sprites.add(bullet)
            Level_1_bullets.add(bullet)
            Level_1_friendly_bullets.add(bullet)
            self.equipment_role.last_magazine_bullets -= 1
            self.equipment_role.last_shoot_time = now

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
        self.image_original = image_bullet_rifle
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.centery = center_y
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.difference_x = self.mouse_x - self.rect.centerx
        self.difference_y = self.mouse_y - self.rect.centery
        print("x: " + str(self.difference_x))
        print("y: " + str(self.difference_y))
        self.difference_hypotenuse = ((self.difference_x** 2 + self.difference_y** 2)** 0.5)
        # 子彈飛行速度
        self.speed = 8
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
            if self.difference_x > 0 and self.difference_y > 0:
                self.rect.x += self.fly_speedx
                self.rect.y -= self.fly_speedy
                self.flyingDistance += self.speed
            elif self.difference_x < 0 and self.difference_y > 0:
                self.rect.x -= self.fly_speedx
                self.rect.y -= self.fly_speedy
                self.flyingDistance += self.speed
            elif self.difference_x < 0 and self.difference_y < 0:
                self.rect.x -= self.fly_speedx
                self.rect.y += self.fly_speedy
                self.flyingDistance += self.speed
            elif self.difference_x > 0 and self.difference_y < 0:
                self.rect.x += self.fly_speedx
                self.rect.y += self.fly_speedy
                self.flyingDistance += self.speed
        if self.flyingDistance > self.maxFlyingDistance or self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

    def rotate(self):
        if self.difference_x > 0 and self.difference_y > 0:
            self.image = pygame.transform.rotate(self.image_original, -(int((math.acos(self.difference_x / self.difference_hypotenuse) / math.pi) * 180 - 90)))
        elif self.difference_x < 0 and self.difference_y > 0:
            self.image = pygame.transform.rotate(self.image_original, (270 - int((math.acos(self.difference_x / self.difference_hypotenuse) / math.pi) * 180)))
        elif self.difference_x < 0 and self.difference_y < 0:
            self.image = pygame.transform.rotate(self.image_original, (90 + int((math.acos(self.difference_x / self.difference_hypotenuse) / math.pi) * 180)))
        elif self.difference_x > 0 and self.difference_y < 0:
            self.image = pygame.transform.rotate(self.image_original, (90 + int((math.acos(self.difference_x / self.difference_hypotenuse) / math.pi) * 180)))
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
        self.speedx = 8 * (FPS / 60)
        self.speedy = 8 * (FPS / 60)
        self.flyingDistance = 0
        self.maxFlyingDistance = 400

    def update(self):
        if self.direction == "Up" and self.flyingDistance <= self.maxFlyingDistance:
            self.rotate()
            self.rect.y -= self.speedy
            self.flyingDistance += self.speedy
        elif self.direction == "Left" and self.flyingDistance <= self.maxFlyingDistance:
            self.rotate()
            self.rect.x -= self.speedx
            self.flyingDistance += self.speedx
        elif self.direction == "Down" and self.flyingDistance <= self.maxFlyingDistance:
            self.rotate()
            self.rect.y += self.speedy
            self.flyingDistance += self.speedy
        elif self.direction == "Right" and self.flyingDistance <= self.maxFlyingDistance:
            self.rotate()
            self.rect.x += self.speedx
            self.flyingDistance += self.speedx
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

class Level_2_Player_plane(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

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

# 創建按鈕
startPlayGame_Button = startPlayGameButton(WIDTH / 2, 258 * (HEIGHT / 720), "遊玩", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
gameSetting_Button = gameSettingButton(screen, WIDTH / 2, 360 * (HEIGHT / 720), "設定", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, text_font)
leaveGame_Button = Button(WIDTH / 2, 462 * (HEIGHT / 720), "離開", 28, (0, 0, 0), False, button_background_image_normal, button_background_image_move, button_background_image_down, leaveGame_Button_function, text_font)

# 現在時間(ticks) 1tick = 1ms
nowTime = pygame.time.get_ticks()
# 存檔讀取次數
# 0 未讀擋, 1 完成第一次讀檔
gameSave_readTimes = 0
# 開始遊戲是否被點擊
startPlayGame_Button_clicked = False
# 是否調整過設定
gameSetting_Button_Done = False
# 是否按下ESC
Escape_KeyDown = False
# ESC畫面回傳
escape_screen_return = False
# 關卡開頭
show_levelTrip = True

# mainScreen
while program_running:
    clock.tick(FPS)
    # 獲得滑鼠座標
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            program_running = False
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
            leaveGame_Button.mouseUp()

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
        MainVulume = gameConfig['MainVulume']
        EffectVulume = gameConfig['EffectVolume']

    # 畫面顯示
    draw_main_screen()
    pygame.display.update()

    # 按下遊戲開始
    while startPlayGame_Button_clicked:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_running = False
                startPlayGame_Button_clicked = False
                pygame.quit()
        
        # 遊戲存檔讀取
        if gameSave_readTimes == 0:
            GameSave_content = startPlayGameButton.game_save
            gameSave_readTimes = 1
        
        # 畫面顯示
            screen.fill((0, 0, 0))
            pygame.display.update()

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
                enemy_totalAmount = 10
                Use_LargeMagazine = False
                StartUse_LargeMagazine_Time = 0
                LargeMagazine_ValidityPeriod = 0
                Level_1_player_bulletDamage = 25
                Level_1_enemy_bulletDamage = 25
                Level_1_startPlayTime = pygame.time.get_ticks()
                Level_1_remaining_LevelTime = (random.randint(0, 120) + 180) * 1000
                Level_1_enemy_number = {}
                Level_1_sandBag = {}
                player = Level_1_Player_soldier(screen)
                player_weapon = Level_1_rifle(screen, player)
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

                # 添增玩家至群組
                Level_1_all_sprites.add(player)
                Level_1_friendly_sprites_group.add(player)
                Level_1_all_sprites.add(player_weapon)
                Level_1_weapons_group.add(player_weapon)
                # 產生掩體
                Level_1_sandBag[1] = SandBag(screen, 595, 255, 0)
                Level_1_sandBag[2] = SandBag(screen, 685, 255, 0)
                Level_1_sandBag[3] = SandBag(screen, 535, 315, 270)
                Level_1_sandBag[4] = SandBag(screen, 535, 405, 270)
                Level_1_sandBag[5] = SandBag(screen, 745, 315, 90)
                Level_1_sandBag[6] = SandBag(screen, 745, 405, 90)
                Level_1_sandBag[7] = SandBag(screen, 595, 465, 180)
                for i in range(1, 8):
                    Level_1_all_sprites.add(Level_1_sandBag[i])
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
                    pygame.quit()
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
                    Use_LargeMagazine = False

            # 判斷電腦
            
            for i in range(0, enemy_totalAmount, 1):
                # 判斷電腦 - 玩家
                if Level_1_enemy_number[i]:
                    # 判斷玩家子彈是否擊中電腦
                    hits = pygame.sprite.spritecollide(Level_1_enemy_number[i], Level_1_friendly_bullets, True, pygame.sprite.collide_rect)
                    for hit in hits:
                        Level_1_enemy_number[i].health -= int(Level_1_player_bulletDamage * player.damageMagnification)
                        if Level_1_enemy_number[i].health <= 0:
                            score += 100
                            # 隨機掉落道具
                            if  random.random() > 0.8:
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
                            if hits:
                                # 掩體右測
                                if Level_1_sandBag[r].rect.centerx < Level_1_enemy_number[i].rect.left < Level_1_sandBag[r].rect.right and Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom and Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom:
                                    Level_1_enemy_number[i].choice_move_direction = 4
                                    Level_1_enemy_number[i].rect.left = Level_1_sandBag[r].rect.right
                                # 掩體左側
                                elif Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right < Level_1_sandBag[r].rect.centerx and Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom and Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom:
                                    Level_1_enemy_number[i].choice_move_direction = 2
                                    Level_1_enemy_number[i].rect.right = Level_1_sandBag[r].rect.left
                                # 掩體上方
                                elif Level_1_sandBag[r].rect.top < Level_1_enemy_number[i].rect.bottom < Level_1_sandBag[r].rect.centery and Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right and Level_1_enemy_number[i].rect.left < Level_1_sandBag[r].rect.right:
                                    Level_1_enemy_number[i].choice_move_direction = 1
                                    Level_1_enemy_number[i].rect.bottom = Level_1_sandBag[r].rect.top
                                # 掩體下方
                                elif Level_1_sandBag[r].rect.centery < Level_1_enemy_number[i].rect.top < Level_1_sandBag[r].rect.bottom and Level_1_sandBag[r].rect.left < Level_1_enemy_number[i].rect.right and Level_1_enemy_number[i].rect.left < Level_1_sandBag[r].rect.right:
                                    Level_1_enemy_number[i].choice_move_direction = 3
                                    Level_1_enemy_number[i].rect.top = Level_1_sandBag[r].rect.bottom
                
            # 判斷玩家

            # 判斷玩家 - 電腦
            # 判斷子彈是否擊中玩家
            hits = pygame.sprite.spritecollide(player, Level_1_enemy_bullets, True, pygame.sprite.collide_rect)
            for hit in hits:
                if player.now_armor <= 0:
                    player.now_health -= int(Level_1_enemy_bulletDamage * Level_1_enemy_number[i].damageMagnification)
                    if player.now_health <= 0:
                        if player.lives > 0:
                            player.lives -= 1
                            player.now_health = player.health
                            player.now_armor = player.armor
                            player.hide()
                            # 重置彈藥
                            Use_LargeMagazine = False
                            LargeMagazine_ValidityPeriod = 0
                            player.magazine_bullets = player.magazine_bullets_original
                            player.last_magazine_bullets = player.magazine_bullets
                elif player.now_armor - int(Level_1_enemy_bulletDamage * 0.5 * Level_1_enemy_number[i].damageMagnification) >= 0:
                    player.now_armor -= int(Level_1_enemy_bulletDamage * 0.5 * Level_1_enemy_number[i].damageMagnification)
                else:
                    player.now_health -= (int(Level_1_enemy_bulletDamage * 0.5 * Level_1_enemy_number[i].damageMagnification) - player.now_armor)
                    player.now_armor = 0

            # 判斷玩家是否與電腦相撞
            for i in range(0, enemy_totalAmount, 1):
                if Level_1_enemy_number[i]:
                    hits = pygame.sprite.collide_rect(player, Level_1_enemy_number[i])
                    # 處理玩家
                    if hits:
                        if player.direction == "Up":
                            player.rect.top += 3
                        elif player.direction == "Left":
                            player.rect.left += 3
                        elif player.direction == "Down":
                            player.rect.bottom -= 3
                        elif player.direction == "Right":
                            player.rect.right -= 3

                    # 處理電腦
                    if hits:
                        if Level_1_enemy_number[i].direction == "Up":
                            Level_1_enemy_number[i].rect.top += 6
                            Level_1_enemy_number[i].choice_move_direction = 3
                        elif Level_1_enemy_number[i].direction == "Left":
                            Level_1_enemy_number[i].rect.left += 6
                            Level_1_enemy_number[i].choice_move_direction = 4
                        elif Level_1_enemy_number[i].direction == "Down":
                            Level_1_enemy_number[i].rect.bottom -= 6
                            Level_1_enemy_number[i].choice_move_direction = 1
                        elif Level_1_enemy_number[i].direction == "Right":
                            Level_1_enemy_number[i].rect.right -= 6
                            Level_1_enemy_number[i].choice_move_direction = 2
            
            # 判斷玩家 - 掩體
            # 判斷玩家是否與掩體相撞
            for i in range(1, 8):
                if Level_1_sandBag[i]:
                    hits = pygame.sprite.collide_rect(player, Level_1_sandBag[i])
                    if hits:
                        # 掩體右測
                        if Level_1_sandBag[i].rect.centerx < player.rect.left < Level_1_sandBag[i].rect.right and Level_1_sandBag[i].rect.top < player.rect.bottom and player.rect.top < Level_1_sandBag[i].rect.bottom:
                            player.rect.left = Level_1_sandBag[i].rect.right
                        # 掩體左側
                        elif Level_1_sandBag[i].rect.left < player.rect.right < Level_1_sandBag[i].rect.centerx and Level_1_sandBag[i].rect.top < player.rect.bottom and player.rect.top < Level_1_sandBag[i].rect.bottom:
                            player.rect.right = Level_1_sandBag[i].rect.left
                        # 掩體上方
                        elif Level_1_sandBag[i].rect.top < player.rect.bottom < Level_1_sandBag[i].rect.centery and Level_1_sandBag[i].rect.left < player.rect.right and player.rect.left < Level_1_sandBag[i].rect.right:
                            player.rect.bottom = Level_1_sandBag[i].rect.top
                        # 掩體下方
                        elif Level_1_sandBag[i].rect.centery < player.rect.top < Level_1_sandBag[i].rect.bottom and Level_1_sandBag[i].rect.left < player.rect.right and player.rect.left < Level_1_sandBag[i].rect.right:
                            player.rect.top = Level_1_sandBag[i].rect.bottom

            # 判斷玩家是否取得道具
            hits = pygame.sprite.spritecollide(player, Level_1_powerItems_group, True)
            for hit in hits:
                if hit.powerType == 'Medkit':
                    player.now_health += 25
                    if player.now_health > 100:
                        player.now_health = 100
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
                if hit.powerType == 'HighSpeedReload':
                    player.last_magazine_bullets = player.magazine_bullets


            # 判斷掩體

            # 判斷掩體 - 電腦
            # 判斷電腦子彈是否擊中掩體
            for i in range(1, 8):
                if Level_1_sandBag[i]:
                    hits = pygame.sprite.spritecollide(Level_1_sandBag[i], Level_1_enemy_bullets, True, pygame.sprite.collide_rect)
                    for hit in hits:
                        Level_1_sandBag[i].health -= int(Level_1_enemy_bulletDamage * Level_1_enemy_number[0].damageMagnification)
                        if Level_1_sandBag[i].health <= 0:
                            Level_1_all_sprites.remove(Level_1_sandBag[i])
                            Level_1_friendly_sprites_group.remove(Level_1_sandBag[i])
                            Level_1_sandBag[i] = None
            
            # 檢查玩家是否失敗
            if player.now_health <= 0 and player.lives <= 0:
                # 啟用關卡初始化
                show_levelTrip = True
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
                    break

            # 檢查是否完成通關條件
            if nowTime - Level_1_startPlayTime - pauseTime >= Level_1_remaining_LevelTime:
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
                GameSave_content['PlayTime_total'] += GameSave_content['PlayTime_Level_1']
                # 檢查是否完成過遊戲
                if GameSave_content['PassGame']:
                    GameSave_content["game_checkpoint"] = 4
                # 更新存檔
                with open(GAMESAVE_FILE_ADDRESS, 'wb') as gamesave:
                    pickle.dump(GameSave_content, gamesave)
                # 呼叫通關畫面
                passLevelScreen_return = draw_passLevelScreen(screen)
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
                    break

            # 畫面顯示
            screen.fill((255, 255, 150))
            Level_1_all_sprites.draw(screen)
            # 可視化圓形碰撞箱
            # pygame.draw.circle(screen, (0, 255, 0), player.rect.center, player.radius)
            # for i in range(0, enemy_totalAmount, 1):
            #     if Level_1_enemy_number[i]:
            #         pygame.draw.circle(screen, (0, 255, 0), Level_1_enemy_number[i].rect.center, Level_1_enemy_number[i].radius)
            
            # 畫角色資訊
            draw_playerInformactionUI(screen, player, score, Level_1_startPlayTime + pauseTime)
            # 畫ESC選單
            if Escape_KeyDown:
                pauseTimeSt = nowTime
                pygame.mouse.set_visible(True)
                escape_screen_return = draw_Key_escape_screen(screen)
            if escape_screen_return == 1:
                nowTime = pygame.time.get_ticks()
                pauseTime += nowTime - pauseTimeSt
                escape_screen_return = 0
                Escape_KeyDown = False
                pygame.mouse.set_visible(False)
            elif escape_screen_return == 2:
                nowTime = pygame.time.get_ticks()
                pauseTime += nowTime - pauseTimeSt
                escape_screen_return = 0
                Escape_KeyDown = False
                pygame.mouse.set_visible(True)
                # 啟用關卡初始化
                show_levelTrip = True
                # 結束遊戲
                startPlayGame_Button_clicked = False
            
            pygame.display.update()

        # 關卡二
        while GameSave_content["game_checkpoint"] == 1 and startPlayGame_Button_clicked:
            clock.tick(FPS)
            
            # 初始化
            if show_levelTrip:
                close = Level_2_draw_levelTrip()
                if close:
                    program_running = False
                    startPlayGame_Button_clicked = False
                    break
                show_levelTrip = False
                score = 0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_running = False
                    startPlayGame_Button_clicked = False
                    pygame.quit()

            # 畫面顯示
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
                    break
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
                    pygame.quit()

            # 畫面顯示
            pygame.display.update()
        
        # 遊戲歷程展示廳
        while GameSave_content["game_checkpoint"] == 4 and startPlayGame_Button_clicked:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_running = False
                    startPlayGame_Button_clicked = False
                    pygame.quit()

            # 畫面顯示
            pygame.display.update()

pygame.quit()